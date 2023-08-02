import logging
from typing import Dict, Any

from common import project_info
from common.project import Pipeline
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
            build_message += "# ## stage: " + build['stage'] + "\n" + \
                             "- **name**: " + build['name'] + "\n " + \
                             "- **status**: " + build['status'] + "\n "
        else:
            return
        if build['failure_reason'] is not None:
            build_message += "- **failure_reason**: " + build['failure_reason'] + "\n "
    body.markdown.text = "### " + event['project']['name'] + " pipeline\n " + build_message
    push_dingding(body)


def pipeline_hook_v2(event: Dict[str, Any]):
    project = mysql_client.find_project_by_project_id(event['project']['id'])
    if not project:
        logging.error("项目未配置")
        return
    success = True
    failure = False
    rollback = False
    failure_reason = ""
    for build in event['builds']:
        if build['status'] != 'success':
            success = False
        if build['name'] == 'rollback_prod_job':
            rollback = True
        if build['failure_reason'] is not None:
            failure = True
            failure_reason += build['failure_reason'] + "\n"
    ci_type = "回滚" if rollback else "上线"
    if success:
        content = (f"「{project[2]} - {event['project']['name']}」"
                   f"{ci_type}成功: {event['object_attributes']['ref']}")
        push_dingding(build_text_DingTalkMessage(project[5], content))
    elif failure:
        pipeline_url = project_info.pipeline_dict.get(event['project']['id'], Pipeline()).pipeline_url
        ref = project_info.pipeline_dict.get(event['project']['id'], Pipeline()).ref or event['object_attributes']['ref']
        content = (f"「{project[2]} - {event['project']['name']}」"
                   f"{ci_type}失败: {ref}，原因: {failure_reason}, 详情: {pipeline_url}")
        push_dingding(build_text_DingTalkMessage(project[5], content))


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
