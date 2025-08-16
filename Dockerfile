FROM python:3.11.5-slim-bookworm
WORKDIR /python-docker

COPY lsp ast_tools/cmd/

RUN chmod 755 ast_tools/cmd/*

COPY copilot_proxy/requirements.txt requirements.txt

RUN apt update

RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

COPY copilot_proxy .

EXPOSE 5000

ENTRYPOINT []

CMD ["python", "app.py"]

