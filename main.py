import python_preprocessor
import rust_preprocessor
from cfg import config


def preprocess_helper(language='Rust', combined=False, mode='train', lowercase=False):
    if mode != 'train' and mode != 'test':
        raise AttributeError('Mode not supported.')

    if language != 'Rust' and language != 'Python':
        raise AttributeError('Language not supported.')

    if mode == 'train':
        input_folder_path = config['train_folder_path']
    else:
        input_folder_path = config['test_folder_path']

    output_folder_path = config['output_folder_path']

    if language == 'Rust':
        rust_preprocessor.preprocess(
            input_folder_path, output_folder_path, combined, mode, lowercase)
    else:
        python_preprocessor.preprocess(
            input_folder_path, output_folder_path, combined, mode, lowercase)


if __name__ == '__main__':
    preprocess_helper()
