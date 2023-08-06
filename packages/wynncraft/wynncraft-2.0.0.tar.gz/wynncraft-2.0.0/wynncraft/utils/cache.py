import json
import os
import time

from wynncraft.utils.constants import CACHE_TIME

PATH = os.path.normpath(f"{os.path.dirname(__file__)}/../.cache")
FILEPATH = PATH + "/cache.json"


def delete_cache():
    os.remove(FILEPATH)
    os.rmdir(PATH)


def read_json():
    try:
        with open(FILEPATH, "r") as f:
            return json.loads(f.read())
    except (FileNotFoundError, json.JSONDecodeError):
        os.makedirs(PATH, exist_ok=True)
        default = {"timestamps": {}, "data": {}}
        
        with open(FILEPATH, "w") as f:
            json.dump(default, f)
        
        return default


def write_json(id, new_data):
    with open(FILEPATH, "r") as f:
        cache = json.loads(f.read())

    cache["data"].update({id: new_data})
    cache["timestamps"].update({id: int(time.time())})

    with open(FILEPATH, "w") as f:
        json.dump(cache, f)


def exists_valid_data(id):
    cache = read_json()
    return ((id in cache["data"]) and (int(time.time()) < cache["timestamps"][id] + CACHE_TIME))
