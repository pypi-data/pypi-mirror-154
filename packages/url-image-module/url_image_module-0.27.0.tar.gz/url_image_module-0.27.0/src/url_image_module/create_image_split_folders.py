#!/usr/bin/env python
# coding: utf-8
import argparse

from .os_utils import (
    construct_labeled_data_folder
)

# Terminal python program to Constructs image data folder that is separated into train, dev, and test split folders using 
# sheets (CSV, TSV, etc.) which provide filenames and labels for each split and saves these splits to some destination folder, folder_name.

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--task_name', type=str, help="Name of the prediction task related to the image data folders we are creating")
  parser.add_argument('--task_splits_folder_path', type=str, help="Path to data split files which contain to path to image data")
  parser.add_argument('--task_data_path', type=str, help="Path to folder which contains image data")
  parser.add_argument('--file_path_col_name', type=str, help="Column name of column containing file paths to data in the dataframes in task_splits_folder_path")
  parser.add_argument('--label_col_name', type=str, help="Column name of the labels corresponding to the data described in dataframes in task_splits_folder_path")
  parser.add_argument('--parent_path', type=str, help="Path to fetch crisis image data splits and save the folder we're going to create.")
  parser.add_argument('--folder_name', type=str, help="Name of the Labeled Image Data Folder to be created")
  args = parser.parse_args()
  task_name = args.task_name
  task_splits_folder_path = args.task_splits_folder_path
  task_data_path = args.task_data_path
  file_path_col_name = args.file_path_col_name
  label_col_name = args.label_col_name
  parent_path = args.parent_path
  folder_name = args.folder_name
  construct_labeled_data_folder(
    task_name,
    task_splits_folder_path,
    task_data_path,
    file_path_col_name,
    label_col_name,
    parent_path,
    folder_name
  )

