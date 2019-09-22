from MyAnalyzer.analyzer import Analyzer as ptt_analyzer
import json
import os


# print(os.getcwd())

analyzer = ptt_analyzer()

# 取得欲分析的 json 檔案
DATA_LAYER = './HTAS/data/'
BOARD = 'PC_Shopping'
DATE = '2019-08-27'
JSON_FILE_NAME = BOARD + '(' + DATE + ').json'
FILE_PATH =DATA_LAYER + JSON_FILE_NAME
# print(FILE_PATH)

# 打開該 json 檔
articles = {}
with open(FILE_PATH, 'r', encoding='utf-8') as read_file:
    articles = json.load(read_file)['articles']

# print(articles[0]['messages'][0]) # 第一篇文章的第一個回覆

# 分析後的結果
result = []

# 試著分析第一篇文章
# article = articles[1]
# tmp_result = analyzer.analysis_article_push(article)

# result.append(tmp_result)

for article in articles:
    result.append(analyzer.analysis_article_push(article))


print(result[0])
print(articles[0]["message_count"])
