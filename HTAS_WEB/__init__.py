import os
from flask import Flask, render_template, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'HTAS.sqlite'),
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # use chartkick
    app.jinja_env.add_extension("chartkick.ext.charts")

    @app.route('/test')
    def test():
        return 'Hello World!'

    from . import db
    db.init_app(app)

    from . import visual
    app.register_blueprint(visual.bp)

    from . import user
    app.register_blueprint(user.bp)

    @app.route('/index')
    def index():
        return render_template('index.html')
    

    @app.route('/init_db')
    def init_db():
        my_db = db.get_db()

        print('init account')
        my_db.execute(
            'INSERT INTO USER (Account, Password, PermissionID, Email) VALUES (?, ?, ?, ?)',
            ('admin', generate_password_hash('123'), '1', 't105590045@ntut.org.tw')
        )

        return redirect(url_for('index'))
        
    return app
