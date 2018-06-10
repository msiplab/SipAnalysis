import pandas as pd
import urllib as ul

# class の定義
class SipSymp:
    # ベースURL の設定
    __base_url = 'http://www.ieice.org/ess/sip/symp/'
    # <br /> の置き換え
    __brstr = '@'

    def __init__(self, year):
        self.__year = year
        # URL の設定
        self.__url = self.__base_url + str(self.__year) + '/?cmd=program'
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
        self.__titles = self.__ser.str.split(self.__brstr,expand=True).iloc[:,0]
        return self.__titles


    @property
    def authors(self):
        # フィールドの設定
        self.__authors = self.__ser.str.split(self.__brstr,expand=True).iloc[:,1]
        return self.__authors

    @property
    def url(self):
        return self.__url

    @classmethod
    def titlesDuring(cls,term):
        # 対象年度内のタイトル表
        df = pd.DataFrame({'Title': [], 'Year': []})
        for year in term:
            # SIPシンポオブジェクトのインスタンス化
            sipSymp = SipSymp(year)
            # タイトルの取得
            titles = sipSymp.titles.reset_index(drop=True)
            nTitles = len(titles)
            # 年度の数列化
            years = pd.Series([ year for idx in range(nTitles)],dtype='int32')
            #
            table = pd.concat({'Title': titles, 'Year': years}, axis=1)
            df = pd.concat([df, table],axis=0)
            # インデックスのリセット
            df = df.reset_index(drop=True)
            df['Year'] = df['Year'].astype(int)
        return df
