import re
import matplotlib.pyplot as plt
from janome.charfilter import *
from janome.analyzer import Analyzer
from janome.tokenizer import Tokenizer
from janome.tokenfilter import *
from wordcloud import WordCloud
from sipsymp import rep_words, stop_words

class SipWordCloud:

    def __init__(self):

        # 日本語が使えるように日本語フォントの設定
        fpath = 'C:\Windows\Fonts\SourceHanCodeJP-Regular.otf'

        # 文字フィルタ
        char_filters = [UnicodeNormalizeCharFilter(),
                        RegexReplaceCharFilter('\(',''),
                        RegexReplaceCharFilter('\)','')]
        # トークンフィルタ
        token_filters = [CompoundNounFilter(),
                        POSKeepFilter(['名詞', '動詞', '形容詞', '副詞'])]

        # 形態素解析オブジェクト生成
        tokenizer = Tokenizer('sipudic.csv', udic_type='simpledic', udic_enc='utf8')
        self.__analyzer = Analyzer(char_filters, tokenizer, token_filters)

        # ワードクラウトオブジェクト生成
        self.__wdcObj = WordCloud(background_color='white',
                      font_path=fpath,
                      width=900,
                      height=500,
                      stopwords=set(stop_words))


    def generate(self,df,wdcfile=''):
        # タイトルの分析
        tokens_list = []
        for title in df.loc[:,'Title']:
            title_ = [token.base_form for token in self.__analyzer.analyze(title)]
            if len(title_) > 0:
                tokens_list.append(title_)

        # 単語のテキスト化
        words = []
        for title in tokens_list:
            words.extend([word+' ' for word in title if word != ''])
        text = ' '.join(words)

        # ワードの和訳
        for idx in range(len(rep_words)):
            text = re.sub(rep_words[idx][0]+'\s', rep_words[idx][1]+' ', text)

        # ワードクラウドの生成
        wordcloud = self.__wdcObj.generate(text)

        # ワードクラウドの描画
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.tight_layout()
        if wdcfile != '':
            plt.savefig(wdcfile)
        plt.show()
