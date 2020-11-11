from nltk.corpus.reader.bnc import BNCCorpusReader
import os
from common import *

# from .mwpreprocessor import mwpreprocess


def preprocess(input_folder_path, output_folder_path, combined=False, mode='train', lowercase=False):
    if input_folder_path[-1] != '/':
        input_folder_path = input_folder_path+'/'
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if not (os.path.exists(input_folder_path) and os.path.isdir(input_folder_path)):
        raise FileNotFoundError('No such folder exists -> '+input_folder_path)

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        os.mkdir(output_folder_path)

    file_list = []

    if combined:
        if mode == 'train':
            output_file_path = output_folder_path + 'train-corpus_preprocessed.txt'
        else:
            output_file_path = output_folder_path + 'test-corpus_preprocessed.txt'
        with open(output_file_path, 'w') as f:
            pass
        file_list = dirWalk(input_folder_path,
                            output_file_path, file_list, combined)
    else:
        if mode == 'train':
            output_folder_path = output_folder_path + 'Train-corpus_preprocessed/'
        else:
            output_folder_path = output_folder_path + 'Test-corpus_preprocessed/'
        if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
            os.mkdir(output_folder_path)
        file_list = dirWalk(input_folder_path,
                            output_folder_path, file_list, combined)

    for file_entry in file_list:
        root_path = file_entry[0]
        file_name = file_entry[1]
        output_file_path = file_entry[2]

        bncreader = BNCCorpusReader(root=root_path, fileids=file_name)
        words = bncreader.tagged_words(c5=True)

        if lowercase:
            data = "".join(
                (str(word[0]).lower() + "_" + str(word[1]) + "\n") for word in words)
        else:
            data = "".join(
                (str(word[0]) + "_" + str(word[1]) + "\n") for word in words)

        # mwdata = mwpreprocess(root_path+file_name, lowercase)
        # data = data+mwdata

        if combined:
            with open(output_file_path, 'a') as f:
                f.write(data)
        else:
            with open(output_file_path, 'w') as f:
                f.write(data)
