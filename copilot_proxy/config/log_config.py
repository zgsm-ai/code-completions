import logging.config
import sys

uvicorn_logger = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s :: %(client_addr)s - "%(request_line)s" %(status_code)s',
            "use_colors": True
        },
        "info": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": '%(levelprefix)s %(asctime)s - %(message)s',
            "use_colors": True
        },
        "error": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": '%(levelprefix)s %(asctime)s - %(message)s',
            "use_colors": True
        },
    },
    "handlers": {
        "console": {  # 新增控制台 handler
            "class": "logging.StreamHandler",
            "formatter": "info",  # 使用 info 格式
            "stream": sys.stdout
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",  # 改为控制台输出
            "stream": sys.stdout  # 指定输出到标准输出
        },
        "info": {
            "formatter": "info",
            "class": "logging.StreamHandler",  # 改为控制台输出
            "stream": sys.stdout  # 指定输出到标准输出
        },
        "error": {
            "formatter": "error",
            "class": "logging.StreamHandler",  # 改为控制台输出
            "stream": sys.stderr  # 错误日志输出到标准错误
        },
    },
    "loggers": {
        "uvicorn.access": {
            "handlers": ["access"],
            "propagate": False
        },
        "uvicorn.info": {
            "handlers": ["info"],
            "propagate": False
        },
        "uvicorn.error": {
            "handlers": ["error"],
            "propagate": False
        },
    },
}
logging.config.dictConfig(uvicorn_logger)
logger = logging.getLogger("uvicorn.info")
