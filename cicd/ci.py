from typing import Dict, Any

from common import project_info
from connect import mysql_client
from dingtalk_bz.dingtalk_client import push_dingding, build_text_DingTalkMessage
from gitlab_bz.gitlab_client import pipeline_create, tag_validate


def parse_event(event: Dict[str, Any]):
    content = event['text']['content'].strip()
    sender_id = event['senderStaffId']
    sender_nick = event['senderNick']
    content_arr = content.split(" ")
    projects = mysql_client.find_project_by_name(content_arr[0])
    if len(projects) > 1:
        solve_multi_project(projects, sender_id)
    elif len(projects) == 0:
        solve_error_project(sender_id)
        return
    else:
        if content_arr[1] == '上线' or content_arr[1] == '回滚':
            create_pipeline(sender_id, sender_nick, content_arr, projects[0])


def solve_multi_project(projects, sender_id):
    content = "命中多个项目，请确认项目名称: "
    for project in projects:
        content += project[2] + " "
    push_dingding(build_text_DingTalkMessage(sender_id, content))


def solve_error_project(sender_id):
    content = "指令不存在 正确格式为 <项目名或简称> <上线/回滚> <分支或者tag名称>\n可用项目: "
    projects = mysql_client.find_project_by_name("")
    for project in projects:
        content += project[2] + " "
    push_dingding(build_text_DingTalkMessage(sender_id, content))


def create_pipeline(sender_id, senderNick, content_arr, project):
    res = None
    ref = ''
    ci_type = 1
    if content_arr[1] == '上线':
        ref = content_arr[2]
        if tag_validate(project[1], ref):
            content = f"「{project[2]} - {project[4]}」开始上线: {ref}"
            push_dingding(build_text_DingTalkMessage(sender_id, content))
            res = pipeline_create(project[1], False, ref)
        else:
            content = f"{ref}标签不存在，请创建标签"
            push_dingding(build_text_DingTalkMessage(sender_id, content))
    elif content_arr[1] == '回滚':
        ci_type = 2
        ci_logs = mysql_client.find_rollback_ref(project[1]) or []
        if len(ci_logs) == 2:
            ref = ci_logs[0][0] + " -> " + ci_logs[1][0]
        elif len(ci_logs) == 1:
            ref = ci_logs[0][0] + " -> unknown"
        else:
            ref = "unknown -> unknown"
        content = f"「{project[2]} - {project[4]}」开始回滚: {ref}"
        push_dingding(build_text_DingTalkMessage(sender_id, content))
        res = pipeline_create(project[1], True)
    mysql_client.update_project_ci((sender_id, senderNick, ref, project[1]))
    mysql_client.save_project_ci((project[1], ci_type, ref, senderNick))
    if res:
        project_info.add_pipeline(res['project_id'], res['id'], res['web_url'], ref)
