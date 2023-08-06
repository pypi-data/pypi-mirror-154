import os
from typing import Dict, Optional

from efficientnet_pytorch import EfficientNet
import torch
from torch.functional import Tensor
import torch.optim as optim
from torchvision import transforms
from torch.optim.optimizer import Optimizer
from torch.utils.data import Dataset
from torchvision import models
import torch.nn as nn

from PIL import Image

from typing import Union, Tuple

from .constants import (
  IGNORE_FILES
)

from .pt_utils import (
  determine_device,
)

from .model_utils import (
  freeze_pretrained_weights_func,
  build_classifier,
  find_params_to_update,
)

# Image Inference Dataset
class PredictionImageDataset(Dataset):
  """Class for loading a directory of images on the host to be used for inference.

  Args:
    image_dir: Path to images folder on the host
    transform: PyTorch transform for transforming images as input for inference
  """
  def __init__(self, image_dir: str, transform: Union[transforms.Compose, None] = None):
    self.image_dir = image_dir
    self.transform = transform
    self.img_paths = os.listdir(image_dir)
    # Removes non-image files, e.g. '.DS_Store'
    for filename in IGNORE_FILES:
      if filename in self.img_paths:
        self.img_paths.remove(filename)
  
  def __len__(self) -> int:
    """Returns number of images present in the Dataset.

    Returns:
      num_images: Total Number of images in the dataset
    """
    return len(self.img_paths)

  def __getitem__(self, idx: int) -> Tuple[Tensor, str]:
    """Returns a tensor representing the image in the dataset at index idx in self.img_paths

    Args:
      idx: index for fetching image with path on the host located at self.img_paths[idx]

    Returns:
      tensor_image: Corresponding tensor for transformed image located at self.img_paths[idx]
      img_filename: filename for image located at self.img_paths[idx]
    """
    img_loc = os.path.join(self.image_dir, self.img_paths[idx])
    img_filename = img_loc.split('/')[-1]
    image = Image.open(img_loc).convert("RGB")
    tensor_image = self.transform(image)
    return tensor_image, img_filename

# Pretrained CNN Models

# Note: PyTorch on pre-trained image classifiers: https://pytorch.org/docs/stable/torchvision/models.html
# I.e. pretrained image models require specific transforms on the inputs.

class PretrainedImageCNN:
  """Base class for wrapper classes around pretrained image PyTorch models used in the URL Image Module Package.
  """
  def __init__(self):
    pass

  def load_model(self, num_classes: int, fc_layers_dict: Optional[Dict[str, int]] = None, feature_extract: bool = False) -> nn.Module:
    """Loads model by making proper request based on specific model type

    Args:
      num_classes: Number of total classes for the classification task. Used for determining
        the number of nodes at the output layer of the model.
      fc_layers_dict: Dictionary containing specifications (number of nodes) for additional fully-connected layers on top of the pretrained model. Defaults to None.
      feature_extract: Determines if we feature extract or finetune the pretrained model during training. 
        If we feature extract, we freeze all pretrained weights during training and only update the parameters in the newly intialized final layer.
        If we finetune, we update all parameters of the model. 
        Defaults to False.

    Returns:
      model: Loaded pretrained image model.
    """
    raise NotImplementedError
  
  def load_optimizer(self, model: nn.Module, optimizer_class: Optimizer, lr: float = 1e-5, feature_extract: bool = False) -> Optimizer:
    """Loads optimizer by making proper request based on specific model type

    Args:
      model: Model used to find the trainable parameters for the optimizer to update.
      optimizer_class: Algorithm used for the optimizer, e.g. Adam, SGD, etc.
      lr: Learning rate used by the optimization algorithm. Defaults to 0.0001.
      feature_extract: Defaults to False.

    Returns:
      optimizer: Optimizer used for updating the weights during training, e.g. Adam or SGD.
    """
    update_params = find_params_to_update(model, feature_extract)
    optimizer = optimizer_class(update_params, lr=lr)
    return optimizer


class PretrainedEfficientNet(PretrainedImageCNN):
  """Wrapper class for loading a pretrained EfficientNet-b* PyTorch Model.

  Args:
    type: Type of EfficientNet model to load, i.e. EfficientNet-{type}. Defaults to 'b1'.
  """
  def __init__(self, type: str = 'b1') -> None:
    self.type = type

  def get_type(self) -> str:
    """Gets type of this EfficientNet instance.

    Returns:
      type: type of the EfficientNet model, e.g. 'b1'.
    """
    return self.type
      
  def load_model(self, num_classes: int, fc_layers_dict: Optional[Dict[str, int]] = None, feature_extract: bool = False):
    if fc_layers_dict is None:
      fc_layers_dict = {}
    
    model = EfficientNet.from_pretrained(f'efficientnet-{self.type}')
    print(f'Loaded base EfficientNet-{self.type} model')
    print('Constructing final model...')
    
    if feature_extract:
      model = freeze_pretrained_weights_func(model)

    classifier_input_nodes_num = model._fc.in_features
    classifier = build_classifier(classifier_input_nodes_num, num_classes, fc_layers_dict)
    model._fc = classifier

    print('Constructed final model.')
    return model

class PretrainedVGG16(PretrainedImageCNN):
  """Wrapper class for loading a pretrained VGG16 PyTorch model.

  Attributes:
    __output_layer_idx (private): Index corresponding to the output layer of the classifier for the VGG16 model, which is 6.
  """
  __output_layer_idx: int = 6

  def load_model(self, num_classes: int, fc_layers_dict: Optional[Dict[str, int]] = None, feature_extract: bool = False):
    if fc_layers_dict is None:
      fc_layers_dict = {}

    model = models.vgg16(pretrained=True)
    print('Loaded base VGG16 Model...')
    print('Constructing final model...')

    if feature_extract:
      model = freeze_pretrained_weights_func(model)

    classifier_input_nodes_num = model.classifier[self.__output_layer_idx].in_features
    classifier = build_classifier(classifier_input_nodes_num, num_classes, fc_layers_dict)
    model.classifier[self.__output_layer_idx] = classifier

    print('Constructed final model.')
    return model

###################################
# Pretrained PyTorch Image Models #
###################################
PRETRAINED_MODELS_DICT: Dict[str, PretrainedImageCNN] = {
    'efficientnet-b1': PretrainedEfficientNet('b1'),
    'vgg16': PretrainedVGG16()
}
"""Instances of various pretrained PyTorch image models.
"""

###################
# Optimizer Types #
###################
OPTIMIZER_DICT: Dict[str, optim.Optimizer] = {
    'Adam': optim.Adam,
    'SGD': optim.SGD
}
"""Various optimizer algorithm classes for updating model weights during training.
"""

###########
# Helpers #
###########
def construct_model(pretrained_model_name: str, num_classes: int, fc_layers_dict: Dict[str, int], feature_extract: bool) -> nn.Module:
  """Returns a base model for a pretrained model architecture and modifying the base architecture for 
    the classification task, i.e. number of output classes (num_classes), freezing pretrained weights during training (feature_extract)

  Args:
    pretrained_model_name: name of pretrained cnn model to use, e.g. 'efficientnet-b1' from the PRETRAINED_MODELS_DICT
    num_classes: Number of total classes for the classification task
    fc_layers_dict: Dictionary containing specifications (number of nodes) for additional fully-connected layers on top of the pretrained model. Defaults to None.
    feature_extract: Determines if we feature extract or finetune the pretrained model during training.  

  Returns:
    model: base pretrained CNN model prepped for training
  """
  model_instance = PRETRAINED_MODELS_DICT[pretrained_model_name]
  model = model_instance.load_model(num_classes, fc_layers_dict=fc_layers_dict, feature_extract=feature_extract)
  return model

def load_model_weights(model: nn.Module, path_to_model_weights: str) -> nn.Module:
  """Loads trained model weights into base model

  Args:
    model: base model without trained weight
    path_to_model_weights: path to PyTorch file containing trained weights for the model model

  Returns:
    model: model loaded with trained weights
  """
  device, _ = determine_device()
  model.load_state_dict(torch.load(path_to_model_weights, map_location=device))
  print('Loaded model weights')
  return model

def construct_optimizer(pretrained_model_name: str, model: nn.Module, optimizer_type: str, learning_rate: float, feature_extract: bool) -> Optimizer:
  """Constructs optimizer for updating model weights during training

  Args:
    pretrained_model_name: name of pretrained cnn model to use, e.g. 'efficientnet-b1' from the PRETRAINED_MODELS_DICT
    model: Pretrained CNN model prepped for training
    optimizer_type: name of optimizer algorithm to use during training, e.g. 'Adam' from the OPTIMIZER_DICT
    learning_rate: Initial learning rate to be used by the optimizer during training.
    feature_extract: Determines if we feature extract or finetune the pretrained model during training.  
  
  Returns:
    optimizer: Optimizer prepped for updating model model weights during training
  """
  model_instance = PRETRAINED_MODELS_DICT[pretrained_model_name]
  optimizer_class = OPTIMIZER_DICT[optimizer_type]
  optimizer = model_instance.load_optimizer(
    model, optimizer_class, lr=learning_rate, feature_extract=feature_extract
  )
  return optimizer
