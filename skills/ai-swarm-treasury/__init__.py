#!/usr/bin/env python3
"""
🤖 NANBA AI SWARM TREASURY
===========================
Futuristic multi-agent USDC management system

Multiple AI agents collaboratively manage USDC treasury:
- Analyst Agent: Market analysis & predictions
- Trader Agent: Execute optimal trades
- Security Agent: Risk monitoring & security
- Treasury Agent: Balance & allocation decisions

All agents vote on decisions using USDC-weighted governance.
"""

import os
import json
import time
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

try:
    import requests
except ImportError:
    raise ImportError("pip install requests")

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', 'your_key_here')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class AgentRole(Enum):
    ANALYST = "analyst"
    TRADER = "trader"
    SECURITY = "security"
    TREASURY = "treasury"

@dataclass
class AgentDecision:
    """Individual agent decision"""
    agent_id: str
    role: AgentRole
    decision: str
    confidence: float
    reasoning: str
    timestamp: str

@dataclass
class SwarmConsensus:
    """Collective swarm decision"""
    action: str
    confidence: float
    votes_for: int
    votes_against: int
    agent_decisions: List[AgentDecision]
    execution_data: Optional[Dict] = None

class AIAgent:
    """Individual AI agent in the swarm"""
    
    def __init__(self, agent_id: str, role: AgentRole, model: str = "anthropic/claude-3.5-sonnet"):
        self.agent_id = agent_id
        self.role = role
        self.model = model
        self.memory = []
        
    def think(self, context: Dict, treasury_state: Dict) -> AgentDecision:
        """Agent analyzes and makes decision using Claude via OpenRouter"""
        
        # Build prompt based on role
        role_prompts = {
            AgentRole.ANALYST: """You are an AI Analyst Agent specializing in crypto market analysis.
Analyze the current market conditions and treasury state.
Provide insights on:
- Market trends
- Risk factors
- Opportunity assessment
Be concise but thorough.""",
            
            AgentRole.TRADER: """You are an AI Trader Agent focused on optimal USDC management.
Analyze trade opportunities:
- Optimal entry/exit points
- Cross-chain arbitrage
- Yield opportunities
Provide specific actionable recommendations.""",
            
            AgentRole.SECURITY: """You are an AI Security Agent monitoring risks.
Assess:
- Smart contract risks
- Market volatility risks
- Operational security
- Fraud detection
Flag any concerns immediately.""",
            
            AgentRole.TREASURY: """You are an AI Treasury Agent managing allocations.
Determine:
- Optimal USDC allocation strategy
- Reserve requirements
- Investment distributions
- Cash flow management"""
        }
        
        system_prompt = role_prompts.get(self.role, "You are an AI agent.")
        
        user_prompt = f"""Context: {json.dumps(context, indent=2)}

Treasury State: {json.dumps(treasury_state, indent=2)}

Your Role: {self.role.value}

Analyze and provide:
1. DECISION: (BUY/SELL/HOLD/REBALANCE/ALERT)
2. CONFIDENCE: (0-100%)
3. REASONING: (Brief explanation)

Format: DECISION|CONFIDENCE|REASONING"""
        
        try:
            response = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://nanba-ai.dev",
                    "X-Title": "Nanba AI Swarm Treasury"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse decision
            parts = content.split('|')
            if len(parts) >= 3:
                decision = parts[0].strip()
                confidence = float(parts[1].replace('%', '').strip())
                reasoning = parts[2].strip()
            else:
                decision = "HOLD"
                confidence = 50.0
                reasoning = content[:200]
            
            return AgentDecision(
                agent_id=self.agent_id,
                role=self.role,
                decision=decision,
                confidence=confidence,
                reasoning=reasoning,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return AgentDecision(
                agent_id=self.agent_id,
                role=self.role,
                decision="HOLD",
                confidence=0.0,
                reasoning=f"Error: {str(e)}",
                timestamp=datetime.now().isoformat()
            )

class AISwarmTreasury:
    """
    Multi-agent USDC treasury management system
    """
    
    def __init__(self):
        self.agents = [
            AIAgent("analyst-1", AgentRole.ANALYST),
            AIAgent("trader-1", AgentRole.TRADER),
            AIAgent("security-1", AgentRole.SECURITY),
            AIAgent("treasury-1", AgentRole.TREASURY)
        ]
        
        self.treasury_state = {
            "total_usdc": 10000.0,
            "base_sepolia": 5000.0,
            "ethereum_sepolia": 3000.0,
            "arbitrum_sepolia": 2000.0,
            "last_updated": datetime.now().isoformat()
        }
        
        self.decision_history = []
        self.consensus_threshold = 0.6  # 60% confidence required
        
    def gather_context(self) -> Dict:
        """Gather market and treasury context"""
        return {
            "timestamp": datetime.now().isoformat(),
            "market_sentiment": "neutral",
            "volatility_index": 0.45,
            "gas_prices": {
                "base": 0.1,
                "ethereum": 15.0,
                "arbitrum": 0.5
            },
            "yield_opportunities": [
                {"protocol": "Aave", "apy": 3.5, "chain": "base"},
                {"protocol": "Compound", "apy": 3.2, "chain": "ethereum"}
            ]
        }
    
    async def run_swarm_consensus(self) -> SwarmConsensus:
        """All agents vote, reach consensus"""
        print("🤖 Running AI Swarm Consensus...")
        
        context = self.gather_context()
        agent_decisions = []
        
        # Each agent makes decision
        for agent in self.agents:
            print(f"  🧠 {agent.agent_id} ({agent.role.value}) thinking...")
            decision = agent.think(context, self.treasury_state)
            agent_decisions.append(decision)
            print(f"     Decision: {decision.decision} ({decision.confidence:.0f}%)")
            time.sleep(1)  # Rate limiting
        
        # Calculate consensus
        decisions = [d.decision for d in agent_decisions]
        confidences = [d.confidence for d in agent_decisions]
        
        # Weighted voting
        action_votes = {}
        for d in agent_decisions:
            if d.decision not in action_votes:
                action_votes[d.decision] = 0
            action_votes[d.decision] += d.confidence
        
        # Determine winning action
        if action_votes:
            winning_action = max(action_votes, key=action_votes.get)
            total_votes = sum(action_votes.values())
            confidence = action_votes[winning_action] / total_votes * 100
        else:
            winning_action = "HOLD"
            confidence = 0.0
        
        votes_for = sum(1 for d in agent_decisions if d.decision == winning_action)
        votes_against = len(agent_decisions) - votes_for
        
        consensus = SwarmConsensus(
            action=winning_action,
            confidence=confidence,
            votes_for=votes_for,
            votes_against=votes_against,
            agent_decisions=agent_decisions
        )
        
        self.decision_history.append({
            "timestamp": datetime.now().isoformat(),
            "consensus": asdict(consensus)
        })
        
        return consensus
    
    def execute_action(self, consensus: SwarmConsensus) -> Dict:
        """Execute the swarm decision"""
        print(f"\n🚀 Executing: {consensus.action} (Confidence: {consensus.confidence:.1f}%)")
        
        if consensus.confidence < self.consensus_threshold * 100:
            print("⚠️ Confidence too low, holding position")
            return {"status": "held", "reason": "low_confidence"}
        
        # Simulate execution
        execution = {
            "action": consensus.action,
            "timestamp": datetime.now().isoformat(),
            "status": "simulated",
            "network": "Base Sepolia Testnet"
        }
        
        if consensus.action == "REBALANCE":
            execution["details"] = "Rebalancing USDC across chains"
        elif consensus.action == "YIELD":
            execution["details"] = "Moving USDC to highest yield opportunity"
        
        consensus.execution_data = execution
        return execution
    
    def generate_report(self) -> str:
        """Generate treasury report"""
        report = f"""
🤖 NANBA AI SWARM TREASURY REPORT
==================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💰 TREASURY STATUS
Total USDC: {self.treasury_state['total_usdc']:,.2f}
├── Base Sepolia: {self.treasury_state['base_sepolia']:,.2f}
├── Ethereum Sepolia: {self.treasury_state['ethereum_sepolia']:,.2f}
└── Arbitrum Sepolia: {self.treasury_state['arbitrum_sepolia']:,.2f}

🤖 ACTIVE AGENTS ({len(self.agents)})
"""
        for agent in self.agents:
            report += f"  • {agent.agent_id} ({agent.role.value})\n"
        
        report += f"\n📊 DECISION HISTORY\nTotal Decisions: {len(self.decision_history)}\n"
        
        if self.decision_history:
            latest = self.decision_history[-1]
            consensus = latest['consensus']
            report += f"\nLatest Consensus: {consensus['action']}\n"
            report += f"Confidence: {consensus['confidence']:.1f}%\n"
            report += f"Votes: {consensus['votes_for']} for, {consensus['votes_against']} against\n"
        
        report += "\n🧪 Testnet Only - Base Sepolia\n"
        return report
    
    async def run(self):
        """Main swarm loop"""
        print("🚀 Starting Nanba AI Swarm Treasury")
        print("=" * 50)
        
        while True:
            try:
                # Run consensus
                consensus = await self.run_swarm_consensus()
                
                # Execute if confident
                execution = self.execute_action(consensus)
                
                # Generate report
                report = self.generate_report()
                print(report)
                
                # Wait before next cycle
                print("\n⏳ Sleeping 60 seconds...\n")
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(60)

# Example usage
if __name__ == "__main__":
    swarm = AISwarmTreasury()
    asyncio.run(swarm.run())
