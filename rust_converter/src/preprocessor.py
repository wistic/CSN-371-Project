import os
import corpusconverter

from cfg import config


def preprocess(mode='train', lowercase=False):
    resource_folder_path = config['resource_folder_path']
    output_folder_path = config['output_folder_path']
    cargo_bin_path = config['cargo_bin_path']

    if resource_folder_path[-1] != '/':
        resource_folder_path = resource_folder_path+'/'
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'
    if cargo_bin_path[-1] != '/':
        cargo_bin_path = cargo_bin_path + '/'

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        os.mkdir(output_folder_path)

    if mode == 'train':
        root_path = resource_folder_path+'Train-corpus/'
    elif mode == 'test':
        root_path = resource_folder_path+'Test-corpus/'
    else:
        raise AttributeError('Mode not supported.')

    if mode == 'train':
        output_folder_path = output_folder_path + 'Train-corpus_preprocessed/'
    else:
        output_folder_path = output_folder_path + 'Test-corpus_preprocessed/'

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        os.mkdir(output_folder_path)

    folders = os.listdir(root_path)
    for folder in folders:
        absolute_folder_path = root_path + folder
        folder_path = output_folder_path + folder + '_preprocessed'
        if not (os.path.exists(folder_path) and os.path.isdir(folder_path)):
            os.mkdir(folder_path)

        file_list = os.listdir(absolute_folder_path)
        for file_name in file_list:
            output_file_path = folder_path + '/' + \
                file_name.split('.', 1)[0]+'_preprocessed.txt'
            input_file_path = absolute_folder_path + '/' + file_name
            if lowercase:
                corpusconverter.convert(input_file_path, output_file_path, True)
            else:
                corpusconverter.convert(input_file_path, output_file_path, False)
