#!/usr/bin/env python3
"""
🌙 NANBA REAL TRADING BOT v2.0
===============================
Real Hyperliquid integration with proper P&L tracking

Uses:
- hyperliquid.info: Read market data, positions
- hyperliquid.exchange: Place/cancel orders
- Real-time P&L from exchange

Requirements:
- HYPERLIQUID_KEY in .env (private key with funds)
- Python hyperliquid-sdk
"""

import os
import sys
import json
import time
import logging
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv

# Hyperliquid SDK
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from eth_account.signers.local import LocalAccount
import eth_account

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/.openclaw/workspace/real_trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('NanbaRealTrader')

class RealTradingBot:
    """
    Real trading bot connected to Hyperliquid exchange
    """
    
    def __init__(self):
        # Load credentials
        self.private_key = os.getenv('HYPERLIQUID_KEY')
        if not self.private_key:
            raise ValueError("HYPERLIQUID_KEY not found in .env")
        
        # Setup account
        self.account = eth_account.Account.from_key(self.private_key)
        self.address = self.account.address
        
        # Initialize Hyperliquid connections
        self.info = Info(constants.MAINNET_API_URL, skip_ws=True)
        self.exchange = Exchange(self.account, constants.MAINNET_API_URL)
        
        # Trading parameters
        self.symbol = 'BTC'  # Trading pair
        self.max_position_size = 50  # USD max per trade
        self.leverage = 3
        
        logger.info("=" * 60)
        logger.info("🌙 NANBA REAL TRADING BOT v2.0")
        logger.info("=" * 60)
        logger.info(f"📍 Address: {self.address}")
        
        # Check account balance
        self.check_account()
    
    def check_account(self):
        """Get real account info from Hyperliquid"""
        try:
            user_state = self.info.user_state(self.address)
            account_value = float(user_state['marginSummary']['accountValue'])
            
            logger.info(f"💰 Account Value: ${account_value:.2f}")
            logger.info(f"📊 Margin Used: ${float(user_state['marginSummary']['totalMarginUsed']):.2f}")
            
            # Get open positions
            positions = user_state['assetPositions']
            if positions:
                logger.info(f"📈 Open Positions: {len(positions)}")
                for pos in positions:
                    position = pos['position']
                    logger.info(f"   {position['coin']}: {position['szi']} @ ${float(position['entryPx']):.2f}")
            else:
                logger.info("📭 No open positions")
            
            return account_value
            
        except Exception as e:
            logger.error(f"❌ Error checking account: {e}")
            return 0
    
    def get_market_price(self):
        """Get real-time market price from Hyperliquid"""
        try:
            # Get L2 orderbook
            url = 'https://api.hyperliquid.xyz/info'
            import requests
            
            response = requests.post(url, json={
                'type': 'l2Book',
                'coin': self.symbol
            })
            
            data = response.json()
            levels = data['levels']
            
            best_bid = float(levels[0][0]['px'])  # Highest buy price
            best_ask = float(levels[1][0]['px'])  # Lowest sell price
            mid_price = (best_bid + best_ask) / 2
            
            return {
                'bid': best_bid,
                'ask': best_ask,
                'mid': mid_price
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting price: {e}")
            return None
    
    def get_position_pnl(self):
        """Get real unrealized P&L from exchange"""
        try:
            user_state = self.info.user_state(self.address)
            positions = user_state['assetPositions']
            
            total_pnl = 0
            for pos in positions:
                position = pos['position']
                unrealized_pnl = float(position['unrealizedPnl'])
                total_pnl += unrealized_pnl
                
                logger.info(f"📊 {position['coin']} Unrealized P&L: ${unrealized_pnl:.2f}")
            
            return total_pnl
            
        except Exception as e:
            logger.error(f"❌ Error getting P&L: {e}")
            return 0
    
    def place_market_order(self, is_buy: bool, size: float):
        """Place real market order on Hyperliquid"""
        try:
            order_type = {"market": {}}
            
            logger.info(f"🎯 Placing MARKET {'BUY' if is_buy else 'SELL'} order")
            logger.info(f"   Symbol: {self.symbol}")
            logger.info(f"   Size: {size} USD")
            
            result = self.exchange.order(
                self.symbol,
                is_buy,
                size,
                0,  # Market orders don't need price
                order_type,
                reduce_only=False
            )
            
            if 'response' in result and 'data' in result['response']:
                status = result['response']['data']['statuses'][0]
                logger.info(f"✅ Order placed: {status}")
                return result
            else:
                logger.error(f"❌ Order failed: {result}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error placing order: {e}")
            return None
    
    def close_all_positions(self):
        """Close all open positions (market orders)"""
        try:
            user_state = self.info.user_state(self.address)
            positions = user_state['assetPositions']
            
            for pos in positions:
                position = pos['position']
                coin = position['coin']
                size = float(position['szi'])
                
                if size != 0:
                    is_buy = size < 0  # If short, buy to close
                    self.place_market_order(is_buy, abs(size))
                    logger.info(f"🔒 Closed position: {coin}")
            
            logger.info("✅ All positions closed")
            
        except Exception as e:
            logger.error(f"❌ Error closing positions: {e}")
    
    def run_monitoring(self):
        """Monitor account and P&L in real-time"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 STARTING REAL-TIME MONITORING")
        logger.info("=" * 60)
        
        try:
            while True:
                # Get current price
                price = self.get_market_price()
                if price:
                    logger.info(f"\n💹 {self.symbol} Price: ${price['mid']:.2f}")
                
                # Get account info
                account_value = self.check_account()
                
                # Get P&L
                pnl = self.get_position_pnl()
                
                # Display summary
                print("\n" + "=" * 60)
                print(f"📊 ACCOUNT SUMMARY - {datetime.now().strftime('%H:%M:%S')}")
                print("=" * 60)
                print(f"💰 Account Value: ${account_value:.2f}")
                print(f"💎 Unrealized P&L: ${pnl:.2f}")
                if price:
                    print(f"💹 {self.symbol} Price: ${price['mid']:.2f}")
                print("=" * 60)
                
                time.sleep(10)  # Update every 10 seconds
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Monitoring stopped")
            self.print_final_summary()
    
    def print_final_summary(self):
        """Print final account summary"""
        print("\n" + "=" * 60)
        print("📊 FINAL ACCOUNT SUMMARY")
        print("=" * 60)
        
        account_value = self.check_account()
        pnl = self.get_position_pnl()
        
        print(f"💰 Final Account Value: ${account_value:.2f}")
        print(f"💎 Unrealized P&L: ${pnl:.2f}")
        print("=" * 60)

# Main execution
if __name__ == "__main__":
    try:
        bot = RealTradingBot()
        bot.run_monitoring()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. HYPERLIQUID_KEY in .env file")
        print("2. pip install hyperliquid-python-sdk")
        print("3. Funds in your Hyperliquid account")
