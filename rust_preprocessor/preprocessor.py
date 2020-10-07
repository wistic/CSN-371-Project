import corpus_processor
import os

def dirWalk(source_path, output_path, file_list, combined=False):
    listing = os.listdir(source_path)
    for entry in listing:
        absolute_path = source_path+entry
        if os.path.isdir(absolute_path):
            if absolute_path[-1] != '/':
                absolute_path = absolute_path+'/'
            if combined:
                dirWalk(absolute_path, output_path, file_list, combined)
            else:
                new_output_path = output_path+entry+'_preprocessed/'
                if not (os.path.exists(new_output_path) and os.path.isdir(new_output_path)):
                    os.mkdir(new_output_path)
                dirWalk(absolute_path, new_output_path, file_list, combined)
        else:
            if absolute_path.split('.')[-1] == 'xml':
                if combined:
                    file_entry = (source_path, entry, output_path)
                else:
                    new_output_path = output_path + \
                        entry.split('.')[0]+'_preprocessed.txt'
                    file_entry = (source_path, entry, new_output_path)
                file_list.append(file_entry)
    return file_list


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
        file_list = dirWalk(input_folder_path,
                            output_file_path, file_list, combined=True)

        source_file_list=[(file_entry[0]+file_entry[1]) for file_entry in file_list]
        corpus_processor.process(source_file_list,output_file_path,lowercase)

    else:
        if mode == 'train':
            output_folder_path = output_folder_path + 'Train-corpus_preprocessed/'
        else:
            output_folder_path = output_folder_path + 'Test-corpus_preprocessed/'
        if not (os.path.exists(output_folder_path) and os.path.isdir(output_folder_path)):
            os.mkdir(output_folder_path)
        file_list = dirWalk(input_folder_path,
                            output_folder_path, file_list, combined=False)
        for file_entry in file_list:
            output_file_path = file_entry[2]
            source_file_list=[file_entry[0]+file_entry[1]]
            corpus_processor.process(source_file_list,output_file_path,lowercase)
