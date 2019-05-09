import jieba
import json

class Analyzer():
    @staticmethod
    def read_ptt_json(url_json):
        read_file = open(url_json, 'r')
        data = json.load(read_file) # dict
        read_file.close()
        return data

    @staticmethod
    def cut(text, is_cut_all=False, is_HMM=True):
        seg_list = jieba.cut(text, cut_all=is_cut_all, HMM=is_HMM)
        return seg_list