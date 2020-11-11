import corpus_processor
import os

from common import *


def preprocess(input_folder_path, output_folder_path, combined, mode, lowercase):
    if input_folder_path[-1] != '/':
        input_folder_path = input_folder_path+'/'
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        os.mkdir(output_folder_path)

    file_list = []

    if combined:
        output_file_path = output_folder_path + mode + '-corpus_preprocessed.txt'
        file_list = dirWalk(input_folder_path,
                            output_file_path, file_list, combined)

        source_file_list = [(file_entry[0]+file_entry[1])
                            for file_entry in file_list]
        corpus_processor.process(source_file_list, output_file_path, lowercase)

    else:
        output_folder_path = output_folder_path + \
            mode.capitalize() + '-corpus_preprocessed/'
        if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
            os.mkdir(output_folder_path)
        file_list = dirWalk(input_folder_path,
                            output_folder_path, file_list, combined)
        for file_entry in file_list:
            output_file_path = file_entry[2]
            source_file_list = [file_entry[0]+file_entry[1]]
            corpus_processor.process(
                source_file_list, output_file_path, lowercase)
