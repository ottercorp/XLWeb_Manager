# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/17 15:18
# @Author  : subjadeites
# @File    : __init__.py.py

from functools import wraps
from flask import Blueprint, request, current_app, jsonify
from flask_restful import Api

from app import auth, csrf

auth, csrf = auth, csrf


def check_secret(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        api_secret = request.headers.get('api-secret')
        if api_secret is None:
            return jsonify({"msg": "INVALID REQUEST"}), 400
        elif api_secret != current_app.config['API_SECRET']:
            return jsonify({"msg": "Api_secret ERROR"}), 401
        else:
            return func(*args, **kwargs)

    return decorated


api_bp = Blueprint("api", __name__)
api = Api(api_bp, decorators=[csrf.exempt, check_secret])

from . import plugins
