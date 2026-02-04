# 🤖 Trading Bot Collection

This directory contains various trading bots for different strategies and exchanges.

## Available Bots

### nanba_real_trading_bot.py
Production-ready trading bot with Hyperliquid integration.
- Real-time P&L tracking
- Live order execution
- Risk management

### nanba_paper_trading_real_price.py
Paper trading bot with real market data.
- Real Hyperliquid prices
- Moon Dev signal integration
- Accurate P&L simulation

## Usage

```bash
# Real trading (requires API key)
python3 nanba_real_trading_bot.py

# Paper trading (safe testing)
python3 nanba_paper_trading_real_price.py
```

## Configuration

Create `.env` file:
```bash
HYPERLIQUID_KEY=your_private_key_here
```

## Risk Warning

⚠️ Trading involves significant risk. Only trade with money you can afford to lose.
