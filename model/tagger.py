import os
import json

from common import *


def process(file_list, output_folder_path, file_mode='json'):
    tagged_words = dict()

    tagged_words_file = output_folder_path+'tagged_words_file.json'
    tagger_map_file = output_folder_path+'tagger_map.json'
    if not (os.path.exists(tagger_map_file) and os.path.isfile(tagger_map_file)):
        raise FileNotFoundError(
            'No such file exists -> '+tagger_map_file)

    with open(tagger_map_file, 'r') as f:
        tagger_map = json.load(f)

    for file_entry in file_list:
        dictionary = get_dictionary(file_entry, file_mode)
        for key, value in dictionary.items():
            word, expected_tag = key.split('_')

            if key not in tagged_words:
                if word in tagger_map:
                    assigned_tag = tagger_map[word]
                else:
                    assigned_tag = ""
                tag_dictionary = {
                    "word": word,
                    "frequency": value,
                    "expected_tag": expected_tag,
                    "assigned_tag": assigned_tag
                }
                tagged_words[key] = tag_dictionary
            else:
                tagged_words[key]["frequency"] = tagged_words[key]["frequency"]+value

    with open(tagged_words_file, 'w') as f:
        json.dump(tagged_words, f, indent=4)


def tag_words(output_folder_path, combined=False, file_mode='json'):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        raise FileNotFoundError('No such folder exists -> '+output_folder_path)

    if combined:
        input_file_path = output_folder_path+'test-corpus_dictionary.'+file_mode
        file_list = [input_file_path]
    else:
        file_list = []
        input_folder_path = output_folder_path+'Test-corpus_dictionary/'
        if not (os.path.exists(input_folder_path) and os.path.isdir(input_folder_path)):
            raise FileNotFoundError(
                'No such folder exists -> '+input_folder_path)
        file_list = dirWalk(input_folder_path, file_list, file_mode)
    process(file_list, output_folder_path, file_mode)
