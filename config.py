"""
Telegram频道监控配置
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API配置（从 https://my.telegram.org 获取）
API_ID = int(os.getenv('TELEGRAM_API_ID', ''))
API_HASH = os.getenv('TELEGRAM_API_HASH', '')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE', '')

# 代理配置（在中国大陆地区需要）
PROXY = os.getenv('TELEGRAM_PROXY', '')  # 格式：socks5://127.0.0.1:1080 或 http://127.0.0.1:7890

# 频道配置
CHANNEL_USERNAME = '@OpenClaw_Group'  # 目标频道
HOURS_TO_COLLECT = 24  # 收集最近多少小时的消息

# 数据目录
SESSION_NAME = 'telegram_session'
DATA_DIR = 'data'
