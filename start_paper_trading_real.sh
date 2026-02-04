#!/bin/bash
# Start Nanba Paper Trading Bot with Real Market Data

cd /root/.openclaw/workspace

echo "🌙 NANBA PAPER TRADING BOT v3.0"
echo "================================"
echo "Using REAL Hyperliquid prices + Moon Dev signals"
echo ""

# Create directories
mkdir -p paper_trading_real_price/positions
mkdir -p paper_trading_real_price/trades

# Check dependencies
python3 -c "import requests" 2>/dev/null || pip install requests -q
python3 -c "import dotenv" 2>/dev/null || pip install python-dotenv -q

echo "✅ Dependencies checked"
echo "🚀 Starting bot..."
echo ""

python3 nanba_paper_trading_real_price.py
