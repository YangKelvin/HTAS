from MyAnalyzer.analyzer import Analyzer as ptt_analyzer
import json
import jieba
from collections import defaultdict

# 取得欲分析的 json 檔案
DATA_LAYER = './HTAS/data/'
BOARD = 'PC_Shopping'
DATE = '2019-08-27'
JSON_FILE_NAME = BOARD + '(' + DATE + ').json'
FILE_PATH =DATA_LAYER + JSON_FILE_NAME

# 打開該 json 檔
posts = {}
with open(FILE_PATH, 'r', encoding='utf-8') as read_file:
    posts = json.load(read_file)['articles']

# 搜集每篇文章的詞，並記錄文章推文數
words = []
scores = []
for post in posts:  # 取得每篇文章
    d = defaultdict(int)
    content = post['content']
    message_count = post['message_count']
    score = message_count['push'] - message_count['boo']
    for l in content.split('\n'):
        # print(l)
        if l:
            for w in jieba.cut(l):
                d[w] += 1
        if len(d) > 0:
            words.append(d)
            scores.append(1 if score > 0 else 0)

# 分析每篇文章下的回覆
c_words = []
c_scores = []
for post in posts:
    for message in post['messages']:
        l = message['push_content'].strip()
        
        # 取得留言的狀況
        message_score = 0
        push_tag = message['push_tag']
        if (push_tag == '推'):
            message_score = 1
        elif (push_tag == '噓'):
            message_score = -1
        
        # 若推文狀況不為 neutral
        if l and message_score != 0:
            d = defaultdict(int)
            for w in jieba.cut(l):
                d[w] += 1
            if len(d) > 0:
                c_scores.append(1 if message_score > 0 else 0)
                c_words.append(d)

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC

# convert to vectors
dvec = DictVectorizer()
tfidf = TfidfTransformer()
X = tfidf.fit_transform(dvec.fit_transform(words))

c_dvec = DictVectorizer()
c_tfidf = TfidfTransformer()
c_X = c_tfidf.fit_transform(c_dvec.fit_transform(c_words))

svc = LinearSVC()
svc.fit(X, scores)

c_svc = LinearSVC()
c_svc.fit(c_X, c_scores)

def display_top_features(weights, names, top_n, select=abs):
    top_features = sorted(zip(weights, names), key=lambda x: select(x[0]), reverse=True)[:top_n]
    top_weights = [x[0] for x in top_features]
    top_names = [x[1] for x in top_features]

    print(top_features)
    print(top_weights)
    print(top_names)

    # fig, ax = plt.subplots(figsize=(10,8))
    # ind = np.arange(top_n)
    # bars = ax.bar(ind, top_weights, color='blue', edgecolor='black')
    # for bar, w in zip(bars, top_weights):
    #     if w < 0:
    #         bar.set_facecolor('red')

    # width = 0.30
    # ax.set_xticks(ind + width)
    # ax.set_xticklabels(top_names, rotation=45, fontsize=12, fontdict={'fontname': 'Droid Sans Fallback', 'fontsize':12})

# 貼文負向詞彙
display_top_features(svc.coef_[0], dvec.get_feature_names(), 5)

# 貼文正向詞彙
display_top_features(svc.coef_[0], dvec.get_feature_names(), 5 , select=lambda x: x)