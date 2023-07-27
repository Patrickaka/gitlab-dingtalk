import base64
import hashlib
import hmac
import json
import logging
import time
import urllib.parse

import requests

from model.DIndtalkModel import DingTalkMessage

push_url = 'https://oapi.dingtalk.com/robot/send?' \
           'access_token=4e2c88202dd673d7fae086bedcd653069c264b33a3c90423666d8957f6d3ba0d'
secret = 'byWSibxjgPA4-q6gi9dDOvdGrYfv2xvkLwN9PDxeSJw9sriWzJA7TbbpaqxMA7g_'


def convert_to_dict(obj):
    if isinstance(obj, dict):
        data = {}
        for key, value in obj.items():
            data[key] = convert_to_dict(value)
        return data
    elif hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            data[key] = convert_to_dict(value)
        return data
    elif isinstance(obj, list):
        data = []
        for item in obj:
            data.append(convert_to_dict(item))
        return data
    else:
        return obj


def cal_sign(timestamp: str, encode: bool) -> str:
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    if encode:
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    else:
        sign = base64.b64encode(hmac_code).decode('utf-8')
    logging.info(f"dingtalk cal_sign = {sign}")
    return sign


def push_dingding(body: DingTalkMessage):
    headers = {'Content-Type': 'application/json'}
    timestamp = str(round(time.time() * 1000))
    sign = cal_sign(timestamp, True)
    new_push_url = push_url + "&timestamp=" + timestamp + "&sign=" + sign
    body_dict = convert_to_dict(vars(body))
    response = requests.post(new_push_url, data=json.dumps(body_dict), headers=headers)
    print(response)
    return True


def build_text_DingTalkMessage(at_user, content):
    body = DingTalkMessage()
    body.msgtype = "text"
    body.text.content = content
    body.at.atUserIds = [at_user]
    return body


if __name__ == '__main__':
    cal_sign('1690265116', False)
