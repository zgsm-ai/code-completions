import os

import redis
from utils.cache.cache_component import CacheComponent


class RedisCache(CacheComponent):
    _pools_map = {}

    def __init__(self):
        self.enabled = 'true' in os.environ.get("ENABLE_REDIS", 'False').lower()
        if self.enabled:
            host = os.environ.get("REDIS_HOST", '127.0.0.1')
            port = os.environ.get("REDIS_PORT", 6379)
            db = os.environ.get("REDIS_DB", 0)
            username = os.environ.get("REDIS_USER", None)
            pwd = os.environ.get("REDIS_PWD", None)
            self.url = self._build_url(host, port, db, username, pwd)
            self._create_pool()
            self.client = redis.Redis(connection_pool=self.pool)

    @staticmethod
    def _build_url(host, port, db, username, pwd):
        if username:
            return f"redis://{username}:{pwd}@{host}:{port}/{db}"
        else:
            return f"redis://:{pwd}@{host}:{port}/{db}"

    def _create_pool(self):
        pool = RedisCache._pools_map.get(self.url)
        if pool:
            self.pool = pool
        else:
            self.pool = redis.ConnectionPool.from_url(self.url)
            RedisCache._pools_map[self.url] = self.pool

    def is_enabled(self):
        return self.enabled

    def get(self, key):
        res = self.client.get(key)
        if res:
            return res.decode('utf-8')
        return res

    def set(self, key, value):
        return self.client.set(key, value)

    def expire(self, key, seconds):
        return self.client.expire(key, seconds)

    def delete(self, key):
        return self.client.delete(key)

    def get_ttl(self, key):
        return self.client.ttl(key)
