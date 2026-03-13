# Telegram 频道自动监控工具

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-API-blue.svg)](https://core.telegram.org/)

自动收集 Telegram 频道消息，生成每日摘要。支持定时任务，可集成到 OpenClaw 或独立运行。

## ✨ 特性

- 📡 自动收集 Telegram 频道消息
- 📊 生成格式化消息摘要
- ⏰ 支持定时任务自动执行
- 🔐 支持代理（适合中国大陆用户）
- 💾 多种输出格式（JSON、TXT、Markdown）
- 🤖 可集成 AI 生成智能摘要
- 📦 轻量级，依赖少

## 🚀 快速开始

### 1. 获取 Telegram API 凭证

访问 [https://my.telegram.org](https://my.telegram.org)：
1. 登录你的 Telegram 账号
2. 进入 "API development tools"
3. 创建应用，获取 `api_id` 和 `api_hash`

### 2. 克隆项目

```bash
git clone https://github.com/yourusername/telegram-channel-monitor.git
cd telegram-channel-monitor
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的凭证
```

编辑 `.env` 文件：

```env
# Telegram API 配置
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_PHONE=+8613800138000

# 代理配置（在中国大陆地区需要）
TELEGRAM_PROXY=http://127.0.0.1:7897
```

### 5. 首次登录

```bash
python3 monitor.py
```

输入 Telegram 发送的验证码完成登录。

### 6. 收集消息

```bash
python3 monitor.py
python3 format_messages.py
```

消息会保存到 `data/` 目录：
- `messages_YYYYMMDD.json` - 原始 JSON 数据
- `messages_YYYYMMDD.txt` - 格式化文本
- `summary_YYYYMMDD.md` - 每日摘要

## 📖 使用方法

### 基本使用

```bash
# 收集频道消息（默认最近24小时）
python3 monitor.py

# 格式化消息为文本
python3 format_messages.py
```

### 自定义配置

编辑 `config.py`：

```python
# 频道用户名（@channelname）
CHANNEL_USERNAME = '@OpenClaw_Group'

# 收集最近多少小时的消息
HOURS_TO_COLLECT = 24
```

### 集成 OpenClaw（可选）

在 OpenClaw 中配置定时任务：

```python
# 每天早上9点执行
0 9 * * * cd ~/Projects/telegram-channel-monitor && python3 monitor.py && python3 format_messages.py
```

## 📁 项目结构

```
telegram-channel-monitor/
├── config.py              # 配置文件
├── monitor.py             # 消息收集脚本
├── format_messages.py     # 消息格式化脚本
├── login.py              # 登录脚本
├── requirements.txt       # Python 依赖
├── .env.example          # 环境变量模板
├── .env                  # 环境变量配置（不提交）
├── README.md             # 项目说明
├── LICENSE               # MIT 许可证
├── data/                # 消息存储目录
│   ├── messages_*.json   # 原始 JSON 数据
│   ├── messages_*.txt    # 格式化文本
│   └── summary_*.md      # 每日摘要
└── .gitignore           # Git 忽略文件
```

## 🔧 高级功能

### AI 摘要生成

使用 OpenAI API 或 GLM 生成智能摘要：

```python
from openai import OpenAI

client = OpenAI(api_key='your_api_key')
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role": "system", "content": "你是一个专业的信息汇总助手"},
        {"role": "user", "content": summary_prompt}
    ]
)
```

### 定时任务（Linux/Mac）

使用 crontab 设置定时任务：

```bash
crontab -e
```

添加：

```
0 9 * * * cd ~/Projects/telegram-channel-monitor && python3 run_daily.sh
```

### 定时任务（OpenClaw）

使用 OpenClaw 的 cron 功能：

```json
{
  "name": "Telegram频道监控",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "执行Telegram频道监控并生成摘要"
  }
}
```

## 🌐 代理配置

### 在中国大陆地区

必须配置代理才能访问 Telegram：

```env
# Clash 默认端口
TELEGRAM_PROXY=http://127.0.0.1:7897

# V2Ray 默认端口
# TELEGRAM_PROXY=socks5://127.0.0.1:10808

# 其他代理
# TELEGRAM_PROXY=http://127.0.0.1:port
```

### 不需要代理的地区

留空即可：
```env
TELEGRAM_PROXY=
```

## 📊 输出示例

### JSON 格式

```json
{
  "channel": "@OpenClaw_Group",
  "collected_at": "2026-03-13T10:32:43",
  "time_range_hours": 24,
  "message_count": 1000,
  "messages": [
    {
      "id": 1,
      "date": "2026-03-13T02:32:00",
      "text": "消息内容",
      "sender": 123456789
    }
  ]
}
```

### Markdown 摘要

```markdown
# @OpenClaw_Group - 24小时消息汇总

## 🔥 核心话题

1. AI 模型对比与选择
2. OpenClaw 功能与配置

## 💡 重要信息

1. 记忆系统问题
2. Plan Mode 优势
```

## ⚠️ 注意事项

1. **Telegram API 限制**：
   - 每个账号每小时有请求限制
   - 建议每天只收集一次

2. **消息数量限制**：
   - 默认最多收集 1000 条消息
   - 可在 `monitor.py` 中调整 `limit` 参数

3. **代理要求**：
   - 在中国大陆地区必须配置代理
   - 确保代理在运行

4. **隐私保护**：
   - `.env` 文件包含敏感信息，不要提交到 Git
   - `telegram_session.session` 文件包含登录凭证

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Telethon](https://docs.telethon.dev/) - Telegram API 客户端
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架

---

**Created by:** 独孤九剑 🗡️
