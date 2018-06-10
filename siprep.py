# config: utf-8

# # 信号処理シンポジウム分析

# モジュール
import pandas as pd
from sipsymp import SipSymp

# 対象年の設定
term = range(2008,2018)

for idx, year in enumerate(term):
    # SIPシンポオブジェクトのインスタンス化
    sipSymp = SipSymp(year)
    #
    titles = sipSymp.titles
    # 年度の追加とDataFrame化
    # インデックスの振り直し
    titles2 = titles.reset_index(drop=True)
    print(sipSymp.url)
    print(titles2)
