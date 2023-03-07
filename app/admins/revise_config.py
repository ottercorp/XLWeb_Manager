# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/6/12 17:15
# @Author  : subjadeites
# @File    : revise_config.py

import json
import subprocess
import time

from flask import render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, IntegerField, URLField
from wtforms.validators import DataRequired, URL, NumberRange

from . import admins, auth

xlweb_config_path = r'/www/wwwroot/XLWebServices-fastapi/.env'


class Config_Form(FlaskForm):
    Logging_LogLevel_Default = StringField('LogLevel_Default', validators=[DataRequired()])
    Logging_LogLevel_Microsoft_AspNetCore = StringField('LogLevel_MS.AspNetCore',
                                                        validators=[DataRequired()])
    ConnectionStrings_Redis = StringField('ConnectionStrings_Redis', validators=[DataRequired()])
    Auth_GitHubToken = StringField('Auth_GitHubToken', validators=[DataRequired()])
    AllowedHosts = StringField('AllowedHosts', validators=[DataRequired()])
    ReleaseEnabled = RadioField('ReleaseEnabled', choices=["True", "False"], validators=[DataRequired()])
    CacheClearKey = StringField('CacheClearKey', validators=[DataRequired()])
    GitHub_LauncherRepository_Owner = StringField('LauncherRepository_Owner', validators=[DataRequired()])
    GitHub_LauncherRepository_Name = StringField('LauncherRepository_Name', validators=[DataRequired()])
    GitHub_PluginRepository_Owner = StringField('PluginRepository_Owner', validators=[DataRequired()])
    GitHub_PluginRepository_Name = StringField('PluginRepository_Name', validators=[DataRequired()])
    GitHub_DalamudRepository_Owner = StringField('DalamudRepository_Owner', validators=[DataRequired()])
    GitHub_DalamudRepository_Name = StringField('DalamudRepository_Name', validators=[DataRequired()])
    GitHub_AssetRepository_Owner = StringField('AssetRepository_Owner', validators=[DataRequired()])
    GitHub_AssetRepository_Name = StringField('AssetRepository_Name', validators=[DataRequired()])
    GitHub_DistribRepository_Owner = StringField('DistribRepository_Owner', validators=[DataRequired()])
    GitHub_DistribRepository_Name = StringField('DistribRepository_Name', validators=[DataRequired()])
    TemplateDownload = URLField('TemplateDownload', validators=[DataRequired(), URL()])
    TemplateUpdate = URLField('TemplateUpdate', validators=[DataRequired(), URL()])
    PluginMaster = URLField('PluginMaster', validators=[DataRequired(), URL()])
    RuntimeHashesUrl = URLField('RuntimeHashesUrl', validators=[DataRequired(), URL()])
    PluginRepoBranch = StringField('PluginRepoBranch', validators=[DataRequired()])
    BannedPlugin = URLField('BannedPlugin', validators=[DataRequired(), URL()])
    ApiLevel = IntegerField('ApiLevel', validators=[DataRequired(), NumberRange(min=5, max=6)])
    HostedUrl = URLField('HostedUrl', validators=[DataRequired(), URL()])
    FileCacheDirectory = StringField('FileCacheDirectory', validators=[DataRequired()])
    submit = SubmitField("修改")


@admins.route('/config', methods=['GET', 'POST'])
@auth.login_required
def _config():
    try:
        with open(xlweb_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        file_path = r'/www/XLWebServices/appsettings.json'
    except FileNotFoundError:
        with open(r'./tests/appsettings.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        file_path = r'./tests/appsettings.json'
    form = Config_Form()
    if request.method == 'GET':
        form.Logging_LogLevel_Default.data = config['Logging']['LogLevel']['Default']
        form.Logging_LogLevel_Microsoft_AspNetCore.data = config['Logging']['LogLevel']['Microsoft.AspNetCore']
        form.ConnectionStrings_Redis.data = config['ConnectionStrings']['Redis']
        form.Auth_GitHubToken.data = config['Auth']['GitHubToken']
        form.AllowedHosts.data = config['AllowedHosts']
        form.ReleaseEnabled.data = str(config['ReleaseEnabled'])
        form.CacheClearKey.data = config['CacheClearKey']
        form.GitHub_LauncherRepository_Owner.data = config['GitHub']['LauncherRepository']['Owner']
        form.GitHub_LauncherRepository_Name.data = config['GitHub']['LauncherRepository']['Name']
        form.GitHub_PluginRepository_Owner.data = config['GitHub']['PluginRepository']['Owner']
        form.GitHub_PluginRepository_Name.data = config['GitHub']['PluginRepository']['Name']
        form.GitHub_DalamudRepository_Owner.data = config['GitHub']['DalamudRepository']['Owner']
        form.GitHub_DalamudRepository_Name.data = config['GitHub']['DalamudRepository']['Name']
        form.GitHub_AssetRepository_Owner.data = config['GitHub']['AssetRepository']['Owner']
        form.GitHub_AssetRepository_Name.data = config['GitHub']['AssetRepository']['Name']
        form.GitHub_DistribRepository_Owner.data = config['GitHub']['DistribRepository']['Owner']
        form.GitHub_DistribRepository_Name.data = config['GitHub']['DistribRepository']['Name']
        form.TemplateDownload.data = config['TemplateDownload']
        form.TemplateUpdate.data = config['TemplateUpdate']
        form.PluginMaster.data = config['PluginMaster']
        form.RuntimeHashesUrl.data = config['RuntimeHashesUrl']
        form.PluginRepoBranch.data = config['PluginRepoBranch']
        form.BannedPlugin.data = config['BannedPlugin']
        form.ApiLevel.data = int(config['ApiLevel'])
        form.HostedUrl.data = config['HostedUrl']
        form.FileCacheDirectory.data = config['FileCacheDirectory']
    if form.validate_on_submit():
        file_path_backup = rf'/www/XLWebServices/appsettings.{int(time.time())}.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        with open(file_path_backup, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        with open(file_path, 'w', encoding='utf-8') as f:
            config['Logging']['LogLevel']['Default'] = form.Logging_LogLevel_Default.data
            config['Logging']['LogLevel']['Microsoft.AspNetCore'] = form.Logging_LogLevel_Microsoft_AspNetCore.data
            config['ConnectionStrings']['Redis'] = form.ConnectionStrings_Redis.data
            config['Auth']['GitHubToken'] = form.Auth_GitHubToken.data
            config['AllowedHosts'] = form.AllowedHosts.data
            config['ReleaseEnabled'] = eval(form.ReleaseEnabled.data)
            config['CacheClearKey'] = form.CacheClearKey.data
            config['GitHub']['LauncherRepository']['Owner'] = form.GitHub_LauncherRepository_Owner.data
            config['GitHub']['LauncherRepository']['Name'] = form.GitHub_LauncherRepository_Name.data
            config['GitHub']['PluginRepository']['Owner'] = form.GitHub_PluginRepository_Owner.data
            config['GitHub']['PluginRepository']['Name'] = form.GitHub_PluginRepository_Name.data
            config['GitHub']['DalamudRepository']['Owner'] = form.GitHub_DalamudRepository_Owner.data
            config['GitHub']['DalamudRepository']['Name'] = form.GitHub_DalamudRepository_Name.data
            config['GitHub']['AssetRepository']['Owner'] = form.GitHub_AssetRepository_Owner.data
            config['GitHub']['AssetRepository']['Name'] = form.GitHub_AssetRepository_Name.data
            config['GitHub']['DistribRepository']['Owner'] = form.GitHub_DistribRepository_Owner.data
            config['GitHub']['DistribRepository']['Name'] = form.GitHub_DistribRepository_Name.data
            config['TemplateDownload'] = form.TemplateDownload.data
            config['TemplateUpdate'] = form.TemplateUpdate.data
            config['PluginMaster'] = form.PluginMaster.data
            config['RuntimeHashesUrl'] = form.RuntimeHashesUrl.data
            config['PluginRepoBranch'] = form.PluginRepoBranch.data
            config['BannedPlugin'] = form.BannedPlugin.data
            config['ApiLevel'] = form.ApiLevel.data
            config['HostedUrl'] = form.HostedUrl.data
            config['FileCacheDirectory'] = form.FileCacheDirectory.data
            json.dump(config, f, indent=4)
            flash('修改成功！正在重启XLWebServices。', 'info')
        subprocess.getoutput("systemctl restart XLWebServices")
        return render_template('admin/config.html', form=form, message='Config saved!')
    return render_template('admin/config.html', form=form)
