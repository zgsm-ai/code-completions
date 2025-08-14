import json
import asyncio
import unittest
from unittest.mock import patch, AsyncMock
from unittest import TestCase
from tests.mock.mock_context_param import MOCK_DEFINITIONS, MOCK_SEMANTICS
from copilot_proxy.context.context import request_context,get_context

class TestRequestContext(TestCase):
    """测试 request_context 函数"""

    async def test_request_context_success(self):
        """测试成功响应"""
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=MOCK_DEFINITIONS[0])
        mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)

        with patch('aiohttp.ClientSession.get', return_value=mock_resp):
            def_results, semantic_results = await request_context(
                client_id="test",
                codebase_path="/test",
                file_path="test.py",
                code_snippets=["test1", "test2"],
                query=["query1", "query2"]
            )

            self.assertTrue(len(def_results) > 0)  # 定义检索结果不为空
            self.assertTrue(len(semantic_results) > 0)  # 语义检索结果不为空

    def test_get_context_success(self):
        """测试成功响应"""
        def mock_get(*args, **kwargs):
            mock_resp = AsyncMock()
            mock_resp.status = 200
            # 根据URL返回不同的mock数据
            if "definition" in str(args[0]):
                mock_resp.json = AsyncMock(return_value=MOCK_DEFINITIONS[1])
            elif "semantic" in str(args[0]):
                mock_resp.json = AsyncMock(return_value=MOCK_SEMANTICS[0])
            else:
                mock_resp.json = AsyncMock(return_value={})
            mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
            return mock_resp

        re = ""
        with patch('aiohttp.ClientSession.get', side_effect=mock_get):
            re = get_context(
                client_id="test",
                project_path="/test",
                file_path="test.py",
                prefix=" ",
                suffix=" ",
                import_content="import os")
        self.assertTrue(len(re) > 0)  # 定义检索结果不为空
        print(re)


if __name__ == "__main__":
    unittest.main()

