import argparse

from .data_labeling_utils import (
    make_tasks_labeling_df_from_folder,
    save_tasks_labeling_csv_from_df
)

# Creates a tasks labeling df using file names contained in the directory located at data_dir_path and prediction tasks specified in task_list.
# Saves the labeling df to the csv_save_path on host with the encoding encoding

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tasks_list', nargs='+', help="List of task names for labeling")
    parser.add_argument('--file_path_col_name', type=str, help="Column name of column which will contain file paths to data in data_dir_path")
    parser.add_argument('--data_dir_path', type=str, help="Path to fetch unlabeled data from")
    parser.add_argument('--csv_save_path', type=str, help="Path for saving the .csv")
    parser.add_argument('--prepended_url', type=str, nargs="?", default=None, help="prepended url for link to resource.")
    parser.add_argument('--encoding', type=str, nargs="?", default=None, help="Encoding the labeling csv will have.")
    parser.add_argument('--index', type=str, nargs="?", default=False, help="Save index of dataframe as index col.")
    args = parser.parse_args()
    tasks_list = args.tasks_list
    file_path_col_name = args.file_path_col_name
    data_folder_path = args.data_folder_path
    csv_save_path = args.csv_save_path
    encoding = args.encoding
    index = args.index
    prepended_url = args.prepended_url
    tasks_labeling_df = make_tasks_labeling_df_from_folder(data_folder_path, file_path_col_name, tasks_list, prepended_url)
    save_tasks_labeling_csv_from_df(tasks_labeling_df, csv_save_path, encoding=encoding, index=index)

