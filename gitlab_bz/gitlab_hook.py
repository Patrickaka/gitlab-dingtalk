from typing import Dict, Any

from common import project_info
from connect import mysql_client
from model.DIndtalkModel import DingTalkMessage
from dingtalk_bz.dingtalk_client import push_dingding, build_text_DingTalkMessage


def pipeline_hook(event: Dict[str, Any]):
    body = DingTalkMessage()
    body.msgtype = "markdown"
    body.at.atUserIds = [mysql_client.find_at_user(event['project']['id'])]
    body.markdown.title = event['project']['name'] + " pipeline"
    build_message = ""
    for build in event['builds']:
        if build['status'] == 'success' or build['failure_reason'] is not None:
            build_message += "### stage: " + build['stage'] + "\n" + \
                             "- **name**: " + build['name'] + "\n " + \
                             "- **status**: " + build['status'] + "\n "
        else:
            return
        if build['failure_reason'] is not None:
            build_message += "- **failure_reason**: " + build['failure_reason'] + "\n "
    body.markdown.text = "### " + event['project']['name'] + " pipeline\n " + build_message
    push_dingding(body)


def pipeline_hook_v2(event: Dict[str, Any]):
    at_user = mysql_client.find_at_user(event['project']['id'])
    success = False
    failure = False
    failure_reason = ""
    for build in event['builds']:
        if build['status'] == 'success':
            success = True
        else:
            success = False
        if build['failure_reason'] is not None:
            failure = True
            failure_reason += failure_reason + "\n"
    if success:
        content = (f"「{event['project']['description']} - {event['project']['name']}」"
                   f"上线成功: {event['object_attributes']['ref']}")
        push_dingding(build_text_DingTalkMessage(at_user, content))
    elif failure:
        pipeline_url = project_info.pipeline_dict.get(event['project']['id'], "")
        content = (f"「{event['project']['description']} - {event['project']['name']}」"
                   f"上线失败: {event['object_attributes']['ref']}，状态: {failure_reason}, 详情: {pipeline_url}")
        push_dingding(build_text_DingTalkMessage(at_user, content))


def job_hook(event: Dict[str, Any]):
    body = DingTalkMessage()
    body.msgtype = "markdown"
    body.markdown.title = event['project_name'] + " " + event['build_name'] + " job"
    project_id = event['project_id']
    body.at.atUserIds = mysql_client.find_at_user(project_id)
    build_message = ""
    sub_build_msg = "- **stage**: " + event['build_stage'] + "\n " + \
                    "- **status**: " + event['build_status'] + "\n "
    if event['build_failure_reason'] is not None and 'unknown_failure' != event['build_failure_reason']:
        sub_build_msg += "- **failure_reason**: " + event['build_failure_reason'] + "\n "
    build_message += sub_build_msg
    body.markdown.text = "### " + event['project_name'] + " " + event['build_name'] + " job\n " + build_message
    push_dingding(body)
