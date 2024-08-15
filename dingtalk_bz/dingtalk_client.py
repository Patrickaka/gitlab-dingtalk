import json
from datetime import datetime, timedelta

import requests
from loguru import logger

from common.config import dz_test_appKey, dz_test_secret, dz_onl_appKey, dz_onl_secret
from event_handler import is_onl

token_url = 'https://api.dingtalk.com/v1.0/oauth2/accessToken'
push_url = 'https://api.dingtalk.com/v1.0/robot/groupMessages/send'

access_token = ''
expire_time = datetime.now()


def get_access_token():
    global access_token, expire_time
    current_time = datetime.now()
    if access_token and current_time < expire_time:
        return access_token
    else:
        body_param = {
            "appKey": dz_onl_appKey if is_onl else dz_test_appKey,
            "appSecret": dz_onl_secret if is_onl else dz_test_secret
        }
        response = requests.post(token_url, json=body_param).json()
        new_time = current_time + timedelta(seconds=response['expireIn'])
        expire_time = new_time
        access_token = response['accessToken']
        return access_token


def push_dingding_text(content: str, open_conversation_id: str, robot_code: str):
    headers = {'x-acs-dingtalk-access-token': get_access_token()}
    body_param = {
        "msgParam": json.dumps({
            "content": content
        }),
        "msgKey": "sampleText",
        "openConversationId": open_conversation_id,
        "robotCode": robot_code
    }
    response = requests.post(push_url, json=body_param, headers=headers).json()
    logger.info("push_dingding_text: body_param = {}, res = {}", json.dumps(body_param), json.dumps(response))
    return True


def push_dingding_markdown(title: str, text: str, open_conversation_id: str, robot_code: str):
    headers = {'x-acs-dingtalk-access-token': get_access_token()}
    body_param = {
        "msgParam": json.dumps({
            "title": title,
            "text": text
        }),
        "msgKey": "sampleMarkdown",
        "openConversationId": open_conversation_id,
        "robotCode": robot_code
    }
    response = requests.post(push_url, json=body_param, headers=headers).json()
    logger.info("push_dingding_text: body_param = {}, res = {}", json.dumps(body_param), json.dumps(response))
    return True


if __name__ == '__main__':
    push_dingding_text('hahaha', 'cid3Ecerb4D29JTp+iecXtA8w==', 'dingsbksjfhqhdlsq3pe')
