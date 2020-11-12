import json
import pandas


def judge_model(output_folder_path: str, matrix_mode: str):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    matrix_file = output_folder_path+'confusion_matrix.'+matrix_mode

    if matrix_mode == 'json':
        with open(matrix_file, 'r') as f:
            confusion_matrix = json.load(f)
    else:
        dataframe = pandas.read_csv(matrix_file, index_col=0)
        confusion_matrix = dataframe.to_dict()
