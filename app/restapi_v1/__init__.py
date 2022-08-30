# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/17 15:18
# @Author  : subjadeites
# @File    : __init__.py.py

from functools import wraps

from flask import Blueprint, request, current_app
from flask_restful import Api, fields

from app import auth, csrf, localhost
from .exceptions import *

auth, csrf, localhost = auth, csrf, localhost


def check_secret(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        api_secret = request.headers.get('api-secret')
        if api_secret is None:
            raise SecretMissingError()
        elif api_secret != current_app.config['API_SECRET']:
            raise SecretIncorrectError()
        else:
            return func(*args, **kwargs)

    return decorated


resource_fields = {
    'message': fields.String,
    'code': fields.Integer,
    'data': fields.Raw or fields.List(fields.Raw) or None,
}


class DefaultApiResponse(object):
    def __init__(self, data: dict | list | None, message: str = 'Success', code: int = 200):
        self.data = data
        self.message = message
        self.code = code


api_bp = Blueprint("api", __name__)
api = Api(api_bp, decorators=[csrf.exempt, check_secret], errors=errors)

from . import plugins, log_analysis
