# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/17 16:42
# @Author  : subjadeites
# @File    : plugins.py
import json

from flask_restful import Resource, fields, marshal_with
import httpx

from . import api

resource_fields = {
    'message': fields.String,
    'status': fields.Integer,
    'task': fields.String,
}


class PluginMasterSiteDao(object):
    def __init__(self, msg: str, task: str, status: int = 200):
        self.msg = msg
        self.task = task
        self.status = status


class PluginMasterSite(Resource):
    @marshal_with(resource_fields)
    def post(self):
        plugin_master_json = httpx.get('https://aonyx.ffxiv.wang/Plugin/PluginMaster', timeout=10).json()
        result_main = {}
        result_test = {}
        result_all = {}
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
            result_all[i['Name']] = {
                'is_test': i['IsTestingExclusive'],
                'is_hidden': i['IsHide'],
                'version': i['AssemblyVersion'],
                'Test_Version': i['TestingAssemblyVersion'],
                'last_update': i['LastUpdate'],
                'api_level': i['DalamudApiLevel']
            }
        with open(r'./cache/plugin_master_main.json', 'w', encoding='utf-8-sig') as f:
            result_main = dict(sorted(result_main.items(), key=lambda x: x[0]))
            json.dump(result_main, f, ensure_ascii=False, indent=4)
        with open(r'./cache/plugin_master_testing.json', 'w', encoding='utf-8-sig') as f:
            result_test = dict(sorted(result_test.items(), key=lambda x: x[0]))
            json.dump(result_test, f, ensure_ascii=False, indent=4)
        with open(r'./cache/plugin_master_all.json', 'w', encoding='utf-8-sig') as f:
            result_all = dict(sorted(result_all.items(), key=lambda x: x[0]))
            json.dump(result_all, f, ensure_ascii=False, indent=4)

        return PluginMasterSiteDao(msg='success', task='flush plugin master site.')


api.add_resource(PluginMasterSite, '/plugin_master_site', endpoint='plugin_master_site')
