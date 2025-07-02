#!/usr/bin/env python
# -*- coding: utf-8 -*-


MOCK_SINGLE_LINE_STREAM_HANDLER = [
    {
        "is_single_completion": True,
        "cursor_line_prefix": "",
        "cursor_line_suffix": "):",
        "completion_code": "for i in range(10)",
        "accurate_code": "for i in range(10",
    },
    {
        "is_single_completion": True,
        "cursor_line_prefix": "",
        "cursor_line_suffix": "):",
        "completion_code": "for i in range(10):::",
        "accurate_code": "for i in range(10"
    },
    {
        "is_single_completion": True,
        "cursor_line_prefix": "def print_hello('1212', ",
        "cursor_line_suffix": "):",
        "completion_code": "print_time=10):",
        "accurate_code": "print_time=10"
    },
    {
        "is_single_completion": True,
        "cursor_line_prefix": "def print_hello('1212 ",
        "cursor_line_suffix": "):",
        "completion_code": ",'print_time=10):",
        "accurate_code": ",'print_time=10"
    },
    {
        "is_single_completion": True,
        "cursor_line_prefix": "def print_hello('1212",
        "cursor_line_suffix": ":",
        "completion_code": "')",
        "accurate_code": "')"
    },
    {
        "is_single_completion": True,
        "cursor_line_prefix": "return [i for i in range(10",
        "cursor_line_suffix": ")]",
        "completion_code": ")]",
        "accurate_code": ""
    },
    {
        "is_single_completion": True,
        "cursor_line_prefix": 'return _parse_srt_lines(',
        "cursor_line_suffix": ")",
        "completion_code": "Lines, bilingual)",
        "accurate_code": "Lines, bilingual"
    },
    {
        "is_single_completion": True,
        "cursor_line_prefix": "        for ax, (model, values)",
        "cursor_line_suffix": "):",
        "completion_code": " in zip(axes, model_group_score.items()):",
        "accurate_code": " in zip(axes, model_group_score.items()"
    },
    {
        "is_single_completion": True,
        "cursor_line_prefix": "tokens = tree_string.replace('(', ' ( ').replace('",
        "cursor_line_suffix": "",
        "completion_code": ")', ' ) ').split()",
        "accurate_code": ")', ' ) ').split()"
    },
]

MOCK_MULTI_LINE_STREAM_HANDLER = [

    # 例1，补全所在的第一行缩进级别12，当遇到缩进低于12的代码行，流式终止
    {
        "is_single_completion": False,

        "language": "python",

        "cursor_line_prefix": "        ",

        "cursor_line_suffix": "",

        "prefix": "            if left < n and arr[left] > arr[largest]:",

        "suffix": "                ",

        "completion_code": """
                largest = left
                a = 1
                if a:
                    print(a)
        """,

        "accurate_code": """
                largest = left
                a = 1
                if a:
                    print(a)
        """,
    },
    # 例2，对于def内符合缩进级别 且 语法正确的代码行，流式输出不会终止
    {
        "is_single_completion": False,

        "language": "python",

        "cursor_line_prefix": "",

        "cursor_line_suffix": "",

        "prefix": "",

        "suffix": "",

        "completion_code": """
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
    """,

        "accurate_code": """
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
    """,
    },
    # 例3，对于headers内符合缩进级别 且 语法正确的代码行，流式输出不会终止。一旦脱离headers缩进，直接退出
    {
        "is_single_completion": False,

        "language": "python",

        "cursor_line_prefix": "        ",

        "cursor_line_suffix": "",

        "prefix": """
def get_headers():
    headers = {

        """,

        "suffix": """
    }
    return headers
        """,

        "completion_code":
            """"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.baidu.com",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.baidu.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    """,

        "accurate_code":
            """"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.baidu.com",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.baidu.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    """,
    },
    # 例4，语法检查正确策略会保证完整块补全
    {
        "is_single_completion": False,

        "language": "go",

        "cursor_line_prefix": "",

        "cursor_line_suffix": "",

        "prefix": """
            def get_headers():
                headers = {

                    """,

                    "suffix": """
                }
                return headers
        """,

        "completion_code": """
            func shellSort(arr []int) {
                n := len(arr)
                for gap := n / 2; gap > 0; gap /= 2 {
                    for i := gap; i < n; i++ {
                        temp := arr[i]
                        j := i
                        for j >= gap && arr[j-gap] > temp {
                            arr[j] = arr[j-gap]
                            j -= gap
                        }
                        arr[j] = temp
                    }
                }
            }
        """,

        "accurate_code": """
            func shellSort(arr []int) {
                n := len(arr)
                for gap := n / 2; gap > 0; gap /= 2 {
                    for i := gap; i < n; i++ {
                        temp := arr[i]
                        j := i
                        for j >= gap && arr[j-gap] > temp {
                            arr[j] = arr[j-gap]
                            j -= gap
                        }
                        arr[j] = temp
                    }
                }
            }
        """,
    }
]
