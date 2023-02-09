# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2023/2/8 11:47
# @File    : feedback.py
from flask import render_template

from . import admins, auth, localhost
from redis_db import redis_connect


@admins.route('/feedback_admin', methods=['GET', 'POST'])
@auth.login_required
def _feedback_admin():
    redis_client = redis_connect()
    # have_feedback_plugins_list = redis_client.hkeys('xlweb-fastapi|feedback-count')
    feedback_list = redis_client.keys('feedback|*')
    return_list = []
    for i in feedback_list:
        temp_list = i.replace('feedback|', '').split('|')
        return_list.append(temp_list)
    return render_template('admin/feedback_admin.html', feedback_list=return_list)


@admins.route('/feedback/<plugin_name>/<feedback_id>', methods=['GET', 'POST'])
@auth.login_required
def _feedback_detail(plugin_name, feedback_id):
    redis_client = redis_connect()
    version = redis_client.hget(f'feedback|{plugin_name}|{feedback_id}', 'version')
    context = redis_client.hget(f'feedback|{plugin_name}|{feedback_id}', 'context')
    email = redis_client.hget(f'feedback|{plugin_name}|{feedback_id}', 'email')
    level = redis_client.hget(f'feedback|{plugin_name}|{feedback_id}', 'level')
    return render_template('admin/feedback_detail.html', plugin_name=plugin_name, feedback_id=feedback_id, version=version, context=context, email=email, level=level)


@admins.route('/feedback/export', methods=['GET', 'POST'])
@auth.login_required
def _feedback_export():
    redis_client = redis_connect()
    feedback_list = redis_client.keys('feedback|*')
    return_dict = {}
    for i in feedback_list:
        temp_list = i.replace('feedback|', '').split('|')
        plugin_name = temp_list[1]
        level = temp_list[0]
        feedback_id = temp_list[2]
        version = redis_client.hget(f'feedback|{level}|{plugin_name}|{feedback_id}', 'version')
        context = redis_client.hget(f'feedback|{level}|{plugin_name}|{feedback_id}', 'context')
        exception = redis_client.hget(f'feedback|{level}|{plugin_name}|{feedback_id}', 'exception')
        description = f"{context}\n\n{exception}" if exception else f"{context}"
        if plugin_name in return_dict.keys():
            return_dict[plugin_name].append((version, level, description))
        else:
            return_dict[plugin_name] = [(version, level, description)]
    for k,v in return_dict.items():
        return_dict[k] = sorted(v, key=lambda x: x[0], reverse=True)
    return render_template('admin/feedback_export.html', export_dict=return_dict)
