# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/20 23:22
# @Author  : subjadeites
# @File    : gun.py

import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

debug = False
loglevel = 'info'
bind = '0.0.0.0:6000'
pidfile = 'logs/gunicorn.pid'
logfile = 'logs/debug.log'

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'
