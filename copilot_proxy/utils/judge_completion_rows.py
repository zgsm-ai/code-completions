import yaml
import re
import os


class LanguageKeywords:
    def __init__(self):
        self.language_keywords = self.init_language_keywords()

    @staticmethod
    def init_language_keywords():
        with open('config/language_keywords.yml', 'r') as f:
            language_keywords_map = yaml.safe_load(f)
        return language_keywords_map

    def is_match_line(self, line, keywords):
        # 如果当前行只有关键字, 则按多行补全
        if line.strip() in keywords:
            return True
        pattern = r'^\s*(?:{})'.format('|'.join(keywords))
        return re.match(pattern, line) is not None

    def filter_code_lines(self, code_lines):
        filtered_lines = []
        for idx, line in enumerate(code_lines):
            if (line.strip() and not line.lstrip().startswith("//") and not line.lstrip().startswith("#")) \
                    or (idx == len(code_lines) - 1):
                filtered_lines.append(line)
        return filtered_lines

    def judge_completion_multiple_lines(self, prefix, language, uedc_components_map=None):
        if os.environ.get("UEDC_MULTIPLE_LINES", '').lower() != 'false' and uedc_components_map:
            # UEDC开启多行补全
            return True
        language_keywords_map = self.language_keywords.get(language)
        # 若没有配置其它语言的关键字yml, 返回True, 不影响其补全
        if not language_keywords_map:
            return True

        language_keywords = language_keywords_map.get("keywords")
        # 这里根据regular内容 匹配指定字符串, 来清除多行注释
        # regular = (['\"]{3}).*?\1  匹配``` ```或者""" """的内容
        # regular = /\*.*?\*/        匹配/* */ 的内容
        # regular = <!--[\s\S]*?-->  匹配<!-- -->的内容, vue注释
        # regular = : '[^']*'        匹配:       的内容, shell注释
        # regular = ^\s*=begin.*?=end\s*$       匹配:=begin =end的内容,ruby注释
        # regular = --\[(=*)\[(.*\n)*?\]\1\]--  匹配--[ ]--的内容，lua注释
        regular = language_keywords_map.get("regular", "")
        # re.MULTILINE 多行模式, re.DOTALL 视为一行
        pattern = re.compile(f"{regular}", re.DOTALL)
        code = pattern.sub('', prefix).replace('\n\n', '\n')
        code_lines = re.split(r'[\r\n\t]+', code)
        # 筛选行, 去除单行注释和空行
        filtered_lines = self.filter_code_lines(code_lines)

        if len(filtered_lines) >= 1 and self.is_match_line(filtered_lines[-1], language_keywords):
            return True
        if len(filtered_lines) >= 2 and self.is_match_line(filtered_lines[-2], language_keywords):
            return True
        return False
