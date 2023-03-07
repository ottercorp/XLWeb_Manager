# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/6/10 15:12
# @Author  : subjadeites
# @File    : static_routing.py

import re
import subprocess

from flask import render_template, send_file, redirect, url_for

from . import admins, auth


@admins.route('/')
@auth.login_required
def _main_website():
    try:
        result = subprocess.getoutput("systemctl status XLWeb-fastapi")
        result_list = result.split("\n")
        result_stauts = re.split(r'[()]', result_list[2])[1]
    except:
        result_stauts = "test"
        result_list = "test"
    return render_template(r'admin/index.html', stauts=result_stauts, message=result_list)


@admins.route('/start', methods=["GET", "POST"])
@auth.login_required
def _start_svr():
    subprocess.getoutput("systemctl start XLWeb-fastapi")
    return redirect(url_for("admins._main_website"))


@admins.route('/restart', methods=["GET", "POST"])
@auth.login_required
def _restart_svr():
    subprocess.getoutput("systemctl restart XLWeb-fastapi")
    return redirect(url_for("admins._main_website"))


@admins.route('/stop', methods=["GET", "POST"])
@auth.login_required
def _stop_svr():
    subprocess.getoutput("systemctl stop XLWeb-fastapi")
    return redirect(url_for("admins._main_website"))


@admins.route('/download_logs', methods=["GET", "POST"])
@auth.login_required
def _download_logs():
    result = subprocess.getoutput("journalctl -xe -u XLWeb-fastapi")
    with open('./app/XLWebServices.log', 'w') as f:
        f.write(result)
    return send_file('XLWebServices.log', '.')


@admins.route('/rebuild_cache/<cache>', methods=["GET", "POST"])
@auth.login_required
def _rebuild_cache(cache):
    if cache == "plugin":
        keyword = "plugin"
    elif cache == "xivlauncher":
        keyword = "xivlauncher"
    elif cache == "dalamud":
        keyword = "dalamud"
    elif cache == "all":
        keyword = ""
    elif cache == "dalamud_changelog":
        keyword = "dalamud_changelog"
    elif cache == "asset":
        keyword = "asset"
    else:
        return redirect(url_for("admins._main_website"))
    process = subprocess.Popen(f"python3 regen.py {keyword}",shell=True,cwd=r"/www/wwwroot/XLWebServices-fastapi")
    process.wait()
    return redirect(url_for("admins._main_website"))
