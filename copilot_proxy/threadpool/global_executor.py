#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue
from concurrent.futures import ThreadPoolExecutor


class BoundThreadPoolExecutor(ThreadPoolExecutor):
    """
    重写线程池修改队列数
    """
    def __init__(self, max_workers=None, thread_name_prefix=''):
        super().__init__(max_workers, thread_name_prefix)
        # 队列大小为最大线程数的三倍
        self._work_queue = queue.Queue(self._max_workers * 3)


# 定义一个全局的线程池执行器
executor = BoundThreadPoolExecutor(max_workers=8)


# 定义关闭函数
def close_executor():
    executor.shutdown(wait=True)
