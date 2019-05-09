import jieba
import json

class Analyzer():
    @staticmethod
    def read_ptt_json(url_json):
        read_file = open(url_json, 'r')
        data = json.load(read_file) # dict
        return data
