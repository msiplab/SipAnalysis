import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from spsconf import rep_words, stop_words

class SpsConfWordCloud:
    def __init__(self):
        self.__wdcObj = WordCloud(background_color='white',
                      width=900,
                      height=500,
                      stopwords=set(stop_words))

    def generate(self,ser,wdcfile=''):
        ser = ser.str.lower()
        nTitles = len(ser)
        words = []
        for idx in range(nTitles):
            title = ser.iloc[idx]
            tokens = title.split()
            if len(tokens) > 0:
                words.extend([word+' ' for word in tokens if word != ''])
        text = ' '.join(words)

        # ワードの置換
        for idx in range(len(rep_words)):
            text = re.sub(rep_words[idx][0]+'\s', rep_words[idx][1]+' ', text)

        # ワードクラウドの生成
        wordcloud = self.__wdcObj.generate(text)

        # ワードクラウドの描画
        plt.figure(figsize=(20, 16))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.tight_layout()
        if wdcfile != '':
            plt.savefig(wdcfile)
        plt.show()
