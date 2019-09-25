from ANALYZER_CONFIG import *
from MyAnalyzer.analyzer import Analyzer as ptt_analyzer
import json
# import jieba
from collections import defaultdict
import datetime
from os import listdir
from os.path import isfile

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC

analyzer = ptt_analyzer()

# 取得欲分析的資料
data = analyzer.get_analysis_data(BOARD_NAME, DATE_START, DATE_END)

# 分析
# ---------------------------------------------------------
words = []
scores = []
for post in data:  # 取得每篇文章
    # print(post)
    try:
        content = post['content']
        # print(content)
        message_count = post['message_count']
        score = message_count['push'] - message_count['boo']
        d = analyzer.jieba_cut(content)
        if (len(d) > 0):
            words.append(d)
            scores.append(1 if score > 0 else 0)
    except:
        print (post)

# print(words[0]['和'])

c_words = []
c_scores = []
for post in data:
    try:
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
                d = analyzer.jieba_cut(l)
                if (len(d) > 0):
                    c_words.append(d)
                    c_scores.append(1 if message_score > 0 else 0)
    except:
        print(post)

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

# 貼文負向詞彙
display_top_features(svc.coef_[0], dvec.get_feature_names(), 5)

# 貼文正向詞彙
display_top_features(svc.coef_[0], dvec.get_feature_names(), 5 , select=lambda x: x)
# ---------------------------------------------------------