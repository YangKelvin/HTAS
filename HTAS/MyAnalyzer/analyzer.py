import jieba
import json


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
        with open('./stops.txt', 'r', encoding='utf-8') as stop_file:
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
