import json
from datetime import datetime, timedelta

import requests
from loguru import logger

from common.config import dz_test_appKey, dz_test_secret, dz_onl_appKey, dz_onl_secret

token_url = 'https://api.dingtalk.com/v1.0/oauth2/accessToken'
push_url = 'https://api.dingtalk.com/v1.0/robot/groupMessages/send'
card_url = 'https://api.dingtalk.com/v1.0/im/v1.0/robot/interactiveCards/send'

access_token = ''
expire_time = datetime.now()


def get_access_token(is_onl):
    # if not is_onl:
    #     return '5222eb8bdec430688b196112fa600d60'
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
        logger.info("get_access_token: body_param = {}, res = {}", json.dumps(body_param), json.dumps(response))
        return access_token


def push_dingding_text(content: str, open_conversation_id: str, robot_code: str, is_onl):
    headers = {'x-acs-dingtalk-access-token': get_access_token(is_onl)}
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


def push_dingding_markdown(title: str, text: str, open_conversation_id: str, robot_code: str, is_onl):
    headers = {'x-acs-dingtalk-access-token': get_access_token(is_onl)}
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
    logger.info("push_dingding_markdown: body_param = {}, res = {}", json.dumps(body_param), json.dumps(response))
    return True


def push_dingding_action_card(title: str, text: str, single_title: str,
                              single_utl: str, open_conversation_id: str, robot_code: str, is_onl):
    headers = {'x-acs-dingtalk-access-token': get_access_token(is_onl)}
    body_param = {
        "msgParam": json.dumps({
            "title": title,
            "text": text,
            "singleTitle": single_title,
            "singleURL": single_utl
        }),
        "msgKey": "sampleActionCard",
        "openConversationId": open_conversation_id,
        "robotCode": robot_code
    }
    response = requests.post(push_url, json=body_param, headers=headers).json()
    logger.info("push_dingding_text: body_param = {}, res = {}", json.dumps(body_param), json.dumps(response))
    return True


def push_dingding_alert_interactive_card(title: str, keyword: str, service: str, suggest: str,
                                         open_conversation_id: str, robot_code: str, conversation_type, is_onl):
    card_data = {
        "config": {
            "autoLayout": True,
            "enableForward": True
        },
        "header": {
            "title": {
                "type": "text",
                "text": "报警查询"
            },
            "logo": "@lALPDefR3hjhflFAQA"
        },
        "contents": [
            {
                "type": "markdown",
                "text": "***" + title + "***",
                "id": "markdown_1724120468090"
            },
            {
                "type": "markdown",
                "text": "**报警关键字**: " + keyword.strip('\'').replace('\"', '\''),
                "id": "markdown_1724120468121"
            },
            {
                "type": "markdown",
                "text": "**服务名称**: " + service,
                "id": "markdown_1724120468134"
            },
            {
                "type": "markdown",
                "text": "**处理建议**: " + suggest,
                "id": "markdown_1724120468134"
            },
            {
                "type": "markdown",
                "text": "<font size=12 color=common_level3_base_color>查看更多报警请点击下方按钮</font>",
                "id": "markdown_1724120468104"
            },
            {
                "type": "action",
                "actions": [
                    {
                        "type": "button",
                        "label": {
                            "type": "text",
                            "text": "查看更多",
                            "id": "text_1724120468090"
                        },
                        "actionType": "openLink",
                        "url": {
                            "all": "https://alidocs.dingtalk.com/i/nodes/7NkDwLng8ZKnmbyoI2M5d2qgWKMEvZBY?doc_type=wiki_notable&iframeQuery=sheetId%3DEb2uBae%26viewId%3DEBj8lcX&rnd=0.4613281523659043"
                        },
                        "status": "normal",
                        "id": "button_1647166782413"
                    }
                ],
                "id": "action_1724120468090"
            }
        ]
    }
    return push_dingding_interactive_card(card_data, open_conversation_id, robot_code, conversation_type, is_onl)


def push_dingding_interactive_card(card_data, open_conversation_id: str, robot_code: str, conversation_type, is_onl):
    headers = {'x-acs-dingtalk-access-token': get_access_token(is_onl)}
    body_param = {
        "cardData": json.dumps(card_data),
        "cardTemplateId": 'StandardCard',
        "robotCode": robot_code,
        "cardBizId": 'bz_' + datetime.now().strftime('%Y%m%d%H%M%S')
    }
    if conversation_type == '1':
        body_param['singleChatReceiver'] = open_conversation_id
    else:
        body_param['openConversationId'] = open_conversation_id
    response = requests.post(card_url, json=body_param, headers=headers).json()
    logger.info("push_dingding_interactive_card: body_param = {}, res = {}", json.dumps(body_param),
                json.dumps(response))
    return True


if __name__ == '__main__':
    # push_dingding_markdown('hahaha', text, 'cid3Ecerb4D29JTp+iecXtA8w==', 'dingsbksjfhqhdlsq3pe', False)
    push_dingding_alert_interactive_card('报警', "content: \'dada\'", "1", "1", 'cid3Ecerb4D29JTp+iecXtA8w==', 'dingsbksjfhqhdlsq3pe',
                                         1,
                                         False)
