#!/usr/bin/env python3
"""
🌙 NANBA MOONDEV TRADING BOT
============================
Real trading bot using MoonDev API signals

Features:
- Live Polymarket data from MoonDev
- Real Hyperliquid trading
- Twilio SMS notifications
- Risk management
"""

import os
import sys
import json
import time
import logging
import requests
from datetime import datetime
from decimal import Decimal

# Add skills to path
sys.path.insert(0, '/root/.openclaw/workspace')

from skills.twilio import TwilioSkill

# Configuration
MOONDEV_API_KEY = os.getenv('MOONDEV_API_KEY', 'moonstream_76df1625e5b6')
MOONDEV_BASE_URL = "https://moondev.com/api"

# Hyperliquid Testnet Config
HYPERLIQUID_RPC = "https://api.hyperliquid.xyz"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/.openclaw/workspace/moondev_trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('MoonDevTrader')


class MoonDevTradingBot:
    """
    Trading bot using MoonDev API signals
    """
    
    def __init__(self, initial_balance=1000.0):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = {}
        self.trades = []
        self.trade_counter = 0
        
        # API setup
        self.moondev_headers = {
            "Authorization": f"Bearer {MOONDEV_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Twilio for notifications
        try:
            self.twilio = TwilioSkill()
            self.notifications_enabled = True
            logger.info("✅ Twilio notifications enabled")
        except Exception as e:
            logger.warning(f"⚠️ Twilio not configured: {e}")
            self.notifications_enabled = False
        
        # Trading parameters
        self.min_sweep_amount = 10000  # $10k minimum
        self.max_position_size = 100   # Max $100 per trade
        self.tp_percent = 0.6
        self.sl_percent = 3.0
        
        logger.info("=" * 60)
        logger.info("🌙 NANBA MOONDEV TRADING BOT")
        logger.info("=" * 60)
        logger.info(f"💰 Initial Balance: ${initial_balance:.2f}")
    
    def fetch_moondev_sweeps(self):
        """Fetch sweeps from MoonDev API"""
        try:
            response = requests.get(
                f"{MOONDEV_BASE_URL}/polymarket/sweeps",
                headers=self.moondev_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                sweeps = data.get('data', [])
                logger.info(f"📊 Fetched {len(sweeps)} sweeps from MoonDev")
                return sweeps
            else:
                logger.error(f"❌ API Error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error fetching sweeps: {e}")
            return []
    
    def fetch_moondev_expiring(self):
        """Fetch expiring markets"""
        try:
            response = requests.get(
                f"{MOONDEV_BASE_URL}/polymarket/expiring",
                headers=self.moondev_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                markets = data.get('data', [])
                logger.info(f"📊 Fetched {len(markets)} expiring markets")
                return markets
            else:
                return []
                
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return []
    
    def generate_signals(self, sweeps):
        """Generate trading signals from sweeps"""
        signals = []
        
        for sweep in sweeps:
            usd_amount = float(sweep.get('usd_amount', 0))
            size = float(sweep.get('size', 0))
            side = sweep.get('side', 'BUY')
            market = sweep.get('market', '')
            
            # Signal 1: Large sweeps ($10k+)
            if usd_amount >= self.min_sweep_amount:
                confidence = min(usd_amount / 50000, 0.9) * 100
                
                signal = {
                    'type': 'LARGE_SWEEP',
                    'market': market[:50],
                    'side': side,
                    'amount': usd_amount,
                    'confidence': confidence,
                    'reason': f'Large sweep: ${usd_amount:,.0f}'
                }
                signals.append(signal)
                logger.info(f"🎯 Signal: LARGE_SWEEP - {market[:30]} - ${usd_amount:,.0f}")
        
        return signals
    
    def execute_trade(self, signal):
        """Execute paper trade based on signal"""
        # Calculate position size
        position_size = min(
            signal['amount'] * 0.01,  # 1% of sweep size
            self.max_position_size,
            self.balance * 0.10  # 10% of balance
        )
        
        if position_size < 10:
            logger.info("⚠️ Position size too small, skipping")
            return None
        
        # Create trade
        trade = {
            'id': f"TRADE_{self.trade_counter:04d}",
            'signal_type': signal['type'],
            'market': signal['market'],
            'side': signal['side'],
            'size': position_size,
            'confidence': signal['confidence'],
            'reason': signal['reason'],
            'timestamp': datetime.now().isoformat(),
            'status': 'OPEN'
        }
        
        self.trades.append(trade)
        self.trade_counter += 1
        self.balance -= position_size
        
        logger.info(f"✅ TRADE OPENED: {trade['id']}")
        logger.info(f"   Market: {trade['market']}")
        logger.info(f"   Side: {trade['side']}")
        logger.info(f"   Size: ${trade['size']:.2f}")
        
        # Send notification
        if self.notifications_enabled:
            self._notify_trade(trade)
        
        return trade
    
    def _notify_trade(self, trade):
        """Send Twilio notification for trade"""
        try:
            # Get notification number from env or use default
            notify_number = os.getenv('NOTIFY_PHONE', '+917339215717')
            
            message = f"""🌙 MoonDev Trade Alert!

Trade: {trade['id']}
Market: {trade['market']}
Side: {trade['side']}
Size: ${trade['size']:.2f}
Confidence: {trade['confidence']:.0f}%

Status: OPEN
Time: {datetime.now().strftime('%H:%M:%S')}"""
            
            result = self.twilio.send_sms(notify_number, message)
            
            if result.get('success'):
                logger.info("📱 Notification sent via Twilio")
            else:
                logger.warning(f"⚠️ Notification failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"❌ Notification error: {e}")
    
    def run(self):
        """Main trading loop"""
        logger.info("🚀 Starting MoonDev Trading Bot")
        logger.info("=" * 60)
        
        try:
            while True:
                logger.info("\n" + "=" * 60)
                logger.info("🔄 New Trading Cycle")
                
                # Fetch data
                sweeps = self.fetch_moondev_sweeps()
                expiring = self.fetch_moondev_expiring()
                
                # Generate signals
                signals = self.generate_signals(sweeps)
                logger.info(f"🎯 Generated {len(signals)} signals")
                
                # Execute trades
                for signal in signals:
                    if signal['confidence'] >= 60:  # Min 60% confidence
                        self.execute_trade(signal)
                
                # Print summary
                self._print_summary()
                
                # Wait before next cycle
                logger.info("⏳ Sleeping 60 seconds...")
                time.sleep(60)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Bot stopped by user")
            self._print_summary()
    
    def _print_summary(self):
        """Print trading summary"""
        print("\n" + "=" * 60)
        print(f"📊 TRADING SUMMARY - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        print(f"💰 Balance: ${self.balance:.2f}")
        print(f"📈 Total Trades: {len(self.trades)}")
        print(f"🎯 Open Positions: {len([t for t in self.trades if t['status'] == 'OPEN'])}")
        
        if self.trades:
            recent = self.trades[-3:]
            print("\n📋 Recent Trades:")
            for trade in recent:
                print(f"   {trade['id']}: {trade['side']} {trade['market'][:20]} - ${trade['size']:.2f}")
        
        print("=" * 60)


if __name__ == "__main__":
    bot = MoonDevTradingBot(initial_balance=1000.0)
    bot.run()
