FROM python:3.11.5-slim-bookworm
WORKDIR /python-docker

RUN apt update

COPY lsp ast_tools/cmd/

RUN chmod 755 ast_tools/cmd/*

COPY copilot_proxy/requirements.txt requirements.txt

RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

COPY copilot_proxy .

EXPOSE 5000

ENTRYPOINT []

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "app:app"]

