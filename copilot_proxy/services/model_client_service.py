#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import requests
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from utils.constant import OpenAIStreamContent
from config.log_config import logger
from services.completion_stream_service import StreamHandlerFactory
from utils.decorator.common import function_timer


class AbstractModelClientStrategy(ABC):
    def __init__(
        self,
        timeout: int = 10,
    ):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": os.environ.get("OPENAI_MODEL_AUTHORIZATION", "")
        }
        self.timeout = timeout

    @function_timer(name="LLM流式输出")
    def generate_stream(self, host, params, context_and_intention, max_model_cost_time):
        url = self.handle_host(host)
        response = None
        try:
            # 设置超时时间，当触发模型排队机制时,可能没有分批返回数据会导致choices_process中的超时处理异常,所以这里设置请求超时时间
            response = requests.post(url, json=params, headers=self.headers, stream=True, timeout=max_model_cost_time/1000)
            if response.status_code == 200:
                return self.choices_process(response, context_and_intention, max_model_cost_time)
        except Exception as e:
            logger.error(f'{url} request error, {e}')
        finally:
            if response:
                response.close()
        return ""

    @staticmethod
    def get_params(
        model: str,
        prompt: str,
        n: int = 1,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        temperature: float = 1.0,
        top_p: float = 1.0,
        stop_sequences: Optional[Union[str, List[str]]] = None,
        max_new_tokens: int = 16,
        logprobs: Optional[int] = None,

    ) -> dict:
        params = {
            'model': model,
            'prompt': prompt,
            'n': n,
            'presence_penalty': presence_penalty,
            'frequency_penalty': frequency_penalty,
            'temperature': temperature,
            'top_p': top_p,
            'stop': stop_sequences if stop_sequences is not None else [],
            'max_tokens': int(max_new_tokens),
            'logprobs': logprobs,
            'stream': True
        }
        return params

    @abstractmethod
    def choices_process(self, response, context_and_intention, max_model_cost_time):
        raise NotImplementedError

    @classmethod
    def handle_host(cls, host):
        return f'http://{host}' if 'http' not in host else host

    @classmethod
    def check_chunk_content(cls, chunk_msg) -> bool:
        return (chunk_msg.startswith(OpenAIStreamContent.CHUNK_START_WORD)
                and not chunk_msg[len(OpenAIStreamContent.CHUNK_START_WORD):]
                .strip().startswith(OpenAIStreamContent.CHUNK_DONE_SIGNAL))

    @classmethod
    def check_chunk_done(cls, chunk_msg) -> bool:
        return (chunk_msg[len(OpenAIStreamContent.CHUNK_START_WORD):]
                .strip().startswith(OpenAIStreamContent.CHUNK_DONE_SIGNAL))


class OpenAIClientStrategy(AbstractModelClientStrategy):
    def __init__(self, timeout: int = 10):
        super().__init__(timeout)

    def choices_process(self, response, context_and_intention, max_model_cost_time):

        if response is None:
            return ''
        stream_handler = StreamHandlerFactory.get_stream_handler(context=context_and_intention)
        try:
            for chunk in response.iter_lines():
                # 模型请求内容超过最大时间，退出
                if int((time.time() - context_and_intention.st) * 1000) >= max_model_cost_time:
                    stream_handler.mark_exception_flag()
                    break

                # 检查到补全内容为空，跳过当前内容
                if not chunk:
                    continue

                chunk_text = chunk.decode('utf-8')
                # 检查到补全正常结束，取消设置异常标记，退出
                if self.check_chunk_done(chunk_text):
                    stream_handler.unmark_exception_flag()
                    break

                # 检查到补全内容无效，跳过当前内容
                if not self.check_chunk_content(chunk_text):
                    continue

                shell_text = json.loads(chunk_text[len(OpenAIStreamContent.CHUNK_START_WORD):])['choices'][0]['text']

                # 流式输出过程中，针对单行/多行场景满足特定逻辑下退出补全
                if not stream_handler.handle(shell_text):
                    logger.info(f"补全流式输出提前终止，内容为: {stream_handler.get_completed_content()}")
                    break

        except Exception as e:
            stream_handler.mark_exception_flag()
            logger.error(f"补全流式异常终止，异常信息为: {e}")
        return stream_handler.get_completed_content_and_handle_ex()


class LocalClientStrategy(AbstractModelClientStrategy):
    def __init__(self, timeout: int = 10):
        super().__init__(timeout)

    def choices_process(self, response, context_and_intention, max_model_cost_time):
        if response is None:
            return ''
        stream_handler = StreamHandlerFactory.get_stream_handler(context=context_and_intention)
        try:
            for c in response:
                if int((time.time() - context_and_intention.st) * 1000) >= max_model_cost_time:
                    stream_handler.mark_exception_flag()
                    break
                # 流式输出过程中，针对单行/多行场景满足特定逻辑下退出补全
                if not stream_handler.handle(c.token.text):
                    logger.info(f"补全流式输出提前终止，内容为: {stream_handler.get_completed_content()}")
                    break
        except Exception as e:
            stream_handler.mark_exception_flag()
            logger.error(f"补全流式异常终止，异常信息为: {e}")
        finally:
            response.close()
        return stream_handler.get_completed_content_and_handle_ex()
