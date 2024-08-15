import json


def json_dumps_custom(obj, **kwargs):
    return json.dumps(obj, ensure_ascii=False, **kwargs)
