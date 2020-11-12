import json
import pandas


def generate_confusion_matrix(output_folder_path: str, matrix_mode: str):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    matrix_file = output_folder_path+'confusion_matrix.'+matrix_mode
    tags_count_file = output_folder_path + 'train-tags-count.json'

    with open(tags_count_file, 'r') as f:
        tags = json.load(f)
    confusion_matrix = dict.fromkeys(tags.keys())
    for key in confusion_matrix.keys():
        confusion_matrix[key] = dict.fromkeys(tags.keys(), 0)
    del tags

    tagged_words_file = output_folder_path+'tagged_words_file.json'
    with open(tagged_words_file, 'r') as f:
        tagged_words = json.load(f)

    # Actual is outer key, predicted is inner key
    for value in tagged_words.values():
        actual_tag = value['expected_tag']
        predicted_tag = value['assigned_tag']
        frequency = value['frequency']
        if actual_tag in confusion_matrix:
            confusion_matrix[actual_tag][predicted_tag] += frequency

    if matrix_mode == 'json':
        with open(matrix_file, 'w') as f:
            json.dump(confusion_matrix, f, indent=4)
    else:
        dataframe = pandas.DataFrame(confusion_matrix)
        dataframe.to_csv(matrix_file)
