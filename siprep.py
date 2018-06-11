# config: utf-8

# # 信号処理シンポジウム分析
#
# 考サイト
# http://www.dskomei.com/entry/2018/04/11/001944
#

# モジュール
import os
import pandas as pd
from sipsymp import SipSymp
from sipwdc import SipWordCloud

# 対象年度の設定
syear = 2008
eyear = 2017

# 期間内の論文タイトル
path = './siprep{0}_{1}.csv'.format(syear,eyear)
if os.path.exists(path):
    print('{0} file exists.'.format(path))
    df = pd.read_csv(path,index_col=0)
else:
    print('{0} file doesn\'t exist.'.format(path))
    term = range(syear,eyear)
    df = SipSymp.titlesDuring(term)
    # CSVへの書き出し
    df.to_csv(path)

# SIPワードクラウドオブジェクトの生成
swc = SipWordCloud()

# 2008-2012のタイトルワードクラウド
df2008_2012 = df.loc[df.loc[:,'Year']<2013].reset_index(drop=True)
swc.generate(df2008_2012,'sipwdc2008_2012.png')

# 2013-2017のタイトルワードクラウド
df2013_2017 = df.loc[df.loc[:,'Year']>2012].reset_index(drop=True)
swc.generate(df2013_2017,'sipwdc2013_2017.png')
