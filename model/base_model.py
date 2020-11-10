import os
import json
import pickle
import itertools


def dirWalk(source_path, file_list, file_mode):
    listing = os.listdir(source_path)
    for entry in listing:
        absolute_path = source_path+entry
        if os.path.isdir(absolute_path) and entry.split('_')[1] == 'dictionary':
            if absolute_path[-1] != '/':
                absolute_path = absolute_path+'/'
            dirWalk(absolute_path, file_list, file_mode)
        else:
            parts = entry.split('.')
            if parts[1] == file_mode and parts[0].split('_')[1] == 'dictionary':
                file_list.append(absolute_path)
    return file_list


def process(file_list, output_folder_path, file_mode='json'):
    frequency_map = dict()

    frequency_map_file = output_folder_path+'frequency_map.json'
    probability_map_file = output_folder_path+'probability_map.json'
    tagger_map_file = output_folder_path+'tagger_map.json'

    for file_entry in file_list:
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

        for key, value in dictionary.items():
            word, tag = key.split('_')

            if word not in frequency_map:
                frequency_map[word] = dict()
                tag_parts = tag.split('-')
                factor = len(tag_parts)
                for tag_part in tag_parts:
                    frequency_map[word][tag_part] = value/factor
            else:
                tag_parts = tag.split('-')
                factor = len(tag_parts)
                for tag_part in tag_parts:
                    if tag_part not in frequency_map[word]:
                        frequency_map[word][tag_part] = value/factor
                    else:
                        frequency_map[word][tag_part] = frequency_map[word][tag_part]+value/factor

    with open(frequency_map_file, 'w') as f:
        json.dump(frequency_map, f, indent=4)

    probability_map = frequency_map
    del frequency_map

    for tag_dictionary in probability_map.values():
        total = sum(tag_dictionary.values())
        for tag in tag_dictionary.keys():
            tag_dictionary[tag] = round(
                tag_dictionary[tag]/total, 7)  # rounded upto 7 digits

    with open(probability_map_file, 'w') as f:
        json.dump(probability_map, f, indent=4)

    tagger_map = dict()
    for word, tag_dictionary in probability_map.items():
        tagger_map[word] = max(tag_dictionary, key=tag_dictionary.get)

    with open(tagger_map_file, 'w') as f:
        json.dump(tagger_map, f, indent=4)


def generate_model(output_folder_path, combined=False, file_mode='json'):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        raise FileNotFoundError('No such folder exists -> '+output_folder_path)

    if combined:
        input_file_path = output_folder_path+'train-corpus_dictionary.'+file_mode
        file_list = [input_file_path]
    else:
        file_list = []
        input_folder_path = output_folder_path+'Train-corpus_dictionary/'
        if not (os.path.exists(input_folder_path) and os.path.isdir(input_folder_path)):
            raise FileNotFoundError(
                'No such folder exists -> '+input_folder_path)
        file_list = dirWalk(input_folder_path, file_list, file_mode)
    process(file_list, output_folder_path, file_mode)
