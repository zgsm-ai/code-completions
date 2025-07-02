# Code Completion Server


English | [中文](README-CN.md)

## 📌 Project Introduction

Shenma's code completion backend

## 🧰 Runtime Environment

> Python: 3.11.5

## 🛠 How to Run

### Create Important Configuration

`.env`

```
# OPENAI model service framework, such as http://ip:port/v1/completions
OPENAI_MODEL_HOST=""
# Model request key, optional
OPENAI_MODEL_AUTHORIZATION=""
# OPENAI model name
OPENAI_MODEL=qwen2.5-coder-3b-instruct
```

### Startup

```shell
cd copilot_proxy
pip install -r requirements.txt
cp lsp/* copilot_proxy/ast_tools/cmd
python app.py
```

## 🛡 License

MIT License

## 📬 Contact

If you have any questions, feel free to submit an issue
