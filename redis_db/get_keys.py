# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/10/12 21:29
# @File    : get_keys.py

from . import redis_connect


# 获取所有的key
def get_keys() -> list:
    redis_client = redis_connect()
    keys = redis_client.keys()
    return keys
