#!/bin/bash
echo "🚀 Telegram频道监控工具 - 初始化脚本"
echo "======================================"
echo ""

cd "$(dirname "$0")"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装Python依赖..."
pip3 install -r requirements.txt

# 创建.env文件
if [ ! -f .env ]; then
    echo ""
    echo "📝 创建.env配置文件..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件"
    echo ""
    echo "⚠️  请编辑 .env 文件，填入以下信息："
    echo "   - TELEGRAM_API_ID（从 https://my.telegram.org 获取）"
    echo "   - TELEGRAM_API_HASH"
    echo "   - TELEGRAM_PHONE（你的手机号，带国家代码）"
    echo "   - OPENAI_API_KEY（用于AI摘要生成）"
else
    echo "✅ .env 文件已存在"
fi

echo ""
echo "🎉 初始化完成！"
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，填入API凭证"
echo "2. 运行 'python3 monitor.py' 首次登录Telegram"
echo "3. 运行 'python3 run_daily.py' 测试完整流程"
echo ""
