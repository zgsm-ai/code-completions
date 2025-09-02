import os
from dotenv import load_dotenv
from .log_config import logger,set_level
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
    for uv in (("uvicorn", logging.INFO), ("uvicorn.error", logging.ERROR), ("uvicorn.access", logging.INFO)):
        log = logging.getLogger(uv[0])
        log.handlers.clear()
        log.addHandler(structlog_handler)  # 使用适配器 handler
        log.propagate = False  # 防止重复
        log.setLevel(uv[1])


set_logger()

set_level(os.getenv('LOG_LEVEL', 'INFO'))

logger.debug("init log ok")
