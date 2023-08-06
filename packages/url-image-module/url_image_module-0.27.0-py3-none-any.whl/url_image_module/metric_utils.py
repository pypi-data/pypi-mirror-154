from typing import Dict, List, Optional
import numpy as np
import sklearn.metrics as skm

from .constants import (
    EVALUATION_METRICS_FUNC_DICT
)

from .misc_utils import (
    prettify_underscore_string
)

# Evaluation Metrics
def calc_metric(y_true: np.ndarray, y_pred: np.ndarray, metric_name: str, verbose: bool = False) -> float:
  """Computes the metric score for an array of predictions and ground truth labels.

  Args:
    y_true: Groud truth labels for the task.
    y_pred: Predicted labels from a model.
    metric_name: Name of the metric we are computing.
    verbose: Determines if metric and associated computed metric should be printed. Default value is False.

  Returns:
    metric_score: Score computed from metric function applied to y_true and y_pred.
  """
  # Calc weighted metrics including F1 score, Accuracy, Recall, Precision, ROC AUC score
  res_string = ''
  split_metric_name = metric_name.split('_')
  if split_metric_name[0] == 'weighted':
    metric = "_".join(split_metric_name[1:])
    is_weighted = True
  else:
    metric = metric_name
    is_weighted = False
  metric_func = EVALUATION_METRICS_FUNC_DICT[metric]
  if is_weighted:
    if metric == 'accuracy':
      metric_func = EVALUATION_METRICS_FUNC_DICT['weighted_accuracy']
      metric_score = metric_func(y_true, y_pred)
    else:
      metric_score = metric_func(y_true, y_pred, average='weighted')
    res_string += f"Weighted "
  else:
    metric_score = metric_func(y_true, y_pred)
  res_string += f"{prettify_underscore_string(metric)} Score: {metric_score}"
  if verbose:
    print(res_string)
  return metric_score

def calc_metric_scores_dict(y_true: np.ndarray, y_pred: np.ndarray, metrics_set: set) -> Dict[str, float]:
  """Computes a metric score for every metric present as a key in evaluation_metrics_func_dict, returns a mapping from metric name to score.

  Args:
    y_true: 1-D numPy row vector, groud truth labels for the task.
    y_pred: 1-D numPy row vector, predicted labels from a model.
    metrics_set: set of metrics to compute, e.g. {'weighted_f1', 'weighted_accuracy'}.
   
  Returns:
    metric_scores_dict: Dictionary mapping metric name to associated metric score computed 
      from the associated metric function applied on y_true and y_pred.
  """
  metric_scores_dict = { metric: calc_metric(y_true, y_pred, metric) for metric in metrics_set }
  return metric_scores_dict

def calc_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, ordered_labels_list: Optional[List[str]] = None) -> np.ndarray:
  """Computes the confusion matrix given ground truth labels y_true and predicted labels y_pred.

  Args:
    y_true: 1-D numPy row vector, groud truth labels for the task.
    y_pred: 1-D numPy row vector, predicted labels from a model.
    ordered_labels_list: List of labels (as they appear in y_true & y_pred), ordered by how they should appear in the confusion matrix.
                            Defaults to None.

  Returns:
    cm: Confusion matrix computed using the ground truth labels and predicted labels. From scikit-learn documentation:
      Link: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
      "By definition a confusion matrix C is such that C_(i,j) is equal to the number of observations known to be in 
      group i and predicted to be in group j. I.e. True label corresponds to the rows, and Predictions correspond to the columns.
  """
  cm = skm.confusion_matrix(y_true, y_pred, labels = ordered_labels_list)
  return cm
