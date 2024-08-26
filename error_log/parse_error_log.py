import json
import os

import pandas as pd
import regex as re
import requests
from loguru import logger

flames_error_log = {}

flames_error_suggest = {

}


def init():
    error_log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..//error_log'))
    flames_file_path = os.path.join(error_log_dir, 'flames_error_content.txt')
    center_file_path = os.path.join(error_log_dir, 'center_error_content.txt')
    error_suggest_path = os.path.join(error_log_dir, 'error_suggest.json')
    ding_talk_excel_path = os.path.join(error_log_dir, 'flames报警.xlsx')
    with open(error_suggest_path, 'r', encoding='utf-8') as file:
        error_suggest = json.load(file)
    error_suggest = do_parse(flames_file_path, error_suggest, 1)
    error_suggest = do_parse(center_file_path, error_suggest, 2)
    df = pd.read_excel(ding_talk_excel_path)
    df = df.applymap(lambda x: None if pd.isna(x) else x)
    suggest_dict = dict(zip(df['报警类型'], df['处理建议']))
    for key, value in error_suggest.items():
        if suggest_dict.get(key):
            error_suggest[key] = suggest_dict.get(key)
    with open(error_suggest_path, 'w') as file:
        json.dump(error_suggest, file)


def extract_e_search_e_set_pairs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        lines = content.splitlines()
        filtered_lines = [line for line in lines if not line.strip().startswith('#')]
        content = '\n' + '\n'.join(filtered_lines)
    matches = re.findall(r'e_switch\((.*)\)', content, re.DOTALL)
    content = matches[0]
    e_search_pattern = r'e_search\((.*?)\)\s*(.*?)(?=\se_search\(|\Z)'
    e_search_matches = re.findall(e_search_pattern, content, re.DOTALL)
    return e_search_matches


def do_parse(file_path, error_suggest, parse_type):
    pairs = extract_e_search_e_set_pairs(file_path)
    for pair in pairs:
        e_search = pair[0]
        e_set = pair[1]
        type_match = re.search(r'"type",\s*"([^"]+)"', e_set)
        error_info_match = re.search(r'"error_info",\s*"([^"]+)"', e_set)
        if parse_type == 1:
            service_match = re.search(r'"service",\s*"([^"]+)"', e_set)
        else:
            service_match = re.search(r'service:"([^"]+)"', e_search)
        type_value = type_match.group(1) if type_match else None
        error_info_value = error_info_match.group(1) if error_info_match else None
        service_value = service_match.group(1) if service_match else None
        flames_error_log[type_value.lstrip('0')] = (e_search.strip(), {
            'error_info': error_info_value,
            'service': service_value
        })
        if type_value not in error_suggest:
            body_param = {
                "alert_name": error_info_value,
                "alert_type": type_value,
                "alert_keyword": e_search.strip(),
                "alert_service": service_value,
                "alert_suggest": ""
            }
            response = requests.post('https://connector.dingtalk.com/webhook/flow/102c243d34340b523850000v',
                                     json=body_param).json()
            logger.info("Push alert info to dingtalk, body_param = {}, response = {}", json.dumps(body_param),
                        json.dumps(response))
            if not response['data']:
                logger.error("Failed to push alert info to dingtalk, body_param = {}", json.dumps(body_param))
            else:
                error_suggest[type_value] = ''
    return error_suggest


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
