import os
from os.path import join, isfile
import shutil

import pandas as pd

from .constants import (
    TRAIN_SPLIT,
    DEV_SPLIT,
    TEST_SPLIT,
    IGNORE_FILES,
)

from typing import List

# Filesystem Helpers
def delete_folder(folder_path: str) -> None:
    """Deletes a folder located at folder_path on the local filesystem.

        Deletes folder at folder_path. If there is an OSError, prints the error.

    Args:
        folder_path: Path where folder being deleted is located on the local filesystem.
    """
    try:
        os.rmdir(folder_path)
    except OSError as e:
        print("Error: %s : %s" % (folder_path, e.strerror))

def make_folder(folder_path: str) -> None:
    """Makes a new folder on the local filesystem at path folder_path.
    
        Creates a new folder on the local filesystem. If a FileExistsError is raised, the function overwrites the directory, 
        by first deleting it, then creating a new folder.

    Args:
        folder_path: Path where the folder will be saved.
    """
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        print(f'{folder_path} directory already exists. Overwriting...')
        delete_folder(folder_path)
        os.mkdir(folder_path)

def get_file_paths(folder_file_path: str) -> List[str]:
    """Recursively creates a list file_paths contained in folder_file_path directory on the local filesystem specified in the original call.
        
        Creates list of file paths contained in folder_file_path. If a directory does not exist, a message indicating so is printed.
    
    Args:
        folder_file_path: Path to folder or file on local filesystem.
    
    Returns:
        file_paths: List of paths to files located at the folder specified by folder_file_path in the original call to the function.
    """
    # Base case -- file located at folder_file_path
    if isfile(folder_file_path):
        return [folder_file_path]
    try:
        # Recursive case -- folder located at folder_file_path, grab file paths inside folder_file_path
        # Files sorted for labeling convenience (i.e. looking at samples one after another rather than searching for each.)
        file_paths = []
        for child in sorted(os.listdir(folder_file_path)):
            if child in IGNORE_FILES:
                continue
            file_paths.extend(get_file_paths(join(folder_file_path, child)))
        return file_paths
    except FileNotFoundError:
        print('The directory you have specified does not exist on your filesystem.')


  
def copy_file_source_to_dest(source_path: str, dest_path: str) -> None:
    """Copies a file on the local file system located at source_path and copies it to dest_path.

    Args:
        source_path: Path on local filesystem where the file is being coped from.
        dest_path: Path on the local filesystem where the file is being copied to.
    """
    shutil.copy(source_path, dest_path)

# Copy over the images into the labeled folders
def copy_images_to_labeled_folders(
  df: pd.DataFrame, 
  source_folder_path: str, 
  dest_folder_path: str,
  file_path_col_name: str,
  label_col_name: str
  ) -> None:
    """Copies images with paths and labels in df from source_folder_path to relevant data split and labels folders in dest_folder_path on the local filesystem.

        Copies an image located at path source_folder_path/df[file_path_col_name][i] to dest_folder_path/df[label_col_name][i]

    Args:
        df: DataFrame containing source image paths and labels.
        source_folder_path: Path to source folder containing images.
        dest_folder_path: Path to destination folder
        file_path_col_name: Column name of column containing file paths to data in df
        label_col_name: Column name of the labels corresponding to the data described in df
    """
    df.apply(lambda row: copy_file_source_to_dest(join(source_folder_path, row[file_path_col_name]), 
                                                   join(dest_folder_path, row[label_col_name])), axis=1)

def construct_labeled_data_folder(
  task_name: str, 
  task_splits_folder_path: str, 
  task_data_path: str,
  file_path_col_name: str,
  label_col_name: str,
  parent_path: str, 
  folder_name: str,
  ) -> None:
    '''Constructs image data folder that is separated into train, dev, and test split folders using 
       sheets (CSV, TSV, etc.) which provide filenames and labels for each split.

        Creates image data folder which contains data split folders for train, dev, and test. The split folders
        are then separated into folders for each of the unique labels in the .
    
    Args:
        task_name: name of the prediction task (snake_case) regarding the data split folders we are creating
        task_splits_folder_path: path to folder containing splits sheets with file paths and labels
        task_data_path: path of the folder containing the actual image data for the task
        file_path_col_name: Column name of column containing file paths to data in the dataframes in task_splits_folder_path
        label_col_name: Column name of the labels corresponding to the data described in dataframes in task_splits_folder_path
        parent_path: path of the parent directory for where we will save the folder containing our organized image data folders
        folder_name: name of the folder we wish to create with this function
    '''
    split_names = [TRAIN_SPLIT, DEV_SPLIT, TEST_SPLIT]
    split_paths = os.listdir(task_splits_folder_path)
    
    folder_path = join(parent_path, folder_name)
    make_folder(parent_path, folder_path)
    # Make train/val/test directories and class labeled directories if they don't already exist
    for split in split_names:
        split_filename = list(filter(lambda filename: split in filename, split_paths))[0]
        split_path = join(task_splits_folder_path, split_filename)
        split_sep = '\t' if '.tsv' in split_path else ','
        split_df = pd.read_csv(split_path, sep=split_sep)
        class_labels = split_df[label_col_name].unique()
        dir_path = join(folder_path, split)
        make_folder(folder_path, split)
        for class_label in class_labels:
            make_folder(dir_path, class_label)
            
        copy_images_to_labeled_folders(split_df, task_data_path, dir_path, file_path_col_name, label_col_name)
        N_samples_in_split = len(split_df)
        print(f"Number of data point in the {split} set for the {task_name} task: {N_samples_in_split}")

# Path utilities
def extract_parent_path(original_path: str) -> str:
    """Extracts the parent path from the original_path

    Args:
        original_path: path whose parent path is being extracted from
  
    Returns:
        parent_path: Parent path extracted from original_path
    """
    split_path = original_path.split('/')
    split_parent_path = split_path[:len(split_path)-1]
    parent_path = "/".join(split_parent_path)
    return parent_path

def extract_filename_from_file_path(file_path: str) -> str:
    """Extracts a filename from a file path

    Args:
        file_path: path to file which to extract a filename, e.g. 'test/test.jpg'
  
    Returns:
        filename: filename extracted from file_path
    """
    filename = file_path.split('/')[-1]
    return filename

def insert_part_of_path(original_path: str, path_to_insert: str, insert_index: int) -> str:
    """Inserts and returns a new path with path_to_insert inserted in the original_path
        
        The original_path is split on the '/' character. The path_to_insert is inserted in the original_path
        at the insert_index in the split original_path

    Args:
        original_path: original path which is being altered by the path_to_insert
        path_to_insert: path to insert in original_path
        insert_index: index to insert the path_to_insert in the original path split on the '/' character
  
    Returns:
        new_path: New path with path_to_insert inserted at the insert_index
            in the split original_path
    """
    split_original_path = original_path.split('/')
    path_before_index = split_original_path[:insert_index]
    path_after_index = split_original_path[insert_index:]
    new_path = join("/".join(path_before_index), path_to_insert, "/".join(path_after_index))
    return new_path