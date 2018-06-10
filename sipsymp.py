import pandas as pd
import urllib as ul

# class の定義
class SipSymp:
    # ベースURL の設定
    __base_url = 'http://www.ieice.org/ess/sip/symp/'
    # <br /> の置き換え
    __brstr = '@'

    def __init__(self, year):
        # URL の設定
        self.__url = self.__base_url + str(year) + '/?cmd=program'
        # HTMLの読み込みと改行タグの置換
        fp = ul.request.urlopen(self.__url)
        html = fp.read()
        html = html.replace(b'<br />', self.__brstr.encode())
        fp.close()
        # プログラムの抽出
        tables = pd.read_html(html)
        nTables = len(tables)
        # タイトル・著者リストの抽出（評価１年目）
        nRows = len(tables[1])
        if nRows > 1:
            self.__ser = tables[1].iloc[1:,1].str.strip()
        else:
            self.__ser = pd.Series([])
        # タイトル・著者リストの結合（評価２年目以降）
        for iTable in range(2,nTables):
            nRows = len(tables[iTable])
            if nRows > 1:
                self.__ser = pd.concat([self.__ser,tables[iTable].iloc[1:,1]],axis=0).str.strip()


    @property
    def titles(self):
        # フィールドの設定
        self.__titles = self.__ser.str.split(self.__brstr,expand=True).iloc[:,0]
        return self.__titles

    @property
    def url(self):
        return self.__url
