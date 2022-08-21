# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/8/19 17:53
# @File    : log_analysis.py
from flask import request
from flask_restful import Resource, fields, marshal_with

from . import api
from app.utils.dalamud_log_analysis import analysis


class LogAnalysis(Resource):
    """日志分析接口"""

    @marshal_with(fields={
        'message': fields.Raw,
        'status': fields.Integer,
        'task': fields.String,
    }
    )
    def post(self):
        """分析日志方法"""
        file_object = request.files['file']
        try:
            msg = analysis(file_object)
        except BaseException:
            return {'message': '分析失败，请确定日志文件是否是dalamud.log', 'status': 500, 'task': 'dalamud日志分析'}, 500
        return {'message': msg, 'status': 200, 'task': 'dalamud日志分析'}


api.add_resource(LogAnalysis, '/logAnalysis', endpoint="logAnalysis")
