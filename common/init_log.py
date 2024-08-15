import os
import sys

from loguru import logger


def init_log():
    # 移除默认的控制台输出
    logger.remove()
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level}</level> | "
        "<level>{thread.id}</level> "
        "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    logger.add(sys.stdout, format=log_format)

    LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..//log'))
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    INFO_LOG_FILE = os.path.join(LOG_DIR, "info_{time:YYYY-MM-DD_HH}.log")
    ERROR_LOG_FILE = os.path.join(LOG_DIR, "error_{time:YYYY-MM-DD}.log")

    logger.add(INFO_LOG_FILE,
               format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {thread.id} {module}:{function}:{line} {message}",
               level="INFO",
               filter=lambda record: record["level"].name == "INFO", rotation='1h',
               retention="10 days",
               enqueue=True)

    logger.add(ERROR_LOG_FILE,
               format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {thread.id} {module}:{function}:{line} {message}",
               level="ERROR",
               filter=lambda record: record["level"].name == "ERROR", rotation='1 day',
               retention="10 days",
               enqueue=True)
