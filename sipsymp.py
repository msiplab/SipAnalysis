import pandas as pd
import urllib as ul

# class の定義
class SipSymp:
    # ベースURL の設定
    __base_url = 'http://www.ieice.org/ess/sip/symp/'
    # <br /> の置き換え
    __brstr = '@'

    def __init__(self, year):
        self.__year = year
        # URL の設定
        self.__url = self.__base_url + str(self.__year) + '/?cmd=program'
        # HTMLの読み込みと改行タグの置換
        fp = ul.request.urlopen(self.__url)
        html = fp.read()
        html = html.replace(b'<br />', self.__brstr.encode())
        fp.close()
        # プログラムの抽出
        tables = pd.read_html(html)
        nTables = len(tables)
        # タイトル・著者リストの抽出（評価１年目）
        nRows = len(tables[1])
        if nRows > 1:
            self.__ser = tables[1].iloc[1:,1].str.strip()
        else:
            self.__ser = pd.Series([])
        # タイトル・著者リストの結合（評価２年目以降）
        for iTable in range(2,nTables):
            nRows = len(tables[iTable])
            if nRows > 1:
                self.__ser = pd.concat([self.__ser,tables[iTable].iloc[1:,1]],axis=0).str.strip()


    @property
    def titles(self):
        self.__titles = self.__ser.str.split(self.__brstr,expand=True).iloc[:,0]
        return self.__titles


    @property
    def authors(self):
        # フィールドの設定
        self.__authors = self.__ser.str.split(self.__brstr,expand=True).iloc[:,1]
        return self.__authors

    @property
    def url(self):
        return self.__url

    @classmethod
    def titlesDuring(cls,term):
        # 対象年度内のタイトル表
        df = pd.DataFrame({'Title': [], 'Year': []})
        for year in term:
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
            # インデックスのリセット
            df = df.reset_index(drop=True)
            df['Year'] = df['Year'].astype(int)
        return df


rep_words = [
    ['[Ii]mages?', u'画像'],
    ['[Nn]oise', u'ノイズ'],
    ['[Aa]daptive', u'適応'],
    ['[Ff]iltering', u'フィルタリング'],
    ['[Ff]ilters?', u'フィルタ'],
    ['[Ss]ignals?', u'信号'],
    ['[Kk]ernel', u'カーネル'],
    ['[Pp]rojection', u'射影'],
    ['[Ee]stimation', u'推定'],
    ['[Ss]ystems?', u'システム'],
    ['[Tt]echniques?', u'技術'],
    ['[Aa]rray', u'アレー'],
    ['[Aa]lgorithms?', u'アルゴリズム'],
    ['[Ss]parse', u'スパース'],
    ['[Ll]earning', u'学習'],
    ['[Ff]requency', u'周波数'],
    ['[Ii]dentification',u'同定'],
    ['[Aa]nalysis', u'分析'],
    ['[Ll]inear', u'線形'],
    ['[Oo]ptimization', u'最適化'],
    ['[Tt]ime', u'時間'],
    ['[Pp]hase',u'位相'],
    ['[Cc]hannel', u'チャネル'],
    ['[Tt]otal.[Vv]ariation', u'全変動'],
    ['[Dd]ata', u'データ'],
    ['[Ss]ource', u'信号源'],
    ['[Rr]egularization', u'正則化'],
    ['[Ss]eparation', u'分離'],
    ['[Pp]rocessing', u'処理'],
    ['[Dd]etection', u'検出'],
    ['[Ff]eedback', u'フィードバック'],
    ['[Bb]lind', u'ブラインド'],
    ['[Ff]orward.[Bb]ackward', u'前方後方'],
    ['[Cc]onstraint', u'制約'],
    ['[Cc]onstrained', u'制約'],
    ['[Aa]pplication', u'応用'],
    ['[Mm]ultiple', u'多'],
    ['[Ss]ingle', u'単'],
    ['[Aa]lternating', u'交互'],
    ['[Bb]ackword.[Ss]plitting', u'後方分離'],
    ['[Ss]peech', u'音声'],
    ['[Ff]requency', u'周波数'],
    ['[Tt]ransforms?', u'変換'],
    ['[Ss]pectral', u'スペクトル'],
    ['[Ss]ubspace', u'部分空間'],
    ['[Ss]pace',u'空間'],
    ['[Cc]olor', u'色'],
    ['[Gg]eneralized', u'一般化'],
    ['[Pp]erformance', u'性能'],
    ['[Dd]irectional', u'方向性'],
    ['[Dd]irection', u'方向'],
    ['[Ee]fficient', u'効率的'],
    ['[Ii]mprovement', u'改善'],
    ['[Cc]anceller', u'キャンセラ'],
    ['[Aa]coustic', u'音響'],
    ['[Cc]omponent', u'成分'],
    ['[Cc]ancellation', u'キャンセル'],
    ['[Dd]ecomposition',u'分解'],
    ['[Ss]plitting', u'分離'],
    ['[Ee]nhancement', u'強調'],
    ['[Ee]cho', u'エコー'],
    ['[Rr]ecognition', u'認識'],
    ['[Gg]radient',u'勾配'],
    ['[Cc]lassification',u'分類'],
    ['[Bb]anks?', u'バンク'],
    ['[Ss]moothing',u'平滑化'],
    ['[Tr]acking',u'追跡'],
    ['[Rr]estoration',u'復元'],
    ['[Ee]xtraction',u'抽出'],
    ['[Mm]atrix',u'行列'],
    ['[Mm]atrices',u'行列'],
    ['[Ff]actorization',u'因子分解'],
    ['[Dd]omain',u'領域'],
    ['[Gg]raph',u'グラフ'],
    ['[Cc]onvergence',u'収束'],
    ['[Pp]roximal', u'近接'],
    ['[Rr]ecovery',u'復元'],
    ['[Rr]obust',u'ロバスト'],
    ['[Rr]ank',u'ランク'],
    ['[Mm]inimization',u'最小化'],
    ['[Dd]igital',u'デジタル'],
    ['[Ll]east',u'最小'],
    ['[Bb]rain',u'脳'],
    ['[Cc]onvex',u'凸'],
    ['ECHO',u'エコー'],
    ['[Tt]wo.[Dd]imensional',u'二次元'],
    ['[Ss]upervised',u'教師あり'],
    ['[Ss]ign',u'符号'],
    ['[Ii]nterpolation',u'補間'],
    ['[Uu]nwrapping',u'アンラッピング'],
    ['[Rr]esolution',u'解像度'],
    ['[Ss]pline',u'スプライン'],
    ['[Aa]pplications?',u'応用'],
    ['[Dd]emosaicing',u'デモザイク'],
    ['[Ee]dge',u'エッジ'],
    ['[Cc]ovariance',u'共分散'],
    ['[Pp]arameter',u'パラメータ'],
    ['[Mm]odeling',u'モデリング'],
    ['[Ss]ensor',u'センサ'],
    ['[Ii]mplementation',u'実装'],
    ['[Nn]on.?[Nn]egative',u'非負'],
    ['[Rr]obot',u'ロボット'],
    ['[Mm]achie',u'機械'],
    ['[Vv]ocoder',u'ボコーダー'],
    ['CLUSTERING',u'クラスタリング'],
    ['[Vv]ideo',u'映像'],
    ['[Vv]ariable',u'可変'],
    ['[Dd]iffusion',u'拡散'],
    ['[Ee]nvelope',u'包絡線'],
    ['INTERFERENCE',u'干渉'],
    ['[Cc]olored',u'有色'],
    ['[Mm]otion',u'動き'],
    ['[Ss]tereo',u'ステレオ'],
    ['[Ee]stimating',u'推定'],
    ['[Aa]pproach',u'アプローチ'],
    ['[Ss]uppression',u'抑圧'],
    ['[Ss]uppressor',u'抑圧器'],
    ['[Ee]rror',u'エラー'],
    ['[Mm]ulti',u'多'],
    ['[Aa]utomatic',u'自動'],
    ['[Cc]orrection',u'訂正'],
    ['[Gg]ain',u'ゲイン'],
    ['[Mm]odel',u'モデル'],
    ['[Ss]eparable',u'可分離'],
    ['[Nn]on',u'非'],
    ['[Mm]usic',u'音楽'],
    ['[Hh]igh',u'高'],
    ['[Ll]ow',u'低'],
    ['[Cc]ondition',u'条件'],
    ['[Cc]onstant',u'一定'],
    ['STRUCTURE',u'構造']
    ]

stop_words = [
    u'チュートリアル講演：',
    u'基づく',
    u'与える',
    u'用いる',
    u'提案',
    u'ため',
    u'する',
    u'一検討',
    u'検討',
    u'もつ',
    u'持つ',
    u'考慮',
    u'利用',
    u'研究',
    u'一考察',
    u'含む',
    u'れる',
    u'ある',
    u'従う',
    u'考察',
    u'新しい',
    'for',
    'of',
    'the',
    'on',
    'with',
    'Using',
    'Based',
    'An',
    'by',
    'in',
    'to',
    'from',
    'and',
    'Method',
    'New',
    'Problem',
    'Its',
    'Novel'
    ]
