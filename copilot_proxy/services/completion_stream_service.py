#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Dict, Type
import os
import time

from models import CompletionContextAndIntention
from utils.common import (
    count_paired_symbols, get_right_paired_symbols,
    remove_strings, is_cursor_in_string, is_code_syntax,
    get_boundary_symbols, get_repetitive_rate, judge_css
)


class AbstractStreamHandler(ABC):

    def __init__(self, context: CompletionContextAndIntention):
        self._completed_content: str = ""
        self._buffered_content: str = ""
        self._exception_flag: bool = False
        self._context = context
        self._first_line_indent = self.get_line_indent(self._context.cursor_line_prefix)

    @staticmethod
    def get_line_indent(line):
        line = line.replace("\t", "    ")
        return len(line) - len(line.lstrip(' '))

    def get_completed_content_and_handle_ex(self) -> str:
        self.post_handle()
        if self._exception_flag:
            self.handle_exception()
        return self._completed_content

    def get_completed_content(self) -> str:
        return self._completed_content

    @abstractmethod
    def handle(self, cur_token_text) -> bool:
        raise NotImplementedError

    @abstractmethod
    def post_handle(self) -> bool:
        pass

    def handle_exception(self) -> bool:
        """
        当输出内容超过MAX_TOKENS，超时，异常等情况时候，exception_flag为True
        :return: 异常退出时，返回值为True
        """

        def judge_last_line_valid(last_line):
            strip_last_line = last_line.strip()
            if strip_last_line in [')', ']', '}', '"""']:
                return True
            return False

        if not self._exception_flag:
            return False
        # 异常终止时，验证最后一行是否无效，是则抛弃
        split_text = self._completed_content.split("\n")
        if len(split_text) > 1 and not judge_last_line_valid(split_text[-1]):
            self._completed_content = "\n".join(split_text[:-1])
        return True

    def mark_exception_flag(self):
        self._exception_flag = True

    def unmark_exception_flag(self):
        self._exception_flag = False

    def clear_all_content(self):
        self._completed_content = ""
        self._buffered_content = ""


class SingleLineStreamHandler(AbstractStreamHandler):
    def handle(self, cur_token_text) -> bool:
        """
        对于单行补全场景，输出一个字符触发一次流式检查，满足以下条件之一可退出流式输出：
            0. 当单行补全超过了1秒 并且 存在字符重复比率较大的情况，清空补全内容
            1. 当前拿到的流式输出字符为成对符号的右半部分（如：`)`，`}`, `]`） 且 加入当前字符后导致单行代码符号失配
            2. 若当前字符为常见边界符号（如：{ ( [ " ' : < ;） 并且 与后缀的首字符相同
        docs: https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=367739189
        :param cur_token_text:
        :return:
        """

        if self._exception_flag:
            return False
        # 当单行补全超过了1秒 并且 存在字符重复比率较大的情况，则清空补全内容退出流式输出
        if (time.time() - self._context.st) * 1000 > 1000 \
                and len(self._completed_content) > 20 \
                and get_repetitive_rate(self._completed_content) > 0.25:
            self.clear_all_content()
            return False

        for c in cur_token_text:
            # 当前拿到的流式输出字符为成对符号的右半部分时，进入成对符号失配判断逻辑
            if c in get_right_paired_symbols():

                full_text = (self._context.cursor_line_prefix +
                             self._completed_content +
                             self._context.cursor_line_suffix)

                # 忽略full_text中包含字符串的部分
                if not is_cursor_in_string(self._context.cursor_line_prefix):
                    full_text = remove_strings(full_text)

                # 统计full_text中的成对符号数量，若当前字符加入后导致成对符号失配，则退出流式输出
                paired_symbols_map = count_paired_symbols(full_text)
                left_c = get_right_paired_symbols()[c]
                if paired_symbols_map.get(left_c, 0) <= paired_symbols_map.get(c, 0):
                    return False

            # 若当前字符为常见边界符号 并且 与后缀的首字符相同，则退出流式输出
            if (self._context.cursor_line_suffix.strip() and
                    self._context.cursor_line_suffix.lstrip()[0] in get_boundary_symbols() and
                    c == self._context.cursor_line_suffix.lstrip()[0]):
                return False
            self._completed_content += c
        return True

    def post_handle(self) -> bool:
        pass


class MultiLineStreamHandler(AbstractStreamHandler):
    def __init__(self, context: CompletionContextAndIntention, k=None):
        super().__init__(context)
        if k is None:
            k = int(os.environ.get("MULTI_LINE_STREAM_K", 8))
        self.k = k
        self.close_stream_flag = False

    def handle(self, cur_token_text):
        """
        对于多行补全场景，输出一行触发一次流式检查，当满足以下条件可退出流式输出：
            1. 当补全行数 < k 且 不符合块级代码
            2. 当补全行数 >= k （k=8），且满足以下其中一个情况：
                2.1 使用tree-sitter做语法检查正确
                2.2 生成的内容不符合块级代码
            3.  补全行数大于等于2 且 补全css样式
        docs: https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=367739189
        :param cur_token_text:
        :return:
        """
        if self._exception_flag:
            return False

        newline_index = cur_token_text.find('\n')
        if newline_index != -1:
            # 一个token可能有很多个换行符，需要循环处理
            while newline_index != -1:
                cur_line = self._buffered_content + cur_token_text[:newline_index + 1]
                # 当补全行数 = 0时，忽略任何判断逻辑，直接采纳（即永远采纳第一行）
                if self._completed_content.count("\n") == 0:
                    pass
                # 当 0 < 补全行数 < k 且 不符合块级代码，结束流式输出
                elif self._completed_content.count('\n') < self.k:
                    if not self.__is_block_code(cur_line):
                        self.close_stream_flag = True
                        break
                # 当补全行数 >= k，且满足以下其中一个情况时，结束流式输出：
                # 1. 使用tree-sitter做语法检查正确
                # 2. 生成的内容不符合块级代码
                else:
                    if not self.__is_block_code(cur_line):
                        self.close_stream_flag = True
                        break
                    if (self._context.language != "python" and
                            is_code_syntax(self._context.language, self._completed_content + cur_line,
                                           self._context.prefix, self._context.suffix)):
                        self.close_stream_flag = True
                        self._completed_content += cur_line
                        break

                self._completed_content += cur_line
                cur_token_text = cur_token_text[newline_index + 1:]
                newline_index = cur_token_text.find('\n')
                self.__clear_buffer()

            # 缓存最后一个换行符的后面部分字符
            self._buffered_content = cur_token_text[newline_index + 1:]

            # 当前补全行数大于等于2 且 补全css样式，则清空补全内容退出流式输出
            if (self._completed_content.count('\n') >= 2 and
                    judge_css(self._context.language, self._completed_content)):
                self.clear_all_content()
                self.close_stream_flag = True
        else:
            self._buffered_content += cur_token_text

        # 当流式输出被主动关闭时，返回False
        return not self.close_stream_flag

    def post_handle(self) -> bool:
        # 若补全内容为空，则将缓存内容加入补全内容
        if not self._completed_content:
            self._completed_content += self._buffered_content
            return True
        # 当非主动关闭流式输出时，若加入缓存内容满足块级代码，则将缓存内容加入到补全内容中
        if not self.close_stream_flag and self.__is_block_code(self._buffered_content):
            self._completed_content += self._buffered_content
            return True
        self.__clear_buffer()
        return True

    def __is_block_code(self, cur_line):
        # 当前行补全的内容包含成对关键字时，也被认为为块级代码，如：except，finally
        words = cur_line.split()
        for keyword in ['catch', 'except', 'finally']:
            if len(words) >= 1 and words[0].startswith(keyword):
                return True
            if len(words) >= 2 and words[1].startswith(keyword):
                return True
        # 缩进级别大于等于第一行缩进级别，则认为当前补全内容为块级代码
        if self._first_line_indent <= self.get_line_indent(cur_line):
            return True
        return False

    def __clear_buffer(self):
        self._buffered_content = ""


class StreamHandlerFactory:
    _handlers: Dict[bool, Type[AbstractStreamHandler]] = {
        True: SingleLineStreamHandler,
        False: MultiLineStreamHandler,
        None: SingleLineStreamHandler,
    }

    @staticmethod
    def get_stream_handler(context: CompletionContextAndIntention) -> AbstractStreamHandler:
        return StreamHandlerFactory._handlers[context.is_single_completion](context)
