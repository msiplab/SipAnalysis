#

# %% モジュール
import pandas as pd

# %% URL の設定
year = '2017'
url = 'http://www.ieice.org/ess/sip/symp/' + year + '/?cmd=program'

# %% プログラムの抽出,
tables = pd.read_html(url)
nTables = len(tables)

# %% タイトル・著者リストの抽出
nRows = len(tables[1])
if nRows > 1:
    ser = tables[1].iloc[1:,1]

# %% タイトル・著者リストの結合,
for iTable in range(2,nTables):
    nRows = len(tables[iTable])
    if nRows > 1:
        ser = pd.concat([ser,tables[iTable].iloc[1:,1]],axis=0)

# %% インデックスの振り直し,
ser.reset_index(drop=True).head()
