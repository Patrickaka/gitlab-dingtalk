import logging
from typing import Union, Dict, Any

import uvicorn
from fastapi import FastAPI, Header

from cicd.ci import parse_event
from connect import mysql_client
from dingtalk_bz.dingtalk_client import cal_sign
from gitlab_bz.gitlab_hook import job_hook, pipeline_hook_v2

app = FastAPI()
logging.getLogger().setLevel(logging.INFO)


@app.post("/gitlab/webhook")
async def webhook(event: Dict[str, Any], X_Gitlab_Event: Union[str, None] = Header(default=None)):
    if X_Gitlab_Event == 'Pipeline Hook':
        pipeline_hook_v2(event)
    elif X_Gitlab_Event == 'Job Hook':
        job_hook(event)
    return True


@app.post("/test")
async def test():
    mysql_client.cnx.close()
    mysql_client.cnx.connect()


@app.post("/robot/dingtalk/webhook")
async def dingtalk_hook(event: Dict[str, Any], sign: Union[str, None] = Header(default=None),
                        timestamp: Union[str, None] = Header(default=None)):
    logging.info(f"event = {event}, sign = {sign}, timestamp = {timestamp}")
    if sign != cal_sign(timestamp, False):
        logging.error("dingtalk sign error")
        return False
    parse_event(event)
    return True

@app.post("/robot/dingtalk/notify")
async def dingtalk_hook(event: Dict[str, Any], sign: Union[str, None] = Header(default=None),
                        timestamp: Union[str, None] = Header(default=None)):
    logging.info(f"event = {event}, sign = {sign}, timestamp = {timestamp}")
    return True


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8091, log_level="info", reload=True)


if __name__ == '__main__':
    main()
