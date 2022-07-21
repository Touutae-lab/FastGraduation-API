import time

import redis


def get_hit_count(cache: redis.Redis):
    """
    I'm get_hit_count
    """
    retries: int = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
