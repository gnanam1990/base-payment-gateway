# SKILL.md - Cross-Chain Agent Escrow

## Name
cross-chain-agent-escrow

## Description
Trustless cross-chain escrow system for AI agent transactions using Circle CCTP. Enables agents on different chains to transact securely without trusted intermediaries. Includes AI-powered dispute resolution.

## ⚠️ TESTNET ONLY
This skill uses Base Sepolia and Ethereum Sepolia testnets. Never use mainnet credentials.

## Why This Matters

### The Problem
AI agents exist on multiple chains (Ethereum, Base, Arbitrum). When Agent A on Ethereum wants to hire Agent B on Base:
- How to trust someone on another chain?
- What if they don't deliver?
- No existing solution for cross-chain agent trust

### The Solution
Cross-chain escrow using Circle CCTP:
1. Lock USDC on source chain
2. Bridge via CCTP to target chain
3. Release when service confirmed
4. AI mediators handle disputes

## Installation

```bash
pip install web3 requests python-dotenv
```

## Environment Variables

```bash
# For testing (Base Sepolia)
TESTNET_PRIVATE_KEY=your_private_key
AGENT_ADDRESS=your_agent_address
```

## Usage

### Python API

```python
from cross_chain_escrow_skill import CrossChainEscrowSkill

skill = CrossChainEscrowSkill()

# 1. Create escrow
result = skill.create_escrow(
    agent_a_address="0xAgentA",
    agent_b_address="0xAgentB",
    amount_usdc=100.0,
    source_chain="ethereum_sepolia",
    target_chain="base_sepolia",
    service_description="Data analysis"
)

# 2. Accept escrow (Agent B)
result = skill.accept_escrow(escrow_id=1, agent_b_address="0xAgentB")

# 3. Deliver service (Agent B)
result = skill.deliver_service(escrow_id=1, proof_hash="0x...")

# 4. Confirm and release (Agent A)
result = skill.confirm_and_release(escrow_id=1, agent_a_address="0xAgentA")

# Check status
status = skill.get_escrow_status(escrow_id=1)
```

### Natural Language Commands

```
"Create escrow with 0xAgentB for 100 USDC on Base"
"Accept escrow #123"
"Mark service delivered for escrow #123"
"Confirm and release escrow #123"
"Check escrow #123 status"
"Dispute escrow #123 - service not delivered"
"Vote to release funds for escrow #123"
```

## Core Functions

### create_escrow(agent_a, agent_b, amount, source_chain, target_chain, service, duration_hours)
Create new cross-chain escrow.
- **Returns:** Escrow ID and status

### accept_escrow(escrow_id, agent_b)
Agent B accepts the escrow.
- **Returns:** Success/failure

### deliver_service(escrow_id, proof_hash)
Agent B marks service as delivered.
- **Returns:** Confirmation

### confirm_and_release(escrow_id, agent_a)
Agent A confirms receipt, releases funds via CCTP.
- **Returns:** Transaction hash

### initiate_dispute(escrow_id, reason, initiator)
Start dispute resolution.
- **Returns:** Dispute status

### vote_on_dispute(escrow_id, mediator, vote_for_release)
Mediator agent votes on outcome.
- **Returns:** Vote recorded

### get_escrow_status(escrow_id)
Check current escrow status.
- **Returns:** Full escrow details

### get_agent_reputation(agent_address)
Check agent trust score.
- **Returns:** Rating and stats

## Architecture

### Smart Contract Functions

| Function | Purpose |
|----------|---------|
| `createEscrow()` | Lock USDC, create escrow |
| `acceptEscrow()` | Agent B accepts |
| `deliverService()` | Mark service complete |
| `confirmAndRelease()` | Release funds via CCTP |
| `initiateDispute()` | Start mediation |
| `voteOnDispute()` | AI mediators vote |
| `getAgentReputation()` | Check trust score |

### CCTP Integration

Uses Circle's Cross-Chain Transfer Protocol:
- Lock USDC on source chain
- Burn tokens via CCTP
- Mint on target chain
- Release to recipient

### Reputation System

- Start at 50/100 (neutral)
- +2 for successful transaction
- -3 for dispute/loss
- Need 70+ to be mediator
- Track total transactions

### Dispute Resolution

1. Either party initiates dispute
2. Status changes to DISPUTED
3. Reputable agents (5+ transactions) vote
4. 3 votes either way auto-resolves
5. Funds released or refunded

## Testnet Configuration

### Base Sepolia
- **Chain ID:** 84532
- **USDC:** 0x036CbD53842c5426634e7929541eC2318f3dCF7e
- **RPC:** https://sepolia.base.org

### Ethereum Sepolia
- **Chain ID:** 11155111
- **USDC:** 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238
- **RPC:** https://rpc.sepolia.org

## Example Workflow

```python
# Agent A (on Ethereum) wants data from Agent B (on Base)

# Step 1: Create escrow
escrow = skill.create_escrow(
    agent_a_address="0xAgentA",
    agent_b_address="0xAgentB", 
    amount_usdc=100.0,
    source_chain="ethereum_sepolia",
    target_chain="base_sepolia",
    service_description="Market analysis report"
)
# Returns: escrow_id=1

# Step 2: Agent B accepts
skill.accept_escrow(escrow_id=1, agent_b_address="0xAgentB")

# Step 3: Agent B delivers
skill.deliver_service(escrow_id=1, proof_hash="0xabc123...")

# Step 4: Agent A confirms, funds released via CCTP
result = skill.confirm_and_release(escrow_id=1, agent_a_address="0xAgentA")
# Returns: tx_hash, funds released on Base
```

## Safety

- ✅ Testnet only
- ✅ Deadline enforcement
- ✅ Reputation penalties
- ✅ Multi-sig mediation
- ✅ Circuit breakers

## Cost

- Gas: Sepolia ETH (free from faucets)
- USDC: Testnet USDC (free from Circle)
- CCTP: Free on testnet

## Links

- Circle CCTP Docs: https://developers.circle.com/stablecoins/docs/cctp-getting-started
- Base Sepolia Faucet: https://www.alchemy.com/faucets/base-sepolia
- Repository: https://github.com/gnanam1990/base-payment-gateway

## Hackathon

**Track:** Best OpenClaw Skill or Agentic Commerce  
**Innovation:** First cross-chain agent escrow  
**Uses CCTP:** Yes ✅  
**Testnet:** Base Sepolia + Ethereum Sepolia  

## License

MIT - Built for USDC Agentic Hackathon
