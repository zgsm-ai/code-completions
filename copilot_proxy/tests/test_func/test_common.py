import time
import unittest
from utils.common import (cut_repetitive_text, cut_suffix_overlap, cut_text_by_tree_sitter,
                          is_cursor_in_parentheses, is_cursor_in_string, judge_css, is_valid_content,
                          cut_prefix_overlap, longest_common_substring, is_extreme_repetition)
from utils.tree_sitter import TreeSitterUtil
from tests.mock.mock_func_param import (
    MOCK_NOT_REPETITIVE_CONTENT,
    MOCK_REPETITIVE_CONTENT,
    MOCK_CUT_SUFFIX_OVERLAP_CONTENT,
    MOCK_CUT_TEXT_BY_TREE_SITTER,
    MOCK_FIND_NEAREST_BLOCK,
    MOCK_FIND_SECOND_LEVEL_NODE_BY_LINE_NUM,
    MOCK_IS_CURSOR_IN_PARENTHESES,
    MOCK_IS_CURSOR_IN_STRING,
    MOCK_CUT_CSS_STYLE,
    MOCK_IS_VALID_CONTEXT,
    MOCK_CUT_PREFIX_OVERLAP,
    MOCK_LONGEST_COMMON_SUBSTRING,
    MOCK_IS_EXTREME_REPETITION,
)


class TestCommonCase(unittest.TestCase):
    def test_cut_repetitive_text_1(self):
        for item in MOCK_NOT_REPETITIVE_CONTENT:
            self.assertEqual(cut_repetitive_text(item['content']), item['label'])

    def test_cut_repetitive_text_2(self):
        for item in MOCK_REPETITIVE_CONTENT:
            self.assertEqual(cut_repetitive_text(item['content']), item['label'])

    def test_cut_suffix_overlap(self):
        for item in MOCK_CUT_SUFFIX_OVERLAP_CONTENT:
            self.assertEqual(cut_suffix_overlap(item['text'], "", item['suffix']), item['label'])

    def test_cut_text_by_tree_sitter(self):
        for item in MOCK_CUT_TEXT_BY_TREE_SITTER:
            self.assertEqual(cut_text_by_tree_sitter(
                item['language'],
                item['text'],
                item['prefix'],
                item['suffix'],
                time.time(),
                3500
            ), item['label'])

    def test_find_nearest_block_1(self):
        for item in MOCK_FIND_NEAREST_BLOCK:
            tree_sitter = TreeSitterUtil(item["language"])
            nearest_block = tree_sitter.find_nearest_block(
                item['code'].encode("utf-8"),
                item['start_number'],
                item['end_number'])
            block_code = tree_sitter.get_text(nearest_block)
            self.assertEqual(block_code, item['label'])

    def test_is_code_syntax(self):
        all_line_num = 0
        for num, item in enumerate(MOCK_FIND_SECOND_LEVEL_NODE_BY_LINE_NUM):
            code = item['code']
            tree_sitter = TreeSitterUtil(item["language"])

            for line_num in range(len(code.split("\n"))):
                cur_node = tree_sitter.find_second_level_node_by_line_num(code.encode("utf-8"), line_num)
                target_block_code = tree_sitter.get_text(cur_node)
                prefix_node, suffix_node = tree_sitter.find_second_level_nearest_node_by_line_num(
                    code.encode("utf-8"), line_num)
                prefix_block_code = tree_sitter.get_text(prefix_node)
                suffix_block_code = tree_sitter.get_text(suffix_node)
                new_code = prefix_block_code + '\n' + target_block_code + '\n' + suffix_block_code
                is_syntax = tree_sitter.is_code_syntax(new_code)
                self.assertEqual(is_syntax, True)
                all_line_num += 1

        print(f"共{all_line_num}个用例，测试成功")

    def test_is_cursor_in_parentheses(self):
        for item in MOCK_IS_CURSOR_IN_PARENTHESES:
            self.assertEqual(is_cursor_in_parentheses(item['prefix'], item['suffix']), item['label'])

    def test_is_cursor_in_string(self):
        for item in MOCK_IS_CURSOR_IN_STRING:
            self.assertEqual(is_cursor_in_string(item['prefix']), item['label'])

    def test_cut_css_style(self):
        for item in MOCK_CUT_CSS_STYLE:
            self.assertEqual(judge_css(item['language'], item['content']), item['label'])

    def test_is_valid_content(self):
        for item in MOCK_IS_VALID_CONTEXT:
            self.assertEqual(is_valid_content(item['text']), item["label"])

    def test_cut_prefix_overlap(self):
        for item in MOCK_CUT_PREFIX_OVERLAP:
            self.assertEqual(
                cut_prefix_overlap(text=item["text"], prefix=item["prefix"], suffix="", cut_line=3),
                item["label"]
            )

    def test_longest_common_substring(self):
        for item in MOCK_LONGEST_COMMON_SUBSTRING:
            self.assertEqual(longest_common_substring(item['str1'], item['str2']), item['label'])

    def test_is_extreme_repetition(self):
        for item in MOCK_IS_EXTREME_REPETITION:
            self.assertEqual(is_extreme_repetition(item['code'])[0], item['label'])


if __name__ == '__main__':
    unittest.main()
