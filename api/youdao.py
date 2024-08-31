# -*- coding: utf-8 -*-
import json
import sys
import uuid
import requests
import hashlib
from importlib import reload

import time

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translate(text="Hello", APP_KEY='', APP_SECRET='',*args):
    data = {'from': 'auto', 'to': 'zh-CHS', 'signType': 'v3'}
    current_time = str(int(time.time()))
    data['curtime'] = current_time
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(text) + salt + current_time + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = text
    data['salt'] = salt
    data['sign'] = sign
    data['domain'] = 'game'
    # data['vocabId'] = "9E24A4397FD345ADAD330DF0F803D1B9"

    response = do_request(data)
    # print(str(response.content))
    ret = json.loads(str(response.content, encoding='utf-8'))
    # print(str(ret))
    if str(ret['errorCode']) == '0':
        return ret['translation'][0]
    else:
        return "API错误，错误代码" + ret['errorCode']
