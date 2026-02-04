# SKILL.md - AI Swarm Treasury

## Name
ai-swarm-treasury

## Description
Futuristic multi-agent USDC treasury management system. Four AI agents (Analyst, Trader, Security, Treasury) collaborate using Claude via OpenRouter to autonomously manage USDC across multiple chains.

## ⚠️ TESTNET ONLY
This skill operates exclusively on testnets (Base Sepolia, Ethereum Sepolia, Arbitrum Sepolia). Never use mainnet credentials.

## Why This Is Revolutionary

### Traditional Treasury Management:
- Human analysts working 9-5
- Emotional decision making
- Slow reaction times
- High operational costs

### AI Swarm Treasury:
- **4 AI agents** working 24/7
- **Data-driven** consensus decisions
- **Instant** analysis and execution
- **Autonomous** operation

## Installation

```bash
pip install requests python-dotenv asyncio
```

## Environment Variables

```bash
OPENROUTER_API_KEY=sk-or-v1-your_key_here
```

Get OpenRouter key: https://openrouter.ai/keys

## Usage

### Basic Usage

```python
from skills.ai_swarm_treasury import AISwarmTreasury
import asyncio

swarm = AISwarmTreasury()
asyncio.run(swarm.run())
```

### Advanced: Single Consensus Round

```python
consensus = await swarm.run_swarm_consensus()
print(f"Decision: {consensus.action}")
print(f"Confidence: {consensus.confidence}%")

for decision in consensus.agent_decisions:
    print(f"{decision.agent_id}: {decision.decision}")
```

### Get Treasury Report

```python
report = swarm.generate_report()
print(report)
```

## The Agent Swarm

### 1. Analyst Agent
- **Model:** Claude 3.5 Sonnet via OpenRouter
- **Role:** Market analysis and prediction
- **Decisions:** BULLISH/BEARISH/NEUTRAL

### 2. Trader Agent
- **Model:** Claude 3.5 Sonnet via OpenRouter
- **Role:** Trade execution optimization
- **Decisions:** BUY/SELL/HOLD/ARBITRAGE

### 3. Security Agent
- **Model:** Claude 3.5 Sonnet via OpenRouter
- **Role:** Risk monitoring and threat detection
- **Decisions:** SAFE/CAUTION/ALERT/BLOCK

### 4. Treasury Agent
- **Model:** Claude 3.5 Sonnet via OpenRouter
- **Role:** Capital allocation strategy
- **Decisions:** ACCUMULATE/DISTRIBUTE/REBALANCE

## Swarm Consensus

### How It Works:
1. All 4 agents analyze current market conditions
2. Each agent makes independent decision using Claude
3. Decisions weighted by confidence scores
4. Collective action determined by majority
5. Action executed if confidence > 60%

### Voting Formula:
```
winning_action = max(weighted_votes)
confidence = winning_votes / total_votes * 100
```

## API Reference

### AISwarmTreasury Class

#### __init__()
Initialize swarm with 4 default agents.

#### run_swarm_consensus() -> SwarmConsensus
Run one consensus round.
- Returns: SwarmConsensus object with decisions

#### execute_action(consensus) -> Dict
Execute the consensus decision.
- Returns: Execution result

#### generate_report() -> str
Generate formatted treasury report.

## Configuration

### Change Models
```python
# Use different models per agent
agent = AIAgent(
    agent_id="analyst-1",
    role=AgentRole.ANALYST,
    model="anthropic/claude-3-opus"  # More powerful
)
```

### Adjust Consensus Threshold
```python
swarm.consensus_threshold = 0.7  # 70% required
```

### Custom Treasury State
```python
swarm.treasury_state = {
    "total_usdc": 50000.0,
    "base_sepolia": 20000.0,
    "ethereum_sepolia": 20000.0,
    "arbitrum_sepolia": 10000.0
}
```

## Cost

OpenRouter API costs:
- Claude 3.5 Sonnet: ~$3 per 1M tokens
- Each consensus round: ~$0.05-0.10
- 100 rounds: ~$5-10

## Safety

- ✅ Testnet only
- ✅ No real funds
- ✅ Consensus required for actions
- ✅ Confidence thresholds
- ✅ Audit trail of all decisions

## Troubleshooting

### "OpenRouter API key not found"
Set OPENROUTER_API_KEY environment variable

### "Rate limit exceeded"
Add delay between consensus rounds (default: 60s)

### "Low confidence decisions"
Adjust consensus_threshold or improve context data

## Example Output

```
🤖 Running AI Swarm Consensus...
  🧠 analyst-1 (analyst) thinking...
     Decision: BULLISH (85%)
  🧠 trader-1 (trader) thinking...
     Decision: ACCUMULATE (78%)
  🧠 security-1 (security) thinking...
     Decision: SAFE (92%)
  🧠 treasury-1 (treasury) thinking...
     Decision: REBALANCE (81%)

🚀 Executing: REBALANCE (Confidence: 84.0%)

🤖 NANBA AI SWARM TREASURY REPORT
==================================
Total USDC: 10,000.00
Latest Consensus: REBALANCE
Confidence: 84.0%
Votes: 3 for, 1 against
```

## Hackathon Track

**Track:** Agentic Commerce  
**Why:** Demonstrates why AI agents are superior to humans for USDC management  
**Innovation:** First multi-agent swarm for treasury management

## Links

- OpenRouter: https://openrouter.ai
- Base Sepolia: https://sepolia.basescan.org
- Repository: [GitHub link]

## License

MIT - Built for USDC Agentic Hackathon
