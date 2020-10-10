import python_preprocessor
import dict_processor
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
    if mode != 'train' and mode != 'test':
        raise AttributeError('Mode not supported.')

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
    if mode != 'train' and mode != 'test':
        raise AttributeError('Mode not supported.')

    if file_mode != 'json' and file_mode != 'txt' and file_mode != 'pickle':
        raise AttributeError('File mode not supported.')

    output_folder_path = config['output_folder_path']

    dict_processor.dictprocess(output_folder_path, combined, mode, file_mode)


if __name__ == '__main__':
    preprocess_helper()
    dictprocess_helper()
