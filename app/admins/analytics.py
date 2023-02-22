# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/6/12 17:36
# @Author  : subjadeites
# @File    : analytics.py

import requests
from flask import render_template, redirect, url_for, flash, request, current_app
from . import admins, auth
from redis_db import xlweb_redis_connect


@admins.route('/analytics')
@auth.login_required
def _analytics():
    redis_client = xlweb_redis_connect()
    xivlauncher_count = redis_client.hgetall('xlweb-fastapi|xivlauncher-count')
    xivlauncher_install_times = xivlauncher_count['XLUniqueInstalls']
    xivlauncher_start_times = xivlauncher_count['XLStarts']

    plugin_count: dict[str:int] = redis_client.hgetall('xlweb-fastapi|plugin-count')
    plugin_install_times = plugin_count['accumulated']
    del plugin_count['accumulated']
    plugin_list_1: dict[str:int] = {}
    plugin_list_2: dict[str:int] = {}
    i = 0
    plugin_count = dict(sorted(plugin_count.items(), key=lambda x: int(x[1]), reverse=True))
    for k, v in plugin_count.items():
        if i % 2 == 0:
            plugin_list_1[i] = (k,v)
        else:
            plugin_list_2[i] = (k,v)
        i += 1

    return render_template('admin/analytics.html',
                           xivlauncher_install_times=xivlauncher_install_times,
                           xivlauncher_start_times=xivlauncher_start_times,
                           plugin_install_times=plugin_install_times,
                           plugin_list_1=plugin_list_1,
                           plugin_list_2=plugin_list_2)
