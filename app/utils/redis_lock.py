from app.extensions import redis_client, REDIS_AVAILABLE
import time


class RedisLock:

    def __init__(self, key, ttl=5):
        self.key = f"lock:{key}"
        self.ttl = ttl

    def acquire(self):

        if not REDIS_AVAILABLE:
            return True   # fallback — allow DB lock only

        end_time = time.time() + self.ttl

        while time.time() < end_time:

            if redis_client.set(
                self.key,
                "1",
                nx=True,
                ex=self.ttl
            ):
                return True

            time.sleep(0.05)

        return False

    def release(self):

        if REDIS_AVAILABLE:
            redis_client.delete(self.key)
