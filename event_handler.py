#!/usr/bin/env python

import argparse
import logging
from datetime import time

import dingtalk_stream
from dingtalk_stream import AckMessage
from loguru import logger

from common.config import dz_test_appKey, dz_test_secret, dz_onl_appKey, dz_onl_secret

is_onl = False


def define_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--client_id', dest='client_id', required=False, default='dingbksjfhqhdlsq3pe',
        help='app_key or suite_key from https://open-dev.digntalk.com'
    )
    parser.add_argument(
        '--client_secret', dest='client_secret', required=False,
        default='5FB4UF91toiDYbPzXMWIysSz46RFTFYJOKc6i7FTghWR8SS5Vbs4cgScA7NRNmfF',
        help='app_secret or suite_secret from https://open-dev.digntalk.com'
    )
    parser.add_argument(
        '--is_onl', dest='is_onl', required=False,
        default=False,
        help='is_onl'
    )
    options = parser.parse_args()
    return options


class MyEventHandler(dingtalk_stream.EventHandler):
    async def process(self, event: dingtalk_stream.EventMessage):
        if event.headers.event_type != 'chat_update_title':
            return dingtalk_stream.AckMessage.STATUS_OK, 'OK'
        logger.info(
            'received event, delay=%sms, eventType=%s, eventId=%s, eventBornTime=%d, eventCorpId=%s, '
            'eventUnifiedAppId=%s, data=%s',
            int(time.time() * 1000) - event.headers.event_born_time,
            event.headers.event_type,
            event.headers.event_id,
            event.headers.event_born_time,
            event.headers.event_corp_id,
            event.headers.event_unified_app_id,
            event.data)
        return dingtalk_stream.AckMessage.STATUS_OK, 'OK'


class MyCallbackHandler(dingtalk_stream.CallbackHandler):
    async def process(self, message: dingtalk_stream.CallbackMessage):
        if message.headers.topic == dingtalk_stream.ChatbotMessage.TOPIC:
            from parse import parser
            parser.parse_event(message.data, is_onl)
            return AckMessage.STATUS_OK, 'OK'
        print(message.headers.topic,
              message.data)
        return AckMessage.STATUS_OK, 'OK'


def main():
    options = define_options()
    global is_onl
    is_onl = options.is_onl
    logger.info('is_onl: {}', is_onl)
    if is_onl:
        credential = dingtalk_stream.Credential(dz_onl_appKey, dz_onl_secret)
    else:
        credential = dingtalk_stream.Credential(dz_test_appKey, dz_test_secret)
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_all_event_handler(MyEventHandler())
    client.register_callback_handler(dingtalk_stream.ChatbotMessage.TOPIC, MyCallbackHandler())
    client.start_forever()


if __name__ == '__main__':
    from common import init_log
    main()
    init_log.init_log()

