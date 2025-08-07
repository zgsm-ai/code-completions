import structlog
from collections import OrderedDict


def move_pos_arg_to_message(_, method_name, ed):
    """
    ed 的结构：
    {
        'event': '固定字符串',   # 来自第一个位置参数
        'x': 1,                # 来自关键字参数
        'y': 2,
        ...
    }
    把 event -> message，其余不动
    """
    ed['msg'] = ed.pop('event', '')
    return ed


def reorder_fields(_, __, ed):
    """保证 level 始终在最前"""
    ordered = OrderedDict()
    ordered["level"] = ed.pop("level")    # 先把 level 放第一
    ordered["msg"] = ed.pop("event")  # event -> message
    ordered.update(ed)                    # 其余字段追加
    return ordered


structlog.configure(
    processors=[
        structlog.processors.add_log_level,   # 添加 level 字段
        reorder_fields,              # 重排字段,性能影响极低,可以忽略 可替换为move_pos_arg_to_message
        structlog.processors.JSONRenderer(ensure_ascii=False),  # 输出纯 JSON,不编码为\u形式
    ],
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

access_logger = structlog.get_logger("access")


if __name__ == '__main__':
    logger.info("hello", error="this is a test", error_zh_CN="这是一个测试")
