# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/19 17:53
# @File    : log_analysis.py
import base64
import json

from flask import request
from flask_restful import Resource, marshal_with

from app.utils.dalamud_log_analysis import analysis
from redis_db import read_log_short_url
from . import api, resource_fields, DefaultApiResponse


class LogAnalysis(Resource):
    """日志分析接口"""

    @marshal_with(resource_fields)
    def post(self):
        """分析日志方法"""
        file_object = request.files['file']
        try:
            msg = analysis(file_object)
        except BaseException:
            return DefaultApiResponse(data=None, message='分析失败，请确定日志文件是否是dalamud.log', code=202), 202
        return DefaultApiResponse(data=msg)

    @marshal_with(resource_fields)
    def get(self):
        """从短网址获取日志分析结果"""
        short_url = request.args.get('short_url')
        redis_result = read_log_short_url(short_url)
        if redis_result is not None:
            try:
                msg = json.loads(base64.urlsafe_b64decode(redis_result))
                return DefaultApiResponse(data=msg)
            except:
                return DefaultApiResponse(data=None, message='短网址对应的存储信息有误', code=400), 400
        else:
            return DefaultApiResponse(data=None, message='短网址不存在', code=404), 404


api.add_resource(LogAnalysis, '/logAnalysis', endpoint="logAnalysis")
