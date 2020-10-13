import os
import json
import pickle


def dirWalk(source_path, output_path, file_list, file_mode='json'):
    listing = os.listdir(source_path)
    for entry in listing:
        absolute_path = source_path+entry
        if os.path.isdir(absolute_path) and entry.split('_')[1] == 'preprocessed':
            if absolute_path[-1] != '/':
                absolute_path = absolute_path+'/'
            new_output_path = output_path+entry.split('_')[0]+'_dictionary/'
            if not (os.path.exists(new_output_path) and os.path.isdir(new_output_path)):
                os.mkdir(new_output_path)
            dirWalk(absolute_path, new_output_path, file_list, file_mode)
        else:
            parts = entry.split('.')
            if parts[1] == 'txt' and parts[0].split('_')[1] == 'preprocessed':
                new_output_path = output_path + \
                    parts[0].split('_')[0]+'_dictionary.'+file_mode
                file_entry = (absolute_path, new_output_path)
                file_list.append(file_entry)
    return file_list


def convert(input_file_path, output_file_path, file_mode='json'):
    with open(input_file_path, 'r') as f:
        preprocessed_list = f.readlines()
    trimmed_list = [entry.strip('\n') for entry in preprocessed_list]
    del preprocessed_list
    dictionary = dict()
    for entry in trimmed_list:
        if entry not in dictionary:
            dictionary[entry] = 1
        else:
            dictionary[entry] = dictionary[entry]+1
    del trimmed_list
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


def dictprocess(output_folder_path, combined=False, mode='train', file_mode='json'):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        raise FileNotFoundError('No such folder exists -> '+output_folder_path)

    if combined:
        if mode == 'train':
            input_file_path = output_folder_path+'train-corpus_preprocessed.txt'
            output_file_path = output_folder_path+'train-corpus_dictionary.'+file_mode
        else:
            input_file_path = output_folder_path+'test-corpus_preprocessed.txt'
            output_file_path = output_folder_path+'test-corpus_dictionary.'+file_mode
        convert(input_file_path, output_file_path, file_mode)
    else:
        file_list = []
        if mode == 'train':
            input_folder_path = output_folder_path+'Train-corpus_preprocessed/'
            new_output_folder_path = output_folder_path+'Train-corpus_dictionary/'
        else:
            input_folder_path = output_folder_path+'Test-corpus_preprocessed/'
            new_output_folder_path = output_folder_path+'Test-corpus_dictionary/'
        if not (os.path.exists(new_output_folder_path) and os.path.isdir(new_output_folder_path)):
            os.mkdir(new_output_folder_path)
        file_list = dirWalk(input_folder_path,
                            new_output_folder_path, file_list, file_mode)
        for file_entry in file_list:
            input_file_path = file_entry[0]
            output_file_path = file_entry[1]
            convert(input_file_path, output_file_path, file_mode)
