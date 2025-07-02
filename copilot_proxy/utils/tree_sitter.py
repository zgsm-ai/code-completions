#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import functools
import tree_sitter
import time
from config.log_config import logger
from copy import deepcopy

LANGUAGES_SO_PATH = os.path.abspath("./utils/languages-29.so")


def calculate_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"函数 {func.__name__} 的执行耗时为: {execution_time:.6f} 秒")
        return result

    return wrapper


class TreeSitterUtil:
    def __init__(self, language):
        self.language = language
        self.parser = tree_sitter.Parser()
        self.tree_language = tree_sitter.Language(LANGUAGES_SO_PATH, language)
        self.parser.set_language(self.tree_language)

    def is_code_syntax(self, code):
        root_node = self.parser.parse(bytes(code, 'utf8')).root_node
        if self.language.lower() == 'lua':
            # lua 脚本需要执行两次才能识别正确，根因待定位
            root_node = self.parser.parse(bytes(code, 'utf8')).root_node
        return not root_node.has_error

    @calculate_time
    def intercept_syntax_error_code(self, code, prefix="", suffix="", time_start=None, time_out_threshold=3500):
        """
        对补全代码做语法校验, 如果不满足, 则循环从最后一个字符切割代码, 直到满足语法格式
        若超过了切割行数限制仍然校验不通过, 返回原有code
        """
        if not code:
            return code
        if time_start is None:
            time_start = time.time()
        cut_code = deepcopy(code)
        max_cut_count = self.get_last_k_line_str_len(cut_code, 1)
        try:
            for i in range(max_cut_count):
                if self.is_code_syntax(prefix + cut_code + suffix) and cut_code.strip():
                    if i != 0:
                        logger.info(f"{self.language}切割代码成功，切割前的内容：{code}， 切割后的内容：{cut_code}")
                    return cut_code.rstrip()
                cut_code = cut_code[:-1]
                # 如果超时, 则返回原有code
                if ((time.time() - time_start) * 1000) > time_out_threshold:
                    logger.info(f"{self.language}切割代码超时: {code}")
                    return code
        except Exception as e:
            logger.error(f"{self.language}切割代码失败:", e)
            return code
        logger.info(f"{self.language}切割代码失败: {code}")
        return code

    def get_last_k_line_str_len(self, code, k=3):
        """
        获取代码最后k行字符串长度
        :param code: 代码
        :param k: 获取最后k行
        :return: 最后k行字符串长度
        """
        code_split = code.split("\n")
        last_k_lines = []
        for i in range(len(code_split) - 1, -1, -1):
            if len(code_split[i]) == 0:
                continue
            if len(last_k_lines) == k:
                break
            last_k_lines.append(code_split[i])
        return sum(map(len, last_k_lines)) + max(k - 1, len(last_k_lines) - 1)

    @staticmethod
    def get_node_text(source_code, node):
        if node is None:
            return ""
        return source_code[node.start_byte - node.start_point[1]:node.end_byte].decode('utf-8')

    @staticmethod
    def get_text(node):
        if node is None:
            return ""
        return node.text.decode("utf-8")

    def find_nearest_block(self, code, start_number, end_number):
        """
        DFS，在指定遍历的深度条件下找到包含指定范围行数的完整block
        :param code:
        :param start_number:
        :param end_number:
        :return:
        """
        def traverse(node, sn, en, depth=3):
            if depth == 0:
                return None
            if node.start_point[0] <= sn <= node.end_point[0] and node.start_point[0] <= en <= node.end_point[0]:
                for child in node.children:
                    block = traverse(child, sn, en, depth - 1)
                    if block:
                        return block
                return node
            return None

        root_node = self.parser.parse(code).root_node
        return traverse(root_node, start_number, end_number, depth=3)

    def find_second_level_node_by_line_num(self, code, line_num):
        """
        找到第二个层级下指定行号的节点
        :param code:
        :param line_num:
        :return:
        """
        node = self.parser.parse(code).root_node
        for child in node.children:
            if child.start_point[0] <= line_num <= child.end_point[0]:
                return child
        return None

    def find_second_level_nearest_node_by_line_num(self, code, line_num):
        """
        找到第二个层级下指定行号的附近两个节点（prefix_node 和 suffix_node）
        :param code:
        :param line_num:
        :return:
        """
        prefix_node, suffix_node = None, None
        node = self.parser.parse(code).root_node
        for child in node.children:
            if not child.has_error and line_num > child.end_point[0]:
                prefix_node = child
            if not child.has_error and line_num < child.start_point[0]:
                suffix_node = child
                break
        return prefix_node, suffix_node
