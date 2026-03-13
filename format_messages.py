"""
格式化消息文件为文本，供OpenClaw读取并生成摘要
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from config import DATA_DIR

def format_messages(messages_file: str) -> str:
    """将消息JSON格式化为可读文本"""
    with open(messages_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = data['messages']
    channel = data['channel']
    collected_at = data['collected_at']
    time_range = data['time_range_hours']

    if not messages:
        return f"频道 {channel} 在最近{time_range}小时内没有新消息。"

    # 构建消息文本
    header = f"""# {channel} 频道消息汇总
- 收集时间: {collected_at}
- 时间范围: 最近{time_range}小时
- 消息数量: {len(messages)}

"""

    msg_text = ""
    for i, msg in enumerate(messages, 1):
        time = msg['date'][:16]  # 取到分钟
        text = msg['text'] or "[非文本消息]"
        views = f" 👁️{msg['views']}" if msg['views'] else ""
        reply = f" ↩️回复#{msg['reply_to']}" if msg['reply_to'] else ""

        msg_text += f"{i}. [{time}]{reply}{views}\n{text}\n\n"

    full_text = header + msg_text

    # 保存到文本文件
    date_str = datetime.now().strftime('%Y%m%d')
    text_file = Path(DATA_DIR) / f'messages_{date_str}.txt'

    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"✅ 消息文本已保存到: {text_file}")

    return full_text

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # 使用最新的消息文件
        data_files = sorted(Path('data').glob('messages_*.json'))
        if not data_files:
            print("❌ 没有找到消息文件")
            sys.exit(1)
        file_path = data_files[-1]

    print(f"📄 格式化文件: {file_path}")
    text = format_messages(file_path)

    # 输出前500字符预览
    print("\n预览:")
    print("="*50)
    print(text[:500] + "..." if len(text) > 500 else text)
    print("="*50)
