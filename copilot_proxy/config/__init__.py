import os
from dotenv import load_dotenv
from .log_config import logger
import logging


# from ../../.env load env
load_dotenv(os.path.join(os.path.dirname(__file__), '../..', '.env'))


def set_logger():
    # change uvicorn logger
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        log = logging.getLogger(name)
        log.handlers.clear()
        log.addHandler(logger)  # 2. 挂到我们的 JSON handler
        log.propagate = False  # 3. 防止重复



set_logger()