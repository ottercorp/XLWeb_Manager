# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2023/2/8 11:47
# @File    : feedback.py
from flask import render_template, redirect, url_for, request

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
    dhash = request.args.get('dhash')
    redis_client = redis_connect()
    version = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{feedback_id}', 'version')
    content = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{feedback_id}', 'content')
    exception = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{feedback_id}', 'exception')
    email = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{feedback_id}', 'email')
    level = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{feedback_id}', 'level')
    return render_template('admin/feedback_detail.html', plugin_name=plugin_name, feedback_id=feedback_id, version=version, content=content, email=email, level=level,exception=exception)


@admins.route('/feedback/export', methods=['GET', 'POST'])
@auth.login_required
def _feedback_export():
    redis_client = redis_connect()
    feedback_list = redis_client.keys('feedback|*')
    return_dict = {}
    for i in feedback_list:
        temp_list = i.replace('feedback|', '').split('|')
        dhash = temp_list[0]
        plugin_name = temp_list[1]
        order_id = temp_list[2]
        version = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{order_id}', 'version')
        content = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{order_id}', 'content')
        exception = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{order_id}', 'exception')
        reporter = redis_client.hget(f'feedback|{dhash}|{plugin_name}|{order_id}', 'reporter')
        description = [content, exception] if exception else [content]
        if plugin_name in return_dict.keys():
            return_dict[plugin_name].append((version, dhash, description, reporter, order_id))
        else:
            return_dict[plugin_name] = [(version, dhash, description, reporter, order_id)]
    for k, v in return_dict.items():
        return_dict[k] = sorted(v, key=lambda x: x[0], reverse=True)
    return render_template('admin/feedback_export.html', export_dict=return_dict)


@admins.route('/feedback/solve/<feedback_id>', methods=['GET'])
@auth.login_required
def _feedback_solve(feedback_id):
    from_page = request.args.get('from')
    redis_client = redis_connect()
    feedback_list = redis_client.keys(f'feedback|*|{feedback_id}')
    if len(feedback_list) == 1:
        redis_client.delete(feedback_list[0])
        if from_page == "export":
            return redirect(url_for('admins._feedback_export'))
        else:
            return redirect(url_for('admins._feedback_admin'))
    elif len(feedback_list) > 1:
        return 'Error: More than one feedback found.'
    else:
        return 'Error: No feedback found.'


@admins.route('/feedback/reply/<feedback_id>', methods=['GET', 'POST'])
@auth.login_required
def _feedback_reply():
    return 'Not implemented yet.'
