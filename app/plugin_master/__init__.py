# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/14 17:29
# @Author  : subjadeites
# @File    : __init__.py.py
from flask import Blueprint

from app import auth

auth = auth

plugin_master = Blueprint("plugin_master", __name__)

from . import plugin_status
