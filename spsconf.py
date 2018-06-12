import bs4
import pandas as pd

# class の定義
class SpsConf:

    def __init__(self, file = './SessionIndex.html'):
        with open(file, 'r', encoding='utf-8') as fp:
            html = fp.read()
            soup = bs4.BeautifulSoup(html,'html.parser')
            elems = soup.select('p')
            list = []
            for elem in elems:
                list.append(elem.getText())
            df = pd.Series(list).str.split(': ', 1, expand=True)
            table = pd.concat([df[0],df[1].str.split('\n', expand=True)],axis=1)
            table.columns = ['Session','Title','Authors']
            self.__table = table

    @property
    def titles(self):
        self.__titles = self.__table.loc[:,'Title']
        return self.__titles

    @property
    def authors(self):
        self.__authors = self.__table.loc[:,'Authors']
        return self.__authors

rep_words = []
stop_words = [
    'and',
    'of',
    'in',
    'with',
    'the',
    'for',
    'via',
    'on',
    'using',
    'from',
    'based',
    'an',
    'by'
    ]
