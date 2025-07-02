#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from services.completion_stream_service import StreamHandlerFactory
from models import CompletionContextAndIntention
from tests.mock.mock_completion_stream_service_data import (
    MOCK_SINGLE_LINE_STREAM_HANDLER,
    MOCK_MULTI_LINE_STREAM_HANDLER
)


class TestStreamServiceCase(unittest.TestCase):
    def test_single_line_stream_handler(self):
        for item in MOCK_SINGLE_LINE_STREAM_HANDLER:
            context = CompletionContextAndIntention(
                is_single_completion=item['is_single_completion'],
                cursor_line_prefix=item['cursor_line_prefix'],
                cursor_line_suffix=item['cursor_line_suffix'],
            )
            stream_handler = StreamHandlerFactory.get_stream_handler(context)
            for c in item['completion_code']:
                if not stream_handler.handle(c):
                    break
            completed_content = stream_handler.get_completed_content_and_handle_ex()
            self.assertEqual(item['accurate_code'], completed_content)

    def test_multi_line_stream_handler(self):
        for item in MOCK_MULTI_LINE_STREAM_HANDLER:
            context = CompletionContextAndIntention(
                language=item['language'],
                prefix=item['prefix'],
                suffix=item['suffix'],
                is_single_completion=item['is_single_completion'],
                cursor_line_prefix=item['cursor_line_prefix'],
                cursor_line_suffix=item['cursor_line_suffix'],

            )
            stream_handler = StreamHandlerFactory.get_stream_handler(context)
            for c in item['completion_code']:
                if not stream_handler.handle(c):
                    break
            completed_content = stream_handler.get_completed_content_and_handle_ex()
            self.assertEqual(item['accurate_code'].rstrip(), completed_content.rstrip())


if __name__ == '__main__':
    unittest.main()
