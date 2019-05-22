import jieba
import json
import pandas

class Analyzer():

    def __init__(self, *args, **kwargs):
        jieba.set_dictionary('HTAS/MyAnalyzer/dict.txt.big')
        jieba.add_word('拉抬')
        jieba.add_word('人渣文本')
        jieba.add_word('自經區')
        jieba.add_word('CNN')
        jieba.add_word('NCC')
        jieba.add_word('懶人包')
        jieba.add_word('FB')
        jieba.add_word('fb')

        stopWords = []
        with open('HTAS/MyAnalyzer/stops.txt', 'r', encoding='utf-8') as stop_file:
            for stop in stop_file.readlines():
                stop = stop.strip()
                stopWords.append(stop)

    @staticmethod
    def read_ptt_json(url_json):
        read_file = open(url_json, 'r')
        data = json.load(read_file)  # dict
        read_file.close()
        return data

    @staticmethod
    def cut(text, is_cut_all=False, is_HMM=True):
        seg_list = jieba.cut(text, cut_all=is_cut_all, HMM=is_HMM)
        return seg_list

    @staticmethod
    def analysis_articles():
        titles = []
        contents = []
        totalLen = []
        df = pd.DataFrame(columns=['Words', 'Vec', 'TF', 'IDF'])
        for i in range(len(data['articles'])):
            # title分詞並去除停用詞
            title = jieba.cut(data['articles'][i]['article_title'], cut_all=False)
            title = list(filter(lambda t: t not in stopWords and t != ' ' and t != '\u3000', title))
            # 去除文章中的URL
            data['articles'][i]['content'] = re.sub(r"http\S+", '', data['articles'][i]['content'], flags=re.MULTILINE)
            # content分詞並去除停用詞
            content = jieba.cut(data['articles'][i]['content'], cut_all=False)
            content = list(filter(lambda c : c not in stopWords and c != ' ' and c != '\u3000', content))
            
            totalLen.append(len(title) + len(content))
            titles.append(title)
            contents.append(content)
