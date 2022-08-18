# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/14 17:30
# @Author  : subjadeites
# @File    : plugin_status.py
import json
import time

from flask import render_template, request, flash

from . import plugin_master


@plugin_master.route('/plugin_status')
def _plugin_status():
    with open(r'./cache/plugin_master_main.json', 'r', encoding='utf-8-sig') as f:
        result_main = json.load(f)
    with open(r'./cache/plugin_master_testing.json', 'r', encoding='utf-8-sig') as f:
        result_test = json.load(f)
    print(result_main)
    return render_template(r'user/plugin_status.html', plugin_master_main=result_main, plugin_master_test=result_test)
