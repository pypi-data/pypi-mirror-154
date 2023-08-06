import os
from os.path import join
from copy import deepcopy
import json

import numpy as np
from torch.functional import Tensor

from torch.nn.parameter import Parameter

from tqdm import tqdm

import torch
import torch.nn as nn
from torch.nn import Sequential
from torch.utils.data import DataLoader
from torchvision import datasets

from typing import Callable, Dict, Optional, Tuple, List, Union

from .constants import (
  HYPERPARAMETERS_FILENAME,
  CLASS_LABEL_FILENAME,
  TRAINING_SETTINGS_FILENAME,
  TRAINING_RESULTS_FILENAME,
  IMAGE_TRANSFORMS,
  CRITERION_DICT,
)

# Construct loss function
def construct_criterion(criterion_type: str, reduction_enum: str = 'mean') -> Callable:
  """Returns loss criterion function for computing loss on samples during training, evaluation, and testing
    with proper reduction type reduction_enum

  Args:
    criterion_type: Name of the loss criterion to select, e.g. 'cce_loss' for Cross Entropy Categorical Loss
    reduction_enum: Method of reduction when computing the loss across samples. This value can be one of 
        'none' | 'mean' | 'sum'. 
        The default value is 'mean' for computing the mean loss on the input samples, which is typically a batch of samples.
  
  Returns:
    criterion_func: Loss function which takes as input an unnormalized tensor of logits produced as the output from a model
       from input samples and class indices for the target values of the input samples
  """
  return CRITERION_DICT[criterion_type](reduction = reduction_enum)

def get_probs_and_preds(logits: Tensor, num_classes: int) -> Tuple[Tensor, Tensor]:
  """Computes the normalized probability for an input of output logits (unnormalized) 
      from a model and the predicted class index

  Args:
    logits: Unnormalized logits from a model's output
    num_classes: Number of classes for model prediction task, used to determine 
    
  Returns:
    probs: Tensor of normalized probabilities associated with each class for the prediction task.
      Determined by a sigmoid function in the binary case and softmax in the n-ary case with n > 2
    preds: Tensor of predicted class for input samples to the model
  """
  if num_classes == 2:
    # predict class based on prob
    sigmoid_func = nn.Sigmoid()
    probs = sigmoid_func(logits)
    preds = torch.round(probs)
  else:
    softmax_func = nn.Softmax(dim = 1)
    probs = softmax_func(logits)
    _, preds = torch.max(probs, 1) # get index of max probability
    probs, preds = probs.squeeze(), preds.squeeze()
  return probs.detach(), preds.detach()

def loss_func_target_arg(targets: Tensor, num_classes: int) -> Tensor:
  """Casts targets as necessary depending on the number of classes for input to
    the loss function

  Args:
    targets: Raw target tensor containing indices corresponding to ground truth label
    num_classes: Number of classes for model prediction
  
  Returns:
    casted_targets: Target tensor casted to appropriate data type to be used
      as the target input parameter to the loss function
  """
  return targets.float() if num_classes == 2 else targets

# Model Architecture Alteration
def build_classifier(num_input_nodes: int, num_classes: int, fc_layers_dict: Optional[Dict[str, int]] = None) -> Sequential:
  """Builds a classifier to be added to a PyTorch Neural Architecture.

    Classifier is constructed from a dictionary of layer indexes as keys and the number of nodes
    for that layer as the value. Each fully-connected layer applies ReLU activation and 
      dropout with p=0.5.

  Args:
    num_input_nodes: Number of input nodes to the first layer of the classifier
    num_classes: Number of classes for model prediction
    fc_layers_dict: Dictionary used to construct the number of nodes in each fully-connected
      layer of the classifier. E.g. fc_layers_dict = {fc_1_nodes_num: 512, fc_2_nodes_num: 1024}
      Thus the classifier would have two fully-connected layers of 512 nodes followed by 1024 nodes.
      Defaults to None.
  
  Returns:
    classifier: Container of fully-connected layers with the number of input nodes num_input_nodes,
      fully-connected layers with the number of nodes described in fc_layers_dict,
      and an output layer with num_classes nodes representing the unnormalized class scores (logits).
  """
  if fc_layers_dict is None:
    fc_layers_dict = {}
  num_top_fc_layers = len(fc_layers_dict)
  output_layer_i = num_top_fc_layers + 1
  classifier_list = []

  for i in range(num_top_fc_layers + 1):
    if i + 1 == output_layer_i:
      # handle binary case:
      if num_classes == 2:
        output_layer_modules = [nn.Linear(num_input_nodes, 1)]
      else:
        output_layer_modules = [nn.Linear(num_input_nodes, num_classes)]
      classifier_list.extend(output_layer_modules)
      classifier = nn.Sequential(*classifier_list)
    else:
      fc_layer_key = 'fc_{}_nodes_num'.format(i + 1)
      num_fc_layer_nodes = fc_layers_dict[fc_layer_key]
      fc_layer_modules = [nn.Linear(num_input_nodes, num_fc_layer_nodes), nn.ReLU(), nn.Dropout(p=0.5)]
      classifier_list.extend(fc_layer_modules)
      num_input_nodes = num_fc_layer_nodes

  return classifier

def freeze_pretrained_weights_func(model: nn.Module) -> nn.Module:
  """Freezes weights of a PyTorch model.

  Args:
    model: Model whose pretrained weights are being frozen.
  
  Returns:
    model: Model with frozen pretrained weights.
  """
  for param in model.parameters():
    param.requires_grad = False
  return model

# Code inspired from PyTorch tutorial
# https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html
def find_params_to_update(model: nn.Module, feature_extract: bool = False) -> List[Parameter]:
  """Returns learnable (trainable) parameters for the provided model model.

  Args:
    model: Model to be trained.
    feature_extract: Determines if we feature extract or finetune the pretrained model during training. 
  
  Returns:
    params_to_update: List of parameters that will be updated during training by the optimizer algorithm.
  """
  params_to_update = model.parameters()
  if feature_extract:
    params_to_update = []
    for _, param in model.named_parameters():
      if param.requires_grad == True:
        params_to_update.append(param)
  return params_to_update

# Printing model metadata    
def calc_total_trainable_parameters(model: nn.Module) -> int:
  """Calculates the total number of parameters which can be updated during training.

  Args:
    model: The model which the total number of trainable parameters is calculated from.
  
  Returns:
    total_trainable_parameters: Total number of trainable parameters for the model.
  """
  return sum(p.numel() for p in model.parameters() if p.requires_grad)

def calc_total_parameters(model: nn.Module) -> int:
  """Calculates the total number of parameters of a model regardless if they are trainable.

  Args:
    model: The model which the total number of parameters is calculated from.

  Returns:
    total_parameters: Total number of parameters for the model.
  """
  return sum(p.numel() for p in model.parameters())

def calc_and_print_parameters(model: nn.Module) -> Tuple[float, float]:
  """Prints and returns the total number of trainable parameters and total number of parameters for the model model.
    
  Args:
    model: The model from which the total trainable parameters and nontrainable parameters are 
      calculated.

  Returns:
    total_trainable_params: Total number of trainable parameters.
    total_params: Total number of parameters for a model, both trainable and not trainable.
  """
  total_trainable_params, total_params = calc_total_trainable_parameters(model), calc_total_parameters(model)
  print("Total number of trainable parameters for model: ", total_trainable_params)
  print("Total number of parameters for model: ", total_params)
  return total_trainable_params, total_params

# Data Loading
def construct_tqdm_batches(data_loader, verbose=False, unit="batch") -> Union[tqdm, enumerate]:
  """Constructs a tqdm enumeration, which shows the progress of the unit of iteration during training, evaluation, testing, etc.
    but only if verbose is true.

  Args:
    data_loader: DataLoader which contains the batched dataset
    verbose: Determines whether to display tqdm progress during iteration. 
        Default value is False
    unit: string describing unit of iteration. Default is 'batch'
  
  Returns:
    batches: enumeration object with or without tqdm based on verbose with iteration unit unit
  """
  if verbose:
    batches = tqdm(enumerate(data_loader), total=len(data_loader), unit=unit)
  else:
    batches = enumerate(data_loader)
  return batches

def load_split_data(src_dir: str, split_name: str, batch_size: int, shuffle: bool, kwargs={}) -> DataLoader:
  """For a given data split (e.g., "train"), constructs a DataLoader with batches of size batch_size.
    
  Args:
    src_dir: Source directory containing data split folders (e.g. consolidated_crisis_images/train -> src_dir == consolidated_crisis_images)
    split_name: Name of the split. Must be one of 'train', 'dev', or 'test'. Used to index into src_dir.
    batch_size: Size of the batches constructed for the DataLoader. Should be 2**n, where n is an int >=1.
    shuffle: Shuffles data at every epoch if True.
    kwargs: Dictionary containing additional keyword arguments such as num_workers and pin_memory, which are useful for CUDA training. Defaults to {}.
    See more kwargs here: https://pytorch.org/docs/stable/data.html#iterable-style-datasets

  Returns:
    split_loader: DataLoader for the data in the provided split.
  """
  split_path = join(src_dir, split_name)
  split_set = datasets.ImageFolder(split_path, deepcopy(IMAGE_TRANSFORMS[split_name]))
  split_loader = DataLoader(split_set, batch_size=batch_size, shuffle=shuffle, **kwargs)
  return split_loader

def load_class_label_dict(loader: DataLoader) -> Dict[str, int]:
  """Returns a dictionary mapping for classes class label string to integer label index.

  Args:
    loader: DataLoader which contains the dataset with the class mappings.
  
  Returns:
    class_label_dict: Mapping from class name string to index number label.
  """
  return loader.dataset.class_to_idx.copy()

def get_label_to_class_mapping(class_label_dict: Dict[str, int]) -> Dict[int, str]:
  """Returns a dictionary mapping from integer to class string

  Args:
    class_label_dict: Mapping from class name string to index number label
  
  Returns:
    label_class_dict: Mapping from index number label to class name string
  """
  return {label: class_name for class_name, label in class_label_dict.items()}

def label_to_class_np_v_func(class_label_dict: Dict[str, int]) -> Callable:
  """Constructs vectorized function which maps a numpy vector of index labels to their
      corresponding 

  Args:
    class_label_dict: Mapping from class name string to index number label
  
  Returns:
    v_func: Function which takes as input numpy vector of index labels and maps them
      to their class string, e.g. 0 -> 'flood', 1 -> 'not_flood'
  """
  label_class_dict = get_label_to_class_mapping(class_label_dict)
  return np.vectorize(lambda float_label: label_class_dict[int(float_label)])

# Saving and Loading Model Metadata

def save_model_metadata(
  model_weights_path: str, 
  model_dir_path: str,
  hyperparameters_dict: Dict,
  class_label_dict: Dict[str, int],
  training_settings_dict: Dict,
  training_results_dict: Dict
) -> Tuple[Dict, Dict, Dict, Dict]:
  """Saves various dictionaries as JSON files containing model metadata such hyperparameters, class labels, 
      settings used during training and the the results of training at the model_dir_path on the host's filesystem

  Args:
    model_weights_path: Path where model weights are located on the host. Used to copy the 
      PyTorch weights to the model_dir_path on the host
    model_dir_path: Directory on the host where model metadata dictionaries will be saved on
      the host. PyTorch weights file for the model located at model_weights_path are copied to 
      model_dir_path on host
    hyperparameters_dict: Dictionary containing information about hyperparameters used to train the model
    class_label_dict: Dictionary mapping the string class name to index label
    training_settings_dict: Dictionary containing information about settings used for training, e.g. 
      using cuda or cpu during training, version of url_image_module being used, etc. 
      Maps training settings key to corresponding value
    training_results_dict: Dictionary containing information about the results of training.
      Information contained includes average training loss on each epoch and general information
      of model performance on training and dev sets during training
  
  Returns:
    hyperparameters_dict: Dictionary containing information about hyperparameters used to train the model
    class_label_dict: Dictionary mapping the string class name to index label
    training_settings_dict: Dictionary containing information about settings used for training, e.g. 
      using cuda or cpu during training, version of url_image_module being used, etc. 
      Maps training settings key to corresponding value
    training_results_dict: Dictionary containing information about the results of training.
      Information contained includes average training loss on each epoch and general information
      of model performance on training and dev sets during training
  """
  os.system(f'cp {model_weights_path} {model_dir_path}')
  with open(join(model_dir_path, HYPERPARAMETERS_FILENAME), 'w') as f:
    hyperparameters_json = json.dumps(hyperparameters_dict)
    f.write(hyperparameters_json)
  with open(join(model_dir_path, CLASS_LABEL_FILENAME), 'w') as f:
    class_label_json = json.dumps(class_label_dict)
    f.write(class_label_json)
  with open(join(model_dir_path, TRAINING_SETTINGS_FILENAME), 'w') as f:
    training_settings_json = json.dumps(training_settings_dict)
    f.write(training_settings_json)
  with open(join(model_dir_path, TRAINING_RESULTS_FILENAME), 'w') as f:
    training_results_json = json.dumps(training_results_dict)
    f.write(training_results_json)
  return hyperparameters_dict, class_label_dict, training_settings_dict, training_results_dict

def load_model_metadata_dicts(model_dir_path: str) -> Tuple[Dict, Dict, Dict, Dict]:
  """Loads various dictionaries which contain metadata about a specific model located at
      model_dir_path on the host's filesystem

  Args:
    model_dir_path: path on the host containing model metadata dictionaries
  
  Returns:
    hyperparameters_dict: Dictionary containing information about hyperparameters used to train the model
    class_label_dict: Dictionary mapping the string class name to index label
    training_settings_dict: Dictionary containing information about settings used for training, e.g. 
      using cuda or cpu during training, version of url_image_module being used, etc. 
      Maps training settings key to corresponding value
    training_results_dict: Dictionary containing information about the results of training.
      Information contained includes average training loss on each epoch and general information
      of model performance on training and dev sets during training
    
  """
  with open(join(model_dir_path, HYPERPARAMETERS_FILENAME)) as f:
    hyperparameters_dict = json.load(f)
  with open(join(model_dir_path, CLASS_LABEL_FILENAME)) as f:
    class_label_dict = json.load(f)
  with open(join(model_dir_path, TRAINING_SETTINGS_FILENAME)) as f:
    training_settings_dict = json.load(f)
  with open(join(model_dir_path, TRAINING_RESULTS_FILENAME)) as f:
    training_results_dict = json.load(f)
  return hyperparameters_dict, class_label_dict, training_settings_dict, training_results_dict

if __name__ == "__main__":
  pass
