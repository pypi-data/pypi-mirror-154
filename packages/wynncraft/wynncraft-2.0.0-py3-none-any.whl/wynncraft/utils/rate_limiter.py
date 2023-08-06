import time

from wynncraft.utils.constants import RATE_LIMITER


class RateLimiter:
    def __init__(self):
        self.rl_reset = 0
        self.rl_remaining = 0

    def limit(self):
        if RATE_LIMITER:
            if self.rl_reset > self.rl_remaining:
                time.sleep(self.rl_reset - self.rl_remaining)

    def update(self, info):
        try:
            self.rl_reset = int(info["RateLimit-Reset"])
            self.rl_remaining = int(info["RateLimit-Remaining"])
        except TypeError:
            # Wynncraft v3 and wynntils api don't have these headers
            pass
