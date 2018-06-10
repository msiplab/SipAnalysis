# config: utf-8

# # 信号処理シンポジウム分析

# モジュール
import os
import pandas as pd
from sipsymp import SipSymp

# 対象年度の設定
syear = 2008
eyear = 2017

# 期間内の論文タイトル
path = './siprep{0}_{1}.csv'.format(syear,eyear)
if os.path.exists(path):
    print('{0} file exists.'.format(path))
    df = pd.read_csv(path)
else:
    print('{0} file doesn\'t exist.'.format(path))
    term = range(syear,eyear)
    df = SipSymp.titlesDuring(term)
    # CSVへの書き出し
    df.to_csv(path)

#
df
