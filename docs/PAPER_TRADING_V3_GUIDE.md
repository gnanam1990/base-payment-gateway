# 📊 NANBA PAPER TRADING v3.0 - REAL MARKET DATA

## ✅ READY FOR USE!

---

## 🎯 What This Bot Does

**HYBRID APPROACH:**
- ✅ **REAL prices** from Hyperliquid L2 orderbook
- ✅ **REAL P&L** based on actual market movements
- ✅ **PAPER execution** (no real money risk)
- ✅ **Moon Dev signals** for entry points

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────┐
│                   BOT FLOW                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. FETCH REAL PRICES                                   │
│     └─ Hyperliquid L2 orderbook API                     │
│        BTC: $76,172.50 (real-time)                      │
│                                                         │
│  2. FETCH SIGNALS                                       │
│     └─ Moon Dev API (/polymarket/sweeps)                │
│        Liquidations, Whale activity                     │
│                                                         │
│  3. GENERATE SIGNALS                                    │
│     └─ If $50k+ liquidation → Entry signal              │
│     └─ If whale active → Copy signal                    │
│                                                         │
│  4. PAPER EXECUTION                                     │
│     └─ Virtual position (no real money)                 │
│     └─ Entry at REAL market price                       │
│                                                         │
│  5. MONITOR WITH REAL PRICES                            │
│     └─ Check TP/SL every 30 seconds                     │
│     └─ Using ACTUAL Hyperliquid prices                  │
│                                                         │
│  6. ACCURATE P&L                                        │
│     └─ Based on real price movements                    │
│     └─ NOT simulated/fake numbers                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🆚 Comparison

| Feature | Old Paper Bot | New Paper Bot | Real Trading |
|---------|---------------|---------------|--------------|
| **Price Source** | Moon Dev sweeps | Hyperliquid L2 | Hyperliquid L2 |
| **Price Accuracy** | ❌ Wrong | ✅ Real | ✅ Real |
| **P&L Accuracy** | ❌ Simulated | ✅ Real movement | ✅ Real money |
| **Risk** | None | None | Real loss |
| **Money** | Fake | Fake | Real USDC |

---

## 🚀 Quick Start

### 1. Start the Bot
```bash
cd /root/.openclaw/workspace
./start_paper_trading_real.sh
```

### 2. What You'll See
```
🌙 NANBA PAPER TRADING v3.0 - REAL MARKET DATA
==================================================
💰 Initial Balance: $1000.00
📊 Current Balance: $1000.00

🔄 Starting Trading Cycle
💹 BTC: $76172.50 (Spread: 0.0013%)
💹 ETH: $2845.20 (Spread: 0.0021%)
💹 SOL: $145.80 (Spread: 0.0035%)
📊 Fetched 137 sweeps from Moon Dev
🎯 Generated 2 signals
✅ POSITION OPENED: BTC BUY
   Entry: $76172.50
   Size: $150.00
   TP: $76629.69 (+0.6%)
   SL: $73887.33 (-3%)
```

---

## 📊 Key Features

### Real-Time Price Updates
- Fetches from Hyperliquid every 30 seconds
- Bid/Ask/Mid prices
- Shows spread

### Accurate P&L
- Based on ACTUAL price movements
- Real-time unrealized P&L
- Closed trade P&L from real exit prices

### Telegram Notifications
- 🟢 New position opened
- ✅ Position closed with P&L
- Real-time updates

### State Persistence
- Saves balance to JSON
- Tracks all positions
- Saves trade history
- Continues after restart

---

## 📁 Files

| File | Purpose |
|------|---------|
| `nanba_paper_trading_real_price.py` | Main bot code |
| `start_paper_trading_real.sh` | Startup script |
| `paper_trading_real_price/state.json` | Account state |
| `paper_trading_real_price/bot.log` | Trading log |

---

## ⚙️ Configuration

Edit bot parameters in `nanba_paper_trading_real_price.py`:

```python
initial_balance = 1000.0    # Starting virtual balance
max_position_size = 150      # Max $ per position
tp_percent = 0.6            # Take profit 0.6%
sl_percent = 3.0            # Stop loss 3%
min_confidence = 60         # Min signal confidence
symbols = ['BTC', 'ETH', 'SOL']  # Track these coins
```

---

## ✅ Advantages Over Old Bot

| Old Bot | New Bot |
|---------|---------|
| ❌ Used sweep prices | ✅ Real Hyperliquid L2 prices |
| ❌ Fake P&L | ✅ Accurate based on real movements |
| ❌ 60s delay | ✅ Real-time updates |
| ❌ Wrong calculations | ✅ Proper TP/SL from real prices |

---

## 🎯 Use Case

**Perfect for:**
- Testing strategies with REAL market conditions
- Validating Moon Dev signals
- Learning without risking money
- Getting accurate performance metrics

**NOT for:**
- Making real money (it's paper trading)
- Production trading (no real execution)

---

**Ready to run boss!** Start with:
```bash
./start_paper_trading_real.sh
```

🐾🚀
