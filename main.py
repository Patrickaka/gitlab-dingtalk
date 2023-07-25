import logging
from typing import Union, Dict, Any

import uvicorn
from fastapi import FastAPI, Header

from common import projects
from dingtalk_bz.dingtalk_client import cal_sign
from gitlab_bz.gitlab_client import pipeline_create
from gitlab_bz.gitlab_hook import pipeline_hook, job_hook

app = FastAPI()
logging.getLogger().setLevel(logging.INFO)


@app.post("/gitlab/webhook")
async def webhook(event: Dict[str, Any], X_Gitlab_Event: Union[str, None] = Header(default=None)):
    if X_Gitlab_Event == 'Pipeline Hook':
        pipeline_hook(event)
    elif X_Gitlab_Event == 'Job Hook':
        job_hook(event)
    return True


@app.post("/dingtalk/webhook")
async def dingtalk_hook(event: Dict[str, Any], sign: Union[str, None] = Header(default=None),
                        timestamp: Union[str, None] = Header(default=None)):
    logging.info(f"event = {event}, sign = {sign}, timestamp = {timestamp}")
    if sign != cal_sign(timestamp):
        logging.error("dingtalk sign error")
        return False
    ci_cd(event)
    return True


def ci_cd(event: Dict[str, Any]):
    content = event['content']
    sender_id = event['senderStaffId']
    content_arr = content.split(" ")
    project_id = projects.project_dict[content_arr[0]]
    projects.pipeline_dict[project_id] = sender_id
    if content_arr[1] == '上线':
        ref = content_arr[2]
        pipeline_create(project_id, False, ref)
    elif content_arr[1] == '回滚':
        pipeline_create(project_id, True)


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8091, log_level="info", reload=True)


if __name__ == '__main__':
    main()
