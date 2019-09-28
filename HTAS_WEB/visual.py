from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from HTAS.MyAnalyzer.analyzer import Analyzer

# from flaskr.auth import login_required
from HTAS_WEB.db import get_db

# from bokeh.plotting import figure, output_file, show
import chartkick

bp = Blueprint('visual', __name__, url_prefix='/visual')

# 測試 bar 
@bp.route('/test_bar')
def test_bar():
    data = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
    return render_template('visual/test_bar.html', data=data)

# 分析畫面
@bp.route('/analysis')
def analysis():
    fake_data = get_fate_data()

    return render_template('visual/analysis.html', posts=fake_data)


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