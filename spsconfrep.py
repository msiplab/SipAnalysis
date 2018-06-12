# config: utf-8

# # SPS Conf.
#
#

# モジュール
import os
import pandas as pd
from spsconf import SpsConf
from spsconfwdc import SpsConfWordCloud

# USBに入っている SessionIndex.htmlを
# SessionIndexYYYY.html のように名前を変えて保存
# (YYYY の部分は西暦)
year = 2018
sessionfile = 'SessionIndex{0}.html'.format(year)

# 期間内の論文タイトル
path = './spsconfrep{0}.csv'.format(year)
if os.path.exists(path):
    print('{0} file exists.'.format(path))
    df = pd.read_csv(path,index_col=0)
    ser = df.iloc[:,0]
else:
    print('{0} file doesn\'t exist.'.format(path))
    ser = SpsConf(file=sessionfile).titles
    ser.to_csv(path)

# SIPワードクラウドオブジェクトの生成
swc = SpsConfWordCloud()

# タイトルワードクラウド
swc.generate(ser,wdcfile='spsconf{0}.png'.format(year))
