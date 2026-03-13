"""
首次登录脚本 - 输入验证码
"""
import asyncio
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER, PROXY

from urllib.parse import urlparse

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

async def login():
    """登录并保存会话"""
    proxy = parse_proxy(PROXY) if PROXY else None

    if proxy:
        print(f"🔧 使用代理: {PROXY}")
        client = TelegramClient('telegram_session', API_ID, API_HASH, proxy=proxy)
    else:
        client = TelegramClient('telegram_session', API_ID, API_HASH)

    print(f"🔐 正在登录，使用手机号: {PHONE_NUMBER}")
    print("请输入Telegram发送的验证码:")

    try:
        await client.start(PHONE_NUMBER)
        print("✅ 登录成功！会话已保存。")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(login())
