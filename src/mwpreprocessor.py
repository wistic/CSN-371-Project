from bs4 import BeautifulSoup
import bs4


def mwpreprocess(path):
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
