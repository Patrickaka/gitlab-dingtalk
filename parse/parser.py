import json
from typing import Dict, Any

from loguru import logger

from dingtalk_bz import dingtalk_client


def page_bind_response(open_conversation_id: str, robot_code: str):
    logger.info("success_response: open_conversation_id = {}, robot_code = {}", open_conversation_id, robot_code)
    dingtalk_client.push_dingding_text('绑定成功 请稍等1-5分钟查看', open_conversation_id, robot_code)
    return True


def error_response(open_conversation_id: str, robot_code: str):
    logger.info("error_response: open_conversation_id = {}, robot_code = {}", open_conversation_id, robot_code)
    dingtalk_client.push_dingding_text('指令错误 请使用#help查看可用指令', open_conversation_id, robot_code)
    return True


def help_response(open_conversation_id: str, robot_code: str):
    dingtalk_client.push_dingding_text('指令错误 请使用#help查看可用指令', open_conversation_id, robot_code)
    return True


def parse_event(event: Dict[str, Any]):
    logger.info("parse_event: event = {}", json.dumps(event))
    open_conversation_id = event['conversationId']
    robot_code = event['robotCode']
    content = event['text']['content'].strip()
    content_arr = content.split(" ")
    instruction = content_arr[0]
    if not instruction.startswith('#'):
        error_response(open_conversation_id, robot_code)
    if instruction == "#页面绑定":
        # todo 调用接口
        page_bind_response(open_conversation_id, robot_code)
    elif instruction == "#help":
        help_response(open_conversation_id, robot_code)
