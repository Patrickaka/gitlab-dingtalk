import json
from typing import Dict, Any

from loguru import logger

from dingtalk_bz import dingtalk_client
from error_log.parse_error_log import get_alert_info


def page_bind_response(open_conversation_id: str, robot_code: str, is_onl):
    logger.info("success_response: open_conversation_id = {}, robot_code = {}", open_conversation_id, robot_code)
    dingtalk_client.push_dingding_text('绑定成功 请稍等1-5分钟查看', open_conversation_id, robot_code, is_onl)
    return True


def build_alert_text(alert_info):
    return ("关键字:" + alert_info['key_word'] + "\n" +
            "服务:" + alert_info['service'] + "\n" +
            "建议:" + alert_info['suggest'])


def alert_query_response(alert_type, open_conversation_id: str, robot_code: str, is_onl):
    logger.info("success_response: open_conversation_id = {}, robot_code = {}", open_conversation_id, robot_code)
    alert_info = get_alert_info(alert_type)
    # dingtalk_client.push_dingding_markdown(alert_info['title'], "# 一级标题\n## 二级标题", open_conversation_id, robot_code,
    #                                        is_onl)
    dingtalk_client.push_dingding_action_card(alert_info['title'],
                                              build_alert_text(alert_info),
                                              "查看全部报警",
                                              "https://alidocs.dingtalk.com/i/nodes/7NkDwLng8ZKnmbyoI2M5d2qgWKMEvZBY?doc_type=wiki_notable&iframeQuery=sheetId%3DEb2uBae%26viewId%3DEBj8lcX&rnd=0.4209990224605611",
                                              open_conversation_id,
                                              robot_code, is_onl)
    return True


def error_response(open_conversation_id: str, robot_code: str, is_onl):
    logger.info("error_response: open_conversation_id = {}, robot_code = {}", open_conversation_id, robot_code)
    dingtalk_client.push_dingding_text('指令错误 请使用#help查看可用指令', open_conversation_id, robot_code, is_onl)
    return True


def help_response(open_conversation_id: str, robot_code: str, is_onl):
    from common.help import build_help_text
    dingtalk_client.push_dingding_text(build_help_text(), open_conversation_id, robot_code, is_onl)
    return True


def parse_event(event: Dict[str, Any], is_onl):
    logger.info("parse_event: event = {}", json.dumps(event))
    open_conversation_id = event['conversationId']
    robot_code = event['robotCode']
    content = event['text']['content'].strip()
    content_arr = content.split(" ")
    instruction = content_arr[0]
    if not instruction.startswith('#'):
        error_response(open_conversation_id, robot_code, is_onl)
    if instruction == "#页面绑定":
        # todo 调用接口
        page_bind_response(open_conversation_id, robot_code, is_onl)
    if instruction == "#报警查询":
        alert_type = content_arr[1]
        alert_query_response(alert_type, open_conversation_id, robot_code, is_onl)
    elif instruction == "#help":
        help_response(open_conversation_id, robot_code, is_onl)
