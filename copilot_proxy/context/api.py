# 上下文请求封装模块
# 封装了对 Codebase Indexer API 的 HTTP 请求调用
#
# 功能：
# - search_definition: 代码定义搜索功能
# - search_semantic: 语义搜索功能
#
# API 基础地址: 环境变量CODEBASE_INDEXER_API_BASE_URL定义
# 授权方式: 无

import time
import aiohttp
import os
from config.log_config import logger

codebase_relation_url = ""
codebase_definition_url = ""
codebase_semantic_url = ""
CONTEXT_COST_TIME = 0


def init():
    global codebase_relation_url, codebase_definition_url, codebase_semantic_url, CONTEXT_COST_TIME
    # codebase_relation_url = os.environ.get('CODEBASE_RELATION_URL',
    #                                        "http://localhost:8080/codebase-indexer/api/v1/search/relation")
    codebase_definition_url = os.environ.get('CODEBASE_DEFINITION_URL',
                                            "http://localhost:8080/codebase-indexer/api/v1/search/definition")
    codebase_semantic_url = os.environ.get('CODEBASE_SEMANTIC_URL',
                                           "http://localhost:8080/codebase-embedder/api/v1/search/semantic")
    global CONTEXT_COST_TIME
    if CONTEXT_COST_TIME is None:
        CONTEXT_COST_TIME = int(os.environ.get("CONTEXT_COST_TIME", 1500)) / 1000
    return


async def req(session: aiohttp.client, url: str, params: dict, request_id: str = "", method="get") -> dict | None:
    start = time.time()
    headers = {
        "X-Request-ID": request_id
    }

    """发送HTTP请求"""
    global CONTEXT_COST_TIME
    try:
        if method == "get":
            async with session.get(url, params=params, headers=headers, timeout=CONTEXT_COST_TIME) as resp:
                if resp.status != 200:
                    logger.warning(f"request failed, status code: {resp.status}, url: {url}", request_id=request_id)
                    return None
                return await resp.json()
        else:
            async with session.post(url, json=params, headers=headers, timeout=CONTEXT_COST_TIME) as resp:
                if resp.status != 200:
                    logger.warning(f"request failed, status code: {resp.status}, url: {url}", request_id=request_id)
                    logger.debug(await resp.text())
                    return None
                return await resp.json()
    except aiohttp.ClientError as e:
        logger.warning(f"Network or client error: {str(e)}, url: {url}", request_id=request_id)
        return None
    except BaseException as e:
        logger.warning(f"Unexpected error: {str(e)}, url: {url}", request_id=request_id)
        return None
    # finally:
        # end = time.time()
        # logger.info(f"request cost time: {end - start}")


async def search_definition(session: aiohttp.client, client_id,
                            codebase_path, file_path, code_snippet, start_line: int | None = None, end_line: int | None = None,
                            request_id: str = ""):
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
        request_id: 请求id

    Returns:
        dict: 成功返回response.json()，失败返回None

    """
    global codebase_definition_url
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

    return await req(session, codebase_definition_url, params, request_id=request_id)


async def search_semantic(session: aiohttp.client, client_id, codebase_path, query, top_k, request_id: str = ""):
    """语义搜索（异步）
    Args:
        session: aiohttp.client: aiohttp.ClientSession对象
        client_id: 客户端ID
        codebase_path: 代码库路径
        query: 查询字符串
        top_k: 返回结果数量
        request_id: 请求id

    Returns:
        dict: 成功返回response.json()，失败返回None
    """
    global codebase_semantic_url
    params = {
        'clientId': client_id,
        'codebasePath': codebase_path,
        'query': query,
        'topK': top_k
    }

    return await req(session, codebase_semantic_url, params, request_id=request_id, method="post")


async def search_relation(session: aiohttp.client, client_id, codebase_path,
                          file_path, code_snippet, include_content=False, max_layer=5, request_id: str = ""):
    """关系检索（异步）
    Args:
        session: aiohttp.client: aiohttp.ClientSession对象
        client_id: 客户端ID
        codebase_path: 代码库路径
        file_path: 文件路径
        code_snippet: 代码片段
        include_content: 是否包含代码内容
        max_layer: 最大层级
        request_id: 请求id

    Returns:
        dict: 成功返回response.json()，失败返回None
    """
    global codebase_relation_url
    params = {
        'clientId': client_id,
        'codebasePath': codebase_path,
        'filePath': file_path,
        'codeSnippet': code_snippet,
        'maxLayer': max_layer
    }

    return await req(session, codebase_relation_url, params,request_id=request_id)


