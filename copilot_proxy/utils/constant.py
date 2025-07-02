#!/usr/bin/env python
# -*- coding: utf-8 -*-


from enum import Enum


class TriggerModeConst:
    AUTO = 'auto'
    MANUAL = 'manual'
    CONTINUE = "continue"


class FrontLanguageEnum(Enum):
    VUE = 'vue'
    TS = 'typescript'
    HTML = 'html'
    CSS = 'css'
    JS = 'javascript'

    @staticmethod
    def get_values():
        return [lang.value for lang in FrontLanguageEnum]


class VueTagConst:
    TS_START = '<script'
    TS_END = '\n</script>'
    HTML_START = '<template'
    HTML_END = '\n</template>'
    STYLE_START = '<style'
    STYLE_END = '\n</style>'


class ModelType:
    MAIN = "main"
    SMALL = "small"
    UEDC = "uedc"
    OPENAI = "openai"
    LOCAL = "local"


class OpenAIStreamContent:
    CHUNK_START_WORD = "data:"
    CHUNK_DONE_SIGNAL = "[DONE]"


FIM_INDICATOR = "<FILL_HERE>"

WIN_NL = '\r\n'
LINUX_NL = '\n'

RESPONSE_TEMPLATE = {
    'id': 'cmpl-x4Om5xLGYwvm7grsBhN2njODEPRnp',
    'model': 'bigcode/starcoder',
    'object': 'text_completion',
    'created': 1691977448,  # 需重新复制time
    'choices': [
        {
            'text': ''
        }
    ],
    'model_start_time': '2023-08-14T03:50:39.963960+0800',  # 需重新赋值
    'model_end_time': '2023-08-14T03:50:39.963960+0800',
    'model_cost_time': 0,
    'completion_tokens': 0,
    'cost_time': 0,
    'start_time': '2023-08-14T03:50:39.963960+0800',
    'end_time': '2023-08-14T03:50:39.963960+0800',
    'prompt_tokens': 0,
    'max_token': '30',
    'prompt': '',
    'is_same': True,
    'model_choices': [
        {
            'text': ''
        }
    ],
    'server_extra_kwargs': {
        'is_cache': True,
        'score': 0
    }
}
