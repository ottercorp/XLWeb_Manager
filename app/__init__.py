# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/6/10 15:07
# @Author  : subjadeites
# @File    : __init__.py.py
import json

from flask import Flask
from flask_cors import CORS
from flask_bootstrap import Bootstrap5
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap5()
csrf = CSRFProtect()
auth = HTTPBasicAuth()

# 读取配置文件
try:
    with open(r'appsettings.json', 'r') as f:
        appsettings = json.load(f)
        username = appsettings['auth_username']
        password = appsettings['auth_password']
except FileNotFoundError:
    print("appsettings.json not found")
    exit()
except KeyError:
    print("appsettings.json not correct")
    exit()
except json.decoder.JSONDecodeError:
    print("appsettings.json not correct")
    exit()
except Exception as e:
    print(e)
    exit()


def create_app():
    app = Flask(__name__)

    bootstrap.init_app(app)
    csrf.init_app(app)
    CORS(app, supports_credentials=True)
    # login_manager.init_app(app)

    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config["SECRET_KEY"] = appsettings['Flask_SECRET_KEY']
    app.config["WTF_CSRF_SECRET_KEY "] = appsettings['Flask_WTF_CSRF_SECRET_KEY']
    app.config["API_SECRET"] = appsettings['API_SECRET']

    # 注册蓝图
    from app.admins import admins as admins_blueprint
    app.register_blueprint(admins_blueprint)
    from app.front import front as front_blueprint
    app.register_blueprint(front_blueprint)
    from app.restapi_v1 import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app


# 注册auth
@auth.verify_password
def verify_password(name, pwd):
    if name == username and pwd == password:
        return True
    return False
