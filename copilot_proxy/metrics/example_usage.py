"""示例：如何使用 Prometheus 指标功能"""

import time
import random
from .prometheus_metrics import (
    record_completion_duration,
    record_completion_tokens,
    increment_completion_requests,
    timer
)


def example_usage():
    """演示如何使用各个指标函数"""
    
    # 示例1：记录请求耗时
    # 模拟一个 GPT-4 请求的总耗时
    record_completion_duration(
        phase="total",
        model="gpt-4",
        status="success",
        duration=2.5  # 2.5秒
    )
    
    # 模拟一个 Claude-3 请求的 LLM 调用耗时
    record_completion_duration(
        phase="llm",
        model="claude-3",
        status="success",
        duration=1.8  # 1.8秒
    )
    
    # 示例2：记录 Token 数量
    # 记录 GPT-4 请求的输入 token 数
    record_completion_tokens(
        token_type="input",
        model="gpt-4",
        token_count=1500
    )
    
    # 记录 GPT-4 请求的输出 token 数
    record_completion_tokens(
        token_type="output",
        model="gpt-4",
        token_count=500
    )
    
    # 示例3：记录请求总数
    # 记录成功的 GPT-4 请求
    increment_completion_requests(
        model="gpt-4",
        status="success"
    )
    
    # 记录超时的 Claude-3 请求
    increment_completion_requests(
        model="claude-3",
        status="timeout"
    )


def example_with_timer():
    """使用计时器上下文管理器的示例"""
    
    # 使用计时器自动记录耗时
    with timer("context", "gpt-4", "success"):
        # 模拟上下文处理
        time.sleep(0.5)
    
    # 使用计时器记录 LLM 调用耗时
    with timer("llm", "claude-3", "success"):
        # 模拟 LLM 调用
        time.sleep(1.2)


def simulate_real_request():
    """模拟真实的代码补全请求"""
    
    model = random.choice(["gpt-4", "claude-3", "starcoder"])
    status = random.choice(["success", "error_too_long", "timeout"])
    
    # 记录请求总数
    increment_completion_requests(model=model, status=status)
    
    # 记录输入 token
    input_tokens = random.randint(100, 5000)
    record_completion_tokens("input", model, input_tokens)
    
    # 记录输出 token（仅成功状态）
    if status == "success":
        output_tokens = random.randint(50, 2000)
        record_completion_tokens("output", model, output_tokens)
    
    # 记录各阶段耗时
    if status == "success":
        # 上下文处理耗时
        record_completion_duration("context", model, status, random.uniform(0.1, 0.5))
        
        # LLM 调用耗时
        record_completion_duration("llm", model, status, random.uniform(0.5, 3.0))
        
        # 总耗时
        record_completion_duration("total", model, status, random.uniform(1.0, 4.0))
    else:
        # 错误情况的总耗时
        record_completion_duration("total", model, status, random.uniform(0.5, 2.0))


if __name__ == "__main__":
    # 运行示例
    print("运行指标使用示例...")
    example_usage()
    
    print("运行计时器示例...")
    example_with_timer()
    
    print("模拟多个请求...")
    for i in range(10):
        simulate_real_request()
    
    print("示例完成！可以访问 /metrics 查看指标数据")