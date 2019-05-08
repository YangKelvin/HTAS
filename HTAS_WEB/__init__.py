import os
from flask import Flask, render_template, redirect, url_for


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

    @app.route('/test')
    def HTAS():
        return 'Hello World!'
    return app