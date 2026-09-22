import time
from collections import defaultdict
from threading import Lock


class RateLimiter:

    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
        self.lock = Lock()

    def check(self, key_id: int):

        now = time.time()
        window_start = now - 60

        with self.lock:

            timestamps = self.requests[key_id]

            timestamps[:] = [
                timestamp
                for timestamp in timestamps
                if timestamp > window_start
            ]

            if len(timestamps) >= self.requests_per_minute:
                return False

            timestamps.append(now)

            return True


rate_limiter = RateLimiter(
    requests_per_minute=60
)
