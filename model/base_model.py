import os
import json

from common import *


def process(file_list, output_folder_path, file_mode='json'):
    frequency_map = dict()

    frequency_map_file = output_folder_path+'frequency_map.json'
    probability_map_file = output_folder_path+'probability_map.json'
    tagger_map_file = output_folder_path+'tagger_map.json'

    for file_entry in file_list:
        dictionary = get_dictionary(file_entry, file_mode)
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

    # with open(frequency_map_file, 'w') as f:
    #     json.dump(frequency_map, f, indent=4)

    probability_map = frequency_map
    del frequency_map

    for tag_dictionary in probability_map.values():
        total = sum(tag_dictionary.values())
        for tag in tag_dictionary.keys():
            tag_dictionary[tag] = round(
                tag_dictionary[tag]/total, 7)  # rounded upto 7 digits

    # with open(probability_map_file, 'w') as f:
    #     json.dump(probability_map, f, indent=4)

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
