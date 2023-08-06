from typing import Callable, Dict, List

from torchvision import transforms
import torch.nn as nn

import numpy as np

import sklearn.metrics as skm

from ._version import get_versions

__version__: str = get_versions()['version']
del get_versions
"""Version of URL Image Module
"""

ABBREVIATION_DICT: Dict[str, str] = {
    'lr': 'Learning Rate',
    'fc': 'Fully-Connected',
    'kwargs': 'kwargs',
}
"""Mapping from abbreviation to prettified string.
"""

###############
# Data Splits #
###############
TRAIN_SPLIT: str = 'train'
DEV_SPLIT: str = 'dev'
TEST_SPLIT: str = 'test'
"""Constants useful for referring to data folders for different splits on the local filesystem.
"""

############################################################################
# PyTorch Pretrained Model Input Normalization Constants for Preprocessing #
############################################################################
# pretrained image PyTorch models require specific transforms on the inputs.
IMAGE_SIZE: int = 224
IMAGE_RESIZE: int = 256
IMAGE_NORMALIZE_MEAN: List[float] = [0.485, 0.456, 0.406]
IMAGE_NORMALIZE_STD: List[float] = [0.229, 0.224, 0.225]

# Transformations to the input images as part of data augmentation -- May be better as a user-provided hyperparameter
SCALE_ARG_1: float = 0.8
SCALE_ARG_2: float = 1.0
DEGREES: float = 15

#########################################################################################################
# Image Transformation for providing more training examples and normalizing input data as preprocessing #
#########################################################################################################
IMAGE_TRANSFORMS: Dict[str, transforms.Compose] = {
    # Data augmentation, and normalization for training
    TRAIN_SPLIT: transforms.Compose([
        transforms.RandomResizedCrop(size=IMAGE_RESIZE, scale=(SCALE_ARG_1, SCALE_ARG_2)),
        transforms.RandomRotation(degrees=DEGREES),
        transforms.RandomHorizontalFlip(),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(IMAGE_NORMALIZE_MEAN, IMAGE_NORMALIZE_STD)
    ]),
    # Just normalization for dev and testing
    DEV_SPLIT: transforms.Compose([
        transforms.Resize(IMAGE_RESIZE),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(IMAGE_NORMALIZE_MEAN, IMAGE_NORMALIZE_STD)
    ]),
    TEST_SPLIT: transforms.Compose([
        transforms.Resize(IMAGE_RESIZE),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(IMAGE_NORMALIZE_MEAN, IMAGE_NORMALIZE_STD)
    ])
}
"""Image transformations applied to respective data splits.

    Data augmentations applied to train set as a form of regularization.
    Data augmentations not applied to dev or test sets, only necessary transformations
    applied for model input for prediction.
    
"""

###################
# Loss Criterions #
###################
CRITERION_DICT: Dict[str, Callable] = {
    'cce_loss': nn.CrossEntropyLoss,
    'bce_loss': nn.BCEWithLogitsLoss
}
"""Various loss criterion functions for computing losses on samples during training and evaluation.
"""


###############################
# Evaluation Metric Functions #
###############################
EVALUATION_METRICS_FUNC_DICT: Dict[str, Callable[[np.ndarray, np.ndarray], float]] = {
    'f1': skm.f1_score,
    'weighted_accuracy': skm.balanced_accuracy_score,
    'accuracy': skm.accuracy_score,
    'recall': skm.recall_score,
    'precision': skm.precision_score,
    'roc_auc': skm.roc_auc_score
}
"""Various functions for computing a metric score based on the predicted outputs of a model and the associated targets.
"""

###########################
# Dataframe Column Names  #
###########################
SOURCE_KEY: str = 'source'
FILENAME_KEY: str = 'filename'
INDICES_SET_KEY: str = 'indices_set'
FILENAMES_SET_KEY: str = 'filenames_set'
ORIGINAL_COL_NAME_KEY: str = 'original_col_name'
TASK_NAME_KEY: str = 'task_name'
AUTHOR_ID_KEY: str = 'author_id'
TASK_NAME_AUTHOR_ID_KEY: str = 'task_name.author_id'
LABEL_KEY: str = 'label'
PRED_KEY: str = 'pred'
TRUE_KEY: str = 'true'
PRED_PROBS_KEY: str = 'pred_probs'
"""Pandas column names and dictionary keys useful for providing standard columns names for ease of
    access of pandas and data labeling utilies
"""

####################
# Prediction Types #
####################
CORRECT_KEY: str = 'correct'
INCORRECT_KEY: str = 'incorrect'
UNLABELED_KEY: str = 'unlabeled'
PRED_TYPES = [CORRECT_KEY, INCORRECT_KEY, UNLABELED_KEY]
"""Different types of model predictions, i.e. only can be correct (equals from ground-truth label), 
    incorrect (does not equal ground-truth label), or the data is actually unlabeled
"""

###########################
# Labeling Predicate Keys #
###########################
IS_COMPLETE_AGREEMENT_KEY: str = 'is_complete_agreement'
IS_COMPLETE_DISAGREEMENT_KEY: str = 'is_complete_disagreement'
IS_PLURALITY_AGREEMENT_AND_NOT_COMPLETE_AGREEMENT_KEY: str = 'is_plurality_agreement_and_not_complete_agreement'
"""Different types of labeling predicates, i.e. is complete agreement across all annotators, which are useful
    for data labeling review utilities
"""

############################
# Model Metadata Filenames #
############################
HYPERPARAMETERS_FILENAME: str = 'hyperparameters.json'
TRAINING_SETTINGS_FILENAME: str = 'training_settings.json'
TRAINING_RESULTS_FILENAME: str = 'training_results.json'
CLASS_LABEL_FILENAME: str = 'class_label_dict.json'
"""Filenames useful for saving and loading model metadata for 
    determining model hyperparameters, training settings used for training the model,
    the resultant trained weights file, the dictionary mapping string label to index label
    and other important metadata
"""

#####################
# Test Results Keys #
#####################
METRICS_KEY: str = 'metrics'
CONFUSION_MATRIX_KEY: str = 'confusion_matrix'
CLASS_LABEL_DICT_KEY: str = 'class_label_dict'
"""Dictionary keys useful for saving model performance metadata, such as resultant metrics,
    confusion matrix, and the class label dictionary mapping string label to index
"""

##################################
# PyTorch Weights File Extension #
##################################
PYTORCH_EXT: str = '.pt'
"""Extension for PyTorch files which store model weights.
"""

#####################
# PyTorch Specifics #
#####################
CPU: str = 'cpu'
CUDA: str = 'cuda'
"""Host system settings important for PyTorch tensor computations
"""

###########################
# Miscellaneous Constants #
###########################
IGNORE_FILES: List[str] = [
    '.DS_Store'
]
"""Files which to ignore when looking in directories for data samples in a filesystem.
"""










