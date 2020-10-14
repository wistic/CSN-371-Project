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


def process(file_list, output_folder_path, mode='train', file_mode='json'):
    words = dict()
    tags = dict()

    if mode == 'train':
        words_count_file = output_folder_path+'train-words-count.json'
        tags_count_file = output_folder_path+'train-tags-count.json'
        top_words_file = output_folder_path+'train-top-words.txt'
        top_tags_file = output_folder_path+'train-top-tags.txt'
    else:
        words_count_file = output_folder_path+'test-words-count.json'
        tags_count_file = output_folder_path+'test-tags-count.json'
        top_words_file = output_folder_path+'test-top-words.txt'
        top_tags_file = output_folder_path+'test-top-tags.txt'

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

            if word not in words:
                words[word] = value
            else:
                words[word] = words[word]+value

        ### BEGIN EDITABLE ###
        # Use only one of these

        # Not separarting multiple tags like NN1-VVG
            # if tag not in tags:
            #     tags[tag] = value
            # else:
            #     tags[tag] = tags[tag]+value

        # Separarting multiple tags like NN1-VVG
            tag_parts = tag.split('-')
            factor = len(tag_parts)
            for tag_part in tag_parts:
                if tag_part not in tags:
                    tags[tag_part] = value/factor
                else:
                    tags[tag_part] = tags[tag_part]+value/factor

        ### END EDITABLE ###

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


def gettoppers(output_folder_path, combined=False, mode='train', file_mode='json'):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        raise FileNotFoundError('No such folder exists -> '+output_folder_path)

    if combined:
        if mode == 'train':
            input_file_path = output_folder_path+'train-corpus_dictionary.'+file_mode
        else:
            input_file_path = output_folder_path+'test-corpus_dictionary.'+file_mode
        file_list = [input_file_path]
    else:
        file_list = []
        if mode == 'train':
            input_folder_path = output_folder_path+'Train-corpus_dictionary/'
        else:
            input_folder_path = output_folder_path+'Test-corpus_dictionary/'
        file_list = dirWalk(input_folder_path, file_list, file_mode)
    process(file_list, output_folder_path, mode, file_mode)
