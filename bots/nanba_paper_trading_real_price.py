#!/usr/bin/env python3
"""
🌙 NANBA PAPER TRADING BOT v3.0 - REAL MARKET DATA
==================================================
Paper trading with REAL Hyperliquid prices + Moon Dev signals

Features:
- Real-time prices from Hyperliquid L2 orderbook
- Moon Dev API for signals (liquidations, whales)
- Paper trading (no real money)
- Accurate P&L based on real market movements
"""

import os
import json
import time
import logging
import requests
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/.openclaw/workspace/paper_trading_real_price/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('NanbaPaperTraderRealPrice')

class PaperTradingBotRealPrice:
    """
    Paper trading bot using REAL market data from Hyperliquid
    but virtual execution (no real money)
    """
    
    def __init__(self, initial_balance=1000.0):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.positions = {}
        self.trades = []
        self.trade_counter = 0
        
        # Trading parameters
        self.symbols = ['BTC', 'ETH', 'SOL']
        self.max_position_size = 150  # Max $ per position
        self.tp_percent = 0.6  # 0.6% take profit
        self.sl_percent = 3.0  # 3% stop loss
        self.min_confidence = 60  # 60% minimum confidence
        
        # State file
        self.state_file = '/root/.openclaw/workspace/paper_trading_real_price/state.json'
        self.load_state()
        
        logger.info("=" * 60)
        logger.info("🌙 NANBA PAPER TRADING v3.0 - REAL MARKET DATA")
        logger.info("=" * 60)
        logger.info(f"💰 Initial Balance: ${self.initial_balance:.2f}")
        logger.info(f"📊 Current Balance: ${self.balance:.2f}")
        
    def load_state(self):
        """Load trading state from file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.balance = state.get('balance', self.balance)
                    self.positions = state.get('positions', {})
                    self.trades = state.get('trades', [])
                    self.trade_counter = state.get('trade_counter', 0)
                logger.info(f"📂 Loaded state: ${self.balance:.2f} balance")
        except Exception as e:
            logger.error(f"❌ Error loading state: {e}")
    
    def save_state(self):
        """Save trading state to file"""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            state = {
                'balance': self.balance,
                'positions': self.positions,
                'trades': self.trades,
                'trade_counter': self.trade_counter,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Error saving state: {e}")
    
    def get_hyperliquid_price(self, symbol):
        """Get REAL price from Hyperliquid L2 orderbook"""
        try:
            url = 'https://api.hyperliquid.xyz/info'
            response = requests.post(url, json={
                'type': 'l2Book',
                'coin': symbol
            }, timeout=10)
            
            data = response.json()
            levels = data['levels']
            
            best_bid = float(levels[0][0]['px'])  # Highest buy
            best_ask = float(levels[1][0]['px'])  # Lowest sell
            mid_price = (best_bid + best_ask) / 2
            
            return {
                'symbol': symbol,
                'bid': best_bid,
                'ask': best_ask,
                'mid': mid_price,
                'spread': ((best_ask - best_bid) / mid_price) * 100
            }
            
        except Exception as e:
            logger.error(f"❌ Error fetching {symbol} price: {e}")
            return None
    
    def get_all_prices(self):
        """Get prices for all tracked symbols"""
        prices = {}
        for symbol in self.symbols:
            price_data = self.get_hyperliquid_price(symbol)
            if price_data:
                prices[symbol] = price_data
        return prices
    
    def fetch_moondev_sweeps(self):
        """Fetch signals from Moon Dev API"""
        try:
            url = "https://moondev.com/api/polymarket/sweeps"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            logger.error(f"❌ Error fetching Moon Dev data: {e}")
            return []
    
    def generate_signals(self, sweeps, prices):
        """Generate trading signals from Moon Dev data + real prices"""
        signals = []
        
        # Group by trader for whale detection
        trader_activity = {}
        for sweep in sweeps:
            trader = sweep.get('trader', 'unknown')
            if trader not in trader_activity:
                trader_activity[trader] = []
            trader_activity[trader].append(sweep)
        
        for sweep in sweeps:
            usd_amount = float(sweep.get('usd_amount', 0))
            size = float(sweep.get('size', 0))
            side = sweep.get('side', 'BUY')
            market = sweep.get('market', '')
            
            # Extract symbol from market name
            symbol = None
            for s in self.symbols:
                if s in market.upper():
                    symbol = s
                    break
            
            if not symbol or symbol not in prices:
                continue
            
            # Signal 1: Large liquidation ($50k+)
            if usd_amount >= 50000 and size > 1000:
                confidence = min(usd_amount / 100000, 0.9) * 100
                signal = {
                    'symbol': symbol,
                    'side': 'BUY' if side == 'SELL' else 'SELL',  # Inverse
                    'reason': f'Large liquidation: ${usd_amount:,.0f}',
                    'confidence': confidence,
                    'size': min(usd_amount * 0.01, self.balance * 0.15, self.max_position_size),
                    'price': prices[symbol]['mid']
                }
                signals.append(signal)
                logger.info(f"🎯 Liquidation Signal: {symbol} {signal['side']} @ ${signal['price']:.2f}")
            
            # Signal 2: Whale activity (2+ trades > $10k)
            trader = sweep.get('trader', '')
            if trader in trader_activity:
                trader_trades = [t for t in trader_activity[trader] 
                               if float(t.get('usd_amount', 0)) >= 10000]
                if len(trader_trades) >= 2:
                    confidence = 75
                    signal = {
                        'symbol': symbol,
                        'side': side,
                        'reason': f'Whale {trader[:10]}... active ({len(trader_trades)} trades)',
                        'confidence': confidence,
                        'size': min(usd_amount * 0.1, self.balance * 0.15, self.max_position_size),
                        'price': prices[symbol]['mid']
                    }
                    signals.append(signal)
                    logger.info(f"🐋 Whale Signal: {symbol} {signal['side']} @ ${signal['price']:.2f}")
        
        return signals
    
    def open_position(self, signal):
        """Open paper position with REAL price"""
        symbol = signal['symbol']
        
        # Check if already have position
        if symbol in self.positions:
            logger.info(f"⚠️ Already have {symbol} position, skipping")
            return
        
        # Check balance
        size = signal['size']
        if size > self.balance:
            logger.warning(f"⚠️ Insufficient balance for {symbol}")
            return
        
        # Calculate TP/SL based on REAL price
        entry_price = signal['price']
        if signal['side'] == 'BUY':
            tp_price = entry_price * (1 + self.tp_percent / 100)
            sl_price = entry_price * (1 - self.sl_percent / 100)
        else:
            tp_price = entry_price * (1 - self.tp_percent / 100)
            sl_price = entry_price * (1 + self.sl_percent / 100)
        
        position = {
            'id': f"POS_{self.trade_counter:04d}",
            'symbol': symbol,
            'side': signal['side'],
            'entry_price': entry_price,
            'size': size,
            'tp_price': tp_price,
            'sl_price': sl_price,
            'confidence': signal['confidence'],
            'reason': signal['reason'],
            'opened_at': datetime.now().isoformat()
        }
        
        self.positions[symbol] = position
        self.balance -= size
        self.trade_counter += 1
        
        # Send Telegram notification
        self.notify_telegram_open(position)
        
        logger.info(f"✅ POSITION OPENED: {symbol} {signal['side']}")
        logger.info(f"   Entry: ${entry_price:.2f}")
        logger.info(f"   Size: ${size:.2f}")
        logger.info(f"   TP: ${tp_price:.4f} (+{self.tp_percent}%)")
        logger.info(f"   SL: ${sl_price:.4f} (-{self.sl_percent}%)")
        
        self.save_state()
    
    def update_positions(self, prices):
        """Check TP/SL with REAL market prices"""
        for symbol, position in list(self.positions.items()):
            if symbol not in prices:
                continue
            
            current_price = prices[symbol]['mid']
            entry_price = position['entry_price']
            
            # Calculate P&L
            if position['side'] == 'BUY':
                pnl_pct = ((current_price - entry_price) / entry_price) * 100
            else:
                pnl_pct = ((entry_price - current_price) / entry_price) * 100
            
            # Check TP
            if pnl_pct >= self.tp_percent:
                self.close_position(position, current_price, 'TAKE_PROFIT', pnl_pct)
            # Check SL
            elif pnl_pct <= -self.sl_percent:
                self.close_position(position, current_price, 'STOP_LOSS', pnl_pct)
    
    def close_position(self, position, exit_price, reason, pnl_pct):
        """Close paper position and calculate REAL P&L"""
        symbol = position['symbol']
        size = position['size']
        
        # Calculate profit/loss
        pnl_amount = size * (pnl_pct / 100)
        self.balance += size + pnl_amount
        
        trade = {
            'id': position['id'],
            'symbol': symbol,
            'side': position['side'],
            'entry_price': position['entry_price'],
            'exit_price': exit_price,
            'size': size,
            'pnl_pct': pnl_pct,
            'pnl_amount': pnl_amount,
            'reason': reason,
            'opened_at': position['opened_at'],
            'closed_at': datetime.now().isoformat()
        }
        
        self.trades.append(trade)
        del self.positions[symbol]
        
        # Send Telegram notification
        self.notify_telegram_close(trade)
        
        emoji = "🟢" if pnl_amount > 0 else "🔴"
        logger.info(f"{emoji} POSITION CLOSED: {symbol}")
        logger.info(f"   Exit: ${exit_price:.2f}")
        logger.info(f"   P&L: ${pnl_amount:.2f} ({pnl_pct:+.2f}%)")
        logger.info(f"   Reason: {reason}")
        logger.info(f"   Balance: ${self.balance:.2f}")
        
        self.save_state()
    
    def notify_telegram_open(self, position):
        """Send Telegram notification for new position"""
        try:
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '8149630851:AAEXwTNQ03o1o7XSF3DfusmzlewvSK6qlcc')
            chat_id = os.getenv('TELEGRAM_CHAT_ID', '6102672721')
            
            emoji = "🟢" if position['side'] == 'BUY' else "🔴"
            message = f"""{emoji} <b>NEW PAPER POSITION</b>

<b>{position['symbol']}</b> {position['side']}
💰 Entry: ${position['entry_price']:.2f}
📊 Size: ${position['size']:.2f}
🎯 TP: ${position['tp_price']:.4f} (+0.6%)
🛑 SL: ${position['sl_price']:.4f} (-3%)
🎲 Confidence: {position['confidence']:.0f}%
💡 {position['reason']}

<i>Paper Trading - Not Real Money</i>"""
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }, timeout=10)
            
        except Exception as e:
            logger.error(f"Telegram error: {e}")
    
    def notify_telegram_close(self, trade):
        """Send Telegram notification for closed trade"""
        try:
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '8149630851:AAEXwTNQ03o1o7XSF3DfusmzlewvSK6qlcc')
            chat_id = os.getenv('TELEGRAM_CHAT_ID', '6102672721')
            
            emoji = "✅" if trade['pnl_amount'] > 0 else "❌"
            message = f"""{emoji} <b>POSITION CLOSED</b>

<b>{trade['symbol']}</b> {trade['side']}
💰 Entry: ${trade['entry_price']:.2f}
💰 Exit: ${trade['exit_price']:.2f}
💵 P&L: ${trade['pnl_amount']:.2f} ({trade['pnl_pct']:+.2f}%)
📊 Size: ${trade['size']:.2f}
🎯 Reason: {trade['reason']}

<i>Paper Trading - Not Real Money</i>"""
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }, timeout=10)
            
        except Exception as e:
            logger.error(f"Telegram error: {e}")
    
    def print_summary(self, prices):
        """Print current trading summary"""
        total_pnl = self.balance - self.initial_balance
        total_pnl_pct = (total_pnl / self.initial_balance) * 100
        
        print("\n" + "=" * 60)
        print(f"📊 PAPER TRADING SUMMARY - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        print(f"💰 Balance: ${self.balance:.2f}")
        print(f"💵 Initial: ${self.initial_balance:.2f}")
        print(f"💎 Total P&L: ${total_pnl:+.2f} ({total_pnl_pct:+.2f}%)")
        print(f"📈 Open Positions: {len(self.positions)}")
        
        for symbol, pos in self.positions.items():
            if symbol in prices:
                current = prices[symbol]['mid']
                entry = pos['entry_price']
                if pos['side'] == 'BUY':
                    pnl_pct = ((current - entry) / entry) * 100
                else:
                    pnl_pct = ((entry - current) / entry) * 100
                print(f"   {symbol}: {pos['side']} @ ${entry:.2f} | Now: ${current:.2f} | P&L: {pnl_pct:+.2f}%")
        
        print(f"✅ Closed Trades: {len(self.trades)}")
        print("=" * 60)
    
    def run(self):
        """Main trading loop"""
        logger.info("🚀 Starting Paper Trading with REAL Market Data")
        
        try:
            while True:
                logger.info("\n" + "=" * 60)
                logger.info("🔄 Starting Trading Cycle")
                
                # Step 1: Get REAL prices from Hyperliquid
                prices = self.get_all_prices()
                if not prices:
                    logger.error("❌ Failed to fetch prices, retrying...")
                    time.sleep(10)
                    continue
                
                for symbol, price in prices.items():
                    logger.info(f"💹 {symbol}: ${price['mid']:.2f} (Spread: {price['spread']:.4f}%)")
                
                # Step 2: Fetch Moon Dev signals
                sweeps = self.fetch_moondev_sweeps()
                logger.info(f"📊 Fetched {len(sweeps)} sweeps from Moon Dev")
                
                # Step 3: Generate signals
                signals = self.generate_signals(sweeps, prices)
                logger.info(f"🎯 Generated {len(signals)} signals")
                
                # Step 4: Open positions (paper trading)
                for signal in signals:
                    if signal['confidence'] >= self.min_confidence:
                        self.open_position(signal)
                
                # Step 5: Update positions with REAL prices
                self.update_positions(prices)
                
                # Step 6: Print summary
                self.print_summary(prices)
                
                logger.info("✅ Cycle complete, sleeping 30s...")
                time.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Trading stopped by user")
            self.print_summary(self.get_all_prices())
            self.save_state()

if __name__ == "__main__":
    bot = PaperTradingBotRealPrice(initial_balance=1000.0)
    bot.run()
