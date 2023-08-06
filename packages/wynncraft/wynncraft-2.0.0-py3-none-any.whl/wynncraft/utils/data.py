import wynncraft.utils.cache as cache
import wynncraft.utils.request as request
from wynncraft.utils.constants import CACHE_TIME, URL_V1, URL_V2, URL_V3, URL_WYNNTILS

def get(url):
    for prefix in [URL_V1, URL_V2, URL_V3, URL_WYNNTILS]:
        if prefix in url:
            id = url.replace(prefix, "")
            break

    if CACHE_TIME and cache.exists_valid_data(id):
        return cache.read_json()["data"][id]
    else:
        data = request.get(url)
        
        if CACHE_TIME:
            cache.write_json(id, data)
        
        return data
