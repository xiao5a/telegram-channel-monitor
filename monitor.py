"""
Telegram频道消息监控脚本
"""
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
from telethon import TelegramClient, functions
from telethon.tl.types import InputPeerChannel
from config import (
    API_ID, API_HASH, PROXY, CHANNEL_USERNAME,
    HOURS_TO_COLLECT, SESSION_NAME,
    DATA_DIR, PHONE_NUMBER
)

# 创建数据目录
Path(DATA_DIR).mkdir(exist_ok=True)

def parse_proxy(proxy_url: str):
    """解析代理URL为Telethon格式"""
    if not proxy_url:
        return None

    parsed = urlparse(proxy_url)

    if parsed.scheme == 'http':
        return ('http', parsed.hostname, parsed.port or 80)
    elif parsed.scheme == 'https':
        return ('http', parsed.hostname, parsed.port or 443)
    elif parsed.scheme == 'socks5':
        return ('socks5', parsed.hostname, parsed.port or 1080, True, parsed.username or '', parsed.password or '')
    else:
        return None

async def collect_messages():
    """收集频道消息"""
    print(f"📡 开始收集频道 {CHANNEL_USERNAME} 的消息...")

    # 解析代理
    proxy = parse_proxy(PROXY) if PROXY else None

    # 创建客户端（支持代理）
    if proxy:
        print(f"🔧 使用代理: {PROXY}")
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=proxy)
    else:
        print("⚠️  未配置代理，可能无法连接（中国大陆需要）")
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    try:
        # 开始连接和登录
        print(f"🔐 正在连接Telegram，使用手机号: {PHONE_NUMBER}")
        await client.start(PHONE_NUMBER)
        print("✅ 登录成功！")

        # 获取频道实体
        channel = await client.get_entity(CHANNEL_USERNAME)
        print(f"✅ 已连接到频道: {channel.title}")

        # 计算时间范围
        cutoff_time = datetime.now() - timedelta(hours=HOURS_TO_COLLECT)
        print(f"📅 收取时间范围: {cutoff_time.strftime('%Y-%m-%d %H:%M')} 到现在")

        # 收集消息
        messages = []
        async for message in client.iter_messages(channel, limit=1000):
            if message.date.replace(tzinfo=None) < cutoff_time:
                break

            msg_data = {
                'id': message.id,
                'date': message.date.isoformat(),
                'sender': message.sender_id,
                'text': message.text,
                'reply_to': message.reply_to_msg_id if message.reply_to else None,
                'views': message.views
            }
            messages.append(msg_data)

        print(f"📊 共收集到 {len(messages)} 条消息")

        # 保存到JSON
        date_str = datetime.now().strftime('%Y%m%d')
        output_file = Path(DATA_DIR) / f'messages_{date_str}.json'

        data = {
            'channel': CHANNEL_USERNAME,
            'collected_at': datetime.now().isoformat(),
            'time_range_hours': HOURS_TO_COLLECT,
            'message_count': len(messages),
            'messages': messages
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ 消息已保存到: {output_file}")

        return output_file

    except Exception as e:
        print(f"❌ 错误: {e}")
        raise
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(collect_messages())
