# config: utf-8

# # 信号処理シンポジウム分析

# モジュール
import pandas as pd
import urllib as ul

# ベースURL の設定
base_url = 'http://www.ieice.org/ess/sip/symp/'

# <br /> の置き換え
brstr = '@'

# 対象年の設定
term = range(2008,2018)

# class の定義
class SipSymp:

    def __init__(self, url):
        # HTMLの読み込みと改行タグの置換
        fp = ul.request.urlopen(url)
        html = fp.read()
        html = html.replace(b'<br />', brstr.encode())
        fp.close()

        # プログラムの抽出
        tables = pd.read_html(html)
        nTables = len(tables)

        # タイトル・著者リストの抽出（評価１年目）
        nRows = len(tables[1])
        if nRows > 1:
            ser = tables[1].iloc[1:,1]
        else:
            ser = pd.Series([])

        # タイトル・著者リストの結合（評価２年目以降）
        for iTable in range(2,nTables):
            nRows = len(tables[iTable])
            if nRows > 1:
                ser = pd.concat([ser,tables[iTable].iloc[1:,1]],axis=0)

        # フィールドの設定
        self.titles = ser.str.split(brstr,expand=True).iloc[:,0]

# main関数
def main():
    for idx, year in enumerate(term):
        # URL の設定
        url = base_url + str(year) + '/?cmd=program'

        # SIPシンポオブジェクトのインスタンス化
        sipSymp = SipSymp(url)

        #
        titles = sipSymp.titles
        # 年度の追加とDataFrame化
        # インデックスの振り直し
        titles2 = titles.reset_index(drop=True)
        print(url)
        print(titles2.head())

if __name__ == '__main__':
    main()
