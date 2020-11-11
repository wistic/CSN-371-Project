import os
import json
import pickle


def get_dictionary(file_entry, file_mode):
    if file_mode == 'json':
        with open(file_entry, 'r') as f:
            dictionary = json.load(f)
    elif file_mode == 'pickle':
        with open(file_entry, 'rb') as f:
            dictionary = pickle.load(f)
    else:
        with open(file_entry, 'r') as f:
            dictionary_list = f.readlines()
        trimmed_list = [entry.strip('\n') for entry in dictionary_list]
        del dictionary_list
        dictionary = dict()
        for entry in trimmed_list:
            parts = entry.split(' -> ')
            dictionary[parts[0]] = int(parts[1])
        del trimmed_list
    return dictionary
