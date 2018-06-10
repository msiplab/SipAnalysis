# config: utf-8

# # 信号処理シンポジウム分析

# モジュール
import pandas as pd
from sipsymp import SipSymp

# 対象年度の設定
term = range(2008,2018)

# 対象年度内のタイトル表
df = pd.DataFrame({'Title': [], 'Year': []})
for idx, year in enumerate(term):
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
df = df.reset_index(drop=True)

#
