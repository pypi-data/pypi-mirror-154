import torch
from torch.utils.data import DataLoader

import numpy as np
import pandas as pd

from typing import Dict, List, Tuple

from .classes import (
    PredictionImageDataset,
    construct_model,
    load_model_weights,
)

from .constants import (
    IMAGE_TRANSFORMS,
    TEST_SPLIT,
    CPU,
    FILENAME_KEY,
    PRED_KEY,
    PRED_PROBS_KEY
)

from .pd_utils import (
    construct_filename_series,
    left_join_dfs_by_filename,
)

from .pt_utils import (
    determine_device
)

from .model_utils import (
    get_probs_and_preds,
    construct_tqdm_batches,
    label_to_class_np_v_func,
    load_model_metadata_dicts,
)

def predict_on_dataset(
    task_name: str,
    pred_data_dir: str,
    pretrained_model_name: str,
    fc_layers_dict: Dict[str, int],
    feature_extract: bool,
    num_classes: int,
    model_weights_path: str,
    batch_size: int,
    no_cuda: bool, 
    kwargs: Dict,
    verbose: bool = False
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    '''Uses a trained model to predict on a folder of image samples located at pred_data_dir on the host's filesystem and returns the
        predictions, prediction probabilities, and their respective filenames

    Args:
        task_name: Name of the classification task of the model
        pred_data_dir: Path to directory on the host's filesystem which contains images whose labels is being predicted by the model
        pretrained_model_name: Name of pretrained (ImageNet) PyTorch model to load e.g. 'efficientnet-b1', see PRETRAINED_MODELS_DICT for all options
        fc_layers_dict: Dictionary containing specifications (number of nodes) for additional fully-connected layers on top of the pretrained model
        feature_extract: Determines if we fine-tune (False) the pretrained model to the task
        num_classes: Number of classes (labels) for prediction task for the model
        model_weights_path: Path on host's filesystem to model's trained weights
        batch_size: Number of data samples in each batch
        no_cuda: Determines if we should / should not use CUDA even if it is available on the host machine.
        kwargs: Additional settings for CUDA (e.g. num_workers, pin_memory, etc.), if CUDA is available and no_cuda is False. Defaults to {}.
        verbose: Determines if progress updates from processing image batches throughout prediction should be logged to stdout. Defaults to False.
    
    Returns:
        y_pred: 1-D numPy row vector, predicted labels from the model
        pred_probs: numPy array of normalized probabilities associated with each class for the prediction task.
            Determined by a sigmoid function in the binary case and softmax in the n-ary case with n > 2
        filenames: List of filenames corresponding to y_pred predictions
    '''

    # Determine prediction conditions
    device, use_cuda = determine_device(no_cuda)
    kwargs = kwargs if use_cuda else {}

    pred_dataset = PredictionImageDataset(pred_data_dir, transform=IMAGE_TRANSFORMS[TEST_SPLIT])
    pred_data_loader = DataLoader(pred_dataset, batch_size=batch_size, shuffle=False, **kwargs)
    print("Loaded data for prediction.")
    model = construct_model(pretrained_model_name, num_classes, fc_layers_dict=fc_layers_dict, feature_extract=feature_extract)
    model = load_model_weights(model, model_weights_path)
    model.to(device)
    model.eval()
    batches = construct_tqdm_batches(pred_data_loader, verbose, unit='batch')

    with torch.no_grad():
        y_pred, pred_probs = torch.tensor([], device=CPU), torch.tensor([], device=CPU)
        filenames = []
        for batch_idx, (inputs, batch_filenames) in batches:
            inputs = inputs.to(device)
            outputs = model(inputs)
            if num_classes == 2:
                outputs = outputs.squeeze()

            probs, preds = get_probs_and_preds(outputs, num_classes)

            y_pred, pred_probs = torch.cat((y_pred, preds.to(CPU)), dim=0), torch.cat((pred_probs, probs.to(CPU)), dim=0)
            filenames.extend(batch_filenames)

        y_pred, pred_probs = y_pred.numpy(), pred_probs.numpy()
        if verbose:
            print(f"\nFinished {task_name} Model Predictions on Dataset located at {pred_data_dir}")
                
    return y_pred, pred_probs, filenames

def prepare_prediction_df(df: pd.DataFrame, file_path_col_name: str) -> pd.DataFrame:
    """Adds a FILENAME_KEY column in DataFrame df using source file paths in the file_path_col_name column in df

    Args:
        df: DataFrame to add FILENAME_KEY column to
        file_path_col_name: Name of column in df which has source file paths
    
    Returns:
        df: DataFrame with FILENAME_KEY column added with respective filenames present in the file_path_col_name column 
            source file paths
    """
    df[FILENAME_KEY] = construct_filename_series(df, file_path_col_name)
    return df

def transform_pred_results(y_pred: np.ndarray, pred_probs: np.ndarray, filenames: List[str], class_label_dict: Dict[str, int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Transforms prediction vectors and associated filenames into numpy row vectors with appropriate data types

    Args:
        y_pred: 1-D numPy row vector, predicted labels from the model with float values
        pred_probs: numPy array of normalized probabilities associated with each class for the prediction task.
            Determined by a sigmoid function in the binary case and softmax in the n-ary case with n > 2
        filenames: List of filenames corresponding to y_pred predictions
        class_label_dict: Dictionary mapping class label string to integer index label
    
    Returns:
        y_pred_int: 1-D numPy row vector of predicted labels from the model with integer values
        pred_probs: numPy array of normalized probabilities associated with each class for the prediction task.
            Determined by a sigmoid function in the binary case and softmax in the n-ary case with n > 2
        filenames_np: 1-D numPy row vector of filenames associated with predictions in y_pred_int
    """
    v_func = label_to_class_np_v_func(class_label_dict)
    y_pred_int= v_func(y_pred)
    filenames_np = np.array(filenames)
    return y_pred_int, pred_probs, filenames_np

def construct_preds_df(task_name: str, y_pred_int: np.ndarray, pred_probs: np.ndarray, filenames_np: np.ndarray) -> pd.DataFrame:
    """Constructs a prediction DataFrame for a prediction task with task name task_name consisting of a 
        column of filenames (column name: FILENAME_KEY), a column of predicted labels (column name: '{task_name}_{PRED_KEY}'), and
        a column of prediction probabilities (column name: '{task_name}_{PRED_PROBS_KEY}')

    Args:
        task_name: Name of prediction task for the predictions in y_pred_int
        y_pred_int: 1-D NumPy row vector of model predictions as index labels
        pred_probs: NumPy array of model normalized prediction probabilties associated with each label in the prediction task
        filenames_np: 1-D NumPy row vector of filenames associated with model predictions in y_pred_int row vector
    
    Returns:
        preds_df: Predictions DataFrame of task_name model prediction, prediction probabilities, and associated filenames
    """
    preds_df =  pd.DataFrame(data={
        FILENAME_KEY: filenames_np, 
        f"{task_name}-{PRED_KEY}": y_pred_int,
        f"{task_name}-{PRED_PROBS_KEY}": pred_probs.tolist()
        })
    return preds_df

def predict_and_construct_pred_df(data_dir: str, task_name: str, model_metadata_path_dict: Dict[str, str], verbose: bool = False) -> pd.DataFrame:
    """Loads pretrained model with model weights located at path in model_metadata_path_dict on the host's filesystem
        for prediction task named task_name on image data present in the directory located at 
        data_dir on the host's filesystem and constructs a prediction DataFrame with the subsequent
        predictions by the model on the image files

    Args:
        data_dir: Path to directory on the host's filesystem which contains images whose labels is being predicted by the model
        task_name: Name of prediction task the model is made for
        model_metadata_path_dict: Dictionary containing path to model metadata directory on the host's filesystem (key: 'model_dir')
            and the path to the model's trained weights (key: 'model_weights_path')
        verbose: Determines if progress updates from processing image batches throughout prediction should be logged to stdout. Defaults to False
    
    Returns:
        preds_df: Predictions DataFrame of task_name model prediction, prediction probabilities, and associated filenames
    """
    model_dir = model_metadata_path_dict['model_dir']
    model_weights_path = model_metadata_path_dict['model_weights_path']
    hyperparameters_dict, class_label_dict, training_settings_dict, _ = load_model_metadata_dicts(model_dir)
    num_classes = len(class_label_dict)
    y_pred, pred_probs, filenames = predict_on_dataset(
      task_name,
      data_dir,
      hyperparameters_dict['pretrainedModelName'],
      hyperparameters_dict['fcLayersDict'],
      hyperparameters_dict['featureExtract'],
      num_classes,
      model_weights_path,
      training_settings_dict['devBatchSize'],
      training_settings_dict['noCuda'], 
      training_settings_dict['kwargs'],
      verbose=verbose
    )
    y_pred_int_np, pred_probs_np, filenames_np = transform_pred_results(y_pred, pred_probs, filenames, class_label_dict)
    preds_df = construct_preds_df(task_name, y_pred_int_np, pred_probs_np, filenames_np)
    return preds_df

def construct_multiple_prediction_dfs(data_dir: str, task_model_dict: Dict[str, Dict[str, str]], verbose: bool = False) -> List[pd.DataFrame]:
    """Constructs a list of prediction DataFrames for images in the directory located at data_dir on the host's filesystem
        based on a dictionary mapping task name to a dictionary of model metadata path details

    Args:
        data_dir: Path to directory on the host's filesystem containing images to predict on
        task_model_dict: Dictionary mapping task name to a model model_metadata_path_dict dictionary. 
            model_metadata_path_dict is a dictionary containing a path to a model's metadata directory on the host's filesystem (key: 'model_dir')
            and the path to the model's trained weights (key: 'model_weights_path')
        verbose: Determines if progress updates from processing image batches throughout prediction should be logged to stdout. Defaults to False.
    
    Returns:
        pred_dfs: List of prediction DataFrames for task, model metadata path pairs in the task_model_dict
    """
    pred_dfs = []
    for task_name, model_metadata_path_dict in task_model_dict.items():
        preds_df = predict_and_construct_pred_df(data_dir, task_name, model_metadata_path_dict, verbose)
        pred_dfs.append(preds_df)
    return pred_dfs

def merge_pred_dfs_by_filename(base_df: pd.DataFrame, pred_dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """Left joins a base_df DataFrame (left) with multiple prediction DataFrame pred_dfs (right) on 
        the FILENAME_KEY column present in all the DataFrames

    Args:
        base_df: Base DataFrame which contains a FILENAME_KEY column will be the left DataFrame in a 
            series of left joins with each prediction dataframe in the pred_dfs list
        pred_dfs: List of prediction DataFrames which contain a FILENAME_KEY column and their respective
            predictions by the model, one DataFrame for a different model and/or prediction tasks
    
    Returns:
        merged_df: Resultant DataFrame from multiple left joins on the FILENAME_KEY column 
            with base_df as the left DataFrame and each DataFrame in the pred_dfs list as the right
            DataFrame
    """
    merged_df = base_df.copy()
    for pred_df in pred_dfs:
        merged_df = left_join_dfs_by_filename(merged_df, pred_df)
    return merged_df