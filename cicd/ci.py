from typing import Dict, Any

from connect import mysql_client
from connect.mysql_client import MysqlClient
from dingtalk_bz.dingtalk_client import push_dingding
from gitlab_bz.gitlab_client import pipeline_create
from model.DIndtalkModel import DingTalkMessage


def parse_event(event: Dict[str, Any]):
    content = event['text']['content'].strip()
    sender_id = event['senderStaffId']
    sender_nick = event['senderNick']
    content_arr = content.split(" ")
    projects = mysql_client.find_project(content_arr[0])
    if len(projects) > 1:
        solve_multi_project(projects, sender_id)
    elif len(projects) == 0:
        solve_error_project(sender_id, mysql_client)
        return
    else:
        if content_arr[1] == '上线' or content_arr[1] == '回滚':
            create_pipeline(sender_id, sender_nick, content_arr, mysql_client, projects[0])


def solve_multi_project(projects, sender_id):
    content = "命中多个项目，请确认项目名称: "
    for project in projects:
        content += project[2] + " "
    push_dingding(build_text_DingTalkMessage(sender_id, content))


def solve_error_project(sender_id, mysql_client):
    content = "指令不存在 正确格式为 <项目名或简称> <上线/回滚> <分支或者tag名称>\n可用项目: "
    projects = mysql_client.find_project("")
    for project in projects:
        content += project[2] + " "
    push_dingding(build_text_DingTalkMessage(sender_id, content))


def create_pipeline(sender_id, senderNick, content_arr, mysql_client: MysqlClient, project):
    ref = ''
    ci_type = 1
    if content_arr[1] == '上线':
        ref = content_arr[2]
        content = f"{project[2]} 上线开始, ref = {ref}"
        push_dingding(build_text_DingTalkMessage(sender_id, content))
        pipeline_create(project[1], False, ref)
    elif content_arr[1] == '回滚':
        ci_type = 2
        ref = mysql_client.find_rollback_ref(project[1]) or 'master'
        content = f"{project[2]} 回滚开始, ref = {ref}"
        push_dingding(build_text_DingTalkMessage(sender_id, content))
        pipeline_create(project[1], True, ref)
    mysql_client.update_project_ci((sender_id, senderNick, ref, project[1]))
    mysql_client.save_project_ci((project[1], ci_type, ref, senderNick))


def build_text_DingTalkMessage(at_user, content):
    body = DingTalkMessage()
    body.msgtype = "text"
    body.text.content = content
    body.at.atUserIds = [at_user]
    return body
