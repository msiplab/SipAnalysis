# config: utf-8

# # 信号処理シンポジウム分析

# モジュール
import pandas as pd
from sipsymp import SipSymp

# 対象年度の設定
term = range(2008,2018)

# 期間内の論文タイトル
df = SipSymp.titlesDuring(term)

#
df
