from os.path import join

import pandas as pd
import numpy as np

from typing import List, Optional

from .constants import (
  SOURCE_KEY,
  FILENAME_KEY
)

from .os_utils import (
  extract_filename_from_file_path,
  insert_part_of_path,
  copy_file_source_to_dest
)

# Pandas DataFrame helpers
def copy_sample_from_file_path_to_dest(file_path: str, dest_dir: str, prepend_path: Optional[str] = None) -> None:
  """Copies a file from a prepended source path on the host to a destination directory (dest_dir)
    on the host

  Args:
    file_path: path to file on host
    dest_dir: path to destination directory where file will be saved
    prepend_path: Path part to prepend to file_path. Default value is None
  """
  src_path = file_path
  if prepend_path is not None:
      src_path = insert_part_of_path(src_path, prepend_path, 0)
  file_name = extract_filename_from_file_path(src_path)
  dest_path = join(dest_dir, file_name)
  copy_file_source_to_dest(src_path, dest_path)

def copy_samples_from_df(df: pd.DataFrame, dest_dir: str, file_path_col_name: str, prepend_path: Optional[str] = None) -> None:
  """Copies a series of files with source file paths on the host in the file_path_col_name column
    of the dataframe df to a destination directory located at dest_dir on the host 

  Args:
    df: DataFrame containing source file paths contained in the file_path_col_name column
    dest_dir: Path to destination directory where files will be saved on the host
    file_path_col_name: Name of the column in df which has the source file paths on the host
    prepend_path: Path part to prepend to source file paths. Default value is None
  """
  df[file_path_col_name].apply(lambda file_path: copy_sample_from_file_path_to_dest(
    file_path, dest_dir, prepend_path
  ))
    
def add_source_col(df: pd.DataFrame) -> pd.DataFrame:
  """Adds a source column named SOURCE_KEY for the samples in the df to describe 
    the source crisis event the data is from

  Args:
    df: DataFrame to add source column to
  
  Returns:
    df: DataFrame with SOURCE_KEY column added with np.nan values
  """
  df[SOURCE_KEY] = np.nan
  return df

def rename_column(df: pd.DataFrame, old_col_name: str, new_col_name: str) -> None:
  """Renames a column in df inplace originally named old_col_name to new_col_name 

  Args:
    df: DataFrame whose old_col_name is being renamed to new_col_name inplace
    old_col_name: Old column name present in df
    new_col_name: New column name
  """
  df.rename(columns={old_col_name: new_col_name}, inplace=True)

def construct_filename_series(df: pd.DataFrame, file_path_col_name: str) -> pd.Series:
  """Constructs a filename series from a column file_path_col_name containing
    souce file paths in the dataframe df

  Args:
    df: DataFrame containing file paths contained in the file_path_col_name column
    file_path_col_name: Name of the column in df which has the source file paths
  
  Returns:
    filenames_series: Series containing corresponding filenames present in the source file paths present
      in the file_path_col_name column in pd
  """
  file_path_series = df[file_path_col_name]
  filename_series = file_path_series.apply(extract_filename_from_file_path) 
  return filename_series

def construct_relevant_columns_regex(relevant_column_prefixes_list: List[str]) -> str:
  """Constructs a relevant column regex using a list of column prefix strings in 
      relevant_column_prefixes_list for relevant

      The relevant column regex is useful for retaining only columns in a df whose
      name matches any of the prefixes in the relevant column regex.

  Args:
    relevant_column_prefixes_list: List of string column name prefixes to 
      create a relevant column prefix regex relevant_col_regex
  
  Returns:
    relevant_col_regex: String regex containing relevant column prefixes contained in
      the relevant_column_prefixes_list
  """
  relevant_col_regex = '|'.join(relevant_column_prefixes_list)
  return relevant_col_regex

def keep_relevant_df_columns(df: pd.DataFrame, relevant_column_prefixes_list: List[str]) -> pd.DataFrame:
  """Constructs a column subsetted DataFrame using column prefixes contained in relevant_column_prefixes_list

    The columns in df with names that contain a prefix present in the relevant_column_prefixes_list
    are the only columns retained in the resultant new_df, i.e. new_df is a column subsetted version of 
    df.

  Args:
    df: DataFrame which may contain columns whose prefixes are contained in the
      relevant_column_prefixes_list
    relevant_column_prefixes_list: List of string column name prefixes for columns
      in df which are to be retained in the resultant new_df, if any
  
  Returns:
    new_df: DataFrame containing only the subset of columns in df which have a prefix contained in 
      the relevant_column_prefixes_list
  """
  # Only keep relevant columns
  relevant_col_regex = construct_relevant_columns_regex(relevant_column_prefixes_list)
  new_df = df.loc[:, df.columns.str.contains(relevant_col_regex)]
  return new_df

def drop_empty_df_rows(df: pd.DataFrame, how: str = 'any') -> pd.DataFrame:
  """Removes rows which have np.nan values in either all columns (how = 'all') or
    in any of the columns (how = 'any')

  Args:
    df: DataFrame whose rows with np.nan values are being dropped
    how: Determines which rows containing np.nan values are dropped.
      If 'all' only rows which have np.nan values in all columns in df are dropped.
      If 'any' rows which have np.nan in any of the columns in df are dropped.
      Default value is 'any'
  
  Returns:
    new_df: DataFrame without relevant rows containing np.nan values dropped
  """
  # Remove rows which have all NaN values
  assert how == 'any' or how == 'all'
  new_df = df.dropna(axis = 0, how = how)
  return new_df

def left_join_dfs_by_filename(left_df: pd.DataFrame, right_df: pd.DataFrame) -> pd.DataFrame:
  """Left joins a left_df and right_df on the left_df, specifically on a shared FILENAME_KEY column.

      left_df and right_df must both have a FILENAME_KEY column

  Args:
    left_df: Left DataFrame in the left join 
    right_df: Right DataFrame in the left join
  
  Returns:
    merged_df: Resultant DataFrame from left join between left_df and right_df on the FILENAME_KEY
      column
  """
  assert FILENAME_KEY in left_df.columns and FILENAME_KEY in right_df.columns
  merged_df = left_df.merge(right_df, how='left', on=FILENAME_KEY)
  return merged_df

def save_df(df: pd.DataFrame, save_csv_path: str, encoding: Optional[str] = None, index: bool = False) -> None:
  """Saves a dataframe df as a csv file on the host at path save_csv_path with encoding encoding and
    with the index column if index is True

  Args:
    df: Dataframe to save
    save_csv_path: path on host to save csv of the dataframe df
    encoding: encoding to save the df with as csv. Default is None
    index: Determines if index column should be saved in the csv. Default is False
  """
  df.to_csv(save_csv_path, encoding=encoding, index=index)
  print(f"Saved csv to {save_csv_path}")
