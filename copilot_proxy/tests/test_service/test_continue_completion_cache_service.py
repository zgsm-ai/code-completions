#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from tests.mock.mock_continue_completion_cache import (
    MOCK_CONTINUE_COMPLETION_INFO
)
from repositories.continue_completion_cache import ContinueCompletionCache
from instances.redis_cache import RedisCache
import os

os.environ["ENABLE_REDIS"] = "True"
os.environ["REDIS_HOST"] = "127.0.0.1"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_DB"] = "0"
os.environ["REDIS_PWD"] = ""


class TestContinueCompletionCacheCase(unittest.TestCase):
    redis = RedisCache()
    cache = ContinueCompletionCache(redis)

    def test_save_completion_info(self):
        for item in MOCK_CONTINUE_COMPLETION_INFO:
            self.assertEqual(first=True,
                             second=self.cache.save_completion_info(
                                 parent_id=item["parent_id"],
                                 completion=item["completion"],
                                 ttl=item["ttl"]
                             ))

    def test_get_completion_info(self):
        # 先保存数据
        self.test_save_completion_info()
        # 再获取数据
        for item in MOCK_CONTINUE_COMPLETION_INFO:
            self.assertEqual(first=item["completion"],
                             second=self.cache.get_completion_info(parent_id=item["parent_id"]))

    def test_expired_time(self):
        # 先保存数据
        self.test_save_completion_info()

        for item in MOCK_CONTINUE_COMPLETION_INFO:
            self.assertLessEqual(
                a=self.cache.get_ttl(parent_id=item["parent_id"]),
                b=item["ttl"])
        print(f"共{len(MOCK_CONTINUE_COMPLETION_INFO)}个样例，测试成功！")


if __name__ == '__main__':
    unittest.main()
