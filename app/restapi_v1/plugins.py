# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/17 16:42
# @Author  : subjadeites
# @File    : plugins.py

import json

import httpx
from flask import current_app
from flask_restful import Resource, marshal_with

from . import api, localhost, DefaultApiResponse, resource_fields


class PluginMasterSite(Resource):
    @marshal_with(resource_fields)
    def post(self):
        plugin_master_json = httpx.get(f'{localhost(False)}/Plugin/PluginMaster', timeout=10).json()
        result_main = {}
        result_test = {}
        result_all = {}
        for i in plugin_master_json:
            if i['DalamudApiLevel'] != current_app.config['DALAMUD_API_LEVEL']:
                continue # Skip if not compatible with current Dalamud API level
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

        return DefaultApiResponse(data={'msg': 'flush plugin master site success'}, code=200)


api.add_resource(PluginMasterSite, '/plugin_master_site', endpoint='plugin_master_site')
