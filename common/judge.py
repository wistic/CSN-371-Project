import json
import pandas
from .utility import pretty_print


def judge(output_folder_path: str, matrix_mode: str):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    matrix_file = output_folder_path+'confusion_matrix.'+matrix_mode
    tag_report_file = output_folder_path+'tag-report.json'

    if matrix_mode == 'json':
        with open(matrix_file, 'r') as f:
            confusion_matrix = json.load(f)
    else:
        dataframe = pandas.read_csv(matrix_file, index_col=0)
        confusion_matrix = dataframe.to_dict()

    judge_dictionary = dict.fromkeys(confusion_matrix.keys())

    total = 0
    for key in confusion_matrix.keys():
        total += sum(confusion_matrix[key].values())

    for tag in judge_dictionary.keys():
        weight = sum(confusion_matrix[tag].values())
        true_positive = confusion_matrix[tag][tag]
        false_negative = weight - true_positive
        false_positive = 0
        for key in confusion_matrix.keys():
            false_positive += confusion_matrix[key][tag]
        false_positive -= confusion_matrix[tag][tag]
        true_negative = total - true_positive - false_negative - false_positive

        try:
            accuracy = (true_positive+true_negative)/total
        except ZeroDivisionError:
            accuracy = 0
        try:
            precision = true_positive/(true_positive+false_positive)
        except ZeroDivisionError:
            precision = 0
        try:
            recall = true_positive/(true_positive+false_negative)
        except ZeroDivisionError:
            recall = 0
        try:
            f1_score = (2*precision*recall)/(precision+recall)
        except ZeroDivisionError:
            f1_score = 0

        tag_dictionary = {
            'TP': true_positive,
            'FN': false_negative,
            'FP': false_positive,
            'TN': true_negative,
            'weight': weight,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        }
        judge_dictionary[tag] = tag_dictionary

    with open(tag_report_file, 'w') as f:
        json.dump(judge_dictionary, f, indent=4)

    average_f1_score = 0
    for tag in judge_dictionary.keys():
        average_f1_score += judge_dictionary[tag]['f1_score']
    try:
        average_f1_score = average_f1_score/len(judge_dictionary)
    except ZeroDivisionError:
        average_f1_score = 0
        print('Bad dataset')

    weighted_f1_score = 0
    for tag in judge_dictionary.keys():
        weighted_f1_score += (judge_dictionary[tag]
                              ['f1_score']*judge_dictionary[tag]['weight'])
    try:
        weighted_f1_score = weighted_f1_score/total
    except ZeroDivisionError:
        weighted_f1_score = 0
        print('Bad dataset')

    pretty_print("Average F1 score", average_f1_score)
    pretty_print("Weighted F1 score", weighted_f1_score)
