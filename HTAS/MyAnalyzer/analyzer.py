import jieba
import json
import pandas as pd
import os
import re
import datetime
import numpy as np

class Analyzer():

    def __init__(self, *args, **kwargs):
        pass
        # print(self.data_path)
        # jieba.set_dictionary('HTAS/MyAnalyzer/dict.txt.big')
        # jieba.add_word('拉抬')
        # jieba.add_word('人渣文本')
        # jieba.add_word('自經區')
        # jieba.add_word('CNN')
        # jieba.add_word('NCC')
        # jieba.add_word('懶人包')
        # jieba.add_word('FB')
        # jieba.add_word('fb')

        # self.stopWords = []
        # with open('HTAS/MyAnalyzer/stops.txt', 'r', encoding='utf-8') as stop_file:
        #     for stop in stop_file.readlines():
        #         stop = stop.strip()
        #         self.stopWords.append(stop)

    @staticmethod
    def read_ptt_json(data_path, start_date, end_date):
        data = pd.DataFrame(columns=['ID', 'message_count', 'url', 'positive', 'neutral', 'negative'])
        id = []
        url = []
        message_count = []
        for filename in os.listdir(data_path):
            if start_date <= datetime.datetime.strptime(re.split('\(|\)', filename)[1], '%Y-%m-%d') <= end_date:
                with open(data_path+filename, 'r', encoding='utf-8') as read_file:
                    read_file = json.load(read_file)
                    for i in range(len(read_file['articles'])):
                        id.append(read_file['articles'][i]['article_id'])
                        url.append(read_file['articles'][i]['url'])
                        message_count.append(read_file['articles'][i]['message_count']['all'])
        data['ID'] = id
        data['message_count'] = message_count
        data['url'] = url
        data['positive'] = np.NAN
        data['neutral'] = np.NAN
        data['negative'] = np.NAN
        data.set_index(keys='ID', inplace=True)
        data.sort_values(by=['message_count'], inplace=True, ascending=False)
        return data

    # @staticmethod
    # def cut(text, is_cut_all=False, is_HMM=True):
    #     seg_list = jieba.cut(text, cut_all=is_cut_all, HMM=is_HMM)
    #     return seg_list

    # def analysis_articles(self, data):
    #     titles = []
    #     contents = []
    #     totalLen = []
    #     articles = []
        
    #     df = pd.DataFrame(columns=['Words', 'Vec', 'TF', 'IDF'])
    #     for i in range(len(data['articles'])):
    #         # title分詞並去除停用詞
    #         title = jieba.cut(data['articles'][i]['article_title'], cut_all=False)
    #         title = list(filter(lambda t: t not in self.stopWords and t != ' ' and t != '\u3000', title))
            
    #         # 去除文章中的URL
    #         data['articles'][i]['content'] = re.sub(r"http\S+", '', data['articles'][i]['content'], flags=re.MULTILINE)
            
    #         # content分詞並去除停用詞
    #         content = jieba.cut(data['articles'][i]['content'], cut_all=False)
    #         content = list(filter(lambda c : c not in self.stopWords and c != ' ' and c != '\u3000', content))
            
    #         totalLen.append(len(title) + len(content))
    #         titles.append(title)
    #         contents.append(content)

            
    #     for i in range(len(titles)):
    #         articles += titles[i] + contents[i]
    #     df['Words'] = articles
    #     df['Vec'] = df['TF'] = df['IDF'] = np.nan
        
    #     return df, titles, contents, totalLen

    # add by kelvin
    ''' 計算每篇文章的推文、虛文、中立的數目，並回傳一個 dict '''
    def analysis_article_push(self, article):
        positive = 0
        negative = 0
        neutral = 0
        total_count = 0

        messages = article['messages']
        for message in messages:
            status = message['push_tag']
            if (status == '推'):
                positive += 1
            elif (status == '噓'):
                negative += 1
            else:
                neutral += 1
            total_count += 1

        result = {
            'title': article['article_title'],
            'message':{
                'count': total_count,
                'positive': positive,
                'negative': negative,
                'neutral': neutral
            }
        }
        
        return result
        


    '''分析一則訊息'''
    def analysis_message(message):
        # 將訊息利用 jieba 切字
        pass

# ------------------------------------------------------------test------------------------------------------------------------
if __name__ == '__main__':
    start_date = datetime.datetime.strptime('2019-08-01', '%Y-%m-%d')
    end_date = datetime.datetime.strptime('2019-08-20', '%Y-%m-%d')
    data = Analyzer.read_ptt_json(data_path=os.getcwd()+'./HTAS/Data/', start_date=start_date, end_date=end_date)
    print(data.head(20))