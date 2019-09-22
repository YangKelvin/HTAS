from ANALYZER_CONFIG import *
from MyAnalyzer.analyzer import Analyzer as ptt_analyzer
import json
# import jieba
# from collections import defaultdict
import datetime
from os import listdir
from os.path import isfile

analyzer = ptt_analyzer()

# 取得欲分析的資料
data = analyzer.get_analysis_data(BOARD_NAME, DATE_START, DATE_END)

