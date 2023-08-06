import numpy as np

import torch

import json

from typing import Dict, Set, Tuple

from .constants import (
    TEST_SPLIT,
    CPU,
    METRICS_KEY,
    CONFUSION_MATRIX_KEY,
    CLASS_LABEL_DICT_KEY
)

from .misc_utils import (
    prettify_underscore_string
)

from .pt_utils import (
    determine_device
)

from .metric_utils import (
    calc_metric_scores_dict,
    calc_confusion_matrix,
)

from .model_utils import (
    construct_tqdm_batches,
    get_probs_and_preds,
    load_class_label_dict,
    load_split_data,
    construct_criterion,
    loss_func_target_arg,
)

from .classes import (
    construct_model,
    load_model_weights,
)

def test(
    data_dir: str,
    pretrained_model_name: str,
    fc_layers_dict: Dict[str, int],
    feature_extract: bool,
    model_weights_path: str,
    batch_size: int,
    criterion_type: str,
    metrics_set: Set[str],
    no_cuda: bool, 
    kwargs: Dict,
    verbose: bool = False
) -> Tuple[Dict[str, float], np.ndarray, np.ndarray, np.ndarray, np.ndarray, float, Dict[str, int]]:
    '''Tests a model on a test set with the label separated folders of images located on the host's filesystem

        Tests a model on the label separated folders of images and returns metric scores, confusion matrix,
        predicted and truth label arrays, the test loss as determined by the criterion function, and the mapping 
        from class label string to index integer label. 

    Args:
        data_dir: Path to directory containing the image dataset folders based on split ex. data_dir/train, data_dir/dev, data_dir/test.
        pretrained_model_name: Name of pretrained (ImageNet) PyTorch model to load e.g. 'efficientnet-b1', see PRETRAINED_MODELS_DICT for all options.
        fc_layers_dict: Dictionary containing specifications (number of nodes) for additional fully-connected layers on top of the pretrained model.
        feature_extract: Determines if we fine-tune (False) the pretrained model to the task.
        model_weights_path: path on the host's filesystem to the trained model weights PyTorch file
        batch_size: Number of samples from test set in each batch.
        criterion_type: Type of loss criterion, e.g. 'nll_loss' (Negative Log-Likelihood Loss).
        metrics_set: Set of metrics to compute, e.g. {'weighted_f1', 'weighted_accuracy'}
        no_cuda: Determines if we should / should not use CUDA even if it is available on the host machine.
        kwargs: Additional settings for CUDA (e.g. num_workers, pin_memory, etc.), if CUDA is available and no_cuda is False. Defaults to {}.
        verbose: Determines if progress inferring on test batches should be logged to stdout throughout testing. Default to False.
    
    Returns:
        metrics_dict: Dictionary mapping metric name to score by a model on the test set. Metrics present in the dictionary are 
            those specified by the metrics_set input parameter
        confusion_matrix: Confusion matrix numPy array of model predictions on a specific test set
        y_true: 1-D numPy row vector, groud truth labels for the task
        y_pred: 1-D numPy row vector, predicted labels from a model
        pred_probs: numPy array of normalized probabilities associated with each class for the prediction task.
            Determined by a sigmoid function in the binary case and softmax in the n-ary case with n > 2
        test_loss: Average loss across the test set using the loss function criterion specified by the criterion_type input parameter
        class_labels_dict: Dictionary mapping class label string to integer index label
    '''
    # Determine testing conditions
    device, use_cuda = determine_device(no_cuda)
    kwargs = kwargs if use_cuda else {}

    test_loader = load_split_data(data_dir, TEST_SPLIT, batch_size, shuffle=False, kwargs=kwargs)
    print("Loaded test data.")
    class_labels_dict = load_class_label_dict(test_loader)
    num_classes = len(class_labels_dict)

    model = construct_model(pretrained_model_name, num_classes, fc_layers_dict=fc_layers_dict, feature_extract=feature_extract)
    model = load_model_weights(model, model_weights_path)
    model.to(device)
    print('Loaded model weights')
    model.eval()

    criterion = construct_criterion(criterion_type, reduction_enum='sum')

    batches = construct_tqdm_batches(test_loader, verbose, unit='batch')

    test_set_n = len(test_loader.dataset)
    test_loss = 0
    correct = 0
    with torch.no_grad():
        y_true, y_pred, pred_probs = torch.tensor([], device=CPU), torch.tensor([], device=CPU), torch.tensor([], device=CPU)
        for batch_idx, (inputs, labels) in batches:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            if num_classes == 2:
                outputs = outputs.squeeze()

            # reduction = 'sum' is used to ignore the impact of batch size
            test_loss += torch.sum(criterion(outputs, loss_func_target_arg(labels, num_classes))).item()

            probs, preds = get_probs_and_preds(outputs, num_classes)

            correct += preds.eq(labels).sum().item()
            y_true, y_pred, pred_probs = torch.cat((y_true, labels.to(CPU)), dim=0), torch.cat((y_pred, preds.to(CPU)), dim=0), torch.cat((pred_probs, probs.to(CPU)), dim=0)

        test_loss /= test_set_n
        y_true, y_pred, pred_probs = y_true.numpy(), y_pred.numpy(), pred_probs.numpy()
        metrics_dict = calc_metric_scores_dict(y_true, y_pred, metrics_set)
        if verbose:
            summary_string = '\nTest set: Average Loss: {:.2e}'.format(test_loss)
            for metric, value in metrics_dict.items():
                summary_string += f'\n {prettify_underscore_string(metric)} Score on Test Set: {value}'
            print(summary_string)
        
        confusion_matrix = calc_confusion_matrix(y_true, y_pred)

    return metrics_dict, confusion_matrix, y_true, y_pred, pred_probs, test_loss, class_labels_dict

def save_test_results(test_json_save_path: str, results_metrics_dict: Dict[str, float], confusion_matrix: np.ndarray, class_label_dict: Dict[str, int]) -> Dict:
    """Saves testing results as a JSON for a model on a specific test set including metric scores,
        a confusion matrix, and a class label mapping at the test_json_save_path on the host's filesystem

  Args:
    test_json_save_path: Path to save test results dictionary as a JSON on the host's filesystem
    results_metrics_dict: Dictionary mapping metric name to score by a model on a specific test set
    confusion_matrix: Confusion matrix numPy array of model predictions on a specific test set
    class_label_dict: Dictionary mapping class label string to integer index label
    
  Returns:
    test_results_dict: Dictionary containing testing results for a model on a specific test set.
        Dictionary contains a dictionary of metrics scores under the METRICS_KEY, a confusion matrix saved as
        nested list under the CONFUSION_MATRIX_KEY, and the class string index label mapping under the CLASS_LABEL_DICT_KEY
  """
    with open(test_json_save_path, 'w') as f:
        test_results_dict = dict()
        test_results_dict[METRICS_KEY] = results_metrics_dict.copy()
        test_results_dict[CONFUSION_MATRIX_KEY] = confusion_matrix.tolist()
        test_results_dict[CLASS_LABEL_DICT_KEY]= class_label_dict
        f.write(json.dumps(test_results_dict))
    return test_results_dict