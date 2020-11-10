import python_preprocessor
import dict_processor
import analysis
import model
import importlib
import os

if os.path.exists('cfg_modified.py'):
    from cfg_modified import config
else:
    from cfg_default import config

RUST_SUPPORTED = False

corpus_spec = importlib.util.find_spec("corpus_processor")
RUST_SUPPORTED = corpus_spec is not None

if RUST_SUPPORTED:
    import rust_preprocessor


def preprocess_helper(combined=False, mode='train', lowercase=False):
    if mode == 'train':
        input_folder_path = config['train_folder_path']
    else:
        input_folder_path = config['test_folder_path']

    output_folder_path = config['output_folder_path']

    if RUST_SUPPORTED:
        rust_preprocessor.preprocess(
            input_folder_path, output_folder_path, combined, mode, lowercase)
    else:
        python_preprocessor.preprocess(
            input_folder_path, output_folder_path, combined, mode, lowercase)


def dictprocess_helper(combined=False, mode='train', file_mode='json'):
    output_folder_path = config['output_folder_path']
    dict_processor.dictprocess(output_folder_path, combined, mode, file_mode)


def gettoppers_helper(combined=False, mode='train', file_mode='json'):
    output_folder_path = config['output_folder_path']
    analysis.gettoppers(output_folder_path, combined, mode, file_mode)


def plotter_helper(mode='train'):
    output_folder_path = config['output_folder_path']
    analysis.plotgraphs(output_folder_path, mode)


def model_helper(combined=False, file_mode='json'):
    output_folder_path = config['output_folder_path']
    model.generate_model(output_folder_path, combined, file_mode)


def checkAttributes(mode, file_mode):
    if mode != 'train' and mode != 'test':
        raise AttributeError('Mode not supported.')

    if file_mode != 'json' and file_mode != 'txt' and file_mode != 'pickle':
        raise AttributeError('File mode not supported.')


if __name__ == '__main__':

    ### BEGIN EDITABLE ###
    # Change the values of these variables
    lowercase = False
    combined = False
    mode = 'train'
    file_mode = 'json'
    ### END EDITABLE ###

    checkAttributes(mode, file_mode)

    ### BEGIN EDITABLE ###
    # Comment any of these as per your needs
    preprocess_helper(combined, mode, lowercase)
    dictprocess_helper(combined, mode, file_mode)
    # gettoppers_helper(combined, mode, file_mode)
    # plotter_helper(mode)
    model_helper(combined, file_mode)
    ### END EDITABLE ###
