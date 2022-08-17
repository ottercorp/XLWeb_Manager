# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/6/12 17:36
# @Author  : subjadeites
# @File    : analytics.py
import requests

from . import front, auth


@front.route('/analytics')
@auth.login_required
def _analytics():
    r = requests.get("http://localhost:3000/goto/uhhVP8C7z?orgId=1", allow_redirects=True)
    return r.content
