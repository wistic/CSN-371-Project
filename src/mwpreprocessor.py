from bs4 import BeautifulSoup
import bs4
import os


def mwpreprocess(path, combined=False):
    if combined:
        combined_mwdata = ""
        train_folders = os.listdir(path)
        for folder in train_folders:
            source_folder_path = path+folder+'/'
            file_list = os.listdir(source_folder_path)
            for file_name in file_list:
                with open(source_folder_path+file_name, 'r') as f:
                    xml_string = f.read()
                soup = BeautifulSoup(xml_string, 'xml')
                mwdata = ""
                for tag in soup.find_all('mw'):
                    mw = ""
                    for child in tag.contents:
                        if isinstance(child, bs4.element.Tag):
                            mw = mw+child.text
                    mw = mw.strip()+'_'+tag['c5']
                    mwdata = mwdata+mw+'\n'
                combined_mwdata = combined_mwdata+mwdata
        return combined_mwdata.strip('\n')
    else:
        with open(path, 'r') as f:
            xml_string = f.read()
        soup = BeautifulSoup(xml_string, 'xml')
        mwdata = ""
        for tag in soup.find_all('mw'):
            mw = ""
            for child in tag.contents:
                if isinstance(child, bs4.element.Tag):
                    mw = mw+child.text
            mw = mw.strip()+'_'+tag['c5']
            mwdata = mwdata+mw+'\n'
        return mwdata.strip('\n')
