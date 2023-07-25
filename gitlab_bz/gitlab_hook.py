from typing import Dict, Any

from common import projects
from model.DIndtalkModel import DingTalkMessage
from dingtalk_bz.dingtalk_client import push_dingding


def pipeline_hook(event: Dict[str, Any]):
    body = DingTalkMessage()
    body.msgtype = "markdown"
    body.markdown.title = event['project']['name'] + " pipeline"
    build_message = ""
    for build in event['builds']:
        sub_build_msg = "- **stage**: <br>" + build['stage'] + "\n name = " + build['name'] + \
                        " status = " + build['status'] + "\n "
        if build['failure_reason'] is not None:
            sub_build_msg += " failure_reason = " + build['failure_reason'] + "\n "
        build_message += sub_build_msg
    body.markdown.text = "### " + event['project']['name'] + " pipeline\n " + "### build info\n " + build_message
    push_dingding(body)


def job_hook(event: Dict[str, Any]):
    body = DingTalkMessage()
    body.msgtype = "markdown"
    body.markdown.title = event['project_name'] + " " + event['build_name'] + " job"
    project_id = event['project_id']
    if project_id in projects.pipeline_dict:
        body.at.atUserIds = [projects.pipeline_dict.get(project_id)]
    build_message = ""
    sub_build_msg = "- **stage**: <br>" + event['build_stage'] + "\n " + \
                    "- **status**: <br>" + event['build_status'] + "\n "
    if event['build_failure_reason'] is not None:
        sub_build_msg += "- **failure_reason**: <br>" + event['build_failure_reason'] + "\n "
    build_message += sub_build_msg
    body.markdown.text = "### " + event['project_name'] + " " + event['build_name'] + " job\n " + build_message
    push_dingding(body)
