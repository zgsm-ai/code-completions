import asyncio

from typing import List, Tuple

import os
import aiohttp

from .utils import get_code_last_n_lines, get_code_first_n_lines
from .notes_code import get_comment
from .parse import parse_semantic, parse_definition, r_slice_after_nth_instance
from .api import search_semantic, search_definition

CONTEXT_COST_TIME = None
DISABLE_CONTEXT_DEF_SEARCH = None
DISABLE_CONTEXT_SEMANTIC = None
def get_context_cost_time():
    """获取上下文获取时间"""
    global CONTEXT_COST_TIME
    if CONTEXT_COST_TIME is None:
        CONTEXT_COST_TIME = int(os.environ.get("CONTEXT_COST_TIME", 1500)) / 1000
    return CONTEXT_COST_TIME


def get_search_switch() -> (bool, bool):
    """返回搜索开关, 是否开启定义检索, 是否开启语义检索"""
    global DISABLE_CONTEXT_DEF_SEARCH, DISABLE_CONTEXT_SEMANTIC
    if DISABLE_CONTEXT_DEF_SEARCH is None:
        DISABLE_CONTEXT_DEF_SEARCH = os.environ.get("DISABLE_CONTEXT_DEF_SEARCH", "false").lower() == "false"
    if DISABLE_CONTEXT_SEMANTIC is None:
        DISABLE_CONTEXT_SEMANTIC = os.environ.get("DISABLE_CONTEXT_SEMANTIC", "false").lower() == "false"
    return DISABLE_CONTEXT_DEF_SEARCH, DISABLE_CONTEXT_SEMANTIC


async def request_context(client_id: str, codebase_path: str, file_path: str,
                          code_snippets: list[str],
                          query: List[Tuple[str, int]],
                          request_id: str = ""
                          ) -> (List, List, List):
    """ 请求上下文信息, 使用异步请求, 直接返回响应
    Args:
        client_id (str): 客户端id
        codebase_path (str): 代码库路径
        file_path (str): 文件路径
        code_snippets (list[str]): 定义检索 代码片段 n个片段, 异步并行查询
        query (List[Tuple[str, int]]): 语义检索 查询信息,元组内分别是查询的内容和返回的个数
        request_id: 请求id

    Returns:
        List, List: 返回上下文信息（定义信息、语义检索信息） 不会返回None,但列表元素可能为None或为空
    """
    if not client_id or not codebase_path or not file_path:
        return [], []
    async with (aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, limit_per_host=10, keepalive_timeout=3))
                as session):
        tasks = []
        def_on, semantic_on = get_search_switch()
        # 定义检索
        if code_snippets and def_on:
            for code_snippet in code_snippets:
                if code_snippet:
                    tasks.append(
                        search_definition(session, client_id, codebase_path, file_path, code_snippet, None, None, request_id=request_id))
        definition_index = len(tasks)

        # 语义检索
        if query and semantic_on:
            for q in query:
                if q and len(q) == 2:
                    tasks.append(search_semantic(session, client_id, codebase_path, q[0], q[1], request_id=request_id))
        # semantic_index = len(tasks)
        if len(tasks) == 0:
            return [], []
        # 等待所有任务完成
        try:
            # 给每个任务关联上它的索引位置
            indexed_tasks = [(asyncio.create_task(task), i) for i, task in enumerate(tasks)]

            # 执行所有任务，并设置超时
            done, pending = await asyncio.wait([task for task, _ in indexed_tasks], timeout=get_context_cost_time())

            # 收集已完成任务的结果，同时保持它们的原始索引信息
            results_with_index = [(t.result(), index) for t, index in indexed_tasks if t in done and t.done()]

            # 根据原始索引，分别整理前relation_index个任务和后边的任务的结果
            first_part_results = [result for result, index in results_with_index if index < definition_index]
            second_part_results = [result for result, index in results_with_index if index >= definition_index]

            # 取消未完成的任务
            for task in pending:
                task.cancel()
            return first_part_results, second_part_results
        except Exception as e:
            return [], []


def get_context(client_id: str, project_path: str, file_path, prefix: str, suffix: str,
                import_content: str | None = None, request_id: str = "") -> str:
    """获取上下文信息
    Args:
        client_id (str): 客户端id
        project_path (str): 项目路径
        file_path (str): 文件路径
        prefix (str): 前缀
        suffix (str): 后缀
        import_content (str): 导入内容
        request_id: 请求id

    Returns:
        str: 返回上下文信息
    """
    if not client_id or not project_path or not file_path or (not prefix and not suffix):
        return ""
    if prefix is None:
        prefix = ""
    if suffix is None:
        suffix = ""
    if import_content is None:
        import_content = ""
    file_path = os.path.join(project_path, file_path)
    # win 风格路径
    if len(project_path) > 1 and project_path[1:3] == ':\\':
        file_path = file_path.replace("/", "\\")

    # 获取prefix最后n行代码 (语义检索),
    # n_line_code = get_code_last_n_lines(prefix, 3)
    semantic_search_content = r_slice_after_nth_instance(prefix, "\n", 4)
    # 定义检索分为两次,一次周围行,一次全部
    definition_code_snap = [
        # 周围30行在前,后续处理权重更高,暂时弃用
        # "{}{}{}".format(import_content, prefix[:find_str_n(prefix, "\n", 20)+1], suffix[:find_str_n(suffix, "\n", 10)+1]),
        # 全部行在后, 后续处理权重更低
        "{}{}{}".format(import_content, prefix, suffix)
    ]
    # 请求定义、语义
    definition, semantic = asyncio.run(request_context(client_id,
                                                       project_path,
                                                       file_path,
                                                       definition_code_snap,
                                                       [(semantic_search_content, 10)], request_id=request_id))
    # 解析返回的语义检索结果,返回全部结果
    semantic_codes = parse_semantic(semantic)
    # 解析定义检索的结果
    def_codes = parse_definition(definition)
    all_codes = []

    # 合并定义检索结果
    if def_codes:
        all_codes.extend([item for sublist in def_codes for item in sublist[1:]])

    # 合并语义检索结果
    if semantic_codes:
        all_codes.extend([item for sublist in semantic_codes for item in sublist[:2]])  # 语义结果
    # 合并语义检索结果
    semantic_result = "\n".join(all_codes)
    # 解析返回的关系检索结果
    return get_comment(file_path, semantic_result)

