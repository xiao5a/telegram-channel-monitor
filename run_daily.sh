#!/bin/bash
# 每日频道监控脚本
cd ~/Projects/telegram-channel-monitor

# 收集消息
echo "$(date '+%Y-%m-%d %H:%M:%S') - 开始收集频道消息..."
python3 monitor.py

# 格式化消息
echo "$(date '+%Y-%m-%d %H:%M:%S') - 格式化消息..."
python3 format_messages.py

echo "$(date '+%Y-%m-%d %H:%M:%S') - 完成！"
