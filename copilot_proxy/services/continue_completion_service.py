#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import HTTPException
from typing import Union
from repositories.continue_completion_cache import ContinueCompletionCache
from models import CompletionRequest
from threadpool.global_executor import executor
from utils.constant import TriggerModeConst
from config.log_config import logger


class ContinueCompletionService:
    """
    连续代码补全服务
    """

    def __init__(self, cache: ContinueCompletionCache):
        self.cache = cache

    def is_enabled(self):
        return self.cache.is_enabled()

    def is_continue_completion(self, parent_id: str, trigger_mode: str) -> bool:
        return parent_id and trigger_mode == TriggerModeConst.CONTINUE and self.cache.is_enabled()

    def get_continue_completion(self, completion_request: CompletionRequest) -> dict:
        parent_id = completion_request.parent_id
        try:
            # cache hit
            completion_info = self.cache.get_completion_info(parent_id)
            if completion_info:
                logger.info(f"获取连续补全缓存成功，parent_id: {parent_id}")

                # 继续触发连续补全
                new_completion_request = self.build_completion_request(completion_request, completion_info)
                self.async_send_v2_completion(new_completion_request)
                return completion_info
        except Exception as e:
            logger.warning(f"获取连续补全缓存异常，降级成同步请求连续补全。parent_id: {parent_id}，error: {e}")

        # cache miss，返回空，交给主流程进行同步请求补全
        return {}

    def save_continue_completion(self, parent_id: str, completion_info: dict, ttl=30):
        """
        缓存连续补全结果
        :param parent_id:
        :param completion_info:
        :param ttl: 过期时间 单位s
        :return:
        """
        self.cache.save_completion_info(parent_id, completion_info, ttl)

    @staticmethod
    def request_v2_completion(completion_request: CompletionRequest):
        """
        同步请求 v2/completion接口
        :param completion_request:
        :return:
        """
        from services.coder_completions import coder_completions
        from instances.tgi_proxy_v2 import TGIProxyV2
        try:
            return coder_completions(data=completion_request.dict(), proxy=TGIProxyV2(headers={"X-Request-ID": "continue-completion"}))
        except Exception as e:
            logger.error(f"请求补全接口异常，parent_id: {completion_request.parent_id}，error: {e}")
            raise HTTPException(status_code=500, detail=f"请求补全接口异常: {e}")

    def async_send_v2_completion(self, completion_request: CompletionRequest):
        """
        异步请求 v2/completion接口
        :param completion_request:
        :return:
        """
        logger.info(f"正在异步请求 v2/completion接口，连续补全！parent_id: {completion_request.parent_id}")
        executor.submit(self.request_v2_completion, completion_request)

    @staticmethod
    def build_completion_request(data: Union[CompletionRequest, dict], completion_info: dict) \
            -> CompletionRequest:
        if isinstance(data, dict):
            data = CompletionRequest.parse_obj(data)

        data.prompt = ""
        # 此处修改为不需要特别设置key 已经取消了认证
        # data.authorization = "Bearer " + data.api_key
        data.parent_id = completion_info.get("id")
        data.trigger_mode = TriggerModeConst.CONTINUE
        choices = completion_info.get('choices', [{"text": ""}])
        choices_text = ""
        if len(choices) > 0:
            choices_text = choices[0]["text"]
        data.prompt_options.prefix = (data.prompt_options.prefix + choices_text)
        data.prompt_options.cursor_line_prefix = data.prompt_options.prefix.split('\n')[-1]
        split_suffix = data.prompt_options.suffix.split('\n')
        data.prompt_options.cursor_line_suffix = split_suffix[0]
        return data
