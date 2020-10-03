from nltk.corpus.reader.bnc import BNCCorpusReader
import os

from cfg import config
from .mwpreprocessor import mwpreprocess


def preprocess(combined=False, mode='train', lowercase=False):
    resource_folder_path = config['resource_folder_path']
    output_folder_path = config['output_folder_path']

    if resource_folder_path[-1] != '/':
        resource_folder_path = resource_folder_path+'/'
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
        os.mkdir(output_folder_path)

    if mode == 'train':
        root_path = resource_folder_path+'Train-corpus/'
    elif mode == 'test':
        root_path = resource_folder_path+'Test-corpus/'
    else:
        raise AttributeError('Mode not supported.')

    if combined:
        bncreader = BNCCorpusReader(
            root=root_path, fileids='\w*/\w*.xml')
        words = bncreader.tagged_words(
            fileids=None, c5=True, strip_space=True, stem=False)
        if mode == 'train':
            output_file_path = output_folder_path + 'train_corpus_preprocessed.txt'
        else:
            output_file_path = output_folder_path + 'test_corpus_preprocessed.txt'
        if lowercase:
            data = "".join(
                (str(word[0]).lower() + "_" + str(word[1]) + "\n") for word in words)
            combined_mwdata = mwpreprocess(
                root_path, combined=True, lowercase=True)
        else:
            data = "".join(
                (str(word[0]) + "_" + str(word[1]) + "\n") for word in words)
            combined_mwdata = mwpreprocess(
                root_path, combined=True, lowercase=False)
        data = data+combined_mwdata
        with open(output_file_path, "w") as f:
            f.write(data)
    else:
        if mode == 'train':
            output_folder_path = output_folder_path + 'Train-corpus_preprocessed/'
        else:
            output_folder_path = output_folder_path + 'Test-corpus_preprocessed/'

        if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
            os.mkdir(output_folder_path)

        folders = os.listdir(root_path)
        for folder in folders:
            absolute_folder_path = root_path+folder
            folder_path = output_folder_path + folder + '_preprocessed'
            if not (os.path.exists(folder_path) and os.path.isdir(folder_path)):
                os.mkdir(folder_path)

            file_list = os.listdir(absolute_folder_path)
            for file_name in file_list:
                output_file_path = folder_path+'/' + \
                    file_name.split('.', 1)[0]+'_preprocessed.txt'
                bncreader = BNCCorpusReader(
                    root=absolute_folder_path, fileids=file_name)
                words = bncreader.tagged_words(
                    fileids=None, c5=True, strip_space=True, stem=False)
                if lowercase:
                    data = "".join(
                        (str(word[0]).lower() + "_" + str(word[1]) + "\n") for word in words)
                    mwdata = mwpreprocess(
                        absolute_folder_path+'/'+file_name, combined=False, lowercase=True)
                else:
                    data = "".join(
                        (str(word[0]) + "_" + str(word[1]) + "\n") for word in words)
                    mwdata = mwpreprocess(
                        absolute_folder_path+'/'+file_name, combined=False, lowercase=False)
                data = data+mwdata
                with open(output_file_path, "w") as f:
                    f.write(data)
