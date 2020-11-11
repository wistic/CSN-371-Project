import os
import json
import pickle

from common import *


def clean(dictionary: dict):
    """
    Used to remove inconsistencies such as word_tag1-tag2
    Converts it to word_tag1 and word_tag2
    """
    clean_dictionary = dictionary.copy()
    for key, value in dictionary.items():
        word, tag = key.split('_', 1)
        tag_parts = tag.split('-')
        if len(tag_parts) > 1:
            factor = len(tag_parts)
            value = value/factor
            del clean_dictionary[key]
            for tag_part in tag_parts:
                word_tag = word+'_'+tag_part
                if word_tag in clean_dictionary:
                    clean_dictionary[word_tag] = clean_dictionary[word_tag]+value
                else:
                    clean_dictionary[word_tag] = value
    return clean_dictionary


def convert(input_file_path, output_file_path, file_mode):
    with open(input_file_path, 'r') as f:
        preprocessed_list = f.readlines()
    trimmed_list = [entry.strip('\n') for entry in preprocessed_list]
    del preprocessed_list
    dictionary = dict()
    for entry in trimmed_list:
        if entry not in dictionary:
            dictionary[entry] = 1
        else:
            dictionary[entry] += 1
    del trimmed_list
    dictionary = clean(dictionary)
    if file_mode == 'json':
        with open(output_file_path, 'w') as f:
            json.dump(dictionary, f, indent=4)
    elif file_mode == 'pickle':
        with open(output_file_path, 'wb') as f:
            pickle.dump(dictionary, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        data = "".join((str(key) + " -> " + str(value) + "\n")
                       for key, value in dictionary.items())
        del dictionary
        with open(output_file_path, 'w') as f:
            f.write(data)


def dictprocess(output_folder_path, combined, mode, file_mode):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if combined:
        input_file_path = output_folder_path + mode + '-corpus_preprocessed.txt'
        output_file_path = output_folder_path + mode + '-corpus_dictionary.'+file_mode
        convert(input_file_path, output_file_path, file_mode)
    else:
        file_list = []
        input_folder_path = output_folder_path + \
            mode.capitalize() + '-corpus_preprocessed/'
        new_output_folder_path = output_folder_path + \
            mode.capitalize() + '-corpus_dictionary/'
        if not (os.path.exists(new_output_folder_path) and os.path.isdir(new_output_folder_path)):
            os.mkdir(new_output_folder_path)
        file_list = dirWalk(input_folder_path,
                            new_output_folder_path, file_list, file_mode)
        for file_entry in file_list:
            input_file_path = file_entry[0]
            output_file_path = file_entry[1]
            convert(input_file_path, output_file_path, file_mode)
