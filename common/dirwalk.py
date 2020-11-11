import os
from multipledispatch import dispatch


@dispatch(str, str, list, bool)
def dirWalk(source_path, output_path, file_list, combined):
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


@dispatch(str, str, list, str)
def dirWalk(source_path, output_path, file_list, file_mode):
    listing = os.listdir(source_path)
    for entry in listing:
        absolute_path = source_path+entry
        if os.path.isdir(absolute_path) and entry.split('_')[1] == 'preprocessed':
            if absolute_path[-1] != '/':
                absolute_path = absolute_path+'/'
            new_output_path = output_path+entry.split('_')[0]+'_dictionary/'
            if not (os.path.exists(new_output_path) and os.path.isdir(new_output_path)):
                os.mkdir(new_output_path)
            dirWalk(absolute_path, new_output_path, file_list, file_mode)
        else:
            parts = entry.split('.')
            if parts[1] == 'txt' and parts[0].split('_')[1] == 'preprocessed':
                new_output_path = output_path + \
                    parts[0].split('_')[0]+'_dictionary.'+file_mode
                file_entry = (absolute_path, new_output_path)
                file_list.append(file_entry)
    return file_list


@dispatch(str, list, str)
def dirWalk(source_path, file_list, file_mode):
    listing = os.listdir(source_path)
    for entry in listing:
        absolute_path = source_path+entry
        if os.path.isdir(absolute_path) and entry.split('_')[1] == 'dictionary':
            if absolute_path[-1] != '/':
                absolute_path = absolute_path+'/'
            dirWalk(absolute_path, file_list, file_mode)
        else:
            parts = entry.split('.')
            if parts[1] == file_mode and parts[0].split('_')[1] == 'dictionary':
                file_list.append(absolute_path)
    return file_list
