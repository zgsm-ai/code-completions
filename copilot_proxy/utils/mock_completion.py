#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import time

from utils.constant import RESPONSE_TEMPLATE


class MockCompletion:

    @classmethod
    def get_empty_completion(cls, data):
        datetime_now_str = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z+0800')
        completion = copy.deepcopy(RESPONSE_TEMPLATE)
        completion['id'] = data.get('x-complete-id')
        completion['model'] = data.get('model')
        completion['created'] = time.time()
        completion['model_start_time'] = datetime_now_str
        completion['model_end_time'] = datetime_now_str
        completion['start_time'] = datetime_now_str
        completion['end_time'] = datetime_now_str
        completion['completion_tokens'] = 0
        completion['prompt_tokens'] = 0
        completion['prompt'] = data.get('prompt')
        return completion
