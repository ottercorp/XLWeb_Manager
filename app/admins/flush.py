# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/6/12 17:36
# @Author  : subjadeites
# @File    : flush.py

import requests
from flask import render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, URL

from app.utils.CDNCtrl import refresh, preload
from . import admins, auth


class Flush_Form(FlaskForm):
    flush_url_type = RadioField('Url类型', choices=['Url', '路径Dir', '正则匹配re'], validators=[DataRequired()], default='Url')
    flush_url = StringField('刷新地址', validators=[DataRequired(), URL()])
    submit = SubmitField("提交刷新")


class Get_Form(FlaskForm):
    get_url = StringField('预取地址', validators=[DataRequired(), URL()])
    submit = SubmitField("提交预取")


@admins.route('/flush', methods=['GET', 'POST'])
@auth.login_required
def _flush():
    form_flush = Flush_Form()
    form_get = Get_Form()
    if request.method == 'GET':
        pass
    if form_flush.validate_on_submit():
        url = form_flush.flush_url.data
        flush_url_type = form_flush.flush_url_type.data
        if flush_url_type == 'Url':
            types = 1
        elif flush_url_type == '路径Dir':
            types = 2
        elif flush_url_type == '正则匹配re':
            types = 3
        else:
            types = 114514
        # http转https
        if url.startswith('http://'):
            url = url.replace('http://', 'https://')
        # 确认域名是否是https://aonyx.ffxiv.wang/
        if url.startswith('https://aonyx.ffxiv.wang/'):
            try:
                response = requests.get(url)
                print(response.status_code)
                assert response.status_code == 200  # 查看url是否能访问
                # 每次提交成功，都会清空刷新地址
                form_flush.flush_url.data = ''
                a = refresh(type=types, urls=[url])
                flash(f'刷新已提交，返回状态：{a[0]}', a[1])
            except:
                flash('提交地址无法访问，请核实地址！', 'error')
        else:
            flash('请输入正确的域名', 'error')
    if form_get.validate_on_submit():
        url = form_get.get_url.data
        # http转https
        if url.startswith('http://'):
            url = url.replace('http://', 'https://')
        # 确认域名是否是https://aonyx.ffxiv.wang/
        if url.startswith('https://aonyx.ffxiv.wang/'):
            try:
                response = requests.get(url)
                print(response.status_code)
                assert response.status_code == 200  # 查看url是否能访问
                # 每次提交成功，都会清空刷新地址
                form_flush.flush_url.data = ''
                a = preload(urls=[url])
                flash(f'预取已提交，返回状态：{a[0]}', a[1])
            except:
                flash('提交地址无法访问，请核实地址！', 'error')
        else:
            flash('请输入正确的域名', 'error')

    return render_template("admin/flush_cdn.html", form_flush=form_flush, form_get=form_get)


@admins.route('/flush/PluginMaster', methods=['GET', 'POST'])
@auth.login_required
def _flush_Plugin_Master():
    try:
        a = refresh(type=1, urls=['https://aonyx.ffxiv.wang/Plugin/PluginMaster', 'https://xlweb.ffxiv.wang/plugin_status'])
        flash(a[0], a[1])
    except Exception as e:
        flash(f"代码运行报错：{str(e)}", "error")
    return redirect(url_for("front._flush"))


@admins.route('/flush/Asset_Meta', methods=['GET', 'POST'])
@auth.login_required
def _flush_Asset_Meta():
    try:
        a = refresh(type=1, urls=['https://aonyx.ffxiv.wang/Dalamud/Asset/Meta'])
        flash(a[0], a[1])
    except Exception as e:
        flash(f"代码运行报错：{str(e)}", "error")
    return redirect(url_for("front._flush"))


@admins.route('/flush/XL_Release', methods=['GET', 'POST'])
@auth.login_required
def _flush_XL_Release():
    try:
        a = refresh(type=1, urls=['https://aonyx.ffxiv.wang/Proxy/Update/Release/RELEASES'])
        flash(a[0], a[1])
    except Exception as e:
        flash(f"代码运行报错：{str(e)}", "error")
    return redirect(url_for("front._flush"))
