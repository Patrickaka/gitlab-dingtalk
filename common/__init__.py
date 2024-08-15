import json
from functools import partial

json.dumps = partial(json.dumps, ensure_ascii=False)
