import math
import yaml
import time
from models import EditorHideScore


class HideScoreConfig(object):
    def __init__(self, config_file, threshold_score=None):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        self.contextual_filter_language_map = config['language']['contextualFilterLanguageMap']
        self.contextual_filter_weights = config['base']['contextualFilterWeights']
        self.contextual_filter_accept_threshold = config['base']['contextualFilterAcceptThreshold']
        self.contextual_filter_intercept = config['base']['contextualFilterIntercept']
        self.contextual_filter_character_map = config['base']['contextualFilterCharacterMap']
        self.threshold_score = config['base']['threshold'] if threshold_score is None else threshold_score

    @staticmethod
    def get_last_line_length(text: str):
        return len(text.split("\n")[-1])

    def calculate_hide_score(self, editor: EditorHideScore, language):
        # 判断光标权重
        whitespace_after_cursor = 0
        if editor.is_whitespace_after_cursor:
            whitespace_after_cursor = 1

        # 触发时间间隔，这里通过后台计算时候和插件端计算是有时间差的，但本身占比不大，误差在可接受范围内
        time_since_previous_label = (int(time.time()) * 1000 - editor.previous_label_timestamp) / 1000

        # 3.6最小值参考copilot的this.previousLabelTimestamp = Date.now() - 3600;
        time_since_previous_label_log = math.log(1 + max(3.6, time_since_previous_label))
        prefix_length_log = 0
        prefix_last_char_weight = 0
        prefix_str = editor.prefix
        if prefix_str:
            prefix_length_log = math.log(1 + self.get_last_line_length(prefix_str))
            prefix_last_char = prefix_str[-1]
            prefix_last_char_weight = self.contextual_filter_character_map.get(prefix_last_char, 0)

        suffix_length_log = 0
        suffix_last_char_weight = 0
        # 参考const g = h.trimEnd();  应该把换行符号也删掉
        trimmed_suffix_str = prefix_str.rstrip()
        if trimmed_suffix_str:
            suffix_length_log = math.log(1 + self.get_last_line_length(trimmed_suffix_str))
            suffix_last_char = trimmed_suffix_str[-1]
            suffix_last_char_weight = self.contextual_filter_character_map.get(suffix_last_char, 0)

        document_length_log = math.log(1 + max(editor.document_length, 0))
        prompt_end_pos_log = math.log(1 + max(editor.prompt_end_pos, 0))
        prompt_end_pos_ratio = (editor.prompt_end_pos + 0.5) / (1 + editor.document_length)

        # 若不支持该语言，默认走python
        language_weight = self.contextual_filter_language_map.get(language, 4)

        # 初始值-0.3
        score = self.contextual_filter_intercept
        # 上一个标签的权重(上一次接受的话，下一次基本都会给予补全) +0.99
        score += self.contextual_filter_weights[0] * editor.previous_label
        # 当前行光标后为空的话倾向补全 + 0.7
        score += self.contextual_filter_weights[1] * whitespace_after_cursor
        # 时间间隔的权重，上一次触发的时间越久越不补全 - 0.17
        score += self.contextual_filter_weights[2] * time_since_previous_label_log
        # 前缀尾行长度的权重，尾行越长越不补全 - 0.22
        score += self.contextual_filter_weights[3] * prefix_length_log
        # 前缀去除空行或者空格后尾行长度的权重（去除空格或空行后的尾行），后缀越长越补全 + 0.13
        score += self.contextual_filter_weights[4] * suffix_length_log
        # 文档长度的权重，越长越不补 - 0.007
        score += self.contextual_filter_weights[5] * document_length_log
        # 光标所在文档位置的权重，越靠后越补 + 0.005
        score += self.contextual_filter_weights[6] * prompt_end_pos_log
        # 光标位置与文档长度的比值的权重，越靠后越补 + 0.41
        score += self.contextual_filter_weights[7] * prompt_end_pos_ratio
        # 语言
        score += self.contextual_filter_weights[8 + language_weight]
        # 前缀的最后一个字符的权重
        score += self.contextual_filter_weights[29 + prefix_last_char_weight]
        # 前缀最后一个有效行的最后一个字符的权重
        score += self.contextual_filter_weights[125 + suffix_last_char_weight]
        probability_accept = 1 / (1 + math.exp(-score))
        return probability_accept
