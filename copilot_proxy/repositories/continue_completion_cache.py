#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from utils.cache.cache_component import CacheComponent
from repositories.constants.redis_keys import CONTINUE_COMPLETION_KEY
from config.log_config import logger


class ContinueCompletionCache:
    """
    连续补全缓存类，用于缓存连续补全请求的代码补全信息
    """
    def __init__(self, cache_component: CacheComponent):
        self.cache_component = cache_component

    @staticmethod
    def wrap_key(key):
        return CONTINUE_COMPLETION_KEY.format(parent_id=key)

    def is_enabled(self):
        return self.cache_component.is_enabled()

    def save_completion_info(self, parent_id: str, completion: dict, ttl=30) -> bool:
        """
        缓存连续补全信息
        :param parent_id: 父id
        :param completion: 补全信息
        :param ttl: 过期时间
        :return:
        """

        try:
            key = self.wrap_key(parent_id)
            # 序列化
            value = json.dumps(completion)
            self.cache_component.set(key, value)
            self.cache_component.expire(key, ttl)
            return True
        except Exception as e:
            logger.error(f"缓存连续补全信息失败: {e}")
            return False

    def get_completion_info(self, parent_id) -> dict:
        value = self.cache_component.get(self.wrap_key(parent_id))
        if value is None:
            return {}
        # 反序列化
        return json.loads(value)

    def get_ttl(self, parent_id):
        return self.cache_component.get_ttl(self.wrap_key(parent_id))
