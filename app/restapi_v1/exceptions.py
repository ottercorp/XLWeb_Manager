# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/18 16:12
# @File    : exceptions.py
from flask_restful import fields
from werkzeug.exceptions import HTTPException

errors = {
    'MethodNotAllowed': {
        'message': 'Method Not Allowed',
        'status': 405,
    },
    'Unauthorized': {
        'message': "Unauthorized",
        'status': 401,
    },
    'BadRequest': {
        'message': "BadRequest",
        'status': 400,
    },
    'SecretMissingError': {
        'message': 'INVALID REQUEST',
        'status': 400,
    },
    'SecretIncorrectError': {
        'message': 'API_SECRET INCORRECT',
        'status': 401,
    }
}


class SecretMissingError(HTTPException):
    code = 400


class SecretIncorrectError(HTTPException):
    code = 401
