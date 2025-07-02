# 定义信息 mock数据
MOCK_DEFINITIONS = [
    # data1
    {
      "code": 0,
      "message": "ok",
      "data": {
        "list": [
          {
            "name": "github.com/zgsm/review-checker/config",
            "content": "package config",
            "type": "package",
            "filePath": "config/config.go",
            "position": {
              "startLine": 1,
              "startColumn": 1,
              "endLine": 1,
              "endColumn": 15
            }
          },
          {
            "name": "Config",
            "content": "type Config struct {\n\tServer struct {\n\t\tPort int    `yaml:\"port\"`\n\t\tMode string `yaml:\"mode\"` // debug, release, test\n\t} `yaml:\"server\"`\n\n\tDatabase Database `yaml:\"database\"`\n\n\tRedis struct {\n\t\tHost     string `yaml:\"host\"`\n\t\tPort     int    `yaml:\"port\"`\n\t\tPassword string `yaml:\"password\"`\n\t\tDB       int    `yaml:\"db\"`\n\t\tEnabled  bool   `yaml:\"enabled\"` // Whether to enable Redis\n\t} `yaml:\"redis\"`\n\n\t// Asynchronous task queue configuration\n\tAsynq struct {\n\t\tConcurrency   int            `yaml:\"concurrency\"`     // Number of concurrent workers\n\t\tRetryCount    int            `yaml:\"retry_count\"`     // Maximum retry count\n\t\tRetryDelay    int            `yaml:\"retry_delay\"`     // Retry delay in seconds\n\t\tRedisPoolSize int            `yaml:\"redis_pool_size\"` // Redis connection pool size\n\t\tQueues        map[string]int `yaml:\"queues\"`          // Queue priorities\n\t\tLog           Log            `yaml:\"log\"`             // Asynq log configuration\n\t\tEnabled       bool           `yaml:\"enabled\"`         // Whether to enable Asynq\n\t} `yaml:\"asynq\"`\n\n\tLog Log `yaml:\"log\"`\n\n\t// HeaderPropagation configuration for propagating headers to context\n\tHeaderPropagation struct {\n\t\t// Headers to propagate from request to context\n\t\tHeaders []string `yaml:\"headers\"`\n\t} `yaml:\"header_propagation\"`\n\n\tI18n struct {\n\t\tDefaultLocale string `yaml:\"default_locale\"`\n\t\tBundlePath    string `yaml:\"bundle_path\"`\n\t} `yaml:\"i18n\"`\n\n\t// HTTPClient HTTP client configuration\n\tHTTPClient struct {\n\t\t// Default timeout in seconds\n\t\tTimeout int `yaml:\"timeout\"`\n\t\t// Default retry count\n\t\tMaxRetries int `yaml:\"max_retries\"`\n\t\t// Retry delay in seconds\n\t\tRetryDelay int `yaml:\"retry_delay\"`\n\t\t// Whether to enable request logging\n\t\tEnableRequestLog bool `yaml:\"enable_request_log\"`\n\t\t// Whether to enable response logging\n\t\tEnableResponseLog bool `yaml:\"enable_response_log\"`\n\t\t// Default request headers\n\t\tHeaders map[string]string `yaml:\"headers\"`\n\t\t// Proxy URL\n\t\tProxyURL string `yaml:\"proxy_url\"`\n\t\t// TLS configuration\n\t\tInsecureSkipVerify bool `yaml:\"insecure_skip_verify\"`\n\t\t// Dependent service configurations\n\t\tServices map[string]ServiceConfig `yaml:\"services\"`\n\t} `yaml:\"http_client\"`\n\t// ChatRag chatRag service configuration\n\tChatRag ChatRagConfig `yaml:\"chat_rag\"`\n\n\t// SeverityLevels defines thresholds for severity levels\n\tSeverityLevels SeverityLevels `yaml:\"severity_levels\"`\n\n\t// DefinitionTypes defines supported definition types for code analysis\n\t// ContextTypes defines supported types for context content\n\tContextTypes struct {\n\t\tSupportedTypes   []string `yaml:\"supported_types\"`    // Supported context content types\n\t\tAllowSkipContext bool     `yaml:\"allow_skip_context\"` // Whether to allow skipping context content\n\t} `yaml:\"context_types\"`\n}",
            "type": "declaration.struct",
            "filePath": "config/config.go",
            "position": {
              "startLine": 58,
              "startColumn": 1,
              "endLine": 131,
              "endColumn": 2
            }
          },

        ]
      },
    },
    # data2
    {
      "code": 0,
      "message": "ok",
      "data": {
        "list": [
          {
            "name": "Error",
            "content": "func Error(msg string, keysAndValues ...interface{}) {\n\tif logger == nil {\n\t\treturn\n\t}\n\tsugar := logger.Sugar()\n\tsugar.Errorw(msg, keysAndValues...)\n}",
            "type": "declaration.function",
            "filePath": "pkg/logger/logger.go",
            "position": {
              "startLine": 185,
              "startColumn": 1,
              "endLine": 191,
              "endColumn": 2
            }
          },
          {
            "name": "github.com/zgsm/review-checker/pkg/db",
            "content": "package db",
            "type": "package",
            "filePath": "pkg/db/db.go",
            "position": {
              "startLine": 1,
              "startColumn": 1,
              "endLine": 1,
              "endColumn": 11
            }
          },
        ]
      }
    }
]

# 语义检索的信息 mock数据
MOCK_SEMANTICS = [
    {
      "code": 0,
      "message": "ok",
      "data": {
        "list": [
          {
            "content": "def format_date_display(date_str: str) -> str:\n    \"\"\"\n    格式化日期显示为更友好的格式\n    \n    :param date_str: 日期字符串(YYYY-MM-DD)\n    :return: 格式化后的日期字符串(如: 2023年5月20日 星期六)\n    \"\"\"\n    date = datetime.strptime(date_str, \"%Y-%m-%d\")\n    weekday = [\"星期一\", \"星期二\", \"星期三\", \"星期四\", \"星期五\", \"星期六\", \"星期日\"][date.weekday()]\n    return f\"{date.year}年{date.month}月{date.day}日 {weekday}\"",
            "filePath": "diary/utils/formatter.py",
            "score": 0.6458103
          },
          {
            "content": "def format_content(content: str, width: int = 80) -> str:\n    \"\"\"\n    格式化日记内容，保持段落结构的同时自动换行\n    \n    :param content: 原始内容\n    :param width: 每行最大宽度\n    :return: 格式化后的内容\n    \"\"\"\n    paragraphs = content.split('\\n\\n')\n    formatted_paragraphs = []\n    \n    for para in paragraphs:\n        # 保持原有换行，仅处理超长行\n        lines = para.split('\\n')\n        wrapped_lines = []\n        for line in lines:\n            if len(line) > width:\n                wrapped_lines.append(textwrap.fill(line, width))\n            else:\n                wrapped_lines.append(line)\n        formatted_paragraphs.append('\\n'.join(wrapped_lines))\n    \n    return '\\n\\n'.join(formatted_paragraphs)",
            "filePath": "diary/utils/formatter.py",
            "score": 0.6458103
          },
        ]
      }
    },
    {
      "code": 0,
      "message": "ok",
      "data": {
        "list": [
          {
            "content": "def markdown_to_html(content: str) -> str:\n    \"\"\"\n    将Markdown格式的日记内容转换为HTML\n    \n    :param content: Markdown格式内容\n    :return: HTML格式内容\n    \"\"\"\n    # 简单实现，可扩展更多Markdown语法\n    html = content\n    html = html.replace('\\n', '<br>')\n    html = html.replace('**', '<strong>', 1).replace('**', '</strong>', 1)\n    html = html.replace('*', '<em>', 1).replace('*', '</em>', 1)\n    return html",
            "filePath": "diary/utils/formatter.py",
            "score": 0.6458103
          },
          {
            "content": "def get_manager() -> DiaryManager:\n    \"\"\"获取日记管理器实例\"\"\"\n    storage = FileStorage()\n    return DiaryManager(storage)",
            "filePath": "cli/commands.py",
            "score": 0.6458103
          },
        ]
      }
    }
]
