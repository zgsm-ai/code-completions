"""Prometheus metrics module for code completion service."""

from .prometheus_metrics import (
    record_completion_duration,
    record_completion_tokens,
    increment_completion_requests,
    get_metrics_registry
)

__all__ = [
    'record_completion_duration',
    'record_completion_tokens',
    'increment_completion_requests',
    'get_metrics_registry'
]