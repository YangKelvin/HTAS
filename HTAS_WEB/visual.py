from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

# from flaskr.auth import login_required
from HTAS_WEB.db import get_db
# from bokeh.plotting import figure, output_file, show
import chartkick

bp = Blueprint('visual', __name__, url_prefix='/visual')


@bp.route('/bar')
def bar():
    data = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
    return render_template('visual/bar.html', data=data)