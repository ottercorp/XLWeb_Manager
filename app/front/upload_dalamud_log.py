# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/20 23:07
# @Author  : subjadeites
# @File    : upload_dalamud_log.py

import base64
import json

from flask import render_template, request, redirect, url_for, jsonify, flash, current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from app.utils.dalamud_log_analysis import analysis
from redis_db import save_log, read_log_short_url
from . import front


class UploadDalamudLog(FlaskForm):
    file = FileField('上传dalamud日志', validators=[FileRequired(), FileAllowed(['log'], '只能上传log文件')])
    submit = SubmitField("提交分析")


@front.route('/upload_dalamud_log', methods=['GET', 'POST'])
def _upload_dalamud_log():
    upload_form = UploadDalamudLog()
    if upload_form.validate_on_submit():
        file = request.files['file']
        if file and file.filename != '':
            try:
                analysis_result = analysis(file,current_app.config['DALAMUD_API_LEVEL'])
                if 'Penumbra' in analysis_result['Third_party_plugins']:
                    flash('90%的报错都是因为Penumbra加载了不恰当的MOD导致，请停用Penumbra后试试是否还会报错。', 'warning')
                    flash('请将分析后的网页地址复制给相关人员，链接有效期为一天。', 'info')
                    return render_template('user/upload_dalamud_log.html', form=upload_form)
                elif analysis_result['Third_party_plugins'] != []:
                    flash('该日志包含第三方插件，请删除你的第三方插件。', 'warning')
                    flash(f'您启用的第三方插件如下：{analysis_result["Third_party_plugins"]}', 'warning')
                    flash('第三方插件的支持频道并不在此处，想在此处寻求帮助请删除你的第三方插件。第三方插件会在插件管理器中图标的右下角有一个黄色的3。', 'warning')
                    flash('请将分析后的网页地址复制给相关人员，链接有效期为一天。', 'info')
                    return render_template('user/upload_dalamud_log.html', form=upload_form)
                msg = str(base64.urlsafe_b64encode(json.dumps(analysis_result).encode('utf-8')), 'utf-8')
                short_url = save_log(msg)
                return redirect(url_for('front._log_result_short', short_url=short_url))
            except Exception as e:
                print(e)  # TODO: 异常日志打印
                flash('文件解析失败，请检查是否是dalamud.log。', 'error')
                return redirect(url_for('front._upload_dalamud_log'))
        else:
            flash('文件解析失败，请检查是否是dalamud.log。', 'error')
            return redirect(url_for('front._upload_dalamud_log', form=upload_form))
    flash('请将分析后的网页地址复制给相关人员，链接有效期为一天。', 'info')
    return render_template(r'user/upload_dalamud_log.html', form=upload_form)


@front.get('/log/<short_url>')
def _log_result_short(short_url):
    redis_result = read_log_short_url(short_url)
    if redis_result is not None:
        try:
            msg = json.loads(base64.urlsafe_b64decode(redis_result))
            return jsonify(msg)
        except:
            return jsonify({'msg': '短网址对应的存储信息有误'}), 400
    else:
        return jsonify({'msg': '短网址不存在'}), 404
