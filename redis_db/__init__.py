# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/21 22:42
# @Author  : subjadeites
# @File    : __init__.py.py

import redis

redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='', db=1, decode_responses=True)
xlweb_redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='', db=0, decode_responses=True)


def redis_connect():
    return redis.Redis(connection_pool=redis_pool)

def xlweb_redis_connect():
    return redis.Redis(connection_pool=xlweb_redis_pool)

from .main_func import *
from .get_keys import *
