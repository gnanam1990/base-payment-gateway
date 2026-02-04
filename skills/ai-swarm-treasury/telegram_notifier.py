"""
📱 NANBA AI SWARM - TELEGRAM NOTIFICATIONS
===========================================
Real-time alerts for swarm decisions and treasury updates
"""

import os
import requests
from typing import Dict, Any
from datetime import datetime

class SwarmTelegramNotifier:
    """
    Telegram notifications for AI Swarm Treasury
    """
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '8149630851:AAEXwTNQ03o1o7XSF3DfusmzlewvSK6qlcc')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', '6102672721')
        self.enabled = True
    
    def send_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        """Send Telegram message"""
        if not self.enabled:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            response = requests.post(url, json={
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }, timeout=10)
            
            return response.json().get('ok', False)
        except Exception as e:
            print(f"❌ Telegram error: {e}")
            return False
    
    def notify_consensus(self, consensus) -> bool:
        """Notify when swarm reaches consensus"""
        
        # Build agent votes text
        votes_text = ""
        for decision in consensus.agent_decisions:
            emoji = "✅" if decision.decision == consensus.action else "⚪"
            votes_text += f"\n{emoji} <b>{decision.agent_id}</b>: {decision.decision} ({decision.confidence:.0f}%)"
        
        message = f"""🤖 <b>AI SWARM CONSENSUS REACHED!</b>

<b>Action:</b> {consensus.action}
<b>Confidence:</b> {consensus.confidence:.1f}%
<b>Votes:</b> {consensus.votes_for} for, {consensus.votes_against} against

<b>🗳️ Agent Votes:</b>{votes_text}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🧪 Testnet Only - Base Sepolia"""
        
        return self.send_message(message)
    
    def notify_trade_executed(self, trade_data: Dict[str, Any]) -> bool:
        """Notify when trade is executed"""
        
        emoji = "🟢" if trade_data.get('profit', 0) >= 0 else "🔴"
        
        message = f"""{emoji} <b>TRADE EXECUTED</b>

<b>Action:</b> {trade_data.get('action', 'UNKNOWN')}
<b>Amount:</b> {trade_data.get('amount', 0):.2f} USDC
<b>Chain:</b> {trade_data.get('chain', 'Base Sepolia')}

<b>Result:</b> {trade_data.get('result', 'Pending')}

⏰ {datetime.now().strftime('%H:%M:%S')}"""
        
        return self.send_message(message)
    
    def notify_risk_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Notify when security agent raises alert"""
        
        message = f"""🚨 <b>RISK ALERT!</b>

<b>Level:</b> {alert_data.get('level', 'MEDIUM')}
<b>Source:</b> {alert_data.get('source', 'Security Agent')}

<b>Issue:</b> {alert_data.get('message', 'Unknown risk detected')}

<b>Recommended Action:</b> {alert_data.get('recommendation', 'Review and act')}

⚠️ Review immediately!
⏰ {datetime.now().strftime('%H:%M:%S')}"""
        
        return self.send_message(message)
    
    def notify_daily_summary(self, treasury_state: Dict[str, Any], performance: Dict[str, Any]) -> bool:
        """Send daily treasury summary"""
        
        # Calculate profit/loss
        initial = performance.get('initial_balance', 10000)
        current = treasury_state.get('total_usdc', 10000)
        profit = current - initial
        profit_pct = (profit / initial) * 100 if initial > 0 else 0
        
        emoji = "🟢" if profit >= 0 else "🔴"
        
        message = f"""📊 <b>DAILY TREASURY SUMMARY</b>

💰 <b>Balance:</b> {current:,.2f} USDC
📈 <b>Initial:</b> {initial:,.2f} USDC
{emoji} <b>P&L:</b> {profit:+.2f} USDC ({profit_pct:+.2f}%)

🏦 <b>Allocation:</b>
• Base Sepolia: {treasury_state.get('base_sepolia', 0):,.2f}
• Ethereum Sepolia: {treasury_state.get('ethereum_sepolia', 0):,.2f}
• Arbitrum Sepolia: {treasury_state.get('arbitrum_sepolia', 0):,.2f}

📊 <b>Performance:</b>
• Win Rate: {performance.get('win_rate', 0):.1f}%
• Total Trades: {performance.get('total_trades', 0)}
• Best Trade: +{performance.get('best_trade', 0):.2f} USDC

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}
🧪 Testnet Only"""
        
        return self.send_message(message)
    
    def notify_agent_thinking(self, agent_name: str, role: str) -> bool:
        """Notify when agent starts thinking"""
        
        message = f"""🧠 <b>{agent_name}</b> is analyzing...

Role: {role}
Status: Processing market data

⏰ {datetime.now().strftime('%H:%M:%S')}"""
        
        return self.send_message(message)


# Quick test function
def test_telegram():
    """Test Telegram notifications"""
    print("🧪 Testing Telegram notifications...")
    
    notifier = SwarmTelegramNotifier()
    
    # Test basic message
    success = notifier.send_message(
        "🤖 <b>Nanba AI Swarm Treasury</b>\n\n"
        "Telegram notifications are now active!\n"
        "You'll receive real-time updates from all 4 agents.\n\n"
        "🧪 Testnet Only - Base Sepolia"
    )
    
    if success:
        print("✅ Telegram notifications working!")
    else:
        print("❌ Telegram test failed")
    
    return success


if __name__ == "__main__":
    test_telegram()
