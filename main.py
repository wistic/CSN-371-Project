import os
import importlib

from model import generate_model, tag_words
from analysis import gettoppers, plotgraphs
from dict_processor import dictprocess
from common import *
import python_preprocessor

if os.path.exists('cfg_modified.py'):
    from cfg_modified import config
else:
    from cfg_default import config

RUST_SUPPORTED = False

corpus_spec = importlib.util.find_spec("corpus_processor")
RUST_SUPPORTED = corpus_spec is not None

if RUST_SUPPORTED:
    import rust_preprocessor

output_folder_path = config['output_folder_path']


def preprocess_helper(combined, mode, lowercase):
    if mode == 'train':
        input_folder_path = config['train_folder_path']
    else:
        input_folder_path = config['test_folder_path']

    if RUST_SUPPORTED:
        rust_preprocessor.preprocess(
            input_folder_path, output_folder_path, combined, mode, lowercase)
    else:
        python_preprocessor.preprocess(
            input_folder_path, output_folder_path, combined, mode, lowercase)


def checkAttributes(mode, file_mode, matrix_mode):
    if mode != 'train' and mode != 'test':
        raise AttributeError('Mode not supported.')

    if file_mode != 'json' and file_mode != 'txt' and file_mode != 'pickle':
        raise AttributeError('File mode not supported.')

    if matrix_mode != 'json' and matrix_mode != 'csv':
        raise AttributeError('Matrix mode not supported')


if __name__ == '__main__':

    ### BEGIN EDITABLE ###
    # Change the values of these variables
    lowercase = False
    combined = False
    mode = 'train'
    file_mode = 'json'
    matrix_mode = 'csv'
    ### END EDITABLE ###

    checkAttributes(mode, file_mode, matrix_mode)

    ### BEGIN EDITABLE ###
    # Comment any of these as per your needs
    preprocess_helper(combined, 'train', lowercase)
    dictprocess(output_folder_path, combined, 'train', file_mode)
    gettoppers(output_folder_path, combined, 'train', file_mode)
    plotgraphs(output_folder_path, 'train')

    preprocess_helper(combined, 'test', lowercase)
    dictprocess(output_folder_path, combined, 'test', file_mode)

    generate_model(output_folder_path, combined, file_mode)
    tag_words(output_folder_path, combined, file_mode)
    generate_confusion_matrix(output_folder_path, matrix_mode)
    ### END EDITABLE ###
