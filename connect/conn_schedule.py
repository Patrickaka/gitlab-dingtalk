import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from connect import mysql_client


def job(cnx):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(f"{t} 触发了定时任务！")
    cnx.ping(reconnect=True)


def scheduler_task():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, 'interval', hours=8, args=[mysql_client.cnx])
    scheduler.start()
