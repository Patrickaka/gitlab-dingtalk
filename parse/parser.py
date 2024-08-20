import json
from typing import Dict, Any

from loguru import logger

from common import config
from dingtalk_bz import dingtalk_client
from error_log.parse_error_log import get_alert_info


def page_bind_response(open_conversation_id: str, robot_code: str, is_onl):
    logger.info("success_response: open_conversation_id = {}, robot_code = {}", open_conversation_id, robot_code)
    dingtalk_client.push_dingding_text('绑定成功 请稍等1-5分钟查看', open_conversation_id, robot_code, is_onl)
    return True


def alert_query_response(alert_type, open_conversation_id: str, robot_code: str, conversation_type, is_onl):
    logger.info("success_response: open_conversation_id = {}, robot_code = {}", open_conversation_id, robot_code)
    alert_info = get_alert_info(alert_type)
    dingtalk_client.push_dingding_alert_interactive_card(alert_info['title'], alert_info['key_word'],
                                                         alert_info['service'],
                                                         alert_info['suggest'], open_conversation_id,
                                                         robot_code, conversation_type, is_onl)
    return True


def error_response(open_conversation_id: str, robot_code: str, is_onl):
    logger.info("error_response: open_conversation_id = {}, robot_code = {}", open_conversation_id, robot_code)
    dingtalk_client.push_dingding_text('指令错误 请使用#help查看可用指令', open_conversation_id, robot_code, is_onl)
    return True


def help_response(open_conversation_id: str, robot_code: str, conversation_type, is_onl):
    dingtalk_client.push_dingding_interactive_card(config.help_card_data, open_conversation_id, robot_code,
                                                   conversation_type, is_onl)
    return True


def parse_event(event: Dict[str, Any], is_onl):
    logger.info("parse_event: event = {}", json.dumps(event))
    open_conversation_id = event['conversationId']
    conversation_type = event['conversationType']
    robot_code = event['robotCode']
    content = event['text']['content'].strip()
    content_arr = content.split(" ")
    instruction = content_arr[0]
    if not instruction.startswith('#'):
        error_response(open_conversation_id, robot_code, is_onl)
    if instruction == "#页面绑定" or instruction == "#2":
        # todo 调用接口
        page_bind_response(open_conversation_id, robot_code, is_onl)
    if instruction == "#报警查询" or instruction == "#1":
        alert_type = content_arr[1]
        alert_query_response(alert_type, open_conversation_id, robot_code, conversation_type, is_onl)
    elif instruction == "#help":
        help_response(open_conversation_id, robot_code, conversation_type, is_onl)
