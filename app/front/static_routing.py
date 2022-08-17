# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/6/10 15:12
# @Author  : subjadeites
# @File    : static_routing.py
import re
import subprocess

from flask import render_template, send_file

from . import front, auth


@front.route('/')
@auth.login_required
def _main_website():
    try:
        result = subprocess.getoutput("systemctl status XLWebServices")
        result_list = result.split("\n")
        result_stauts = re.split(r'[()]', result_list[2])[1]
    except:
        result_stauts = "test"
        result_list = "test"
    return render_template(r'admin/index.html', stauts=result_stauts, message=result_list)


@front.route('/start', methods=["GET", "POST"])
@auth.login_required
def _start_svr():
    result = subprocess.getoutput("systemctl start XLWebServices")
    result = subprocess.getoutput("systemctl status XLWebServices")
    result_list = result.split("\n")
    result_stauts = re.split(r'[()]', result_list[2])[1]
    return render_template(r'admin/index.html', stauts=result_stauts, message=result_list)


@front.route('/restart', methods=["GET", "POST"])
@auth.login_required
def _restart_svr():
    result = subprocess.getoutput("systemctl restart XLWebServices")
    result = subprocess.getoutput("systemctl status XLWebServices")
    result_list = result.split("\n")
    result_stauts = re.split(r'[()]', result_list[2])[1]
    return render_template(r'admin/index.html', stauts=result_stauts, message=result_list)


@front.route('/stop', methods=["GET", "POST"])
@auth.login_required
def _stop_svr():
    result = subprocess.getoutput("systemctl stop XLWebServices")
    result = subprocess.getoutput("systemctl status XLWebServices")
    result_list = result.split("\n")
    result_stauts = re.split(r'[()]', result_list[2])[1]
    return render_template(r'admin/index.html', stauts=result_stauts, message=result_list)


@front.route('/download_logs', methods=["GET", "POST"])
@auth.login_required
def _download_logs():
    result = subprocess.getoutput("journalctl -xe -u XLWebServices")
    with open('./app/XLWebServices.log', 'w') as f:
        f.write(result)
    return send_file('XLWebServices.log', '.')
