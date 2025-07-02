#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re

from ast_tools.endpoint import get_endpoint
from config.log_config import logger
from utils.constant import FIM_INDICATOR, VueTagConst
from utils.common import random_completion_id
import ast
import os

LANGUAGE_LIST = ["python", "typescript", "javascript", "vue"]

STR_PATTERN = r"import +.*|from +.*|from +.* import *.*"
TREE_PATTERN = r"\(comment.*|\(string.*|\(set \(string.*|\(dictionary.*|\(integer.*|\(list.*|\(tuple.*"
TREE_STATUS = os.environ.get("TREE_STATUS", "") if os.environ.get("TREE_STATUS", "") else 'off'
# 需要外部环境变量传入所以设置为字符格式
END_TAG = os.environ.get("END_TAG", "") if os.environ.get("END_TAG", "") else "('>',';','}',')')"
LINE_COUNT_THRESHOLD = os.environ.get("LINE_COUNT_THRESHOLD", "") if os.environ.get("LINE_COUNT_THRESHOLD", "") else 5


class CodeFilters:
    def __init__(self, threshold_score: float = 0.3, str_pattern: str = '', tree_pattern: str = '',
                 fim_indicator: str = '', end_tag: str = ''):
        self.threshold_score = threshold_score
        self.str_pattern = str_pattern if str_pattern else STR_PATTERN
        self.tree_pattern = tree_pattern if tree_pattern else TREE_PATTERN
        self.fim_indicator = fim_indicator if fim_indicator else FIM_INDICATOR
        self.end_tag = end_tag if end_tag else END_TAG

    @staticmethod
    def too_few_lines(data):
        """
        prompt行数太少不触发补全，排除空行场景
        """
        prompt = data['prompt']
        lines = prompt.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != ""]
        line_count = len(non_empty_lines)
        if line_count < LINE_COUNT_THRESHOLD:
            logger.info(f"prompt行数{line_count}小于阈值{LINE_COUNT_THRESHOLD}，跳过自动补全")
            return True
        return False

    @staticmethod
    def split_prompt(prompt):
        text_before_cursor, text_after_cursor = "", ""
        if FIM_INDICATOR in prompt:
            try:
                split = prompt.split(FIM_INDICATOR)
                if len(split) >= 2:
                    text_before_cursor, text_after_cursor = split[-2], split[-1]
                else:
                    text_before_cursor, text_after_cursor = prompt, ""
            except Exception as err:
                raise ValueError(f"Only one {FIM_INDICATOR} allowed in prompt!, err={err}")
        return text_before_cursor, text_after_cursor

    def cursor_is_at_the_end(self, data):
        """
        光标位于行尾的直接不触发补全
        行尾定义：光标左侧是'>'、';'、'}'、')'，右侧是换行符号
        """
        text_before_cursor, text_after_cursor = self.split_prompt(data['prompt'])
        if text_before_cursor and text_after_cursor:
            if text_before_cursor.replace(' ', '').endswith(ast.literal_eval(self.end_tag)) \
                    and not text_after_cursor.split('\n')[0].strip():
                logger.info(f"光标位于行尾，跳过自动补全")
                return True
        return False

    def is_style(self, data):
        """
        光标位于style模块内直接不触发补全
        处于'<style></style>'之间
        """
        text_before_cursor, text_after_cursor = self.split_prompt(data['prompt'])
        if (f"\n{VueTagConst.STYLE_START}" in text_before_cursor or text_before_cursor.startswith(
                VueTagConst.STYLE_START)) and VueTagConst.STYLE_END in text_after_cursor:
            # 双标签齐全场景
            logger.info("is style模块内，跳过自动补全，双标签齐全场景")
            return True
        elif (f"\n{VueTagConst.STYLE_START}" in text_before_cursor or text_before_cursor.startswith(
                VueTagConst.STYLE_START)) and VueTagConst.STYLE_END not in text_before_cursor:
            # <style>单标签场景
            logger.info("is style模块内，跳过自动补全，<style>单标签场景")
            return True
        elif VueTagConst.STYLE_END in text_after_cursor and f"\n{VueTagConst.STYLE_START}" not in text_after_cursor \
                and not text_after_cursor.startswith(VueTagConst.STYLE_START):
            # </style>单标签场景
            logger.info("is style模块内，跳过自动补全，</style>单标签场景")
            return True
        return False

    def is_template(self, data):
        """
        光标位于template模块内直接不触发补全
        处于'<template></template>'之间
        """
        text_before_cursor, text_after_cursor = self.split_prompt(data['prompt'])
        if (f"\n{VueTagConst.HTML_START}" in text_before_cursor or text_before_cursor.startswith(
                VueTagConst.HTML_START)) and VueTagConst.HTML_END in text_after_cursor:
            # 双标签齐全场景
            logger.info("is template模块内，双标签齐全场景")
            return True
        elif (f"\n{VueTagConst.HTML_START}" in text_before_cursor or text_before_cursor.startswith(
                VueTagConst.HTML_START)) and VueTagConst.HTML_END not in text_before_cursor:
            # <template>单标签场景
            logger.info("is template模块内，<template>单标签场景")
            return True
        elif VueTagConst.HTML_END in text_after_cursor and f"\n{VueTagConst.HTML_START}" not in text_after_cursor \
                and not text_after_cursor.startswith(VueTagConst.HTML_START):
            # </template>单标签场景
            logger.info("is template模块内，</template>单标签场景")
            return True
        return False

    def is_script(self, data):
        """
        光标位于script模块内直接不触发补全
        处于'<script></script>'之间
        """
        text_before_cursor, text_after_cursor = self.split_prompt(data['prompt'])
        if (f"\n{VueTagConst.TS_START}" in text_before_cursor or text_before_cursor.startswith(
                VueTagConst.TS_START)) and VueTagConst.TS_END in text_after_cursor:
            # 双标签齐全场景
            logger.info("is script模块内，双标签齐全场景")
            return True
        elif (f"\n{VueTagConst.TS_START}" in text_before_cursor or text_before_cursor.startswith(
                VueTagConst.TS_START)) and VueTagConst.TS_END not in text_before_cursor:
            # <script>单标签场景
            logger.info("is script模块内，<script>单标签场景")
            return True
        elif VueTagConst.TS_END in text_after_cursor and f"\n{VueTagConst.TS_START}" not in text_after_cursor \
                and not text_after_cursor.startswith(VueTagConst.TS_START):
            # </script>单标签场景
            logger.info("is script模块内，</script>单标签场景")
            return True
        return False

    def is_pair_symbols(self, data):
        """
        针对成对符号场景，这里只覆盖单引号和双引号场景
        符号里面有内容则不补全，符号内无内容则补全
        """
        pair_symbols = ('\'', '"')
        text_before_cursor, text_after_cursor = self.split_prompt(data['prompt'])
        if text_before_cursor.split('\n')[-1].strip() and text_after_cursor.split('\n')[0].strip():
            if text_after_cursor.startswith(pair_symbols) and text_before_cursor.split(text_after_cursor[0])[-1]:
                logger.info(f"成对符号内容为非空场景，跳过自动补全")
                return True
        return False

    def text_after_fillhere_startwithword(self, data):
        """
        补全后面直接是英文字母开头或数字的不补全，比如修改变量名称的场景
        """
        _, text_after_cursor = self.split_prompt(data['prompt'])
        if text_after_cursor and (text_after_cursor[0].isalpha() or text_after_cursor[0].isdigit()):
            logger.info(f"光标后面是字符`{text_after_cursor[0]}`，跳过自动补全")
            return True
        return False

    def parse_cursor_text(self, prompt):
        """
        解析光标文本的位置和内容
        :param prompt: 用于解析的文本内容
        :return line, character, line_text:光标位置和光标所在的行
        """
        line = 0
        character = 0
        line_text = ''
        if prompt:
            line_list = prompt.split('\n')
            for i in range(len(line_list)):
                if self.fim_indicator in line_list[i]:
                    line_text = line_list[i].split(self.fim_indicator)[0]
                    line = i
                    character = len(line_text)
                    break
        return line, character, line_text

    def parse_same_level_function(self, data, line_text, line):
        """
        解析和当前行一样的函数，并替换掉data中的prompt
        :param data: 请求数据
        :param line_text: FILL_HERE所在的行内容
        :param line: FILL_HERE所在的行号
        :return func_count: 返回同级别函数名称数量
        """
        prompt = data.get('prompt', "")
        line_list = prompt.split('\n')
        func_prefix = 'def '
        if line_text.startswith(func_prefix):
            # 直接以def开头，说明无class，直接查找上文中也是def开头的函数即可
            func_count = self.update_prompt(data, line_text, line, line_list, func_prefix)
            return func_count
        else:
            # 查找def所属的class，由下往上查找
            start_line, end_line, class_line_text = self.parse_class_code(line, line_list, prompt)
            func_prefix = " " * (len(line_text) - len(line_text.lstrip())) + func_prefix
            func_count = self.update_prompt(data, line_text, line, line_list, func_prefix, start_line, end_line,
                                            class_line_text)
            return func_count

    @staticmethod
    def parse_class_code(line, line_list, prompt):
        """
        解析line行所在的class模块
        :param line: FILL_HERE所在的行号
        :param line_list: FILL_HERE所在的行内容
        :param prompt: FILL_HERE所在的行内容
        :return func_count: 返回同级别函数名称数量
        """
        start_line, end_line = 0, 0
        class_prefix = r' *class +.*:'
        class_line_text = ''
        for i in range(line, 0, -1):
            sub_line_number = i - 1
            sub_line_text = line_list[sub_line_number]
            if re.match(class_prefix, sub_line_text):
                character = len(sub_line_text) - len(sub_line_text.lstrip())
                cursor_position = {
                    "line": sub_line_number,  # 从 0 开始算
                    "character": character  # 从 0 开始算
                }
                try:
                    endpoint_result = get_endpoint('python',
                                                   prompt,
                                                   cursor_position)
                    end_point_line = endpoint_result.get('endPoint').get('line')
                    if end_point_line >= line:
                        class_line_text = sub_line_text
                        start_line, end_line = sub_line_number, end_point_line
                        break
                except Exception as err:
                    # 这里第三方工具异常不应该影响接口执行，直接捕获所有异常
                    print(f"get_endpoint failed, err={str(err)}")
        if end_line < line:
            # 如果查了一圈没有查到class的位置，则按照开头到line的位置找函数
            start_line, end_line = 0, line
        return start_line, end_line, class_line_text

    def update_prompt(self, data, line_text, line, line_list, func_prefix, start_line=0, end_line=0,
                      class_line_text=''):
        """
        组合新的prompt信息，剔除函数体
        """
        before_prompt = ''
        before_line_list = []
        after_prompt = ''
        after_line_list = []
        pass_blank = ' ' * (len(func_prefix) - len(func_prefix.lstrip()) + 4)
        inline_function_pattern = r' *def +__'  # 内置函数正则匹配规则
        if not end_line:
            end_line = len(line_list)
        for i in range(start_line, end_line):
            if line_list[i].startswith(func_prefix) and not bool(re.match(inline_function_pattern, line_list[i])):
                # 保留除内置函数外的其他函数
                if i < line:
                    before_line_list.append(line_list[i])
                if i > line:
                    after_line_list.append(line_list[i])
        if before_line_list:
            for sub_line in before_line_list:
                before_prompt = before_prompt + sub_line + f"\n{pass_blank}pass\n"
        if after_line_list:
            for sub_line in before_line_list:
                after_prompt = after_prompt + sub_line + f"\n{pass_blank}pass\n"
        if before_line_list or after_line_list:
            data['prompt'] = class_line_text + '\n' + before_prompt + line_text \
                             + self.fim_indicator + '\n' + after_prompt
            # print(f"new prompt is: {data['prompt']}.")
        return len(before_line_list) + len(after_line_list)

    def re_filter(self, line_text):
        """
        用于过滤不需要执行自动生成代码的场景
        """
        if re.match(self.str_pattern, line_text.strip()):
            logger.info(f"{line_text} 导包场景不补全")
            return True
        return False

    def tree_sitter_filter(self, data, line, character, language):
        """
        用于过滤不需要执行自动生成代码的场景
        """
        if TREE_STATUS == "off":
            return False
        cursor_position = {
            "line": line,  # 从 0 开始算
            "character": character  # 从 0 开始算
        }
        try:
            endpoint_result = get_endpoint(language,
                                           data.get('prompt', "").replace(self.fim_indicator, ''),
                                           cursor_position)
            if re.match(self.tree_pattern, endpoint_result.get("astResult", "")):
                print(endpoint_result.get("astResult", ""))
                return True
        except Exception as err:
            # 这里第三方工具异常不应该影响接口执行，直接捕获所有异常
            print(f"get_endpoint failed, err={str(err)}")
        return False

    def need_code(self, data):
        """
        是否需要触发模型进行自动补全编码
        :return bool:
        """
        # 暂时关闭， 参考https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=359875859
        # if self.too_few_lines(data):
        #     return False
        if self.cursor_is_at_the_end(data):
            return False
        if self.text_after_fillhere_startwithword(data):
            return False

        # language = data.get("language_id", "python")

        # 暂时关闭， 参考https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=359875859
        # if self.is_pair_symbols(data):
        #     return False

        # 暂时关闭， 参考https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=359875859
        # if language.lower() == FrontLanguageEnum.VUE and self.is_style(data):
        #     return False
        # 暂时关闭， 参考https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=359875859
        # if language.lower() == FrontLanguageEnum.VUE and not self.is_template(data) and not self.is_script(data):
        #     logger.info("vue代码既不是template也不是script模块内，跳过自动补全。")
        #     return False

        # line, character, line_text = self.parse_cursor_text(data.get('prompt', ""))
        # 这块效果不好，而且和后面的多行补全有冲突，暂时注释掉
        # python_function_pattern = r' *def +.*'
        # if re.match(python_function_pattern, line_text):
        #     # 特定补全场景-函数名与函数参数生成 -python
        #     logger.info("特定补全场景-函数名与函数参数生成 -python.")
        #     func_count = self.parse_same_level_function(data, line_text, line)
        #     if func_count > 0:
        #         return True
        #     else:
        #         return False

        # 暂时关闭， 参考https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=359875859
        # if self.re_filter(line_text) or self.tree_sitter_filter(data, line, character, language):
        #     # 特定场景不参与补全-python
        #     return False
        #
        # else:
        #     return True
        return True

    @staticmethod
    def non_streamed_response() -> str:
        completion = dict()
        completion['id'] = random_completion_id()
        completion['choices'] = []
        completion['server_extra_kwargs'] = {"is_cache": True}
        return json.dumps(completion)
