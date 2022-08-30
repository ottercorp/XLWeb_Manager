# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/6/10 15:11
# @Author  : subjadeites
# @File    : __init__.py.py

from flask import Blueprint

from app import auth, csrf, localhost

auth, csrf, localhost = auth, csrf, localhost

admins = Blueprint("admins", __name__)

from . import static_routing, revise_config, flush, analytics
