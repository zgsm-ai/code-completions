#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from enum import Enum
from fastapi import Response
import json
import time
import datetime
import os
from utils.constant import TriggerModeConst
from utils.codefilters import CodeFilters
from models import EditorHideScore
from utils.get_score import HideScoreConfig
from config.log_config import logger


SCORE_INI_PATH = "./config/hide_score.yml"


class RejectCodeEnum(Enum):
    LOW_HIDDEN_SCORE = "LOW_HIDDEN_SCORE"
    AUTH_FAIL = "AUTH_FAIL"
    FEATURE_NOT_SUPPORT = "FEATURE_NOT_SUPPORT"

    @classmethod
    def get_enum_by_value(cls, value):
        for enum_value in cls:
            if enum_value.value == value:
                return enum_value
        return None


class AbstractCompletionRejectHandler(ABC):
    """
    抽象补全拒绝处理类
    """
    def enabled(self) -> bool:
        is_disabled = bool(os.environ.get(f"DISABLED_REJECT_{self.get_env_suffix_name().upper()}", False))
        return not is_disabled

    @abstractmethod
    def get_env_suffix_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def judge(self, data) -> RejectCodeEnum | None:
        raise NotImplementedError


class LanguageFeatureRejectHandler(AbstractCompletionRejectHandler):
    """
    语言特性拒绝处理器
    """

    def __init__(self):
        self.code_filters = CodeFilters(
            threshold_score=float(os.environ.get("THRESHOLD_SCORE", 0.3)),
            str_pattern=os.environ.get("STR_PATTERN", ""),
            tree_pattern=os.environ.get("TREE_PATTERN", "")
        )

    def judge(self, data) -> RejectCodeEnum | None:
        if data.get('trigger_mode', "") in [TriggerModeConst.MANUAL]:
            return None
        if self.code_filters.need_code(data):
            return None
        return RejectCodeEnum.FEATURE_NOT_SUPPORT

    def get_env_suffix_name(self) -> str:
        return "LANGUAGE_FEATURE"


class LowHiddenScoreRejectHandler(AbstractCompletionRejectHandler):
    """
    低隐藏分数拒绝处理器
    """

    def __init__(self):
        super().__init__()
        self.hideScoreConfig = HideScoreConfig(SCORE_INI_PATH,
                                               threshold_score=float(os.environ.get("THRESHOLD_SCORE", 0.3)))

    def judge(self, data) -> RejectCodeEnum | None:
        if data.get("trigger_mode", "") in [TriggerModeConst.MANUAL, TriggerModeConst.CONTINUE]:
            return None
        editor_obj = EditorHideScore(**data.get("calculate_hide_score"))
        score = 0
        if editor_obj.document_length != 0:
            score = self.hideScoreConfig.calculate_hide_score(editor_obj, data.get("language_id", "python"))
        data["score"] = score

        # 通过配置阈值 来过滤隐藏分低的补全
        if score < self.hideScoreConfig.threshold_score:
            logger.info(f'score {score} < {self.hideScoreConfig.threshold_score} skip completion!')
            return RejectCodeEnum.LOW_HIDDEN_SCORE
        return None

    def get_env_suffix_name(self) -> str:
        return "LOW_HIDDEN_SCORE"


class CompletionRejectRuleChain:

    def __init__(self):

        self._default_reject_handlers = []
        if os.environ.get("DISABLED_SCORE_REJECT", "false") == "false":
            self._default_reject_handlers.append(LowHiddenScoreRejectHandler())

        if os.environ.get("DISABLED_REJECT_LANGUAGE_FEATURE", "false") == "false":
            self._default_reject_handlers.append(LanguageFeatureRejectHandler())


    def handle(self, data) -> Response | None:
        """
        「拒绝补全规则链」：只要命中一个规则拒绝补全
        :param data:
        :return:
        """

        for reject_handler in self._default_reject_handlers:
            if reject_handler.enabled():
                reject_code = reject_handler.judge(data)
                if reject_code is not None:
                    return CompletionRejectRuleChain.get_reject_completion_response(data, reject_code)
        return None

    @staticmethod
    def get_reject_completion_response(data, reject_code: RejectCodeEnum):
        def mock_reject_content(data, code):
            completion = dict()
            completion['id'] = data.get('complete_id')
            completion['choices'] = []
            completion['model_choices'] = []

            completion['model'] = "default"
            completion['created'] = int(time.time())
            completion['completion_tokens'] = 0
            completion['prompt_tokens'] = data.get("prompt_tokens", 0)
            completion['prompt'] = data.get('prompt')
            completion['score'] = data.get("score", 0)
            completion['cost_time'] = 0

            mock_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z+0800')
            completion['start_time'] = mock_time
            completion['end_time'] = mock_time
            completion['model_start_time'] = mock_time
            completion['model_end_time'] = mock_time
            completion['model_cost_time'] = 0
            completion['max_token'] = 500

            completion['server_extra_kwargs'] = {'is_cache': True,
                                                 'score': completion.get('score'),
                                                 'rejected_code': code}

            return json.dumps(completion)

        return Response(
            headers={'x-complete-id': data['complete_id']},
            status_code=200,
            content=mock_reject_content(data, reject_code.value),
            media_type="application/json"
        )


completion_reject_rule_chain = CompletionRejectRuleChain()
