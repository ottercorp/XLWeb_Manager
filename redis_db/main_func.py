# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/22 0:25
# @Author  : subjadeites
# @File    : main_func.py
import redis
import secrets

redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='', db=0)


def redis_connect():
    return redis.Redis(connection_pool=redis_pool)


def save_log(log_base64: str) -> str:
    """生成日志解析的短网址

    Arguments:
        log_base64: 日志的base64编码

    Returns:
        token: 短网址
    """
    redis_client = redis_connect()
    token = secrets.token_urlsafe(8)
    redis_client.set(token, log_base64, ex=86400)
    return token


def read_short_url(short_url: str) -> str:
    """读取短网址

    Arguments:
        short_url: 短网址

    Returns:
        短网址对应的base64信息
    """
    redis_client = redis_connect()
    result = redis_client.get(short_url).decode('utf8')
    return result
