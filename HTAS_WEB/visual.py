from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
# from flaskr.auth import login_required
from HTAS_WEB.db import get_db
# from bokeh.plotting import figure, output_file, show
import chartkick
from HTAS.api import *
import datetime
import os

bp = Blueprint('visual', __name__, url_prefix='/visual')

DATE_START = datetime.datetime(2019, 8, 30)
DATE_END = datetime.datetime(2019, 8, 31)

# 測試 bar 
@bp.route('/test_bar')
def test_bar():
    data = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
    return render_template('visual/test_bar.html', data=data)

# 分析畫面
@bp.route('/analysis', methods=('GET', 'POST'))
def analysis():
    # tmp = get_word_vector()
    data_count = 3
    if (request.method == 'GET'):
        data = get_ptt_data(DATE_START, DATE_END)
        return render_template('visual/analysis.html', posts=data[:data_count])

    if (request.method == 'POST'):
        # 取得表單上資料
        date_start = request.form['datepicker-start']   # 起始日期
        date_end = request.form['datepicker-end']       # 結束日期
        data_count = int(request.form['data-count'])    # 資料筆數
        # 將日期格式轉換成 datetime
        date_start = datetime.datetime.strptime(str(date_start), '%Y-%m-%d')    
        date_end = datetime.datetime.strptime(str(date_end), '%Y-%m-%d')
        # 取得資料
        data = get_ptt_data(date_start, date_end)
        return render_template('visual/analysis.html', posts=data[:data_count])

# 貼文和回覆的詞分數
@bp.route('/word_vec', methods=('GET', 'POST'))
def word_vec():
    article_pos = get_word_vector(DATA_VEC_LEN, 'ap')
    article_neg = get_word_vector(DATA_VEC_LEN, 'an')
    message_pos = get_word_vector(DATA_VEC_LEN, 'mp')
    message_neg = get_word_vector(DATA_VEC_LEN, 'mn')

    return render_template('visual/word_vec.html', ap=article_pos, an=article_neg, mp = message_pos, mn = message_neg)

# 取得假資料
def get_fate_data():
    fake_data = []
    
    # 標題、正面、中立、負面
    data1 = {'title': 'title1', 'data':{ 'positive': 60.0, 'neutral': 10.0, 'negative': 30.0}}
    data2 = {'title': 'title2', 'data':{ 'positive': 65.0, 'neutral': 15.0, 'negative': 20.0}}
    data3 = {'title': 'title3', 'data':{ 'positive': 65.0, 'neutral': 20.0, 'negative': 15.0}}

    fake_data.append(data1)
    fake_data.append(data2)
    fake_data.append(data3)

    return fake_data
