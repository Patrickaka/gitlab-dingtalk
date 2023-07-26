import argparse
import logging
from typing import Union, Dict, Any

import uvicorn
from fastapi import FastAPI, Header

from cicd.ci import parse_event
from connect.mysql_client import MysqlClient
from dingtalk_bz.dingtalk_client import cal_sign
from gitlab_bz.gitlab_hook import pipeline_hook, job_hook

app = FastAPI()
logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser(description="cicd")
parser.add_argument(
    "--mysql_host",
    type=str,
)
parser.add_argument(
    "--mysql_port",
    type=int,
)
parser.add_argument(
    "--mysql_user",
    type=str,
)
parser.add_argument(
    "--mysql_password",
    type=str,
)
args, _ = parser.parse_known_args()
mysql_host = args.mysql_host or "82.157.239.83"
mysql_port = args.mysql_port or 3000
mysql_user = args.mysql_user or "root"
mysql_password = args.mysql_password or "JJfkP4bSZ"
mysql_client = MysqlClient(mysql_host, mysql_port, mysql_user, mysql_password)


@app.post("/gitlab/webhook")
async def webhook(event: Dict[str, Any], X_Gitlab_Event: Union[str, None] = Header(default=None)):
    if X_Gitlab_Event == 'Pipeline Hook':
        pipeline_hook(event, mysql_client)
    elif X_Gitlab_Event == 'Job Hook':
        job_hook(event, mysql_client)
    return True


@app.post("/dingtalk/webhook")
async def dingtalk_hook(event: Dict[str, Any], sign: Union[str, None] = Header(default=None),
                        timestamp: Union[str, None] = Header(default=None)):
    logging.info(f"event = {event}, sign = {sign}, timestamp = {timestamp}")
    if sign != cal_sign(timestamp, False):
        logging.error("dingtalk sign error")
        return False
    parse_event(event, mysql_client)
    return True


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8091, log_level="info", reload=True)


if __name__ == '__main__':
    main()
