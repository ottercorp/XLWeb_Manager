# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/10/12 21:15
# @File    : daily_clean_logs_cache.py

import os
from datetime import datetime

import redis_db

# 遍历/cache/upload_logs目录下的所有文件
for root, dirs, files in os.walk("../cache/upload_logs"):
    # 查询文件名去掉.log是否在redis中
    for file in files:
        if file[:-4] in redis_db.get_keys():
            pass
        else:
            os.remove(f'../cache/upload_logs/{file}')
            print(f"[{datetime.today()}] 删除文件：{file}")
