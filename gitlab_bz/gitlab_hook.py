from typing import Dict, Any

from model.DIndtalkModel import DingTalkMessage
from dingtalk_bz.dingtalk_client import push_dingding


def pipeline_hook(event: Dict[str, Any], mysql_client):
    body = DingTalkMessage()
    body.msgtype = "markdown"
    body.at.atUserIds = mysql_client.find_at_user(event['project']['id'])
    body.markdown.title = event['project']['name'] + " pipeline"
    build_message = ""
    for build in event['builds']:
        sub_build_msg = "### stage: " + build['stage'] + "\n" + \
                        "- **name**: " + build['name'] + "\n " + \
                        "- **status**: " + build['status'] + "\n "
        if build['failure_reason'] is not None:
            sub_build_msg += "- **failure_reason**: " + build['failure_reason'] + "\n "
        build_message += sub_build_msg
    body.markdown.text = "### " + event['project']['name'] + " pipeline\n " + build_message
    push_dingding(body)


def job_hook(event: Dict[str, Any], mysql_client):
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
