import os
from dotenv import load_dotenv
from .log_config import logger
import logging


# from ../../.env load env
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))


def set_logger():
    # 创建一个适配器来桥接 structlog 和标准 logging
    class StructlogHandler(logging.Handler):
        def emit(self, record):
            # 将标准 logging 记录转换为 structlog 格式
            logger.info(record.getMessage(), **record.__dict__)
    
    structlog_handler = StructlogHandler()
    
    # change uvicorn logger
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        log = logging.getLogger(name)
        log.handlers.clear()
        log.addHandler(structlog_handler)  # 使用适配器 handler
        log.propagate = False  # 防止重复



set_logger()