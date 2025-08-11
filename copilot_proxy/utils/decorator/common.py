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
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Function {func.__name__} execution error: {str(e)}")
            raise e  # 重新抛出异常，让调用者处理

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000

        # 1. 取第一个参数
        first = args[0] if args else None

        # 2. 判断并取值
        rid = None
        try:
            if first is not None and hasattr(first, 'request_id'):
                rid = getattr(first, 'request_id', None)
                if not isinstance(rid, str):
                    rid = None  # 确保一定是字符串，否则忽略
        except Exception as e:
            logger.warning(f"Failed to get request_id: {str(e)}")
            rid = None

        # 3. 组装日志
        function_name = name if name else func.__name__
        if rid is not None:
            logger.info(f"{function_name} 执行耗时：{execution_time:.4f} ms", request_id=rid)
        else:
            logger.info(f"{function_name} 执行耗时：{execution_time:.4f} ms")

        return res

    return wrapper
