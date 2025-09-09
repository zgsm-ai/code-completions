"""Thread-safe Prometheus metrics for code completion service."""

import threading
import time
from typing import Optional, Literal
from prometheus_client import Histogram, Counter, CollectorRegistry, generate_latest

# 线程安全的指标注册表
_metrics_registry = CollectorRegistry()

# 请求耗时分布指标 (Histogram)
completion_duration_seconds = Histogram(
    'completion_duration_seconds',
    'Duration of completion requests in different phases',
    ['phase', 'model', 'status'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0),
    registry=_metrics_registry
)

# Token 数量分布指标 (Histogram)
completion_tokens = Histogram(
    'completion_tokens',
    'Number of input/output tokens in completion requests',
    ['type', 'model'],
    buckets=(10, 50, 100, 500, 1000, 2000, 5000, 10000, 50000),
    registry=_metrics_registry
)

# 请求总数指标 (Counter)
completion_requests_total = Counter(
    'completion_requests_total',
    'Total number of completion requests',
    ['model', 'status'],
    registry=_metrics_registry
)

# 线程锁，确保线程安全
_metrics_lock = threading.Lock()


def record_completion_duration(
    phase: Literal["total", "context", "llm"],
    model: str,
    status: Literal["success", "error_too_long", "timeout"],
    duration: float
) -> None:
    """
    记录请求在不同阶段的耗时分布
    
    Args:
        phase: 阶段，取值为 "total"、"context"、"llm"
        model: 模型名称，如 "gpt-4"、"claude-3"
        status: 请求状态，如 "success"、"error_too_long"、"timeout"
        duration: 耗时（单位：秒）
    """
    with _metrics_lock:
        completion_duration_seconds.labels(
            phase=phase,
            model=model,
            status=status
        ).observe(duration)


def record_completion_tokens(
    token_type: Literal["input", "output"],
    model: str,
    token_count: int
) -> None:
    """
    记录每次请求的输入和输出 token 数分布
    
    Args:
        token_type: 类型，取值为 "input" 或 "output"
        model: 模型名称
        token_count: token 数量（整数）
    """
    with _metrics_lock:
        completion_tokens.labels(
            type=token_type,
            model=model
        ).observe(token_count)


def increment_completion_requests(
    model: str,
    status: Literal["success", "error_too_long", "timeout"]
) -> None:
    """
    记录请求总数，用于计算 QPS 和错误率
    
    Args:
        model: 模型名称
        status: 请求状态
    """
    with _metrics_lock:
        completion_requests_total.labels(
            model=model,
            status=status
        ).inc()


def get_metrics_registry() -> CollectorRegistry:
    """
    获取指标注册表，用于暴露指标数据
    
    Returns:
        CollectorRegistry: Prometheus 指标注册表
    """
    return _metrics_registry


def get_metrics_data() -> bytes:
    """
    获取格式化的指标数据，用于 HTTP 响应
    
    Returns:
        bytes: 格式化的 Prometheus 指标数据
    """
    return generate_latest(_metrics_registry)

