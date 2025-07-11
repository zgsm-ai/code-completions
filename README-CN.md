# Code Completion Server


中文 | [English](README.md)

## 📌 项目简介

Costrict 的代码补全后端服务


# 🧰 运行环境


> Python: 3.11.5


# 🛠 如何运行

## 创建重要配置

`.env`

```
# OPENAI模型服务框架,如 http://ip:port/v1/completions
OPENAI_MODEL_HOST=""
# 模型请求模型的key,可选
OPENAI_MODEL_AUTHORIZATION=""
# OPENAI模型名称
OPENAI_MODEL=qwen2.5-coder-3b-instruct
```

## 启动

```shell
cd copilot_proxy
pip install -r requirements.txt
cp lsp/* copilot_proxy/ast_tools/cmd
python app.py
```


# 🛡 许可证

MIT License

# 📬 联系方式

如有问题欢迎提 issue