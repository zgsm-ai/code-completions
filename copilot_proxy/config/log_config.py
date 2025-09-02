import sys

import structlog
import logging
from collections import OrderedDict

# --- 1. 配置标准库 logging ---
# 创建一个 logger 对象
std_logger = logging.getLogger("my_structlog_logger")  # 使用特定名称避免干扰根 logger
# 设置 logger 的最低处理级别为 INFO
# std_logger.setLevel(logging.INFO)

# 创建一个 StreamHandler 来输出到控制台
handler = logging.StreamHandler(sys.stdout)
# （可选）可以在这里给 handler 设置级别，但通常在 logger 上设置就足够了
# handler.setLevel(logging.INFO)

# （可选）设置 handler 的格式，虽然 structlog 会处理大部分格式，但这里可以设置基础格式
# 如果不设置，structlog 的 JSONRenderer 输出可能会被 handler 的默认格式包裹
# formatter = logging.Formatter('%(message)s')
# handler.setFormatter(formatter)

# 将 handler 添加到 logger
std_logger.addHandler(handler)


def set_level(level: int | str):
    std_logger.setLevel(level)


# --- 2. 定义 structlog 处理器 ---
def move_pos_arg_to_message(_, method_name, ed):
    """
    将 'event' 键重命名为 'msg'。
    ed 的结构：
    {
        'event': '固定字符串',   # 来自第一个位置参数
        'x': 1,                # 来自关键字参数
        'y': 2,
        ...
    }
    """
    ed['msg'] = ed.pop('event', '')
    return ed

def reorder_fields(_, __, ed):
    """保证 level 始终在最前"""
    ordered = OrderedDict()
    # 注意：add_log_level 添加的是 'level'，但标准库期望的是 'levelname'
    # 我们在这里使用 'level'，因为 JSONRenderer 会直接输出它
    # 如果需要与标准库字段名完全一致，可以添加一个重命名步骤
    level = ed.pop("level", "unknown") # 安全地弹出 level
    ordered["level"] = level
    # msg 应该是 event 的内容，这里假设 move_pos_arg_to_message 已经处理过
    # 或者直接从 event 获取
    msg = ed.pop("event", "") # 如果 move_pos_arg_to_message 没有先运行
    ordered["msg"] = msg
    ordered.update(ed) # 其余字段追加
    return ordered

# --- 3. 配置 structlog ---
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,  # 添加 level 字段 (例如 'info', 'debug')
        reorder_fields,
        # 使用标准库的过滤功能
        structlog.stdlib.filter_by_level,  # 这个处理器会根据绑定的 stdlib logger 的级别进行过滤
        structlog.processors.JSONRenderer(ensure_ascii=False), # 输出纯 JSON
    ],
    # 使用标准库的包装器
    wrapper_class=structlog.stdlib.BoundLogger,
    # 使用标准库的日志记录器工厂
    logger_factory=structlog.stdlib.LoggerFactory(),
    # 使用标准库的线程本地上下文类
    context_class=dict,
    cache_logger_on_first_use=True,
)

# --- 4. 获取 logger 实例 ---
# 获取 structlog logger，并将其绑定到底层的标准库 logger
logger = structlog.get_logger("my_structlog_logger")


if __name__ == '__main__':
    print("开始打印日志 (INFO 级别及以上):")
    std_logger.setLevel(logging.INFO)
    logger.debug("debug", info="this is debug", info_zh_CN="这是调试信息")  # 这条不会被打印
    logger.info("hello", info="this is a test", info_zh_CN="这是一个测试")  # 这条会被打印
    logger.warning("warning", info="something might be wrong", info_zh_CN="有潜在问题")  # 这条会被打印
    logger.error("error", info="something went wrong", info_zh_CN="出错了")  # 这条会被打印
    logger.critical("critical", info="system is down", info_zh_CN="系统崩溃")  # 这条会被打印

    print("\n--- 将标准库 logger 级别改为 WARNING ---")
    std_logger.setLevel(logging.WARNING)

    print("再次打印日志 (WARNING 级别及以上):")
    logger.debug("debug2", info="this is debug 2") # 不会打印
    logger.info("hello2", info="this is a test 2") # 不会打印
    logger.warning("warning2", info="something might be wrong 2") # 会打印
    logger.error("error2", info="something went wrong 2") # 会打印

    print("\n--- 将标准库 logger 级别改为 DEBUG ---")
    std_logger.setLevel(logging.DEBUG)
    logger.debug("debug3", info="this is debug 3")
    logger.info("hello3", info="this is a test 3")

