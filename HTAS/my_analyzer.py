from MyAnalyzer.analyzer import Analyzer
from PttWebCrawler.crawler import PttWebCrawler
from HTAS.config import *
import json

analyzer = Analyzer()
crawler = PttWebCrawler()

# 分析結果
svc, c_svc, dvec, c_dvec= analyzer.get_word_vector(ML_DATA_LAYER)

# 儲存分析結果
def store_MLResult(weights, names, file_name, select=abs):
    top_features = sorted(zip(weights, names), key=lambda x: select(x[0]), reverse=True)[:]
    top_weights = [x[0] for x in top_features]
    top_names = [x[1] for x in top_features]
    data_count = len(top_features)
    datas = []
    # print(len(top_features))
    for i in range(data_count):
        data = {
            "name" : top_names[i],
            "weights" : top_weights[i]
        } 
        datas.append(data)
    with open(file_name, 'w') as file_object:
        json.dump(datas, file_object)

# 顯示分析結果
def display_top_features(weights, names, top_n, select=abs):
    top_features = sorted(zip(weights, names), key=lambda x: select(x[0]), reverse=True)[:top_n]
    top_weights = [x[0] for x in top_features]
    top_names = [x[1] for x in top_features]

    print(top_features)
    print(top_weights)
    print(top_names)

# 儲存分析結果
store_MLResult(svc.coef_[0], dvec.get_feature_names(), ROOT + '/HTAS/Data/article_positive.json', select=lambda x: x)
store_MLResult(svc.coef_[0], dvec.get_feature_names(), ROOT + '/HTAS/Data/article_negative.json')
store_MLResult(c_svc.coef_[0], c_dvec.get_feature_names(), ROOT + '/HTAS/Data/message_positive.json', select=lambda x: x)
store_MLResult(c_svc.coef_[0], c_dvec.get_feature_names(), ROOT + '/HTAS/Data/message_negative.json')

# 貼文負向詞彙
# display_top_features(svc.coef_[0], dvec.get_feature_names(), 5)
# print('------------------------------------')

# 貼文正向詞彙
# display_top_features(svc.coef_[0], dvec.get_feature_names(), 5 , select=lambda x: x)
# print('------------------------------------')

# 留言正向詞彙
# display_top_features(c_svc.coef_[0], c_dvec.get_feature_names(), 5)
# print('------------------------------------') 

# 留言負向詞彙
# display_top_features(c_svc.coef_[0], c_dvec.get_feature_names(), 5, select=lambda x: x)