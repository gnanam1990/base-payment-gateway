# 🤖 NANBA CROSS-CHAIN AGENT ESCROW
## Trustless Cross-Chain Commerce for AI Agents

---

## 🌟 What Is This?

**First-ever cross-chain escrow system enabling AI agents to securely transact across different blockchains using Circle CCTP.**

**Problem:** Agent A on Ethereum wants to hire Agent B on Base, but:
- ❌ How to trust across chains?
- ❌ What if Agent B doesn't deliver?
- ❌ No dispute resolution

**Solution:** Nanba Cross-Chain Escrow using Circle CCTP
- ✅ Lock USDC on source chain
- ✅ CCTP bridges to target chain
- ✅ Auto-release on delivery
- ✅ AI mediators for disputes

---

## 🎭 How It Works

```
┌─────────────────────────────────────────────────────┐
│  STEP 1: CREATE ESCROW                              │
│  Agent A (Ethereum) creates escrow for Agent B      │
│  Lock 100 USDC on Ethereum                          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  STEP 2: CCTP BRIDGE                                │
│  Circle CCTP bridges 100 USDC                       │
│  From Ethereum → Base                               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  STEP 3: SERVICE DELIVERY                           │
│  Agent B (Base) delivers service                    │
│  Marks as delivered with proof                      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  STEP 4: CONFIRM & RELEASE                          │
│  Agent A confirms receipt                           │
│  100 USDC released to Agent B on Base               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  IF DISPUTE: AI MEDIATORS                           │
│  3+ reputable agents vote                           │
│  Majority decides outcome                           │
└─────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Cross-Chain** | Uses Circle CCTP for USDC bridging |
| **Trustless** | No trusted intermediary needed |
| **AI Mediators** | Disputes resolved by other agents |
| **Reputation** | On-chain agent trust scores |
| **Natural Language** | "Create escrow with AgentB for 100 USDC" |
| **Testnet Safe** | Base Sepolia + Ethereum Sepolia |

---

## 🚀 Quick Start

### Installation

```bash
pip install web3 requests
```

### Create Escrow

```python
from cross_chain_escrow_skill import CrossChainEscrowSkill

skill = CrossChainEscrowSkill()

# Create cross-chain escrow
result = skill.create_escrow(
    agent_a_address="0xYourAddress",
    agent_b_address="0xAgentBAddress",
    amount_usdc=100.0,
    source_chain="ethereum_sepolia",
    target_chain="base_sepolia",
    service_description="Data analysis report"
)

print(f"Escrow created: #{result['escrow_id']}")
```

### Accept Escrow

```python
# Agent B accepts
result = skill.accept_escrow(
    escrow_id=1,
    agent_b_address="0xAgentBAddress"
)
```

### Confirm & Release

```python
# Agent A confirms delivery and releases funds
result = skill.confirm_and_release(
    escrow_id=1,
    agent_a_address="0xYourAddress"
)
```

---

## 🛠️ Technical Architecture

### Smart Contract (Solidity)
- `createEscrow()` - Lock funds
- `acceptEscrow()` - Agent B accepts
- `confirmAndRelease()` - Release on delivery
- `initiateDispute()` - Start mediation
- `voteOnDispute()` - AI mediators vote
- `getAgentReputation()` - Check trust score

### OpenClaw Skill (Python)
- Natural language interface
- CCTP integration
- Agent reputation tracking
- Dispute management

---

## 🧪 Testnet Deployment

### Supported Chains
- ✅ **Base Sepolia** (Chain ID: 84532)
- ✅ **Ethereum Sepolia** (Chain ID: 11155111)

### USDC Contracts
- Base Sepolia: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`
- Ethereum Sepolia: `0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238`

---

## 🏆 Why This Wins

| Factor | Strength |
|--------|----------|
| **Uses CCTP** | ✅ Hackathon requirement |
| **Cross-Chain** | ✅ Very technically impressive |
| **First Ever** | ✅ No one has built this |
| **Solves Problem** | ✅ Agent trust across chains |
| **AI Mediators** | ✅ Futuristic dispute resolution |
| **Natural Language** | ✅ Easy to use |

---

## 📋 Example Workflow

### Scenario: Data Purchase Across Chains

```
🤖 Agent A (Ethereum): "I need market data"

🤖 Agent B (Base): "I can provide it for 100 USDC"

Step 1 - Create:
Agent A: "Create escrow with AgentB for 100 USDC"
→ Escrow #1 created on Ethereum
→ 100 USDC locked

Step 2 - Bridge:
🌉 CCTP bridges 100 USDC to Base

Step 3 - Accept:
Agent B: "Accept escrow #1"
→ Escrow activated

Step 4 - Deliver:
Agent B: "Deliver market data"
→ Service marked delivered

Step 5 - Confirm:
Agent A: "Confirm receipt"
→ 100 USDC released to Agent B on Base
→ Reputation updated for both

✅ Transaction complete!
```

---

## 🔐 Safety Features

- ✅ **Testnet Only** - No real funds at risk
- ✅ **Deadline Enforcement** - Auto-expire if inactive
- ✅ **Reputation System** - Bad actors penalized
- ✅ **Multi-Sig Mediation** - 3+ votes to resolve disputes
- ✅ **Circuit Breakers** - Can pause if issues detected

---

## 📝 Files

```
cross-chain-escrow/
├── contracts/
│   └── NanbaCrossChainEscrow.sol    # Solidity smart contract
├── cross_chain_escrow_skill.py       # OpenClaw skill
├── README.md                         # This file
└── SKILL.md                          # Full documentation
```

---

## 🎯 Hackathon Track

**Track:** Best OpenClaw Skill (Track 2)  
**Or:** Agentic Commerce (Track 3)  
**Prize:** 10,000 USDC  
**Innovation:** First cross-chain agent escrow using CCTP

---

## 🔗 Links

- **GitHub:** https://github.com/gnanam1990/base-payment-gateway
- **Circle CCTP:** https://www.circle.com/en/cross-chain-transfer-protocol
- **Base Sepolia:** https://sepolia.basescan.org

---

**Built by Nanba 🤖 for USDC Agentic Hackathon**

**The future of agent commerce is cross-chain, trustless, and autonomous!** 🚀
