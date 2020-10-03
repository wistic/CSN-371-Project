from nltk.corpus.reader.bnc import BNCCorpusReader
import os

from cfg import config
from mwpreprocessor import mwpreprocess


def preprocess(combined=False):
    resource_folder_path = config['resource_folder_path']
    output_folder_path = config['output_folder_path']
    if resource_folder_path[-1] == '/':
        train_folder_path = resource_folder_path + 'Train-corpus/'
    else:
        train_folder_path = resource_folder_path + '/Train-corpus/'
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'
    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        os.mkdir(output_folder_path)

    if combined:
        bncreader = BNCCorpusReader(
            root=train_folder_path, fileids='\w*/\w*.xml')
        words = bncreader.tagged_words(
            fileids=None, c5=True, strip_space=True, stem=False)
        output_file_path = output_folder_path + 'train_corpus_preprocessed.txt'
        data = "".join((str(word[0]) + "_" + str(word[1]) + "\n")
                       for word in words)
        combined_mwdata = mwpreprocess(train_folder_path, combined=True)
        data = data+combined_mwdata
        with open(output_file_path, "w") as f:
            f.write(data)
    else:
        train_preprocessed_folder_path = output_folder_path + 'Train-corpus_preprocessed/'
        if not (os.path.exists(train_preprocessed_folder_path) and os.path.isdir(train_preprocessed_folder_path)):
            os.mkdir(train_preprocessed_folder_path)
        train_folders = os.listdir(train_folder_path)
        for folder in train_folders:
            source_folder_path = train_folder_path+folder
            folder_path = train_preprocessed_folder_path + folder + '_preprocessed'
            if not (os.path.exists(folder_path) and os.path.isdir(folder_path)):
                os.mkdir(folder_path)
            file_list = os.listdir(source_folder_path)
            for file_name in file_list:
                output_file_path = folder_path+'/' + \
                    file_name.split('.', 1)[0]+'_preprocessed.txt'
                bncreader = BNCCorpusReader(
                    root=source_folder_path, fileids=file_name)
                words = bncreader.tagged_words(
                    fileids=None, c5=True, strip_space=True, stem=False)
                data = "".join(
                    (str(word[0]) + "_" + str(word[1]) + "\n") for word in words)
                mwdata = mwpreprocess(
                    source_folder_path+'/'+file_name, combined=False)
                data = data+mwdata
                with open(output_file_path, "w") as f:
                    f.write(data)
