#!/usr/bin/env python
# -*- coding: utf-8 -*-


import yaml


class CompletionLineHandler:
    OTHER_LANGUAGE = "other"
    DEFAULT_URL = 'config/code_block_keywords.yml'

    def __init__(self):
        self.code_block_keywords_map = self.init_code_block_keywords()

    @classmethod
    def init_code_block_keywords(cls):
        with open(cls.DEFAULT_URL, 'r') as f:
            code_block_keywords_map = yaml.safe_load(f)
        return code_block_keywords_map

    def get_code_block_keywords(self, language):
        return self.code_block_keywords_map.get(language, self.code_block_keywords_map[self.OTHER_LANGUAGE])

    def judge_single_completion(self, cursor_line_prefix, cursor_line_suffix, language):
        """
        光标所在行后缀非空，则走单行补全（便于语法修复）
        若光标行前非空 且 光标所在行后缀为空 且 首单词和次首单词前缀不包含关键词 且 行间单词不包含关键词 则走单行补全
        ref: https://docs.atrust.sangfor.com/pages/viewpage.action?pageId=361621625
        :param cursor_line_prefix: 光标行前缀
        :param cursor_line_suffix: 光标行后缀
        :param language: 语言
        :return:
        """
        keywords = self.get_code_block_keywords(language)
        cursor_line_prefix_stripped = cursor_line_prefix.strip()
        # 光标所在行后缀非空，单行
        if cursor_line_suffix.strip():
            return True

        # 光标前为空，多行
        if not cursor_line_prefix_stripped:
            return False

        words = cursor_line_prefix_stripped.split()
        for keyword in keywords:
            if len(words) >= 1 and words[0].startswith(keyword):
                return False
            if len(words) >= 2 and words[1].startswith(keyword):
                return False
            if keyword in words:
                return False
        return True
