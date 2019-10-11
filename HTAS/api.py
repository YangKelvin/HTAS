from HTAS.config import *
from HTAS.MyAnalyzer.analyzer import Analyzer
import json

analyzer = Analyzer()

# 取得分析頁面的資料
# 會依據文章熱門程度做排序，資料內容包含文章的標題和推噓文數量
def get_ptt_data(date_start, date_end):
    data = analyzer.read_ptt_json(DATA_LAYER, date_start, date_end)
    result = []
    for index, row in data.iterrows():
        tmp = {
            'title': row['title'], 
            'data':{ 
                'positive': row['positive'],
                'neutral' : row['neutral'],
                'negative': row['negative']
            }
        }
        result.append(tmp)
    return result

# 分析詞向量
def analysis_word_vector():
    svc, c_svc = analyzer.get_word_vector(DATA_FOR_ML_LAYER)

    # 貼文負向詞彙
    display_top_features(svc.coef_[0], dvec.get_feature_names(), 5)

    # 貼文正向詞彙
    display_top_features(svc.coef_[0], dvec.get_feature_names(), 5 , select=lambda x: x)

# 詞向量字典
def vec_num_to_string(num):
    data = {
        'ap' : "article_positive.json",
        'an' : "article_negative.json",
        'mp' : "message_positive.json",
        'mn' : "message_negative.json"
    }
    return data.get(num, None)
    
# 取得詞向量資量
def get_word_vector(data_length, data_type):
    file_path = DATA_ROOT + vec_num_to_string(data_type)
    data = []
    result = {}
    with open(file_path, 'r') as f:
        data = json.load(f)
    for word_vec in data[:data_length]:
        word_name = word_vec['name']
        word_weight = word_vec['weights']
        result[word_name] = word_weight
    return result
