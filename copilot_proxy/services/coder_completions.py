#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import Response
from config.log_config import logger
from utils.common import random_completion_id
from services.completion_reject_service import completion_reject_rule_chain


def coder_completions(data: dict, proxy, request_id: str = ''):

    # c++ -> cpp
    if data.get("language_id") and data.get("language_id") == 'c++':
        data["language_id"] = 'cpp'

    complete_id = random_completion_id()
    data['x-complete-id'] = complete_id
    data['complete_id'] = complete_id
    logger.info(f'{complete_id} start')

    # 补全拒绝规则链处理
    reject_judge_result = completion_reject_rule_chain.handle(data)
    if reject_judge_result is not None:
        return reject_judge_result

    return Response(
        headers={'x-complete-id': complete_id, 'x-request-id': request_id},
        status_code=200,
        content=proxy(data=data),
        media_type="application/json"
    )
