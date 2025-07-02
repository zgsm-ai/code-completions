#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from functools import wraps
from config.log_config import logger


def function_timer(func=None, *, name=None):
    if func is None:
        return lambda f: function_timer(f, name=name)

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        function_name = name if name else func.__name__
        logger.info(f"{function_name} 执行耗时： {execution_time:.4f} ms")
        return res

    return wrapper
