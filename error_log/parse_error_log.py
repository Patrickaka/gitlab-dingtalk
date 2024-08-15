import json
import os
import re

import requests
from loguru import logger

flames_error_log = {}

flames_error_suggest = {

}


def extract_e_search_e_set_pairs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    matches = re.findall(r'e_switch\((.*)\)', content, re.DOTALL)
    content = matches[0]
    e_search_matches = re.findall(r'e_search\((.*?)\)', content, re.DOTALL)
    e_set_matches = re.findall(r'e_set\((.*?)\)', content, re.DOTALL)
    if len(e_search_matches) != len(e_set_matches):
        raise ValueError("Mismatched number of e_search and e_set calls")
    pairs = {e_search: e_set for e_search, e_set in zip(e_search_matches, e_set_matches)}
    return pairs


def init():
    global flames_error_log
    error_log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..//error_log'))
    file_path = os.path.join(error_log_dir, 'error_content.txt')
    type_file_path = os.path.join(error_log_dir, 'error_type.txt')
    with open(type_file_path, 'r', encoding='utf-8') as error_type_file:
        cur_error_type = error_type_file.read().split('\n')
    pairs = extract_e_search_e_set_pairs(file_path)
    with open(type_file_path, 'w', encoding='utf-8') as error_type_file:
        for e_search, e_set in pairs.items():
            type_match = re.search(r'"type",\s*"([^"]+)"', e_set)
            error_info_match = re.search(r'"error_info",\s*"([^"]+)"', e_set)
            service_match = re.search(r'"service",\s*"([^"]+)"', e_set)
            type_value = type_match.group(1) if type_match else None
            error_info_value = error_info_match.group(1) if error_info_match else None
            service_value = service_match.group(1) if service_match else None
            flames_error_log[type_value] = (e_search.strip(), {
                'error_info': error_info_value,
                'service': service_value
            })
            if type_value not in cur_error_type:
                body_param = {
                    "alert_name": error_info_value,
                    "alert_type": type_value,
                    "alert_keyword": e_search.strip(),
                    "alert_service": service_value,
                    "alert_suggest": ""
                }
                response = requests.post('https://connector.dingtalk.com/webhook/flow/102c243d34340b523850000v',
                                         json=body_param).json()
                if not response['data']:
                    logger.error("Failed to push alert info to dingtalk, body_param = {}", json.dumps(body_param))
                else:
                    error_type_file.write(type_value + '\n')
        print(json.dumps(flames_error_log, indent=4, ensure_ascii=False))


def get_alert_info(alert_type):
    res = {}
    if flames_error_log.get(alert_type, None):
        alert_info = flames_error_log.get(alert_type, None)
        res['title'] = alert_info[1]['error_info']
        res['service'] = alert_info[1]['service']
        res['key_word'] = alert_info[0]
        res['suggest'] = flames_error_suggest.get(alert_type) if flames_error_suggest.get(alert_type) else '待补充'
    return res


if __name__ == '__main__':
    init()
    print(get_alert_info('166'))
