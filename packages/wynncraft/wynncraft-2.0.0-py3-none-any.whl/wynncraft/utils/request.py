import json
import urllib.request

from wynncraft.utils.rate_limiter import RateLimiter
from wynncraft import __version__
from wynncraft.utils.constants import (
    API_KEY,
    TIMEOUT,
    URL_V1,
    URL_CODES
)

limiter = RateLimiter()


def get(url):
    for char in url:
        if char in URL_CODES:
            url = url.replace(char, URL_CODES[char])

    if URL_V1 in url:
        url += f"&apikey={API_KEY}"
    
    req = urllib.request.Request(
        url,
        headers={
            "apikey": API_KEY,
            "User-Agent": f"wynncraft-python/{__version__}"
        }
    )
    
    limiter.limit()

    res = urllib.request.urlopen(req, timeout=TIMEOUT)

    limiter.update(res.info())

    return json.loads(res.read().decode("utf-8"))
