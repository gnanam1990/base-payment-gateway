"""
💬 NANBA AI SWARM - AGENT DISCUSSION LOG
=========================================
Shows agents "discussing" before reaching consensus
Makes the swarm feel like a real team meeting
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentMessage:
    """Single message from an agent"""
    agent_id: str
    role: str
    message: str
    timestamp: str
    emotion: str = "neutral"  # excited, concerned, confident, etc.


class AgentDiscussion:
    """
    Simulates agents discussing before voting
    """
    
    def __init__(self):
        self.messages: List[AgentMessage] = []
        self.discussion_topic: str = ""
        self.started_at: str = ""
        self.ended_at: str = ""
    
    def start_discussion(self, topic: str):
        """Start a new discussion"""
        self.discussion_topic = topic
        self.started_at = datetime.now().isoformat()
        self.messages = []
        
        # Add opening message
        self.add_message("System", "Coordinator", f"🎯 New Discussion: {topic}")
    
    def add_message(self, agent_id: str, role: str, message: str, emotion: str = "neutral"):
        """Add a message to the discussion"""
        self.messages.append(AgentMessage(
            agent_id=agent_id,
            role=role,
            message=message,
            timestamp=datetime.now().isoformat(),
            emotion=emotion
        ))
    
    def generate_discussion(self, agent_decisions) -> str:
        """
        Generate natural discussion from agent decisions
        """
        self.start_discussion("Treasury Management Strategy")
        
        # Analyst speaks first
        analyst = next((d for d in agent_decisions if d.role.value == "analyst"), None)
        if analyst:
            self.add_message(
                "analyst-1", "Market Analyst",
                self._get_analyst_comment(analyst),
                self._get_emotion(analyst.confidence)
            )
        
        # Trader responds
        trader = next((d for d in agent_decisions if d.role.value == "trader"), None)
        if trader:
            self.add_message(
                "trader-1", "Trader",
                self._get_trader_comment(trader, analyst),
                self._get_emotion(trader.confidence)
            )
        
        # Security gives opinion
        security = next((d for d in agent_decisions if d.role.value == "security"), None)
        if security:
            self.add_message(
                "security-1", "Security",
                self._get_security_comment(security),
                self._get_emotion(security.confidence)
            )
        
        # Treasury makes final recommendation
        treasury = next((d for d in agent_decisions if d.role.value == "treasury"), None)
        if treasury:
            self.add_message(
                "treasury-1", "Treasury Manager",
                self._get_treasury_comment(treasury, agent_decisions),
                "confident"
            )
        
        self.ended_at = datetime.now().isoformat()
        return self.format_discussion()
    
    def _get_analyst_comment(self, decision) -> str:
        """Generate analyst's comment based on decision"""
        comments = {
            "BULLISH": [
                "Market is showing strong upward momentum. BTC just broke key resistance at $76k.",
                "I'm seeing bullish signals across multiple timeframes. Volume is increasing.",
                "Technical indicators are aligned. MACD crossover confirmed."
            ],
            "BEARISH": [
                "Market sentiment is turning negative. Support levels being tested.",
                "I'm seeing distribution patterns. Whales are selling.",
                "Multiple resistance levels ahead. Momentum is slowing."
            ],
            "NEUTRAL": [
                "Market is in consolidation phase. Waiting for clear direction.",
                "Mixed signals right now. Best to wait for confirmation.",
                "Range-bound movement. No clear trend yet."
            ]
        }
        import random
        return random.choice(comments.get(decision.decision, comments["NEUTRAL"]))
    
    def _get_trader_comment(self, decision, analyst) -> str:
        """Generate trader's comment"""
        if decision.decision in ["BUY", "ACCUMULATE"]:
            return f"I agree with Analyst. Good entry point forming. Liquidity is healthy on Base. I'd recommend {decision.decision.lower()} with tight stop-loss."
        elif decision.decision in ["SELL", "DISTRIBUTE"]:
            return "Time to take profits. Risk/reward ratio no longer favorable. Let's lock in gains."
        else:
            return "I'm seeing some arbitrage opportunities between chains, but spreads are tight. Might be better to wait."
    
    def _get_security_comment(self, decision) -> str:
        """Generate security's comment"""
        if decision.decision == "SAFE":
            return "No red flags detected. Smart contracts look good. Volatility within normal ranges. We're clear to proceed."
        elif decision.decision == "CAUTION":
            return "I'm seeing some unusual on-chain activity. Not critical, but let's be careful with position sizes."
        else:
            return "Multiple risk factors detected. Recommend reducing exposure until situation clears."
    
    def _get_treasury_comment(self, decision, all_decisions) -> str:
        """Generate treasury's final recommendation"""
        # Count how many agree
        agreeing = sum(1 for d in all_decisions if d.decision == decision.decision)
        total = len(all_decisions)
        
        return f"Based on the team's analysis ({agreeing}/{total} agents agree), I recommend we {decision.decision}. Current allocation is suboptimal. Let's execute immediately."
    
    def _get_emotion(self, confidence: float) -> str:
        """Determine emotion based on confidence"""
        if confidence >= 80:
            return "confident"
        elif confidence >= 60:
            return "optimistic"
        elif confidence >= 40:
            return "neutral"
        else:
            return "concerned"
    
    def format_discussion(self) -> str:
        """Format discussion for display"""
        lines = [
            "🗣️ AGENT DISCUSSION",
            "=" * 50,
            f"Topic: {self.discussion_topic}",
            f"Started: {self.started_at[:19]}",
            ""
        ]
        
        for msg in self.messages:
            emoji = self._get_emotion_emoji(msg.emotion)
            lines.append(f"{emoji} <b>{msg.agent_id}</b> ({msg.role}):")
            lines.append(f"   \"{msg.message}\"")
            lines.append("")
        
        lines.append("=" * 50)
        lines.append("✅ Discussion complete. Moving to vote...")
        
        return "\n".join(lines)
    
    def _get_emotion_emoji(self, emotion: str) -> str:
        """Get emoji for emotion"""
        emotions = {
            "confident": "💪",
            "optimistic": "😊",
            "neutral": "😐",
            "concerned": "😰",
            "excited": "🤩"
        }
        return emotions.get(emotion, "😐")
    
    def get_consensus_summary(self, final_action: str, confidence: float) -> str:
        """Get summary of how consensus was reached"""
        return f"""
📊 CONSENSUS REACHED

After {len(self.messages)-1} messages of discussion:
- Agents analyzed market conditions
- Shared perspectives
- Debated strategies

<b>Final Decision:</b> {final_action}
<b>Confidence:</b> {confidence:.1f}%
<b>Status:</b> ✅ APPROVED FOR EXECUTION
"""


# Example usage
def example_discussion():
    """Show example agent discussion"""
    
    # Mock decisions for demo
    from skills.ai_swarm_treasury import AgentDecision, AgentRole
    
    decisions = [
        AgentDecision("analyst-1", AgentRole.ANALYST, "BULLISH", 85, "Market breaking out", datetime.now().isoformat()),
        AgentDecision("trader-1", AgentRole.TRADER, "ACCUMULATE", 78, "Good entry point", datetime.now().isoformat()),
        AgentDecision("security-1", AgentRole.SECURITY, "SAFE", 92, "No risks", datetime.now().isoformat()),
        AgentDecision("treasury-1", AgentRole.TREASURY, "REBALANCE", 81, "Optimize allocation", datetime.now().isoformat())
    ]
    
    discussion = AgentDiscussion()
    output = discussion.generate_discussion(decisions)
    print(output)
    print(discussion.get_consensus_summary("REBALANCE", 84.0))


if __name__ == "__main__":
    print("🧪 Testing Agent Discussion...")
    example_discussion()
