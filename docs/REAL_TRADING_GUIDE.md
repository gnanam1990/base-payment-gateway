# NANBA REAL TRADING BOT v2.0
## Hyperliquid Integration Guide

---

## 🎯 What This Bot Does

**REAL trading bot** (not paper trading):
- ✅ Connects to Hyperliquid exchange
- ✅ Gets REAL market prices from orderbook
- ✅ Shows REAL account balance
- ✅ Tracks REAL unrealized P&L
- ✅ Can place REAL orders (if enabled)

---

## 📋 Prerequisites

### 1. Hyperliquid Account
- Go to https://app.hyperliquid.xyz
- Connect wallet (MetaMask, etc.)
- Deposit USDC (start with $10-50 for testing)

### 2. Get Private Key

⚠️ **SECURITY WARNING:** Never share your private key!

```bash
# Export from MetaMask (for Hyperliquid wallet)
# 1. Open MetaMask
# 2. Click account menu (3 dots)
# 3. Account Details → Export Private Key
# 4. Copy the key (starts with 0x...)
```

### 3. Setup Environment

```bash
# Create .env file
cd /root/.openclaw/workspace
cat > .env << EOF
HYPERLIQUID_KEY=your_private_key_here_starts_with_0x
EOF

# Install dependencies
pip install -r requirements_real_trading.txt
```

---

## 🚀 Usage

### Step 1: Test Connection (Safe)
```bash
python3 nanba_real_trading_bot.py
```

This will:
- Connect to Hyperliquid
- Show your account balance
- Show open positions
- Show unrealized P&L
- **NO trades executed**

### Step 2: Monitor Real-Time

The bot shows:
```
💰 Account Value: $1250.00
💎 Unrealized P&L: $+25.50
💹 BTC Price: $42500.00
```

Updates every 10 seconds with REAL data!

---

## 🔧 How It Works

### Real Price Fetching
```python
# Get from Hyperliquid L2 orderbook
response = requests.post('https://api.hyperliquid.xyz/info', json={
    'type': 'l2Book',
    'coin': 'BTC'
})

# Real bid/ask prices
bid = $42499.50  (highest buyer)
ask = $42500.50  (lowest seller)
mid = $42500.00  (fair price)
```

### Real P&L Calculation
```python
# From Hyperliquid API
user_state = info.user_state(address)
positions = user_state['assetPositions']

for pos in positions:
    unrealized_pnl = pos['unrealizedPnl']  # REAL P&L!
```

### Real Order Placement
```python
# Market order (instant execution)
exchange.order(
    coin='BTC',
    is_buy=True,
    sz=0.01,  # BTC amount
    limit_px=0,  # Market order
    order_type={"market": {}}
)
```

---

## 📊 What You See

### Real Account Info:
```
📍 Address: 0x1234...5678
💰 Account Value: $1250.00
📊 Margin Used: $150.00
📈 Open Positions: 1
   BTC: 0.01 @ $42000.00
📊 BTC Unrealized P&L: $+50.00
```

### Real-Time Updates:
```
💹 BTC Price: $42500.00 (changes every second!)
💎 Unrealized P&L: $+50.00 → $+45.00 → $+52.00
```

---

## ⚠️ IMPORTANT SAFETY

### Current Bot Behavior:
- ✅ **READ-ONLY by default**
- ✅ Shows real data
- ✅ Tracks real P&L
- ❌ **Does NOT place orders** (unless you modify)

### To Enable Trading:
Edit `nanba_real_trading_bot.py`:
```python
# Find this line and uncomment/modify:
# self.place_market_order(True, 10)  # BUY $10 BTC
```

**⚠️ Only enable after testing and with small amounts!**

---

## 🛡️ Risk Management

### Built-in Limits:
```python
max_position_size = 50  # USD per trade
leverage = 3            # Max 3x
```

### Safety Features:
- Check balance before trading
- Position size limits
- Automatic error handling
- No over-leverage

---

## 🆚 Paper vs Real Trading

| Feature | Paper Bot | Real Bot |
|---------|-----------|----------|
| **Money** | Fake | REAL USDC |
| **Price** | Sweep data | Orderbook L2 |
| **P&L** | Simulated | Real from exchange |
| **Orders** | Virtual | Real on Hyperliquid |
| **Risk** | None | Real loss possible |

---

## 🐛 Troubleshooting

### Error: "HYPERLIQUID_KEY not found"
```bash
# Create .env file
echo "HYPERLIQUID_KEY=0x..." > .env
```

### Error: "Insufficient balance"
- Deposit USDC to Hyperliquid
- Minimum $10 recommended for testing

### Error: "Invalid private key"
- Make sure key starts with `0x`
- Should be 64 characters + 0x = 66 total

---

## 📈 Next Steps

1. ✅ Test connection (read-only)
2. ✅ Verify P&L matches Hyperliquid UI
3. ✅ Paper trade first (manual small trades)
4. ✅ Enable bot trading with $10
5. ✅ Scale up gradually

---

## 💡 Key Differences from Paper Bot

| Aspect | Paper Bot | This Real Bot |
|--------|-----------|---------------|
| **Data Source** | Moon Dev sweeps | Hyperliquid L2 |
| **Price** | Historical sweep | Real-time orderbook |
| **P&L** | Calculated | From exchange API |
| **Positions** | Simulated | Real on chain |
| **Accuracy** | 60s delay | Real-time |

---

## ✅ Verification

Check if data matches:
1. Run bot: `python3 nanba_real_trading_bot.py`
2. Open https://app.hyperliquid.xyz
3. Compare:
   - Account value
   - Open positions
   - Unrealized P&L

**Should match exactly!** 🎯

---

**Ready for real trading, boss!** 🐾🚀
