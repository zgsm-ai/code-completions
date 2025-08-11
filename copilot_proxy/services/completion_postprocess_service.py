#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from abc import ABC, abstractmethod
from config.log_config import logger
from utils.common import (cut_suffix_overlap, cut_repetitive_text, is_python_text,
                          cut_prefix_overlap, is_extreme_repetition
                          )

from models import CompletionPostprocessorContext
from utils.decorator.common import function_timer


class CompletionPostprocessor:
    class ContentDiscardType(Enum):
        # 极端重复
        EXTREME_REPETITION = "discard-extreme_repetition"
        # 文件语言与补全语言不匹配
        NOT_MATCH_COMPLETION_LANGUAGE = "discard-not_match_completion_language"

    class ContentCutType(Enum):
        # 自身文本重复
        REPETITIVE_TEXT = "cut-repetitive_text"
        # 前缀处理
        PREFIX_OVERLAP = "cut-prefix_overlap"
        # 内容重叠裁剪
        SUFFIX_OVERLAP = "cut-suffix_overlap"


class AbstractCompletionPostprocessor(ABC):
    def process_discard(self, context: CompletionPostprocessorContext) -> bool:
        return False

    def process_cut(self, context: CompletionPostprocessorContext) -> str:
        return context.completion_code

    @abstractmethod
    def get_processor_type(self) -> str:
        pass


class DiscardExtremeRepetitionProcessor(AbstractCompletionPostprocessor):
    def process_discard(self, context: CompletionPostprocessorContext) -> bool:
        """
        极端重复内容丢弃
        :param context:
        :return:
        """
        flag, lcs, repeat_lines = is_extreme_repetition(context.completion_code)
        if not flag:
            return False

        logger.info(f"内容丢弃处理器：{self.get_processor_type()}命中，返回空补全！"
                    f"最长公共子串: {lcs}, 重复行数: {repeat_lines}")
        return True

    def get_processor_type(self) -> str:
        return CompletionPostprocessor.ContentDiscardType.EXTREME_REPETITION.value


class DiscardNotMatchCompletionLanguageProcessor(AbstractCompletionPostprocessor):
    def process_discard(self, context: CompletionPostprocessorContext) -> bool:
        """
        非python语言但是python代码，则丢弃补全内容
        :param context:
        :return:
        """
        if context.language.lower() != 'python' and is_python_text(context.completion_code):
            logger.info(f"内容丢弃处理器：{self.get_processor_type()}命中，返回空补全！")
            return True
        return False

    def get_processor_type(self) -> str:
        return CompletionPostprocessor.ContentDiscardType.NOT_MATCH_COMPLETION_LANGUAGE.value


class CutRepetitiveTextProcessor(AbstractCompletionPostprocessor):
    def process_cut(self, context: CompletionPostprocessorContext) -> str:
        """
        补全内容去重
        :param context:
        :return:
        """
        processed_code = cut_repetitive_text(context.completion_code)
        if processed_code != context.completion_code:
            logger.info(f"内容裁剪处理器：{self.get_processor_type()}命中。"
                        f"裁剪后的补全结果为：{processed_code}")
        return processed_code

    def get_processor_type(self) -> str:
        return CompletionPostprocessor.ContentCutType.REPETITIVE_TEXT.value


class CutPrefixOverlapProcessor(AbstractCompletionPostprocessor):
    def process_cut(self, context: CompletionPostprocessorContext) -> str:
        """
        补全内容前缀重复处理
        :param context:
        :return:
        """
        processed_code = cut_prefix_overlap(context.completion_code, context.prefix, context.suffix)
        if processed_code != context.completion_code:
            logger.info(f"内容裁剪处理器：{self.get_processor_type()}命中。"
                        f"裁剪后的补全结果为：{processed_code}")
        return processed_code

    def get_processor_type(self) -> str:
        return CompletionPostprocessor.ContentCutType.PREFIX_OVERLAP.value


class CutSuffixOverlapProcessor(AbstractCompletionPostprocessor):
    def process_cut(self, context: CompletionPostprocessorContext) -> str:
        """
        补全内容重叠裁剪
        :param context:
        :return:
        """
        processed_code = cut_suffix_overlap(context.completion_code, context.prefix, context.suffix)
        if processed_code != context.completion_code:
            logger.info(f"内容裁剪处理器：{self.get_processor_type()}命中。"
                        f"裁剪后的补全结果为：{processed_code}")
        return processed_code

    def get_processor_type(self) -> str:
        return CompletionPostprocessor.ContentCutType.SUFFIX_OVERLAP.value


class CompletionPostprocessorChain:
    def __init__(self, postprocessors: list[AbstractCompletionPostprocessor], request_id=""):
        self.postprocessors = postprocessors
        self.request_id = request_id
        self.__hit_processors = []

    def __process_discard(self, context: CompletionPostprocessorContext) -> bool:
        for postprocessor in self.postprocessors:
            if postprocessor.process_discard(context):
                self.__hit_processors.append(postprocessor.get_processor_type())
                return True
        return False

    def __process_cut(self, context: CompletionPostprocessorContext) -> str:
        for postprocessor in self.postprocessors:
            cut_text = postprocessor.process_cut(context)
            if cut_text != context.completion_code:
                self.__hit_processors.append(postprocessor.get_processor_type())
                context.completion_code = cut_text
        return context.completion_code

    @function_timer(name="补全后处理模块")
    def process(self, context: CompletionPostprocessorContext) -> str:
        """
        先处理内容丢弃情况，再处理内容裁剪情况
        :param context:
        :return:
        """
        logger.info(f"后处理前的补全内容为：{context.completion_code}", request_id=self.request_id)
        discard_flag = self.__process_discard(context)
        if discard_flag:
            context.completion_code = ""
            return context.completion_code
        self.__process_cut(context)
        return context.completion_code

    def get_hit_processors(self):
        return self.__hit_processors


class CompletionPostprocessorFactory:
    @staticmethod
    def create_default(request_id="") -> CompletionPostprocessorChain:
        return CompletionPostprocessorChain(
                [
                    DiscardExtremeRepetitionProcessor(),
                    DiscardNotMatchCompletionLanguageProcessor(),
                    CutRepetitiveTextProcessor(),
                    CutPrefixOverlapProcessor(),
                    CutSuffixOverlapProcessor()
                ],
                request_id=request_id
            )

    @staticmethod
    def create(postprocessors: list[AbstractCompletionPostprocessor]):
        return CompletionPostprocessorChain(postprocessors)
