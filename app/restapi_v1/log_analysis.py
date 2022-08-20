# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/19 17:53
# @File    : log_analysis.py
import json
import base64

import pandas as pd
from flask import request
from flask_restful import Resource, fields, marshal_with

from . import api


def analysis(file_object):
    """分析日志方法

    Arguments:
        file_object {file} -- 日志文件对象，需要具备read()方法

    Returns:
        dict -- {'last_exception': {last_exception}, **troubleshooting}


    """
    df = pd.read_csv(file_object, delim_whitespace=True, index_col=False, names=['data', 'time', 'UTC', 'level', 'message'], on_bad_lines='skip', parse_dates=[0, 1])
    # 删除data列中不是日期且message低于30字符的行
    df = df[(df['data'].str.contains('\d{4}-\d{2}-\d{2}')) & (df['message'].str.len() > 30)]

    # 将df的索引重新倒序排列
    last_exception = {}
    troubleshooting = {}
    # 循环遍历df的每一行
    for index, row in df.iterrows():
        # 如果message中包含“LASTEXCEPTION”
        if 'LASTEXCEPTION' in row['message']:
            base64_ciphertext = row['message'].split(':')[1]
            # 进行base64解码
            plain_text = base64.b64decode(base64_ciphertext)
            plain_dict = json.loads(plain_text)
            # 合并last_exception字典
            last_exception.update(plain_dict)

        # 如果message中包含“TROUBLESHOOTING”，则将该行的message存入troubleshooting字典中
        if 'TROUBLESHOOTING' in row['message']:
            base64_ciphertext = row['message'].split(':')[1]
            # 进行base64解码
            plain_text = base64.b64decode(base64_ciphertext)
            plain_dict = json.loads(plain_text)
            # 合并last_exception字典
            troubleshooting.update(plain_dict)
    LoadedPlugins_list: list[dict] = troubleshooting.get('LoadedPlugins', [])
    LoadedPlugins_dict = {}
    main_plugin_list = []
    testing_plugin_list = []
    third_party_plugin_list = []
    disabled_plugins_list = []
    for i in LoadedPlugins_list:
        temp_dict = {}
        plugin_name = i['Name']
        if i['Disabled'] is True:
            disabled_plugins_list.append(plugin_name)
            temp_dict['plugin_status'] = "disabled"
        elif i['Testing'] is True:
            testing_plugin_list.append(plugin_name)
            temp_dict['plugin_status'] = "testing"
        elif i['IsThirdParty'] is False:
            main_plugin_list.append(plugin_name)
            temp_dict['plugin_status'] = "main"
        else:
            third_party_plugin_list.append(plugin_name)
            temp_dict['plugin_status'] = "3rd"
        LoadedPlugins_dict[plugin_name] = {**temp_dict,
                                           'EffectiveVersion': i['EffectiveVersion'],
                                           'InstalledFromUrl': i['InstalledFromUrl'],
                                           'InternalName': i['InternalName'],
                                           'DalamudApiLevel': i['DalamudApiLevel'],
                                           }
    troubleshooting.pop('LoadedPlugins')
    result = {'last_exception': last_exception,
              'main_plugin_list': main_plugin_list,
              'testing_plugin_list': testing_plugin_list,
              'third_party_plugin_list': third_party_plugin_list,
              **troubleshooting,
              **LoadedPlugins_dict,
              'disabled_plugins_list': disabled_plugins_list, }

    return json.dumps(result)


class LogAnalysis(Resource):
    """日志分析接口"""

    @marshal_with(fields={
        'message': fields.String,
        'status': fields.Integer,
        'task': fields.String,
    }
    )
    def post(self):
        """分析日志方法"""
        file_object = request.files['file']
        try:
            msg = analysis(file_object)
        except BaseException:
            return {'message': '分析失败，请确定日志文件是否是dalamud.log', 'status': 500, 'task': 'dalamud日志分析'}, 500
        return {'message': msg, 'status': 200, 'task': 'dalamud日志分析'}


api.add_resource(LogAnalysis, '/logAnalysis', endpoint="logAnalysis")
