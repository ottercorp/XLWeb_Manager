# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/19 17:53
# @File    : log_analysis.py
from flask import request
from flask_restful import Resource, marshal_with

from app.utils.dalamud_log_analysis import analysis
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
            return DefaultApiResponse(data=None, message='分析失败，请确定日志文件是否是dalamud.log', code=500), 500
        return DefaultApiResponse(data=msg)


api.add_resource(LogAnalysis, '/logAnalysis', endpoint="logAnalysis")
