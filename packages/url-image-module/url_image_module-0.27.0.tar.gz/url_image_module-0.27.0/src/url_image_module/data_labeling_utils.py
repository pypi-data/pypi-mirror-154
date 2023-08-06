from os.path import join

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score
plt.style.use('seaborn')

from statsmodels.stats.inter_rater import fleiss_kappa

from typing import Callable, Dict, List, Optional, Set, Tuple, Union

from .constants import (
  FILENAME_KEY,
  FILENAMES_SET_KEY,
  INDICES_SET_KEY,
  ORIGINAL_COL_NAME_KEY,
  SOURCE_KEY,
  AUTHOR_ID_KEY,
  TASK_NAME_KEY,
  TASK_NAME_AUTHOR_ID_KEY,
  LABEL_KEY,
  PRED_KEY,
  TRUE_KEY,
  CORRECT_KEY,
  INCORRECT_KEY,
  UNLABELED_KEY,
  PRED_TYPES,
  IS_PLURALITY_AGREEMENT_AND_NOT_COMPLETE_AGREEMENT_KEY
)

from .misc_utils import (
  prettify_underscore_string
)

from .os_utils import (
  get_file_paths,
  extract_parent_path,
  extract_filename_from_file_path,
  make_folder,
  insert_part_of_path,
  copy_file_source_to_dest
)

from .pd_utils import (
  add_source_col,
  rename_column,
  construct_filename_series,
  copy_samples_from_df,
  left_join_dfs_by_filename,
  save_df
)

def make_tasks_labeling_df_from_folder(data_dir_path: str, file_path_col_name: str, tasks_list: List[str], prepended_url: Union[str, None] = None) -> pd.DataFrame:
    """Creates a tasks labeling df using file paths contained in the directory located at data_dir_path and prediction tasks specified in task_list.

    Args:
        data_dir_path: Path to directory containing unlabeled data.
        file_path_col_name: Name of the column which will contains file path to data on the host filesystem
        tasks_list: List containing tasks, which we want labels for (e.g. ['damage_severity', 'humanitarian_categories'])
        prepended_url: URL to prepend to file path on the host system, for examples images on Dropbox or AWS S3. Defaults to None
          If prepended_url is provided, creates a column in the labeling DataFrame under the name 'url' which is the values prepended with the
          prepended_url value.
    
    Returns:
        tasks_labeling_df: DataFrame containing file_path_col_name column, specifying location of the unlabeled sample on the local filesystem and
            additional columns for labeling each task in tasks_list.
    """
    URL_COL_NAME = 'url'
    columns = [file_path_col_name] + tasks_list
    tasks_labeling_df = pd.DataFrame(columns=columns)
    file_paths = pd.Series(get_file_paths(data_dir_path))
    tasks_labeling_df[file_path_col_name] = file_paths
    if prepended_url:
        tasks_labeling_df[URL_COL_NAME] = tasks_labeling_df[file_path_col_name].apply(lambda file_path: join(prepended_url, file_path))
    return tasks_labeling_df

def save_tasks_labeling_csv_from_df(tasks_labeling_df: pd.DataFrame, csv_save_path: str, encoding: Union[str, None] = None, index: bool = False) -> None:
    """Saves a csv for labeling for tasks from tasks_labeling_df to csv_save_path on the local filesystem.

    Args:
        tasks_labeling_df: DataFrame containing a 'file_path' column specifying the location of the unlabeled samples on the local filesystem and
            additional columns for tasks we wish to provide labels for.
        csv_save_path: Path on local filesystem where the labeling csv will be saved.
        encoding: encoding to save the df with as csv. Default is None
        index: Determines if index column should be saved in the csv. Default is False
    """
    # Must specify 'utf_8' because we're dealing with Japanese characters
    save_df(tasks_labeling_df, csv_save_path, encoding, index)

def get_label_cols_for_task(labels_df: pd.DataFrame, task_name_prefix: str) -> List[str]:
  """Gets column names of the labeling DataFrame labels_df which contain the task_name_prefix

    Args:
      tasks_labeling_df: DataFrame containing a 'file_path' column specifying the location of the unlabeled samples on the local filesystem and
          additional columns for tasks we wish to provide labels for.
      csv_save_path: Path on local filesystem where the labeling csv will be saved.
      encoding: encoding to save the df with as csv. Default is None
      index: Determines if index column should be saved in the csv. Default is False
    
    Returns:
      label_cols: List of column names in labels_df which contain the task_name_prefix. Useful
        for subsetting all columns of labels_df to just those which correspond to labels for a 
        particular task with the task_name_prefix. 
    """
  label_cols = list(filter(lambda col_name: task_name_prefix in col_name, list(labels_df.columns)))
  return label_cols


# Computing Labeling Stats
def get_unique_labels(label_array: np.ndarray) -> Set[str]:
  """Returns unique labels present in an array of labels.

  Args:
    label_array: Array of potentially nonunique labels.
  
  Returns:
    unique_labels_set: Unique set of labels from label_array.
  """
  unique_labels_set = set()
  for label in label_array:
    if label not in unique_labels_set:
      unique_labels_set.add(label)
  return unique_labels_set

def label_count_dict(label_array: np.ndarray) -> Dict[str, int]:
  """Finds counts for each label in label_array.

    Returns a dictionary mapping unique labels in label_array to their associated counts in label_array.

  Args:
    label_array: Array of potentially nonunique labels.
  
  Returns:
    count_dict: Dictionary mapping unique labels in label_array to their associated counts in label_array.
  """
  labels_set = get_unique_labels(label_array)
  count_dict = {label: 0 for label in labels_set}
  for label in label_array:
    count_dict[label] += 1
  return count_dict

# Determine Label by annotation row, i.e. multiple annotators for a given data point

def compute_plurality_label(annotation_row: pd.Series, label_cols: List[str]) -> Union[str, None]:
  """Computes a plurality (most frequent) label from labels provided by multiple annotators in the annotation_row, specifically
    for the label_cols columns, typically corresponding to a particular task

  Args:
    annotation_row: row in a labeling DataFrame which contains labels by multiple annotators
    label_cols: List of column names to access in the annotation_row relevant to a particular task
  
  Returns:
    plurality_label: Label which appears most frequently amongst the label_cols in the annotation_row
  """
  label_count_dict = {}
  max_label_count = -np.inf
  for label_n in label_cols:
    label = annotation_row[label_n]
    if label not in label_count_dict:
      label_count_dict[label] = 1
    else:
      label_count_dict[label] += 1
    label_freq = label_count_dict[label]
    if max_label_count < label_freq:
      plurality_labels = set([label])
      max_label_count = label_freq
    elif max_label_count == label_freq:
      plurality_labels.add(label)
  return None if len(plurality_labels) > 1 else list(plurality_labels)[0]

# Determine Agreement Predicate by annotation row, i.e. multiple annotators for a given data point

def is_complete_agreement(annotation_row: pd.Series, label_cols: List[str]) -> bool:
  """Determines if labels provided by multiple annotators in the annotation_row for the label_cols columns are 
    all the same, i.e. all annotators agree on the same label

  Args:
    annotation_row: row in a labeling DataFrame which contains labels by multiple annotators
    label_cols: List of column names to access in the annotation_row relevant to a particular task
  
  Returns:
    annotators_agree: Boolean indicating if annotators completely agree on a label, as in 
      all annotators selected the same label
  """
  annotators_agree = True
  if len(label_cols) <= 1:
    return annotators_agree
  for i in range(len(label_cols)-1):
    annotator_i_label = annotation_row[label_cols[i]]
    annotator_i_plus_1_label = annotation_row[label_cols[i+1]]
    annotators_agree = annotators_agree and (annotator_i_label == annotator_i_plus_1_label)
    # short-circuit
    if not annotators_agree:
      return annotators_agree
  return annotators_agree

def is_complete_disagreement(annotation_row: pd.Series, label_cols: List[str]) -> bool:
  """Determines if labels provided by multiple annotators in the annotation_row for the label_cols columns are 
    all different, i.e. all annotators disagree on the label for the data point represented by the row

  Args:
    annotation_row: row in a labeling DataFrame which contains labels by multiple annotators
    label_cols: List of column names to access in the annotation_row relevant to a particular task
  
  Returns:
    annotators_disagree: Boolean indicating if annotators completely disagree on a label, as in 
      no two annotators selected the same label
  """
  if len(label_cols) <= 1:
    return False
  for i in range(len(label_cols)-1):
    for j in range(i+1, len(label_cols)):
      annotator_i_label, annotator_j_label = annotation_row[label_cols[i]], annotation_row[label_cols[j]]
      # return False for any agreement at all, i.e. short-circuit
      if annotator_i_label == annotator_j_label:
        return False
  return True

def is_plurality_agreement(annotation_row: pd.Series, label_cols: List[str]) -> bool:
  """Determines if labels provided by multiple annotators in the annotation_row for the label_cols columns
      yield a plurality agreement, i.e. there is a definitive most frequent label with no ties

  Args:
    annotation_row: row in a labeling DataFrame which contains labels by multiple annotators
    label_cols: List of column names to access in the annotation_row relevant to a particular task
  
  Returns:
    is_plurality_agreement: Boolean indicating if annotators collectively have a most frequent label and no ties
  """
  plurality_label = compute_plurality_label(annotation_row, label_cols)
  return True if plurality_label else False

def is_plurality_agreement_and_not_complete_agreement(annotation_row: pd.Series, label_cols: List[str]) -> bool:
  """Determines if labels provided by multiple annotators in the annotation_row for the label_cols columns
      yield a plurality agreement, i.e. there is a definitive most frequent label with no ties but is also not 
      complete agreement, i.e. not all annotators provided the same label

  Args:
    annotation_row: row in a labeling DataFrame which contains labels by multiple annotators
    label_cols: List of column names to access in the annotation_row relevant to a particular task
  
  Returns:
    is_plurality_agreement_and_not_complete_agreement: Boolean indicating if annotators collectively have plurality
      agreement and not complete agreement
  """
  return is_plurality_agreement(annotation_row, label_cols) and not is_complete_agreement(annotation_row, label_cols)

def is_not_plurality_agreement_and_not_complete_disagreement(annotation_row: pd.Series, label_cols: List[str]) -> bool:
  """Determines if labels provided by multiple annotators in the annotation_row for the label_cols columns
      have a tie amongst the provided labels, no one label appears most frequently, multiple do
      at the same frequency (not plurality agreement), but with a frequency greater than one (not complete disagreement)

  Args:
    annotation_row: row in a labeling DataFrame which contains labels by multiple annotators
    label_cols: List of column names to access in the annotation_row relevant to a particular task
  
  Returns:
    is_plurality_agreement_and_not_complete_disagreement: Boolean indicating if annotators do not have plurality
      agreement and do not completely disagree
  """
  return not is_plurality_agreement(annotation_row, label_cols) and not is_complete_disagreement(annotation_row, label_cols)

def compute_plurality_percentage(plurality_series: pd.Series) -> float:
  """Computes percentage of data samples which achieve plurality agreement amongst multiple annotators

  Args:
    pluraltiy_series: Series of class label strings when data points achieve plurality agreement or np.nan values when 
      plurality is not reached
  
  Returns:
    percentage_plurality: Percentage of data points which achieve plurality agreement, i.e. a most frequent label, no ties
  """
  percentage_plurality = (1 - plurality_series.isna().sum()/len(plurality_series))*100.
  return percentage_plurality

def compute_complete_agreement_on_plurality_labels_percentage(agreement_series: pd.Series, plurality_series: pd.Series) -> float:
  """On labels which DO achieve plurality agreement, this computes percentage of those labels which have pluraltiy agreement

  Args:
    agreement_series: Boolean series which indicates if data sample had complete agreement or not amongst the annotators
    pluraltiy_series: Series of class label strings when a data point achieve plurality agreement or np.nan values when 
      plurality is not reached amongst the annotators
  
  Returns:
    percentage_complete_agreement_on_plurality_labels: Of data points which achieve plurality agreement, percentage of those data points
      which have complete agreement amongst annotators
  """
  # Only unanimous agreement
  assert len(agreement_series) == len(plurality_series)
  agreements = agreement_series[agreement_series == True]
  # Get non-null plurality labels
  plurality_labels = plurality_series[~plurality_series.isna()]
  total_plurality_labels = len(plurality_labels)
  total_agreement_on_plurality_labels = len(agreements.index & plurality_labels.index)
  return (total_agreement_on_plurality_labels/total_plurality_labels)*100.

def compute_complete_agreement_percentage(agreement_series: pd.Series) -> float:
  """Computes percentage of data points which have complete agreement amongst multiple annotators, i.e. all annotators provided the exact
    same label

  Args:
    agreement_series: Boolean series which indicates if data sample had complete agreement or not amongst the annotators
    pluraltiy_series: Series of class label strings when a data point achieve plurality agreement or np.nan values when 
      plurality is not reached amongst the annotators
  
  Returns:
    percentage_complete_agreement_on_plurality_labels: Of data points which achieve plurality agreement, percentage of those data points
      which have complete agreement amongst annotators
  """
  return agreement_series.sum()/len(agreement_series)*100.

def print_agreement_percentages(task_name: str, agreement_series: pd.Series, plurality_series: pd.Series) -> None:
  """Prints percentage of data points which achieve complete agreement, plurality agreement, and among the data points
      which achieve plurality agreement, the percentage which have complete agreement amongst multiple annotators

  Args:
    task_name: Task associated with the labels for which the agreement_series and plurality_series were computed, e.g. 'damage_severity'
    agreement_series: Boolean series which indicates if data sample had complete agreement or not amongst the annotators
    pluraltiy_series: Series of class label strings when a data point achieve plurality agreement or np.nan values when 
      plurality is not reached amongst the annotators
  """
  prettified_task_name = prettify_underscore_string(task_name)
  percentage_complete_agreement = compute_complete_agreement_percentage(agreement_series)
  percentage_plurality_agreement = compute_plurality_percentage(plurality_series)
  percentage_plurality_agreement_complete_agreement = compute_complete_agreement_on_plurality_labels_percentage(agreement_series, plurality_series)
  N_complete_agreement = agreement_series.sum()
  N_plurality_agreement = len(plurality_series.dropna())
  print(f"Percentage of samples for {prettified_task_name} Task which have unanimous agreement between all annotators: ", f"{percentage_complete_agreement}%")
  print(f"Percentage of samples for {prettified_task_name} Task which have plurality agreement: ", f"{percentage_plurality_agreement}%")
  print(f"Percentage of plurality agreement samples for {prettified_task_name} Task which have unanimous agreement: " f"{percentage_plurality_agreement_complete_agreement}%")
  print(f"Number of samples which had unanimous agreement for the {prettified_task_name} Task: ", N_complete_agreement)
  print(f"Number of samples which had a plurality label for the {prettified_task_name} Task: ", N_plurality_agreement)

def compute_series_from_annotation_row_func(
    labels_df: pd.DataFrame, task_name: str, annotation_row_func: Callable[[pd.Series, List[str]], pd.Series]
  ) -> pd.Series:
  """Computes a series using columns of the DataFrame labels_df whose names contain task_name as a prefix applying the 
      annotation_row_func on each row of annotations of the subsetted columns 

  Args:
    labels_df: Labeling DataFrame which contains labels from multiple annotators, potentially
      for multiple tasks
    task_name: Name of specific for which to subset the columns of labels_df
      to only those which contain task_name as a prefix
    annotation_row_func: Function that is applied to annotated rows of the subsetted columns
      of labels_df to those specific to the task

  Returns:
    series: Resultant series computed by applying annotation_row_func to each row of the subsetted columns of labels_df which have
      task_name as a prefix
  """
  label_cols = get_label_cols_for_task(labels_df, task_name)
  series = labels_df.apply(lambda row: annotation_row_func(row, label_cols), axis=1)
  return series

def construct_task_annotation_row_func_series_dict(
  labels_df: pd.DataFrame, task_names_list: List[str], annotation_row_func: Callable[[pd.Series, List[str]], pd.Series]
  ) -> Dict[str, pd.Series]:
  """Computes a dictionary for mapping task names in task_name_list to a series on columns of the DataFrame labels_df whose names 
      contain the task name as a prefix applying the annotation_row_func on each row of annotations of the subsetted columns 

  Args:
    labels_df: Labeling DataFrame which contains labels from multiple annotators, potentially
      for multiple tasks
    task_name_list: List of task names such that for a given task name the columns of labels_df can be subsetted
      to only those which contain task_name as a prefix
    annotation_row_func: Function that is applied to annotated rows of the subsetted columns
      of labels_df to those specific to the task

  Returns:
    task_annotation_row_func_series_dict: Dictionary containing map from task name to 
      resultant series from applying annotation_row_func to the rows of the column subsetted labels_df
      for each task in task_names_list
  """
  task_annotation_row_func_series_dict = {}
  for task_name in task_names_list:
    annotation_row_func_series = compute_series_from_annotation_row_func(
        labels_df,
        task_name,
        annotation_row_func
    )
    task_annotation_row_func_series_dict[task_name] = annotation_row_func_series
  return task_annotation_row_func_series_dict

def add_predicate_columns_to_df(
    agreement_df: pd.DataFrame, task_name: str, labels_df: pd.DataFrame, annotation_row_series_func_dict: Dict[str, Callable[[pd.Series, List[str]], pd.Series]]
  ) -> pd.DataFrame:
  """Inserts annotation agreement predicate based on task task_name columns to the DataFrame agreement_df by applying each predicate
    row function specified in annotation_row_series_func_dict on the column subsetted labels_df, subsetted based on
    columns in labels_df which contain task_name as prefix in their name

  Args:
    agreement_df: DataFrame which task-predicate columns are being inserted to
    task_name: Name of specific for which to subset the columns of labels_df
      to only those which contain task_name as a prefix
    labels_df: Labeling DataFrame which contains labels from multiple annotators, potentially
      for multiple tasks
    annotation_row_series_func_dict: Dictionary mapping predicate func name to predicate function to compute 
      series from annotation rows

  Returns:
    agreement_df: DataFrame containing task agreement predicates (boolean data type) inserted as columns. Newly inserted columns have the name
      '{task_name}-{annotation_row_series_func_name}', i.e. the task name '-' concatenated with the name of predicate function
      specified as a key in annotation_row_series_func_dict used to compute the predicate series on the subsetted columns of 
      labels_df subsetted to columns which have task_name as prefix in their name
  """
  for annotation_row_series_func_name in annotation_row_series_func_dict:
    annotation_row_func = annotation_row_series_func_dict[annotation_row_series_func_name]
    new_col_name = f'{task_name}-{annotation_row_series_func_name}'
    series = compute_series_from_annotation_row_func(labels_df, task_name, annotation_row_func)
    agreement_df[new_col_name] = series
  return agreement_df

def add_predicate_columns_to_df_with_task_list(
    agreement_df: pd.DataFrame, task_name_list: List[str], labels_df: pd.DataFrame, annotation_row_series_funcs: Dict[str, Callable[[pd.Series, List[str]], pd.Series]]
  ) -> pd.DataFrame:
  """Inserts annotation agreement predicate columns based on each task_name in task_name_list to the DataFrame agreement_df by applying each predicate
    row function specified in annotation_row_series_func_dict on the column subsetted labels_df, subsetted based on
    columns in labels_df which contain a task_name as prefix in their name. This occurs for each task name in task_name_list

  Args:
    agreement_df: DataFrame which task-predicate columns are being inserted to
    task_name_list: List of task names for which to subset the columns of labels_df
      to only those which contain task name as a prefix
    labels_df: Labeling DataFrame which contains labels from multiple annotators, potentially
      for multiple tasks
    annotation_row_series_func_dict: Dictionary mapping predicate func name to predicate function to compute 
      series from annotation rows

  Returns:
    agreement_df: DataFrame containing task agreement predicates (boolean data type) inserted as columns. Newly inserted columns have the name
      '{task_name}-{annotation_row_series_func_name}', i.e. the task name '-' concatenated with the name of predicate function
      specified as a key in annotation_row_series_func_dict used to compute the predicate series on the subsetted columns of 
      labels_df subsetted to columns which have task_name as prefix in their name for each task_name in task_name_list. This results in the insertion of 
      columns for each task_name in task_name_list and each predicate in annotation_row_series_func_dict
  """
  for task_name in task_name_list:
    agreement_df = add_predicate_columns_to_df(agreement_df, task_name, labels_df, annotation_row_series_funcs)
  return agreement_df

def add_plurality_labels_to_df(df: pd.DataFrame, task_plurality_label_series_dict: Dict[str, pd.Series]) -> pd.DataFrame:
  """Uses each task name, plurality label series key-value pair in the dictionary task_plurality_label_series_dict
      to insert a ground-truth column of plurality labels into the DataFrame df for each task 

  Args:
    df: DataFrame which the ground truth plurality labels series for each task is inserted into
    task_plurality_label_series_dict: Dictionary mapping task name to ground-truth plurality label series

  Returns:
    df: DataFrame with ground-truth plurality labels inserted as column named '{task_name}-{TRUE_KEY}' for each
        task_name, plurality label series pairing in task_plurality_label_series_dict
  """
  for task_name in task_plurality_label_series_dict:
    task_plurality_label_series = task_plurality_label_series_dict[task_name].copy()
    df[f'{task_name}-{TRUE_KEY}'] = task_plurality_label_series
  return df

def print_agreement_df_task_predicates(
    agreement_df: pd.DataFrame, task_name_list: List[str], annotation_row_series_func_dict: Dict[str, Callable[[pd.Series, List[str]], pd.Series]]
  ) -> None:
  """Prints number of samples corresponding to each combination of task name in task_name_list and predicate in
      annotation_row_series_func_dict

  Args:
    agreement_df: DataFrame which contains task-predicate columns for each pair of task name in task_names_list
        and predicate in annotation_row_series_func_dict
    task_name_list: List of task names
    annotation_row_series_func_dict: Dictionary mapping predicate func name to predicate function to compute 
      series from annotation rows
  """
  for task_name in task_name_list:
    for predicate in annotation_row_series_func_dict:
      task_predicate_string = f'{task_name}-{predicate}'
      print(f'Number of samples for task {prettify_underscore_string(task_name)} and predicate {predicate}: ', len(agreement_df[agreement_df[task_predicate_string]]))

def compute_label_counts(label_series: pd.Series, ordered_label_names: List[str]) -> List[int]:
  """Computes frequency count for each unique label present in label_series

  Args:
    label_series: Series containing labels for a specific task
    ordered_label_names: Ordered list of labels present in label_series
    
  Returns:
    counts: List of label counts ordered the same order as the labels in the ordered_label_names list
  """
  label_value_counts = label_series.value_counts()
  counts = [label_value_counts[label_name] for label_name in ordered_label_names]
  return counts

def compute_fleiss_kappa(task_name: str, labels_df: pd.DataFrame) -> float:
  """Computes Fleiss's Kappa Score between multiple annotators for a task named task_name using the 
      subsetted labeled columns of the DataFrame labels_df which correspond to the specified task

  Args:
    task_name: Name of task for which to subset the columns of labels_df
      to only those which contain task name as a prefix, i.e. labeled columns in labels_df
      which correspond to the specified task task_name
    labels_df: Labeling DataFrame which contains labels from multiple annotators, potentially
      for multiple tasks

  Returns:
    task_label_fleiss_kappa: Fleiss's Kappa Score between multiple annotators on the task labeled in labels_df
  """
  task_df = labels_df.loc[:, labels_df.columns.str.contains(task_name)]
  task_df.reset_index(level=0, inplace=True)
  label_cols = get_label_cols_for_task(task_df, task_name)
  sample_id_label_data = []
  for label_col in label_cols:
    sample_id_label_arr = pd.melt(task_df, id_vars = ['index'], value_vars = [label_col], value_name = 'label').to_numpy()
    sample_id_label_data.append(sample_id_label_arr)
  INDEX_COL_IDX, VARIABLE_COL_IDX, LABEL_COL_IDX = 0, 1, 2
  final_data_arr = np.vstack(sample_id_label_data)[:, [INDEX_COL_IDX, LABEL_COL_IDX]]
  sample_label_df = pd.DataFrame(data = final_data_arr, columns = ['sample_id', 'label'])
  sample_label_cross_tab = pd.crosstab(sample_label_df['sample_id'], sample_label_df['label']).to_numpy()
  task_label_fleiss_kappa = fleiss_kappa(sample_label_cross_tab)
  return task_label_fleiss_kappa

def compute_task_fleiss_kappa_score_dict(task_name_list: List[str], labels_df: pd.DataFrame) -> Dict[str, float]:
  """Computes Fleiss's Kappa Score for each task in task_names using the subsetted columns of the DataFrame labels_df

  Args:
    task_name_list: List of task names for which to subset the columns of labels_df
      to only those which contain task name as a prefix
    labels_df: Labeling DataFrame which contains labels from multiple annotators, potentially
      for multiple tasks

  Returns:
    task_fleiss_kappa_score_dict: Dictionary mapping task to Fleiss's Kappa Score computed from labels_df
  """
  task_fleiss_kappa_score_dict = {}
  for task_name in task_name_list:
    task_fleiss_kappa_score_dict[task_name] = compute_fleiss_kappa(task_name, labels_df)
  return task_fleiss_kappa_score_dict

def print_fleiss_kappa_scores(task_fleiss_kappa_score_dict: Dict[str, float]) -> None:
  """Prints Fleiss's Kappa Score for each task which is a key in the task_fleiss_kappa_score_dict 

  Args:
    task_fleiss_kappa_score_dict: Dictionary mapping task to Fleiss's Kappa Score
  """
  for task_name in task_fleiss_kappa_score_dict:
    task_fleiss_kappa_score = task_fleiss_kappa_score_dict[task_name]
    print(f"Fleiss' Kappa score for {prettify_underscore_string(task_name)} Labeled Data: ", task_fleiss_kappa_score)

# Utilities for labeling review
def make_task_predicate_dir(
  agreement_df: pd.DataFrame, 
  task_dir: str, 
  task_name: str, 
  predicate_name: str, 
  file_path_col_name: str, 
  prepend_path: str = None
) -> None:
  """Constructs and copies files into predicate_name predicate directory on the host's filesystem located at task_dir using
      the '{task_name}-{predicate_name}' column in the DataFrame agreement_df

  Args:
    agreement_df: DataFrame containing source file paths and task-predicate column '{task_name}-{predicate_name}'
    task_dir: Name of task directory which the predicate directory will be constructed in
    task_name: Name of task to assist in indexing the columns of agreement_df
    predicate_name: Name of predicate to assist in indexing the columns of agreement_df
    file_path_col_name: Name of the column in agreement_df which has the source file paths on the host
    prepend_path: Path part to prepend to source file paths. Default value is None
  """
  task_predicate_dir = join(task_dir, predicate_name)
  make_folder(task_predicate_dir)
  task_predicate_string = f'{task_name}-{predicate_name}'
  task_predicate_true_df = agreement_df[agreement_df[task_predicate_string]]
  for _, row in task_predicate_true_df.iterrows():
    src_path = row[file_path_col_name]
    if prepend_path is not None:
      src_path = insert_part_of_path(src_path, prepend_path, 0)
    file_name = extract_filename_from_file_path(src_path)
    dest_path = join(task_predicate_dir, file_name)
    copy_file_source_to_dest(src_path, dest_path)

def make_task_predicate_dirs_from_lists(
  agreement_df: pd.DataFrame, 
  parent_dir: str, 
  task_name_list: List[str], 
  predicate_name_list: List[str], 
  file_path_col_name: str, 
  prepend_path: str = None
) -> None:
  """Constructs task directories for each task name in task_name_list inside the parent_dir path on the 
      host's filesystem and inside the task directories, constructs predicate directories for each predicate name in 
      predicate_name_list using task-predicate columns in the DataFrame agreement_df

  Args:
    agreement_df: DataFrame containing source file paths and task-predicate columns '{task_name}-{predicate_name}'
      for each task name in task_name_list and predicate in predicate_name_list
    parent_dir: Name of directory on host's filesystem where task and predicate directories will be created
    task_name_list: List of task names, where a directory for each task in task_name_list is created in parent_dir
      and the task name is used to assist in indexing for the correct column in agreement_df
    predicate_name: List of predicate names, where a directory for each predicate name in predicate_name_list is created 
      in each task in task_name_list and the predicate name is used to assist in indexing for the correct column in agreement_df
    file_path_col_name: Name of the column in agreement_df which has the source file paths on the host's filesystem
    prepend_path: Path part to prepend to source file paths. Default value is None
  """
  for task_name in task_name_list:
    task_dir = join(parent_dir, task_name)
    make_folder(task_dir)
    for predicate_name in predicate_name_list:
      make_task_predicate_dir(
        agreement_df, 
        task_dir, 
        task_name, 
        predicate_name, 
        file_path_col_name, 
        prepend_path
      )

def determine_prediction_type(true_label: str, pred_label: str) -> str:
    """Determines the type of prediction pred_label is with respect to true_label, i.e. one of  
        UNLABELED_KEY, CORRECT_KEY, INCORRECT_KEY

    Args:
      true_label: string label determined by multiple annotators, typically from the plurality label
      pred_label: string label predicted by a model

    Returns:
      prediction_type: Type of prediction pred_label is with respect to the ground-truth label true_label. Can be one of:
        UNLABELED_KEY if there does not exist a true_label, CORRECT_KEY if pred_label equals the true_label,
        and INCORRECT_KEY when pred_label does not equal true_label
    """
    # unlabeled data point
    if pd.isna(true_label):
        prediction_type = UNLABELED_KEY
    # correct prediction
    elif true_label == pred_label:
        prediction_type = CORRECT_KEY
    # incorrect prediction
    elif true_label != pred_label:
        prediction_type = INCORRECT_KEY
    return prediction_type

def make_pred_type_dirs(
    pred_true_df: pd.DataFrame, task_dir: str, task_name: str, file_path_col_name: str, prepend_path: str = None
  ) -> None:
    """Constructs prediction type directories (UNLABELED_KEY, CORRECT_KEY, INCORRECT_KEY) which are further separated
        into task label directories inside the task_dir path on the host's filesystem using DataFrame pred_true_df and copies data from other locations in the file_path_col_name 
        of pred_true_df to the appropriate newly created directories

    Args:
      pred_true_df: DataFrame containing ground-truth labels for the task task_name under the '{task_name}-{TRUE_KEY}' column
        and model predictions under the '{task_name}-{PRED_KEY}'
      task_dir: Task directory on the host's filesystem which the prediction type directories will be created inside
      task_name: Name of the prediction task
      file_path_col_name: Name of the column in pred_true_df which contains source file paths for the data samples on the host's filesystem
      prepend_path: Path to insert at the beginning of each source path in the file_path_col_name column of pred_true_df 
    """
    task_labels = set(pred_true_df[f'{task_name}-{TRUE_KEY}'].dropna().unique()) | set(pred_true_df[f'{task_name}-{PRED_KEY}'].dropna().unique())
    for pred_type in PRED_TYPES:
        pred_type_dir = join(task_dir, pred_type)
        make_folder(pred_type_dir)
        for task_label in task_labels:
            pred_type_label_dir = join(pred_type_dir, task_label)
            make_folder(pred_type_label_dir)
    for _, row in pred_true_df.iterrows():
        src_path = row[file_path_col_name]
        if prepend_path is not None:
          src_path = insert_part_of_path(src_path, prepend_path, 0)
        file_name = extract_filename_from_file_path(src_path)
        true_label, pred_label = row[f'{task_name}-{TRUE_KEY}'], row[f'{task_name}-{PRED_KEY}']
        pred_type = determine_prediction_type(true_label, pred_label)
        dest_path = join(task_dir, pred_type, pred_label, file_name)
        copy_file_source_to_dest(src_path, dest_path)

def make_pred_type_dirs_from_task_list(
    pred_true_df: pd.DataFrame, 
    parent_dir: str, 
    task_name_list: List[str], 
    file_path_col_name: str, 
    prepend_path: str = None
) -> None:
    """For each task in task_name_list constructs a task directory in the parent_dir on the host's filesystem
        and then constructs prediction type directories (UNLABELED_KEY, CORRECT_KEY, INCORRECT_KEY) which are further separated
        into task label directories inside of each task directory using DataFrame pred_true_df and copies data from other locations in the file_path_col_name 
        of pred_true_df to the appropriate newly created directories

    Args:
      pred_true_df: DataFrame containing ground-truth labels for each task name task_name in task_name_list under the '{task_name}-{TRUE_KEY}' column
        and model predictions under the '{task_name}-{PRED_KEY}'
      parent_dir: Directory on host's filesystem which the task directories will be constructed inside of
      task_name_list: List of task names which are used to create task directories and to index the pred_true_df columns
      file_path_col_name: Name of the column in pred_true_df which contains source file paths for the data samples on the host's filesystem
      prepend_path: Path to insert at the beginning of each source path in the file_path_col_name column of pred_true_df 
    """
    for task_name in task_name_list:
        task_dir = join(parent_dir, task_name)
        make_folder(task_dir)
        make_pred_type_dirs(pred_true_df, task_dir, task_name, file_path_col_name, prepend_path)

def filter_for_incorrect_prediction_and_plurality_not_complete_agreement(pred_true_df: pd.DataFrame, task_name: str) -> pd.DataFrame:
    """Filters DataFrame to rows of pred_true_df to those which the model predictions are incorrect and
        the data samples had plurality but not complete agreement, and the resultant filtered df is returned

    Args:
      pred_true_df: DataFrame containing '{task_name}-{TRUE_KEY}', '{task_name}-{PRED_KEY}', 
        and '{task_name}-{IS_PLURALITY_AGREEMENT_AND_NOT_COMPLETE_AGREEMENT_KEY}' columns
      task_name: Name of task name used for selecting columns of pred_true_df to use a predicates for filtering to the rows
        of pred_true_df for which has incorrect model predictions and plurality but not complete agreement

    Returns:
      filtered_df: Filtered DataFrame to those which contain task_name and for which the model predictions are incorrect
        and have plurality agreement but not complete agreement
    """
    filtered_df = pred_true_df[~(pd.isna(pred_true_df[f'{task_name}-{TRUE_KEY}'])) & (pred_true_df[f'{task_name}-{TRUE_KEY}'] != pred_true_df[f'{task_name}-{PRED_KEY}']) & (pred_true_df[f'{task_name}-{IS_PLURALITY_AGREEMENT_AND_NOT_COMPLETE_AGREEMENT_KEY}'])]
    return filtered_df

def make_plurality_not_complete_agreement_and_misclassified_preds_dir(
    pred_true_df: pd.DataFrame, 
    agreement_df: pd.DataFrame,
    task_dir: str,
    task_name: str,
    file_path_col_name: str,
    prepend_path: Optional[str] = None,
    encoding: Optional[str] = None,
    index: bool = False
) -> None:
    """Creates a directory inside of task_dir located on the host's filesystem of data points which the model mispredicted as well as had plurality agreement 
        but not complete agreement for a specific task task_name. Saves dataframe filtered to mispredictions by the model and which had plurality
        agreement but not complete agreement for the task task_name as '{task_name}.csv' in the parent directory of task_dir with encoding encoding

    Args:
      pred_true_df: DataFrame containing ground-truth labels for the task task_name under the '{task_name}-{TRUE_KEY}' column
        and model predictions under the '{task_name}-{PRED_KEY}'
      agreement_df: DataFrame containing source file paths and task-predicate columns '{task_name}-{predicate_name}'
      task_dir: Directory location on host's filesystem to copy data samples from source file paths in the 
        file_path_col_name to task_dir
      task_name: Name of task name used for filtering of pred_true_df and agreement_df
      file_path_col_name: Name of the column in agreement_df and pred_true_df which has the source file paths on the host's filesystem
      prepend_path: Path part to prepend to source file paths. Default value is None
      encoding: encoding to save the filtered dataframe. Default is None
      index: Determines if index column should be saved in the csv. Default is False
    """
    joined_df = agreement_df.merge(pred_true_df, on=file_path_col_name, how='left')
    joined_df[FILENAME_KEY] = construct_filename_series(joined_df, file_path_col_name)
    relevant_cols = [file_path_col_name, FILENAME_KEY, f'{task_name}-{TRUE_KEY}', f'{task_name}-{PRED_KEY}']
    filtered_task_df = filter_for_incorrect_prediction_and_plurality_not_complete_agreement(joined_df, task_name)[relevant_cols]
    filtered_task_df.rename(columns={f'{task_name}-{TRUE_KEY}': "true_label", f'{task_name}-{PRED_KEY}': "pred_label"}, inplace=True)
    parent_dir = extract_parent_path(task_dir)
    task_csv_path = join(parent_dir, f'{task_name}.csv')
    save_df(filtered_task_df, task_csv_path, encoding=encoding, index=index)
    print(f'{len(filtered_task_df)} samples for {task_name} plurality agreement, nonunanimous agreement, and incorrect predictions')
    copy_samples_from_df(filtered_task_df, task_dir, file_path_col_name, prepend_path)

def make_plurality_not_complete_agreement_and_misclassified_preds_dir_from_task_list(
    pred_true_df: pd.DataFrame, 
    agreement_df: pd.DataFrame,
    parent_dir: str,
    task_name_list: List[str],
    file_path_col_name: str,
    prepend_path: Optional[str] = None,
    encoding: Optional[str] = None,
    index: bool = False
) -> None:
    """Creates a directory in each task directory inside of parent_dir located on the host's filesystem of data points which the model mispredicted as well as had plurality agreement 
        but not complete agreement for each task in task_name_list. Saves dataframe filtered to mispredictions by the model and which had plurality
        agreement but not complete agreement for each task in task_name_list as '{task_name}.csv' in the parent_dir with encoding encoding

    Args:
      pred_true_df: DataFrame containing ground-truth labels for each task name task_name in task_name_list under the '{task_name}-{TRUE_KEY}' column
        and model predictions under the '{task_name}-{PRED_KEY}'
      agreement_df: DataFrame containing source file paths and task-predicate columns '{task_name}-{predicate_name}'
        for each task name in task_name_list
      parent_dir: Directory location on host's filesystem where task directories are created and corresponding csv's are saved
      task_name_list: List of task names used for filtering of pred_true_df and agreement_df
      file_path_col_name: Name of the column in agreement_df and pred_true_df which has the source file paths on the host's filesystem
      prepend_path: Path part to prepend to source file paths. Default value is None
      encoding: encoding to save the filtered dataframes. Default is None
      index: Determines if index column should be saved in the csv. Default is False
    """
    for task_name in task_name_list:
        task_dir = join(parent_dir, task_name)
        make_folder(task_dir)
        make_plurality_not_complete_agreement_and_misclassified_preds_dir(
            pred_true_df, 
            agreement_df,
            task_dir,
            task_name,
            file_path_col_name,
            prepend_path=prepend_path,
            encoding=encoding,
            index=index
        )

def construct_task_name_author_id_string(task_name: str, author_id: int) -> str:
  """Constructs the concatenated task_name with author_id by a '.' character to form a standardized string task_name_author_id used for 
      labeling DataFrames

  Args:
    task_name: Name of the task
    author_id: Integer id for a specific author/labeler
  
  Returns:
    task_name_author_id: concatenated task_name with author_id using '.'
   """
  return task_name + '.' + str(author_id)

def split_task_name_author_id(task_name_author_id: str) -> Tuple[str, int]:
    """Splits the task_name_author_id string by the '.' character into task_name string and author_id integer

    Args:
      task_name_author_id: task_name string concatenated with author_id string by the '.' character
    
    Returns:
      task_name: String for the task name
      author_id: Integer for author/labeler id
    """
    split_input = task_name_author_id.split('.')
    task_name = split_input[0]
    author_id = int(split_input[1]) if len(split_input) == 2 else 0
    return task_name, author_id

def rename_col_to_task_name_author_id(df: pd.DataFrame, old_col_name: str, task_name: str, author_id: int) -> None:
    """Renames the old_col_name column in DataFrame df to the concatenated task_name_author_id string concatenated from 
        task_name string and author_id integer inplace

    Args:
      df: DataFrame which contains old_col_name column being renamed to the concatenation of task_name and author_id inplace
      old_col_name: Name of the column being renamed in df
      task_name: String name of the task
      author_id: Integer id of the author/labeler
    """
    task_name_author_id = construct_task_name_author_id_string(task_name, author_id)
    rename_column(df, old_col_name, task_name_author_id)

def insert_source_info_index(df: pd.DataFrame, start_index: int, end_index: int, source_info: str) -> pd.DataFrame:
    """Inserts source information to DataFrame df in the column named SOURCE_KEY as the source_info value to entries in the row index
        of df specifically in the range start_index to end_index (inclusive)

    Args:
      df: DataFrame containing SOURCE_KEY column
      start_index: Start row index to insert source_info into SOURCE_KEY column
      end_index: End row index to insert source_info into SOURCE_KEY column
      source_info: Information string about the source of the data samples, such as event, original data source, etc.
    
    Returns:
      df: DataFrame with source_info value inserted into SOURCE_KEY column at the row indices in the range start_index to end_index inclusive
    """
    assert end_index >= start_index
    assert SOURCE_KEY in df.columns
    df.loc[start_index:end_index, SOURCE_KEY] = source_info
    return df

def insert_source_info_from_filenames_tup(df: pd.DataFrame, filenames_tuple: Tuple[str], source_info: str) -> pd.DataFrame:
    """Inserts a source information to DataFrame df in the column named SOURCE_KEY as the source_info value to entries which have a filename (in the FILENAME_KEY column of df) 
        contained in the filenames_tuples

    Args:
      df: DataFrame containing SOURCE_KEY and FILENAME_KEY columns
      filenames_tuple: Tuple of filenames for data samples the source_info corresponds to
      source_info: Information string about the source of the data samples, such as event, original data source, etc.
    
    Returns:
      df: DataFrame with source_info value inserted into SOURCE_KEY column for entries/data samples which have a filename contained in the
        filenames_tuple
    """
    assert FILENAME_KEY in df.columns and SOURCE_KEY in df.columns
    df.loc[df[df[FILENAME_KEY].isin(filenames_tuple)].index, SOURCE_KEY] = source_info
    return df

def insert_source_info_from_index_dict(df: pd.DataFrame, indices_source_dict: Dict[Tuple[int, int], str]) -> pd.DataFrame:
    """Inserts a source information to DataFrame df in the column named SOURCE_KEY with relevant entries determined from 
        indices_source_dict which maps relevant indicies and corresponding source information string

    Args:
      df: DataFrame containing SOURCE_KEY column
      indices_source_dict: Dictionary mapping (start_index, end_index) [inclusive] tuples to source_info string, indicating which entries in df by index 
        have the source_info string as their value
    
    Returns:
      df: DataFrame with source_info value inserted into SOURCE_KEY column for all indices tuple, source_info string pairs entries/data samples 
            in indices_source_dict
    """
    for index_tuple, source_info in indices_source_dict.items():
        start_index, end_index = index_tuple[0], index_tuple[1]
        df = insert_source_info_index(df, start_index, end_index, source_info)
    return df

def insert_source_info_from_filenames_tup_dict(df: pd.DataFrame, filenames_tup_source_dict: Dict[Tuple[str], str]) -> pd.DataFrame:
    """Inserts a source information to DataFrame df in the column named SOURCE_KEY with relevant entries determined from 
        filenames_tuple_source_dict which maps relevant filenames (as a tuple) present in df FILENAME_KEY column to their corresponding source information string

    Args:
      df: DataFrame containing SOURCE_KEY and FILENAME_KEY columns
      filenames_tup_source_dict: Dictionary mapping tuple of filenames to source_info string, indicating which entries in df by filename
        contained in filename tuple have the source_info string as their value
    
    Returns:
      df: DataFrame with source_info value inserted into SOURCE_KEY. For each filename tuple, source_info string pair in filenames_tup_source_dict
            the source_info is inserted into the relevant data sample entries which have a filename contained in the corresponding filename tuple 
    """
    for filenames_tuple, source_info in filenames_tup_source_dict.items():
        df = insert_source_info_from_filenames_tup(df, filenames_tuple, source_info)
    return df
  
def select_existing_labels_by_index(labels_df: pd.DataFrame, rel_col_name: str, start_index: int, end_index: int, task_name: str, author_id: int) -> pd.DataFrame:
    """Selects labels from labels_df DataFrame contained in the rel_col_name column from the start_index to end_index (inclusive) made by the author with id author_id
        for task task_name and returns the selected labels as a DataFrame with a FILENAME_KEY column and concatenated task_name author_id column name

    Args:
      labels_df: Labeling DataFrame containing FILENAME_KEY column
      rel_col_name: Column name of column in labels_df which labels are being selected from
      start_index: Start row index for labels being selected
      end_index: End row index for labels being selected 
      task_name: String name of the task for selected labels
      author_id: Integer id of the author/labeler of the selected labels
    
    Returns:
      selected_labels_df: DataFrame of selected labels from labels_df under column name formed from the task_name concatenated with author_id by a '.' character 
        as well as the FILENAME_KEY column containing filenames associated with selected data samples
        
    """
    assert FILENAME_KEY in labels_df.columns
    assert end_index >= start_index
    selected_labels_df = labels_df.loc[start_index:end_index][[FILENAME_KEY, rel_col_name]].copy()
    rename_col_to_task_name_author_id(selected_labels_df, rel_col_name, task_name, author_id)
    return selected_labels_df

def select_existing_labels_by_filenames(labels_df: pd.DataFrame, rel_col_name: str, filenames_list: List[str], task_name: str, author_id: int) -> pd.DataFrame:
    """Selects labels from labels_df DataFrame contained in the rel_col_name column which have a filename contained in filenames_list made by the author with id author_id
          for task task_name and returns the selected labels as a DataFrame with a FILENAME_KEY column and concatenated task_name author_id column name

    Args:
      labels_df: Labeling DataFrame containing FILENAME_KEY column
      rel_col_name: Column name of column in labels_df which labels are being selected from
      filenames_list: List of filenames associated with the labels being selected
      task_name: String name of the task for selected labels
      author_id: Integer id of the author/labeler of the selected labels
    
    Returns:
      selected_labels_df: DataFrame of selected labels from labels_df under column name formed from the task_name concatenated with author_id by a '.' character 
        as well as the FILENAME_KEY column containing filenames associated with selected data samples
    """
    assert FILENAME_KEY in labels_df.columns
    selected_df = labels_df.query(f'{FILENAME_KEY} in @filenames_list')[[FILENAME_KEY, rel_col_name]].copy()
    rename_col_to_task_name_author_id(selected_df, rel_col_name, task_name, author_id)
    return selected_df

def insert_selected_labels(labels_df: pd.DataFrame, selected_labels_df: pd.DataFrame, task_name: str, author_id: int) -> pd.DataFrame:
    """Inserts selected labels contained in DataFrame selected_labels_df into labels_df for a specific task and author for the filenames
        present in the selected_labels_df FILENAME_KEY column 

    Args:
      labels_df: Labeling DataFrame containing FILENAME_KEY column for which the selected labels are being inserted into
      selected_labels_df: DataFrame of labels to be inserted into labels_df under column name formed from the task_name concatenated with author_id by a '.' character 
        as well as the FILENAME_KEY column containing filenames associated with data samples whose labels are being inserted
      task_name: Name of task for which selected labels in selected_labels_df correspond to
      author_id: ID of the author that created the selected labels in selected_labels_df 
    
    Returns:
      labels_df: DataFrame labels_df with FILENAME_KEY column containing filenames associated with newly inserted data samples under column with name formed by
        task_name concatenated with author_id by a '.' character
    """
    assert FILENAME_KEY in labels_df.columns and FILENAME_KEY in selected_labels_df.columns
    task_name_author_id = construct_task_name_author_id_string(task_name, author_id)
    if task_name_author_id not in labels_df.columns:
        labels_df[task_name_author_id] = np.nan
    filenames_list = selected_labels_df[FILENAME_KEY].tolist()
    labels_df.loc[labels_df[labels_df[FILENAME_KEY].isin(filenames_list)].index, task_name_author_id] = selected_labels_df[task_name_author_id].tolist()
    return labels_df

def insert_selected_labels_from_task_indices_dict(labels_df: pd.DataFrame, task_indices_dict: Dict[str, Dict[str, Union[Set[str], str]]], author_id: int) -> pd.DataFrame:
    """Selects labels from labels_df for each specific task in task_indices_dict which maps a task to a dictionary containing the original column name the label reside in
        in labels_df as well as the set of indices ranges in this column to select. The selected labels are inserted labels_df under column with name formed by
        each specific task_name concatenated with author_id by a '.' character

    Args:
      labels_df: Labeling DataFrame containing FILENAME_KEY column for which labels are being extracted and inserted into
      task_indices_dict: Dictionary mapping task name to a dictionary containing the original column name (key: ORIGINAL_COL_NAME_KEY) and a set of indices
        (key: INDICES_SET_KEY), which contains (start_index, end_index) tuples which correspond to labels in labels_df in the 
        task_indices_dict[task_name][ORIGINAL_COL_NAME] column labeled by author author_id from the row index start_index to end_index (inclusive) to select and inserts those same labels
        at the same index range in labels_df under column with name formed by the task_name concatenated with author_id by a '.' character
      author_id: ID of author who created the selected labels in task_indices_dict
    
    Returns:
      labels_df: DataFrame labels_df with FILENAME_KEY column containing filenames associated with newly inserted data samples under columns with name formed by
        task_name concatenated with author_id by a '.' character
    """
    for task_name, indices_dict in task_indices_dict.items():
        original_col_name, indices_set = indices_dict[ORIGINAL_COL_NAME_KEY], indices_dict[INDICES_SET_KEY]
        for index_tuple in indices_set:
            start_index, end_index = index_tuple[0], index_tuple[1]
            selected_df = select_existing_labels_by_index(labels_df,
                                                          original_col_name,
                                                          start_index, 
                                                          end_index,
                                                          task_name,
                                                          author_id)
            labels_df = insert_selected_labels(labels_df, selected_df, task_name, author_id)
    return labels_df

def insert_selected_labels_from_task_filenames_dict(labels_df: pd.DataFrame, task_filenames_dict: Dict[str, Dict[str, Union[Set[str], str]]], author_id: int) -> pd.DataFrame:
    """Selects labels from labels_df for each specific task in task_filenames_dict which maps a task to a dictionary containing the original column name the label reside in
        in labels_df as well as the set of tuples containing associated filenames to labels in this column to select. The selected labels are inserted labels_df under column with name formed by
        each specific task_name concatenated with author_id by a '.' character

    Args:
      labels_df: Labeling DataFrame containing FILENAME_KEY column for which labels are being extracted and inserted into
      task_filenames_dict: Dictionary mapping task name to a dictionary containing the original column name (key: ORIGINAL_COL_NAME_KEY) and a set of filename tuples
        (key: FILENAMES_SET_KEY), the set of filename tuples correspond to specific labels in labels_df in the task_filenames_dict[task_name][ORIGINAL_COL_NAME] column 
        labeled by author author_id to select and inserts those same labels for the same filenames in labels_df under a column with name formed by the task_name 
        concatenated with author_id by a '.' character
      author_id: ID of author who created the selected labels in task_filenames_dict
    
    Returns:
      labels_df: DataFrame labels_df with FILENAME_KEY column containing filenames associated with newly inserted data samples under columns with name formed by
        task_name concatenated with author_id by a '.' character
    """
    for task_name, filenames_dict in task_filenames_dict.items():
        original_col_name, filenames_set = filenames_dict[ORIGINAL_COL_NAME_KEY], filenames_dict[FILENAMES_SET_KEY]
        for filenames_tuple in filenames_set:
            filenames_list = list(filenames_tuple)
            selected_df = select_existing_labels_by_filenames(labels_df,
                                                          original_col_name,
                                                          filenames_list,
                                                          task_name,
                                                          author_id)
            labels_df = insert_selected_labels(labels_df, selected_df, task_name, author_id)
    return labels_df

def insert_selected_labels_from_author_task_indices_dict(labels_df: pd.DataFrame, author_task_indices_dict: Dict[int, Dict[str, Dict[str, Union[Set[str], str]]]]) -> pd.DataFrame:
    """Selects labels from labels_df for each author id in author_task_indices_dict and each specific task in author_task_indices_dict[author_id] which maps a task to a dictionary 
        containing the original column name the labels reside in labels_df as well as the set of indices ranges in this column to select. The selected labels are inserted labels_df 
        under column with name formed by each specific task_name concatenated with author_id by a '.' character for each author id in author_task_indices_dict and each task name in 
        author_task_indices_dict[author_id]

    Args:
      labels_df: Labeling DataFrame containing FILENAME_KEY column for which labels are being extracted and inserted into
      author_task_indices_dict: Dictionary mapping author id to a dictionary mapping task name to a dictionary containing the original column name (key: ORIGINAL_COL_NAME_KEY) and a set of indices
        (key: INDICES_SET_KEY), which contains (start_index, end_index) tuples which correspond to labels in labels_df in the task_indices_dict[task_name][ORIGINAL_COL_NAME] column labeled by the 
        author with that specific author id from the row index start_index to end_index (inclusive) to select and inserts those same labels at the same index range in labels_df under column with 
        name formed by the task_name concatenated with author_id by a '.' character
    
    Returns:
      labels_df: DataFrame labels_df with FILENAME_KEY column containing filenames associated with newly inserted data samples under columns with name formed by
        task_name concatenated with author_id by a '.' character for each author id in author_task_indices_dict and each task name in author_task_indices_dict[author_id]
    """
    for author_id, task_indices_dict in author_task_indices_dict.items():
        labels_df = insert_selected_labels_from_task_indices_dict(
            labels_df,
            task_indices_dict,
            author_id
        )
    return labels_df

def insert_selected_labels_from_author_task_filenames_dict(labels_df: pd.DataFrame, author_task_filenames_dict: Dict[int, Dict[str, Dict[str, Union[Set[str], str]]]]) -> pd.DataFrame:
    """Selects labels from labels_df for each author id in author_task_filenames_dict and each specific task in author_task_filenames_dict[author_id] which maps a task to a dictionary 
        containing the original column name the label reside in labels_df as well as the set of tuples containing associated filenames to labels in this column to select. 
        The selected labels are inserted labels_df under column with name formed by each specific task_name concatenated with author_id by a '.' character for each author id in 
        author_task_filenames_dict and each task name in author_task_filenames_dict[author_id]

    Args:
      labels_df: Labeling DataFrame containing FILENAME_KEY column for which labels are being extracted and inserted into
      author_task_filenames_dict: Dictionary mapping author id to a dictionary mapping task name to a dictionary containing the original column name (key: ORIGINAL_COL_NAME_KEY) and a set of filename tuples
        (key: FILENAMES_SET_KEY), the set of filename tuples corresponding to specific labels in labels_df in the task_filenames_dict[task_name][ORIGINAL_COL_NAME] column 
        labeled by author author_id to select and inserts those same labels for the same filenames in labels_df under a column with name formed by the task_name 
        concatenated with author_id by a '.' character
    
    Returns:
      labels_df: DataFrame labels_df with FILENAME_KEY column containing filenames associated with newly inserted data samples under columns with name formed by
        task_name concatenated with author_id by a '.' character for each author id in author_task_filenames_dict and each task name in author_task_filenames_dict[author_id]
    """
    for author_id, task_filenames_dict in author_task_filenames_dict.items():
        labels_df = insert_selected_labels_from_task_filenames_dict(
            labels_df,
            task_filenames_dict,
            author_id
        )
    return labels_df

def melt_labels_df(labels_df: pd.DataFrame, file_path_col_name: str) -> pd.DataFrame:
    """Melts a DataFrame labels_df containing labels by multiple annotators and potentially multiple tasks into a DataFrame with columns 
        FILENAME_KEY, AUTHOR_ID_KEY, TASK_NAME_KEY, LABEL_KEY, SOURCE_KEY
    
    Args:
      labels_df: DataFrame containing labels by multiple annotators for potentially multiple tasks containing file_path_col_name and columns with names of
        the form '{task_name}.{author_id}' columns containing labels for each task by specific authors
      file_path_col_name: Column name of the column in labels_df which contains souce file paths to data samples 
    
    Returns:
      melted_labels_df: DataFrame with columns FILENAME_KEY, AUTHOR_ID_KEY, TASK_NAME_KEY, LABEL_KEY which is a melted version of labels_df for every unique 
        author_id, filename, task_name triple in labels_df
    """
    if SOURCE_KEY not in labels_df.columns:
        labels_df = add_source_col(labels_df)
    labels_df[FILENAME_KEY] = construct_filename_series(labels_df, file_path_col_name)
    source_df = labels_df[[FILENAME_KEY, SOURCE_KEY]].copy()
    mod_labels_df = labels_df.drop(columns=[file_path_col_name, SOURCE_KEY])
    melted_labels_df = mod_labels_df.melt(
        id_vars=[FILENAME_KEY], 
        var_name=TASK_NAME_AUTHOR_ID_KEY, 
        value_name=LABEL_KEY
    )
    melted_labels_df.dropna(subset=[LABEL_KEY], inplace=True)
    melted_labels_df.reset_index(inplace=True, drop=True)
    melted_labels_df[[TASK_NAME_KEY, AUTHOR_ID_KEY]] = melted_labels_df.apply(lambda row: 
                                                                      split_task_name_author_id(row[TASK_NAME_AUTHOR_ID_KEY]),
                                                                      axis=1,
                                                                      result_type='expand')
    melted_labels_df.drop(columns=TASK_NAME_AUTHOR_ID_KEY, inplace=True)
    melted_labels_df = melted_labels_df[[FILENAME_KEY, AUTHOR_ID_KEY, TASK_NAME_KEY, LABEL_KEY]]
    melted_labels_df = left_join_dfs_by_filename(melted_labels_df, source_df)
    return melted_labels_df

def cohen_kappa(df: pd.DataFrame, authorid1: str, authorid2: str, weight: str= 'unweighted') -> float:
    
    """
    Calculates cohen's kappa score using cohen_kappa_score from sklearn.metrics

      Args:
        data: an unmelted Pandas DataFrame
        authorid1: a string; the column name associated with the first annotator 
        authorid2: a string; the column name associated with the second annotator 
        weight: None (default), 'linear', or 'quadratic' 
  
      Returns:
        kappa: Cohen's kappa score as a float
    """
    
    
    new_df = df.copy(deep=True)
    
    new_df.dropna(subset = [authorid1, authorid2], inplace=True)
    

    pair1 = new_df.loc[:, authorid1].values
    pair2 = new_df.loc[:, authorid2].values
    

    if weight == 'linear':
        kappa = cohen_kappa_score(pair1, pair2, labels=None, weights='linear', sample_weight=None)
    elif weight == "quadratic":
        kappa = cohen_kappa_score(pair1, pair2, labels=None, weights='quadratic', sample_weight=None)
    else:
        kappa = cohen_kappa_score(pair1, pair2, labels=None, weights=None, sample_weight=None)
    
    print(f"Cohen's {weight} kappa score between {authorid1} & {authorid2}: {kappa}")
    return kappa

        