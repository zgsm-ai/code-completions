#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import datetime

# import config to load env and init logger
import config as _
import os
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from metrics.prometheus_metrics import get_metrics_data
from models import CompletionRequest
from utils.common import cache_clear
from utils.errors import FauxPilotException
from instances.tgi_proxy_v2 import TGIProxyV2
from utils.constant import FIM_INDICATOR
from services.coder_completions import coder_completions
from config.log_config import logger
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import CONTENT_TYPE_LATEST


SCORE_INI_PATH = "./config/hide_score.yml"

app = FastAPI(
    title="FauxPilot",
    description="This is an attempt to build a locally hosted version of GitHub Copilot.",
    docs_url="/",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)


@app.exception_handler(FauxPilotException)
async def fauxpilot_handler(request: Request, exc: FauxPilotException):
    return JSONResponse(
        status_code=400,
        content=exc.json()
    )
    
    # 注册 metrics 路由
    app.include_router(metrics_router)
    

# Used to support copilot.vim
@app.get("/copilot_internal/v2/token")
def get_copilot_token():
    content = {'token': '1', 'expires_at': 2600000000, 'refresh_in': 900}
    return JSONResponse(
        status_code=200,
        content=content
    )


@app.post("/v2/engines/codegen/completions")
# Used to support copilot.vim
@app.post("/v2/engines/copilot-codex/completions")
@app.post("/v2/completions")
@app.post("/code-completion/api/v1/completions")
def completions_v2(data: CompletionRequest, request: Request):
    # 参数封装与处理
    if not data.prompt:
        data.prompt = data.prompt_options.prefix + FIM_INDICATOR + data.prompt_options.suffix
    data = data.dict()
    # Header转换为dict
    headers = dict(request.headers)
    x_request_id = request.headers.get("x-request-id")
    return coder_completions(data=data, proxy=TGIProxyV2(headers=headers), request_id=x_request_id)


@app.post("/v2/engines/clear_all_cache")
@app.post("/v1/engines/clear_all_cache")
async def clear_all_cache():
    cache_clear()
    return Response(
        status_code=200,
        content="cache_clear done",
        media_type="application/json"
    )


@app.get("/healthz")
def healthz():
    """K8s health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "code": "oidc-auth.userNotFound",
            "data": "",
            "message": "",
            "success": False,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.get("/ready")
def ready():
    """K8s readiness check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "code": "oidc-auth.userNotFound",
            "data": "",
            "message": "",
            "success": False,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.get("/metrics")
async def get_metrics():
    """
    获取 Prometheus 指标数据

    Returns:
        Response: 包含 Prometheus 格式指标数据的 HTTP 响应
    """
    # 获取格式化的指标数据
    metrics_data = get_metrics_data()

    # 返回 Prometheus 格式的响应
    return Response(
        content=metrics_data,
        media_type=CONTENT_TYPE_LATEST
    )


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info(
            # f"{request.method} {request.url.path} {response.status_code}",
            "",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            client_addr=request.client.host,
            duration_ms=round(duration * 1000, 2),
        )
        return response


app.add_middleware(AccessLogMiddleware)


if __name__ == "__main__":

    host = os.environ.get("UVICORN_HOST", "0.0.0.0")
    port = int(os.environ.get("UVICORN_PORT", 5000))
    workers = int(os.environ.get("UVICORN_WORKERS", 2))
    backlog = int(os.environ.get("UVICORN_BACKLOG", 128))

    logger.info("starting uvicorn server! HOST: {} PORT: {} WORKERS: {} backlog: {}".format(host, port, workers, backlog))

    uvicorn.run("app:app", host=host, port=port, workers=workers, backlog=backlog,access_log=False, log_level="info")

