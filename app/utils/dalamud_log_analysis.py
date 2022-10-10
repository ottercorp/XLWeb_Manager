# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/21 16:58
# @Author  : subjadeites
# @File    : dalamud_log_analysis.py

import base64
import json

import pandas as pd


def merge_message(df, index, start_index, drop_index_list) -> int:
    """合并message

    Args:
        df :DataFrame: 需要合并的DataFrame
        index :int: 当前行的索引

    Returns:
        需要合并的字符串长度
    """
    next_line = df.loc[index + 1]['date']
    # 将下一行的message合并到当前行
    df.iloc[start_index]['message'] += next_line
    drop_index_list.append(index + 1)
    return len(next_line)


def analysis(file_object, api_level: int = 6) -> (dict,int|None):
    """分析日志方法

    Arguments:
        file_object :file: 日志文件对象，需要具备read()方法
        api_level :int: api等级，目前支持6和7，6为当前使用的api，7为上游的api (default: {6})

    Returns:
        result,log_file_type

    result :dict: 返回分析结果

    log_file_type :int: 返回日志文件类型，None：未知，0：Dalamud，1：XIVLauncher
    """
    df = pd.read_csv(file_object, delim_whitespace=True, index_col=False, names=['date', 'time', 'UTC', 'level', 'message'], on_bad_lines='skip', parse_dates=[0, 1])
    # 删除data列中不是日期且message低于30字符的行
    df = df[(((df['date'].str.contains('\d{4}-\d{2}-\d{2}')) & (df['message'].str.len() > 35)) | (df['time'].isna()))]
    df = df.reset_index(drop=True)  # 重置index

    # 循环遍历df的每一行，选出base64换行的进行合并，合并后删除；非换行的且非异常行删除。
    # 单行未满10000个字符的换行不会被合并。TODO: 优化
    drop_index_list = []
    i = 0
    while i < len(df):
        row = df.iloc[i]
        if pd.isna(row['time']):
            drop_index_list.append(i)
            i += 1
            if i >= len(df):
                break
        # 如果message长度等于9963，说明下一行还有message，需要合并
        elif len(row['message']) == 9963:
            start_i = i
            a = 10000
            while a == 10000:
                a = merge_message(df, i, start_i, drop_index_list)
                i += 1
            i += 1
            if i >= len(df):
                break
        else:
            i += 1
    df.drop(drop_index_list, inplace=True)

    # 将df的索引重新倒序排列
    last_exception = {}
    second_last_exception = {}
    third_last_exception = {}
    troubleshooting = {}
    # 初始化日志标记
    log_file_type = None  # 0: Dalamud.log, 1: output.log/Dalamud.Updater.log
    # 循环遍历df的每一行
    for index, row in df.iterrows():
        try:
            # 如果message中包含“LASTEXCEPTION”
            if 'LASTEXCEPTION' in row['message']:
                base64_ciphertext = row['message'].split(':')[1]
                # 进行base64解码
                plain_text = base64.b64decode(base64_ciphertext)
                plain_dict = json.loads(plain_text)
                # 合并last_exception字典
                third_last_exception.update(second_last_exception)
                second_last_exception.update(last_exception)
                last_exception.update(plain_dict)

            # 如果message中包含“TROUBLESHOOTING”，则将该行的message存入troubleshooting字典中
            elif 'TROUBLESHOOTING' in row['message']:
                log_file_type = 0  # 0: Dalamud.log, 1: output.log/Dalamud.Updater.log
                base64_ciphertext = row['message'].split(':')[1]
                # 进行base64解码
                plain_text = base64.b64decode(base64_ciphertext)
                plain_dict = json.loads(plain_text)
                # 合并last_exception字典
                troubleshooting.update(plain_dict)
            elif 'TROUBLESHXLTING' in row['message']:
                log_file_type = 1  # 0: Dalamud.log, 1: output.log/Dalamud.Updater.log
                base64_ciphertext = row['message'].split(':')[1]
                # 进行base64解码
                plain_text = base64.b64decode(base64_ciphertext)
                plain_dict = json.loads(plain_text)
                # 合并last_exception字典
                troubleshooting.update(plain_dict)
        except:
            pass  # 遇到傻逼不写满10k就换行的日志就跳过
    if log_file_type == 0:
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
            elif i['DalamudApiLevel'] != api_level:
                disabled_plugins_list.append(plugin_name)
                temp_dict['plugin_status'] = "error_api_level"
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
        result = {
            'Exception_Last': last_exception,
            'Exception_Second_Last': second_last_exception,
            'Exception_Third_Last': third_last_exception,
            'Main_plugins': main_plugin_list,
            'Testing_plugins': testing_plugin_list,
            'Third_party_plugins': third_party_plugin_list,
            'loadedPlugins': LoadedPlugins_dict,
            'disabled_plugins': disabled_plugins_list,
            'troubleshooting': troubleshooting,
        }
    elif log_file_type == 1:
        result = {
            'Exception_Last': last_exception,
            'Exception_Second_Last': second_last_exception,
            'Exception_Third_Last': third_last_exception,
            'troubleshooting': troubleshooting,
        }
    else:
        raise Exception("日志类型不支持或者无法判断日志类型。")
    return result, log_file_type
