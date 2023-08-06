from os.path import join
import os

import torch
from torch import device
from torch.utils.data import DataLoader
import torch.nn as nn
from torch.optim import Optimizer
from torch.optim.lr_scheduler import ReduceLROnPlateau

import numpy as np

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from time import time
from copy import deepcopy
import random
from typing import Dict, Tuple

from .constants import (
  DEV_SPLIT,
  TRAIN_SPLIT,
  CPU,
)

from .classes import (
  construct_model,
  construct_optimizer,
)

from .misc_utils import (
  get_version,
  prettify_underscore_string
)

from .pt_utils import (
  generate_pt_filename,
  determine_device
)

from .metric_utils import (
  calc_metric
)

from .model_utils import (
  construct_criterion,
  calc_and_print_parameters,
  construct_tqdm_batches,
  load_class_label_dict,
  load_split_data,
  get_probs_and_preds,
  loss_func_target_arg
)

def train(
  model: nn.Module, 
  device: device, 
  train_loader: DataLoader,
  grad_accumulation_steps: int,
  optimizer: Optimizer, 
  criterion_type: str, 
  epoch: int, 
  n_epochs: int,
  metric: str,
  verbose: bool = False
) -> Tuple[float, float]:
  '''Trains the model model on one epoch on the entire dataset shuffeled into minibatches of size train_loader.batch_size using optimizer optimizer.

  Model weights are updated based on loss on training samples of training set shuffled into minibatches of size
  train_loader.batch_size and optimizer optimizer. Average training loss and performance metric on training set are returned for tracking
  model progress over epochs on the training set.

  Args:
    model: The model being trained.
    device: Torch device used to cast tensors to CPU or CUDA to speed up computations.
    train_loader: Data loader for training images in the training data folder.`
    grad_accumulation_steps: Number of steps to accumulate gradients before we update parameters using optimizer. train_loader.batch_size * accumulation_steps = global batch size
    optimizer: Optimizer used when performing weight updates from the batch training samples.
    criterion_type: Criterion function used for calculating the loss of a sample. The loss criterion is computed on each sample,
      but is reduced to a single number for the entire minibatch using the value provided for the reduction parameter, such as 'mean' or 'sum'.
    epoch: Number of current epoch e.g. epoch 4 of 12.
    n_epochs: Total number of epochs specified for training the model (used for metric calculations and logging).
    metric: Evaluation metric of interest for tracking training progress on training set.
    verbose: Determines if results of training (i.e. progress, metric performance, etc.) 
      on each batch should be logged to stdout. Defaults to False.
  
  Returns:
    avg_train_loss: Average training loss across training set for this epoch.
    train_score: Score of evaluation metric on training set for this epoch.
  '''
  print("Starting training for this epoch.")
  model.train()
  train_set_num_samples = len(train_loader.dataset)
  num_classes = len(load_class_label_dict(train_loader))
  criterion = construct_criterion(criterion_type)
  total_train_loss = 0
  prettified_metric = prettify_underscore_string(metric)
  y_true, y_pred, pred_probs = torch.tensor([], device=CPU), torch.tensor([], device=CPU), torch.tensor([], device=CPU)

  batches = construct_tqdm_batches(train_loader, verbose, unit='batch')

  for batch_idx, (inputs, labels) in batches:
    inputs, labels = inputs.to(device), labels.to(device)
    outputs = model(inputs)
    if num_classes == 2:
      outputs = outputs.squeeze()
    # loss computed is the average loss across samples in the minibatch computing
    # by summing the loss of each sample in the minibatch divided by the 
    # total number of samples in the batch (e.g. mean loss)
    loss = criterion(outputs, loss_func_target_arg(labels, num_classes))
    # Since we are accumulating the gradient across the batch size of size train_loader.batch_size * grad_accumulation_steps, we need to divide
    # the mean loss across the minibatch of size train_loader.batch_size by grad_accumulaton_steps in order for the mean loss to correspond 
    # to the mean loss of the samples in the desired batch of size train_loader.batch_size * grad_accumulation_steps rather than the mean
    # of samples in the minibatch corresponding to train_loader.batch_size.
    loss = loss / grad_accumulation_steps
    # Accumulates the gradients
    loss.backward()
    # Used to get total loss across samples in minibatch
    num_samples_in_batch = inputs.size(0)
    total_train_loss += loss.item() * num_samples_in_batch * grad_accumulation_steps
    if (batch_idx + 1) % grad_accumulation_steps == 0:
      # Only update model parameters when we have reached the global batch_size, i.e. train_loader.batch_size * grad_accumulation_steps
      optimizer.step()
      optimizer.zero_grad()

    probs, preds = get_probs_and_preds(outputs, num_classes)

    y_true, y_pred, pred_probs = torch.cat((y_true, labels.to(CPU)), dim=0), torch.cat((y_pred, preds.to(CPU)), dim=0), torch.cat((pred_probs, probs.to(CPU)), dim=0)
    metric_score = calc_metric(y_true, y_pred, metric)
    if verbose:
      batches.set_description(
          "Epoch {:d}/{:d}: Loss ({:.2e}), {} Score ({:02.0f}%)".format(
              epoch, n_epochs, loss.item(), prettified_metric, 100. * metric_score
          )
      )

  avg_train_loss = total_train_loss / train_set_num_samples
  train_score = calc_metric(y_true, y_pred, metric)
  print("\nFinished training for this epoch.")

  return avg_train_loss, train_score

def validate(
  model: nn.Module, 
  device: device, 
  dev_loader: DataLoader, 
  criterion_type: str,
  metric: str,
  verbose: bool = False
) -> Tuple[float, float]:
  '''Evaluates the model on the entire dev set to provide performance metrics on data that is unseen during training.

  Model is evaluated on the unseen data in the dev set. Average dev loss and performance metric on dev set are returned for tracking
  model progress over epochs on the dev set.

  Args:
    model: The model being evaluated.
    device: Torch device used to cast tensors to CPU or CUDA to speed up computations.
    dev_loader: Data loader for dev images in the dev data folder.
    criterion_type: Criterion function used for calculating the loss of a sample. The criterion function used in validate reduces the 
      loss across samples in a minibatch to the sum of the loss of those samples in the batch in order to make the dev loss comparable to
      the train loss above.
    metric: Evaluation metric of interest for tracking training progress on dev set.
    verbose: Determines if results of dev evaluation (i.e. loss, metric performance)
      across entire dev set should be logged to stdout. Defaults to False.
  
  Returns:
    avg_dev_loss: Average dev loss across dev set.
    dev_score: Score of evaluation metric on the dev set for this epoch.
  '''
  print("Evaluating Model on the Dev Set...")
  model.eval()
  dev_set_n = len(dev_loader.dataset)
  # reduction='sum' is used to ignore the impact of batch size and make this loss 
  # comparable to the loss in the train loop above.
  criterion = construct_criterion(criterion_type, reduction_enum='sum')
  num_classes = len(load_class_label_dict(dev_loader))
  total_dev_loss = 0
  prettified_metric = prettify_underscore_string(metric)

  batches = construct_tqdm_batches(dev_loader, verbose, unit="batch")

  y_true, y_pred, pred_probs = torch.tensor([], device=CPU), torch.tensor([], device=CPU), torch.tensor([], device=CPU)
  with torch.no_grad():
    for batch_idx, (inputs, labels) in batches:
      inputs, labels = inputs.to(device), labels.to(device)
      outputs = model(inputs)
      if num_classes == 2:
        outputs = outputs.squeeze()
      
      total_dev_loss += torch.sum(criterion(outputs, loss_func_target_arg(labels, num_classes))).item()

      probs, preds = get_probs_and_preds(outputs, num_classes)

      y_true, y_pred, pred_probs = torch.cat((y_true, labels.to(CPU)), dim=0), torch.cat((y_pred, preds.to(CPU)), dim=0), torch.cat((pred_probs, probs.to(CPU)), dim=0)
  
  avg_dev_loss = total_dev_loss / dev_set_n
  dev_score = calc_metric(y_true, y_pred, metric)

  if verbose:
    batches.set_description(
          'Dev Set: Average Loss: {:.2e}, {} Score ({:.0f}%)\n'.format(
        avg_dev_loss, prettified_metric, 100. * dev_score
      )
    )

  return avg_dev_loss, dev_score

def train_on_n_epochs(
  model_id: int,
  task_name: str,
  data_dir: str,
  pretrained_model_name: str,
  epochs: int,
  train_batch_size: int,
  grad_accumulation_steps: int,
  feature_extract: bool,
  fc_layers_dict: Dict[str, int],
  optimizer_type: str,
  learning_rate: float,
  criterion_type: str,
  metric: str,
  patience: int, 
  lr_reduction_factor: float,
  dev_batch_size: int,
  seed: int,
  no_cuda: bool,
  kwargs: Dict = {},
  sio_client = None,
  verbose: bool = True
) -> Tuple[Dict, Dict, Dict, Dict, nn.Module, str]:
  '''Trains a model on epochs epochs and evaluates performance of model on each epoch using unseen data in the dev set.

    Trains, validates, and saves model weights and training metadata. Model weights are saved in the filesystem and correspond to the weights of the model
    at the epoch where the best performance on the dev set is achieved.

  Args:
    model_id: ID of the model, such as in a DB.
    task_name: Name of the classification task the model is being trained to do.
    data_dir: Path to directory containing the image dataset folders based on split ex. data_dir/train, data_dir/dev, data_dir/test.
    pretrained_model_name: Name of pretrained (ImageNet) PyTorch model to load e.g. 'efficientnet-b1', see PRETRAINED_MODELS_DICT for all options.
    epochs: Total number of full passes through the training dataset.
    train_batch_size: Number of training samples from training set in each batch.
    grad_accumulation_steps: Number of steps to accumulate gradients before we update parameters using optimizer. train_loader.batch_size * accumulation_steps = train_batch_size
    feature_extract: Determines if we fine-tune (False) the pretrained model to the task.
    fc_layers_dict: Dictionary containing specifications (number of nodes) for additional fully-connected layers on top of the pretrained model.
    optimizer_type: Name of the optimizer used in the updating of the model weights e.g. 'Adam', see OPTIMIZER_DICT for all options.
    learning_rate: Initial learning rate used by the optimizer for model weight updates during training.
    criterion_type: Type of loss criterion, e.g. 'nll_loss' (Negative Log-Likelihood Loss).
    metric: Evaluation metric used for tracking training progress and improvement/worsening over epochs.
    patience: Number of epochs allowed with no improvement of the model's performance on the dev set until we reduce the learning rate by lr_reduction_rate. 
      We reset patience whenever we reduce the learning rate.
    lr_reduction_rate: Factor we reduce the learning rate by after patience epochs of no improvement on the performance metric on the dev set.
    dev_batch_size: Number of samples in the dev set to process in a minibatch when evaluating the model.
    seed: Sets the seed for generating random numbers in PyTorch as in torch.manual_seed(seed).
    no_cuda: Determines if we should / should not use CUDA even if it is available on the Host machine.
    kwargs: Additional settings for CUDA (e.g. num_workers, pin_memory, etc.), if CUDA is available and no_cuda is False. Defaults to {}.
    sio_client: Socket.io Client, which sends updates about training to a Socket.io server subscribed to the events in the function (namely: 'client-training-update').
      Defaults to None.
    verbose: Determines if progress updates (from tqdm, train, validate) should be logged to stdout throughout training. Default to False.
  
  Returns:
    hyperparameters: Dictionary containing hyperparameters used when training the model such as epochs, training batch size, optimizer type, etc. 
    class_label_dict: Dictionary mapping the string version label for a task to the integer label
    training_settings_dict: Dictionary containing settings for training such as the type of torch device (CUDA or CPU), size of dev batches, version of image module, etc.
    training_results_dict: Dictionary containing training metadata (e.g. total training) and performance results from training and validating over all epochs.
    model: Trained nn.Module model with final weights which attained the best dev set metric during training
    model_weights_path: Path to trained model weights .pt file on the host.
  '''

  training_settings_dict = {
    'devBatchSize': dev_batch_size,
    'gradAccumulationSteps': grad_accumulation_steps,
    'seed': seed,
    'noCuda': no_cuda,
    'imageModuleGitVersion': get_version(),
  }

  hyperparameters_dict =  {
    'pretrainedModelName': pretrained_model_name,
    'taskName': task_name,
    'epochs': epochs,
    'trainBatchSize': train_batch_size,
    'featureExtract': feature_extract,
    'fcLayersDict': fc_layers_dict.copy(),
    'optimizerType': optimizer_type,
    'learningRate': learning_rate,
    'criterionType': criterion_type,
    'metric': metric,
    'patience': patience,
    'learningRateReductionFactor': lr_reduction_factor,
  }
  
  training_results_dict = {}

  model_weights_filename_prefix = f'{task_name}_{model_id}'
  model_weights_path = join(data_dir, generate_pt_filename(model_weights_filename_prefix))

  
  torch.manual_seed(seed)
  torch.cuda.manual_seed_all(seed)
  torch.backends.cudnn.deterministic = True
  torch.backends.cudnn.benchmark = False
  torch.use_deterministic_algorithms(True)
  np.random.seed(seed)
  random.seed(seed)
  os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':16:8'

  def seed_worker(worker_id):
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)

  g = torch.Generator()
  g.manual_seed(seed)

  # Load device according to host GPU hardware and provided training settings
  device, use_cuda = determine_device(no_cuda)
  training_settings_dict['deviceType'] = device.type
  server_update_string = f"Using {device.type.upper()} for training.\n\n"
  if device.type == 'cuda':
      gpu_model = torch.cuda.get_device_name(torch.cuda.current_device())
      training_settings_dict['gpuModel'] = gpu_model
      server_update_string += f"GPU Model: {gpu_model}\n\n"
  print(server_update_string)
  kwargs = kwargs if use_cuda else {}
  training_settings_dict['kwargs'] = kwargs.copy()
  if 'num_workers' in kwargs:
    kwargs['worker_init_fn'] = seed_worker
    kwargs['generator'] = g
  
  # Send finalized hyperparameters & training settings to a subscribed server
  if sio_client:
    sio_client.emit(
      'training-initialized',
      {
        'message': server_update_string,
        'id': model_id,
        'hyperparameters': hyperparameters_dict,
        'trainingSettings': training_settings_dict,
      }, 
      namespace='/model'
    )
  print('Loading images into dataloaders...')

  # TODO: Need to figure out if we can automate the estimation of the optimal grad_accumulation_steps (e.g. using memory constraints of host & memory requirements for dataloaders) 
  # to maximize memory use without having the user manually specify it.

  # Load Train and Dev Data
  train_loader = load_split_data(data_dir, TRAIN_SPLIT, int(train_batch_size / grad_accumulation_steps), shuffle=True, kwargs=kwargs)
  dev_loader = load_split_data(data_dir, DEV_SPLIT, dev_batch_size, shuffle=False, kwargs=kwargs)
  print('Finished loading images to dataloaders.')
  class_label_dict = load_class_label_dict(train_loader)
  num_classes = len(class_label_dict)

  # Configure model
  model = construct_model(pretrained_model_name, num_classes, fc_layers_dict, feature_extract).to(device)

  # Compute & store model metadata
  total_trainable_params, total_params = calc_and_print_parameters(model)
  training_results_dict['totalTrainableParameters'] = total_trainable_params
  training_results_dict['totalParameters'] = total_params

  # Configure optimizer & scheduler
  optimizer = construct_optimizer(pretrained_model_name, model, optimizer_type, learning_rate, feature_extract)
  scheduler = ReduceLROnPlateau(optimizer, 'max', factor=lr_reduction_factor, patience=patience, verbose=verbose)

  # Configure training & dev results
  avg_train_loss_list, train_score_list = [], []
  avg_dev_loss_list, dev_score_list = [], []
  best_dev_score = 0
  best_model_weights = deepcopy(model.state_dict())
  prettified_metric = prettify_underscore_string(metric)
  start_time = time()
  for epoch in range(1, epochs + 1):
    avg_train_loss, train_score = train(model, device, train_loader, grad_accumulation_steps, optimizer, criterion_type, epoch, epochs, metric, verbose=verbose)
    avg_dev_loss, dev_score = validate(model, device, dev_loader, criterion_type, metric, verbose=verbose)
    avg_train_loss_list.append(avg_train_loss)
    train_score_list.append(train_score)
    avg_dev_loss_list.append(avg_dev_loss)
    dev_score_list.append(dev_score)
    scheduler.step(dev_score)
    if verbose:
      print('Epoch {0:d}/{1:d}'.format(epoch, epochs))
      print('-' * 10)
      print("Train {0} Score: {1:.2f}%, Train Loss: {2:.5f}\nDev {3} Score: {4:.2f}%, Dev Loss: {5:.5f}".format(
          prettified_metric, 100. * train_score, avg_train_loss, prettified_metric, 100. * dev_score, avg_dev_loss))

    if dev_score > best_dev_score:
      last_best_dev_score = best_dev_score
      best_dev_score = dev_score
      print(f"Best Dev {prettified_metric} improved from {last_best_dev_score} to {best_dev_score} | Saving model weights...")
      # save best dev score model weights
      best_model_weights = deepcopy(model.state_dict())
      torch.save(best_model_weights, model_weights_path)
      print("Model weights saved.")
  
  end_time = time()
  total_training_time = end_time - start_time # In seconds
  print("Total training time for {0} Epochs: {1:.0f}m {2:.0f}s".format(epochs, total_training_time // 60, total_training_time % 60))
  
  # Training Results and related metadata
  training_results_dict['totalTrainingTime'] = total_training_time
  training_results_dict['avgTrainLossList'], training_results_dict['trainScoreList'] = avg_train_loss_list, train_score_list
  training_results_dict['avgDevLossList'], training_results_dict['devScoreList']  = avg_dev_loss_list, dev_score_list

  training_settings_dict = deepcopy(training_settings_dict)
  hyperparameters_dict = deepcopy(hyperparameters_dict)
  training_results_dict = deepcopy(training_results_dict)

  model.load_state_dict(best_model_weights)

  return hyperparameters_dict, class_label_dict, training_settings_dict, training_results_dict, model, model_weights_path

if __name__ == "__main__":
  pass