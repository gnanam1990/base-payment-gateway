"""
📊 NANBA AI SWARM - PROFIT/LOSS TRACKER
========================================
Real-time performance tracking for treasury operations
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from decimal import Decimal


@dataclass
class TradeRecord:
    """Single trade record"""
    id: str
    timestamp: str
    action: str  # BUY, SELL, REBALANCE, etc.
    asset: str
    amount: float
    price_before: float
    price_after: float
    profit_loss: float
    profit_loss_pct: float
    chain: str
    tx_hash: Optional[str] = None


class PerformanceTracker:
    """
    Track treasury performance and P&L
    """
    
    def __init__(self, data_file: str = "/root/.openclaw/workspace/swarm_performance.json"):
        self.data_file = data_file
        self.initial_balance = 10000.0
        self.current_balance = 10000.0
        self.trades: List[TradeRecord] = []
        self.daily_snapshots: List[Dict] = []
        
        # Statistics
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_profit = 0.0
        self.total_loss = 0.0
        self.best_trade = 0.0
        self.worst_trade = 0.0
        
        self.load_data()
    
    def load_data(self):
        """Load historical data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.initial_balance = data.get('initial_balance', 10000.0)
                    self.current_balance = data.get('current_balance', 10000.0)
                    self.total_trades = data.get('total_trades', 0)
                    self.winning_trades = data.get('winning_trades', 0)
                    self.losing_trades = data.get('losing_trades', 0)
                    self.total_profit = data.get('total_profit', 0.0)
                    self.total_loss = data.get('total_loss', 0.0)
                    self.best_trade = data.get('best_trade', 0.0)
                    self.worst_trade = data.get('worst_trade', 0.0)
                    
                    # Load trades
                    trades_data = data.get('trades', [])
                    self.trades = [TradeRecord(**t) for t in trades_data]
            except Exception as e:
                print(f"⚠️ Could not load performance data: {e}")
    
    def save_data(self):
        """Save performance data"""
        try:
            data = {
                'initial_balance': self.initial_balance,
                'current_balance': self.current_balance,
                'total_trades': self.total_trades,
                'winning_trades': self.winning_trades,
                'losing_trades': self.losing_trades,
                'total_profit': self.total_profit,
                'total_loss': self.total_loss,
                'best_trade': self.best_trade,
                'worst_trade': self.worst_trade,
                'trades': [asdict(t) for t in self.trades[-100:]],  # Keep last 100
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save performance data: {e}")
    
    def record_trade(self, action: str, asset: str, amount: float, 
                     profit_loss: float, chain: str = "Base Sepolia",
                     price_before: float = 0.0, price_after: float = 0.0,
                     tx_hash: Optional[str] = None):
        """Record a new trade"""
        
        # Calculate profit/loss percentage
        if price_before > 0:
            profit_loss_pct = ((price_after - price_before) / price_before) * 100
        else:
            profit_loss_pct = 0.0
        
        trade = TradeRecord(
            id=f"TRADE_{self.total_trades + 1:04d}",
            timestamp=datetime.now().isoformat(),
            action=action,
            asset=asset,
            amount=amount,
            price_before=price_before,
            price_after=price_after,
            profit_loss=profit_loss,
            profit_loss_pct=profit_loss_pct,
            chain=chain,
            tx_hash=tx_hash
        )
        
        self.trades.append(trade)
        self.total_trades += 1
        
        # Update balance
        self.current_balance += profit_loss
        
        # Update statistics
        if profit_loss >= 0:
            self.winning_trades += 1
            self.total_profit += profit_loss
            if profit_loss > self.best_trade:
                self.best_trade = profit_loss
        else:
            self.losing_trades += 1
            self.total_loss += abs(profit_loss)
            if profit_loss < self.worst_trade:
                self.worst_trade = profit_loss
        
        self.save_data()
        return trade
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        total_pnl = self.current_balance - self.initial_balance
        total_pnl_pct = (total_pnl / self.initial_balance) * 100 if self.initial_balance > 0 else 0
        
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        
        return {
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': win_rate,
            'total_profit': self.total_profit,
            'total_loss': self.total_loss,
            'best_trade': self.best_trade,
            'worst_trade': self.worst_trade,
            'avg_profit_per_trade': self.total_profit / self.winning_trades if self.winning_trades > 0 else 0,
            'avg_loss_per_trade': self.total_loss / self.losing_trades if self.losing_trades > 0 else 0
        }
    
    def format_performance_report(self) -> str:
        """Format performance report for display"""
        perf = self.get_performance_summary()
        
        pnl_emoji = "🟢" if perf['total_pnl'] >= 0 else "🔴"
        
        report = f"""
📊 PERFORMANCE REPORT
{'=' * 50}

💰 BALANCE
Initial:  {perf['initial_balance']:,.2f} USDC
Current:  {perf['current_balance']:,.2f} USDC
{pnl_emoji} P&L:     {perf['total_pnl']:+.2f} USDC ({perf['total_pnl_pct']:+.2f}%)

📈 TRADING STATISTICS
Total Trades:     {perf['total_trades']}
Winning Trades:   {perf['winning_trades']} ({perf['win_rate']:.1f}%)
Losing Trades:    {perf['losing_trades']}

💵 PROFIT/LOSS DETAILS
Total Profit:     +{perf['total_profit']:.2f} USDC
Total Loss:       -{perf['total_loss']:.2f} USDC
Net P&L:          {perf['total_pnl']:+.2f} USDC

🏆 EXTREMES
Best Trade:   +{perf['best_trade']:.2f} USDC
Worst Trade:  {perf['worst_trade']:.2f} USDC

📊 AVERAGES
Avg Profit/Win:  +{perf['avg_profit_per_trade']:.2f} USDC
Avg Loss/Loss:   -{perf['avg_loss_per_trade']:.2f} USDC

{'=' * 50}
Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🧪 Testnet Only - Base Sepolia
"""
        return report
    
    def get_recent_trades(self, n: int = 5) -> List[TradeRecord]:
        """Get n most recent trades"""
        return self.trades[-n:] if self.trades else []
    
    def format_recent_trades(self, n: int = 5) -> str:
        """Format recent trades for display"""
        trades = self.get_recent_trades(n)
        
        if not trades:
            return "📭 No trades yet"
        
        lines = [f"📊 RECENT TRADES (Last {len(trades)})", "=" * 50]
        
        for trade in trades:
            emoji = "🟢" if trade.profit_loss >= 0 else "🔴"
            lines.append(f"""
{emoji} {trade.id} | {trade.timestamp[:19]}
Action: {trade.action} {trade.asset}
Amount: {trade.amount:.2f} USDC
P&L: {trade.profit_loss:+.2f} USDC ({trade.profit_loss_pct:+.2f}%)
Chain: {trade.chain}
""")
        
        return "\n".join(lines)
    
    def take_daily_snapshot(self, treasury_state: Dict):
        """Take daily snapshot of performance"""
        snapshot = {
            'date': datetime.now().isoformat(),
            'balance': treasury_state.get('total_usdc', self.current_balance),
            'pnl': self.current_balance - self.initial_balance,
            'trades_today': len([t for t in self.trades if t.timestamp.startswith(datetime.now().strftime('%Y-%m-%d'))])
        }
        self.daily_snapshots.append(snapshot)
        
        # Keep only last 30 days
        if len(self.daily_snapshots) > 30:
            self.daily_snapshots = self.daily_snapshots[-30:]
    
    def get_chart_data(self) -> Dict[str, List]:
        """Get data for charts"""
        return {
            'dates': [s['date'][:10] for s in self.daily_snapshots],
            'balances': [s['balance'] for s in self.daily_snapshots],
            'pnl': [s['pnl'] for s in self.daily_snapshots]
        }


# Example/test function
def test_performance_tracker():
    """Test performance tracker"""
    print("🧪 Testing Performance Tracker...")
    
    tracker = PerformanceTracker()
    
    # Simulate some trades
    tracker.record_trade("BUY", "BTC", 1000.0, 45.50, "Base Sepolia", 76000, 76350)
    tracker.record_trade("SELL", "ETH", 500.0, -12.30, "Base Sepolia", 2250, 2238)
    tracker.record_trade("REBALANCE", "USDC", 2000.0, 23.80, "Ethereum Sepolia")
    tracker.record_trade("ARBITRAGE", "USDC", 1500.0, 8.90, "Arbitrum Sepolia")
    
    print(tracker.format_performance_report())
    print(tracker.format_recent_trades(3))


if __name__ == "__main__":
    test_performance_tracker()
