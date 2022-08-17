# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/14 17:30
# @Author  : subjadeites
# @File    : plugin_status.py
import json
import time

from flask import render_template, request, flash
import httpx

from . import plugin_master


@plugin_master.route('/plugin_status')
def _plugin_status():
    plugin_master_json = httpx.get('https://aonyx.ffxiv.wang/Plugin/PluginMaster').json()
    result_main = {}
    result_test = {}
    for i in plugin_master_json:
        if i['IsTestingExclusive'] is False:
            result_main[i['Name']] = {
                'is_test': i['IsTestingExclusive'],
                'is_hidden': i['IsHide'],
                'version': i['AssemblyVersion'],
                'Test_Version': i['TestingAssemblyVersion'],
                'last_update': i['LastUpdate'],
                'api_level': i['DalamudApiLevel'],
                'description': i['Description']
            }
        else:
            result_test[i['Name']] = {
                'is_test': i['IsTestingExclusive'],
                'is_hidden': i['IsHide'],
                'version': i['AssemblyVersion'],
                'Test_Version': i['TestingAssemblyVersion'],
                'last_update': i['LastUpdate'],
                'api_level': i['DalamudApiLevel']
            }
    return render_template(r'user/plugin_status.html', plugin_master_main=result_main, plugin_master_test=result_test)
