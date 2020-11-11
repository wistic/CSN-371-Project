import os
import json
import itertools

from common import *


def process(file_list, output_folder_path, mode, file_mode):
    words = dict()
    tags = dict()

    words_count_file = output_folder_path + mode + '-words-count.json'
    tags_count_file = output_folder_path + mode + '-tags-count.json'
    top_words_file = output_folder_path + mode + '-top-words.txt'
    top_tags_file = output_folder_path + mode + '-top-tags.txt'

    for file_entry in file_list:
        dictionary = get_dictionary(file_entry, file_mode)
        for key, value in dictionary.items():
            word, tag = key.split('_')

            if word not in words:
                words[word] = value
            else:
                words[word] = words[word]+value

            if tag not in tags:
                tags[tag] = value
            else:
                tags[tag] = tags[tag]+value

    sorted_words = {key: value for key, value in sorted(
        words.items(), key=lambda item: item[1], reverse=True)}
    sorted_tags = {key: value for key, value in sorted(
        tags.items(), key=lambda item: item[1], reverse=True)}

    with open(words_count_file, 'w') as f:
        json.dump(sorted_words, f, indent=4)
    with open(tags_count_file, 'w') as f:
        json.dump(sorted_tags, f, indent=4)

    top_words_list = [key for key in itertools.islice(sorted_words.keys(), 10)]
    top_tags_list = [key for key in itertools.islice(sorted_tags.keys(), 10)]

    with open(top_words_file, 'w') as f:
        data = "\n".join(top_words_list)
        f.write(data)
    with open(top_tags_file, 'w') as f:
        data = "\n".join(top_tags_list)
        f.write(data)


def gettoppers(output_folder_path, combined, mode, file_mode):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if combined:
        input_file_path = output_folder_path + mode + '-corpus_dictionary.'+file_mode
        file_list = [input_file_path]
    else:
        file_list = []
        input_folder_path = output_folder_path + \
            mode.capitalize() + '-corpus_dictionary/'
        file_list = dirWalk(input_folder_path, file_list, file_mode)
    process(file_list, output_folder_path, mode, file_mode)
