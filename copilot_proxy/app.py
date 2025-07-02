#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import config to load env
import config as _
import os
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from models import CompletionRequest
from utils.common import cache_clear
from utils.errors import FauxPilotException
from instances.tgi_proxy_v2 import TGIProxyV2
from utils.constant import FIM_INDICATOR
from services.coder_completions import coder_completions

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

    return coder_completions(data=data, proxy=TGIProxyV2())


@app.post("/v2/engines/clear_all_cache")
@app.post("/v1/engines/clear_all_cache")
async def clear_all_cache():
    cache_clear()
    return Response(
        status_code=200,
        content="cache_clear done",
        media_type="application/json"
    )


if __name__ == "__main__":
    host = os.environ.get("UVICORN_HOST", "0.0.0.0")
    port = int(os.environ.get("UVICORN_PORT", 5000))
    workers = int(os.environ.get("UVICORN_WORKERS", 2))
    backlog = int(os.environ.get("UVICORN_BACKLOG", 128))

    print("starting uvicorn server! HOST: {} PORT: {} WORKERS: {} backlog: {}".format(host, port, workers, backlog))

    uvicorn.run("app:app", host=host, port=port, workers=workers, backlog=backlog)
