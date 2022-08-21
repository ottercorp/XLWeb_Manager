# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import time

import requests
import urllib3

urllib3.disable_warnings()

# 默认HOST
HOST = "open.ctcdn.cn"
try:
    with open(r'appsettings.json', 'r') as f:
        appsettings = json.load(f)
        # 用户的AK\SK 可以自行申请
        AK = appsettings['Ct_CDN_AK']
        SK = appsettings['Ct_CDN_SK']
except FileNotFoundError:
    print("appsettings.json not found")
    exit()
except KeyError:
    print("appsettings.json not correct")
    exit()
except json.decoder.JSONDecodeError:
    print("appsettings.json not correct")
    exit()
except Exception as e:
    print(e)
    exit()

# 默认控制方式
AC = "app"


def encode(key, content):
    """
    sha(secure hash algorithm)
    :param key: 用来加密的key
    :param content: 需要加密的数据
    :return: 密文
    """
    h = hmac.new(
        # base64安全加密，对齐位数
        base64.urlsafe_b64decode(key + "==="),
        content.encode(),
        hashlib.sha256
    )
    signature = base64.urlsafe_b64encode(h.digest()).decode().replace("=", "")
    return signature


def do_get(path):
    """
    构造请求体，发送请求
    注意：uri里必须包含请求参数
    :return:
    """
    # 当前时间戳，单位毫秒
    now = str(int(round(time.time() * 1000)))
    sign_str = AK + "\n" + now + "\n" + path
    t_now = int(int(now) / 86400000)
    # 首次encode
    tem_signature = encode(SK, AK + ":" + str(t_now))
    # 再次encode
    signature = encode(tem_signature, sign_str)
    # 固定的请求头部
    headers = {
        "x-alogic-now": now,
        "x-alogic-app": AK,
        "x-alogic-signature": signature,
        "x-alogic-ac": AC
    }
    url = "https://{}{}".format(HOST, path)
    response = requests.get(url, headers=headers, verify=False)
    msg = response.json()["message"]
    if msg == 'success':
        return (msg, 'info')
    else:
        return (msg, 'error')


def do_post(path, params):
    """
    构造请求体，发送请求
    :return:
    """
    # 当前时间戳，单位毫秒
    now = str(int(round(time.time() * 1000)))
    sign_str = AK + "\n" + now + "\n" + path
    t_now = int(int(now) / 86400000)
    # 首次encode
    tem_signature = encode(SK, AK + ":" + str(t_now))
    # 再次encode
    signature = encode(tem_signature, sign_str)
    # 固定的请求头部
    headers = {
        "x-alogic-now": now,
        "x-alogic-app": AK,
        "x-alogic-signature": signature,
        "x-alogic-ac": AC
    }
    url = "https://{}{}".format(HOST, path)
    response = requests.post(url, data=json.dumps(
        params), headers=headers, verify=False)
    msg = response.json()["message"]
    if msg == 'success':
        return (msg, 'info')
    else:
        return (msg, 'error')


def refresh(type: int, urls: list):
    """刷新任务创建

    Args:
        type (int): 刷新类型，必须,类型说明: 1. url2. 目录dir 3.正则匹配re (数字类型)
        urls (list): 刷新参数值，必须，数组格式；刷新类型为url时单次最多1000条，类型为dir和re时单次最多50条。 (数组类型)
    """
    path = "/v1/refreshmanage/create"
    params = {
        "values": urls,
        "task_type": type
    }
    return do_post(path, params)


def preload(urls: list):
    """预取任务创建

    Args:
        urls (list): 预取文件列表，数组格式，单次最多50条。如域名有做防盗链配置，则相应的预取url需同样带有防盗链。 (数组类型)
    """
    path = "/v1/preloadmanage/create"
    params = {
        "values": urls,
    }
    return do_post(path, params)


def flow_packet():
    """剩余流量包查询
    """
    path = "/v1/order/flow-packet"
    params = ""

    return do_get(path)


def top_url():
    path = "/v1/top_url"
    params = {"domain": ["aonyx.ffxiv.wang"],
              "top_rank": 100,
              "start_time": int(time.time()) - 3600 * 24,
              "end_time": int(time.time())}
    return do_post(path, params)
