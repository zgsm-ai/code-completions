# 上下文请求封装模块
# 封装了对 Codebase Indexer API 的 HTTP 请求调用
#
# 功能：
# - search_definition: 代码定义搜索功能
# - search_semantic: 语义搜索功能
#
# API 基础地址: 环境变量CODEBASE_INDEXER_API_BASE_URL定义
# 授权方式: 无
import asyncio
import time

import aiohttp
import os
# import requests
from config.log_config import logger

BASE_URL = ""


def get_base_url():
    """获取基础URL

    Returns:
        str: 基础URL
    """
    global BASE_URL
    if not BASE_URL:
        BASE_URL = os.environ.get('CODEBASE_INDEXER_API_BASE_URL', "")
    return BASE_URL


headers = {}


CONTEXT_COST_TIME = None


def get_context_cost_time():
    """获取上下文获取时间"""
    global CONTEXT_COST_TIME
    if CONTEXT_COST_TIME is None:
        CONTEXT_COST_TIME = int(os.environ.get("CONTEXT_COST_TIME", 1500)) / 1000
    return CONTEXT_COST_TIME


async def req(session: aiohttp.client, url: str, params: dict) -> dict | None:
    start = time.time()
    """发送HTTP请求"""
    try:
        async with session.get(url, params=params, headers=headers, timeout=get_context_cost_time()) as resp:
            if resp.status != 200:
                logger.error(f"request failed, status code: {resp.status}, url: {url}")
                return None
            return await resp.json()
    except aiohttp.ClientError as e:
        logger.error(f"Network or client error: {str(e)}, url: {url}")
        return None
    except BaseException as e:
        logger.error(f"Unexpected error: {str(e)}, url: {url}")
        return None
    # finally:
        # end = time.time()
        # logger.info(f"request cost time: {end - start}")


async def search_definition(session: aiohttp.client, client_id,
                            codebase_path, file_path, code_snippet, start_line: int | None = None, end_line: int | None = None):
    """搜索代码定义（异步）

    需要满足 start_line & end_lien | code_snippet != None

    Args:
        session: aiohttp.client: aiohttp.ClientSession对象
        client_id: 客户端ID
        codebase_path: 代码库路径
        file_path: 文件路径
        code_snippet: 代码片段
        start_line: 起始行
        end_line: 结束行

    Returns:
        dict: 成功返回response.json()，失败返回None
    """
    url = f"{get_base_url()}/codebase-indexer/api/v1/search/definition"
    params = {
        'clientId': client_id,
        'codebasePath': codebase_path,
        'filePath': file_path,
    }
    if start_line and end_line:
        params['startLine'] = start_line
        params['endLine'] = end_line

    if code_snippet:
        params['codeSnippet'] = code_snippet

    return await req(session, url, params)


async def search_semantic(session: aiohttp.client, client_id, codebase_path, query, top_k):
    """语义搜索（异步）
    Args:
        session: aiohttp.client: aiohttp.ClientSession对象
        client_id: 客户端ID
        codebase_path: 代码库路径
        query: 查询字符串
        top_k: 返回结果数量

    Returns:
        dict: 成功返回response.json()，失败返回None
    """
    url = f"{get_base_url()}/codebase-indexer/api/v1/search/semantic"
    params = {
        'clientId': client_id,
        'codebasePath': codebase_path,
        'query': query,
        'topK': top_k
    }

    return await req(session, url, params)


async def search_relation(session: aiohttp.client, client_id, codebase_path,
                          file_path, code_snippet, include_content=False, max_layer=5):
    """关系检索（异步）
    Args:
        session: aiohttp.client: aiohttp.ClientSession对象
        client_id: 客户端ID
        codebase_path: 代码库路径
        file_path: 文件路径
        code_snippet: 代码片段
        include_content: 是否包含代码内容
        max_layer: 最大层级

    Returns:
        dict: 成功返回response.json()，失败返回None
    """
    url = f"{get_base_url()}/codebase-indexer/api/v1/search/relation"
    params = {
        'clientId': client_id,
        'codebasePath': codebase_path,
        'filePath': file_path,
        'codeSnippet': code_snippet,
        'maxLayer': max_layer
    }

    return await req(session, url, params)


