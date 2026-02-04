# SKILL.md - USDC Operations

## Name
usdc

## Description
OpenClaw skill for USDC testnet operations on Base Sepolia. Supports balance checks, transfers, and cross-chain operations.

## ⚠️ TESTNET ONLY
This skill is designed for **Base Sepolia testnet only**. Never use mainnet credentials.

## Installation

```bash
pip install web3 python-dotenv
```

## Environment Variables

Create `.env` file:
```bash
TESTNET_PRIVATE_KEY=your_base_sepolia_testnet_private_key
```

Get testnet ETH from: https://www.alchemy.com/faucets/base-sepolia

## Usage

### Python API

```python
from skills.usdc import USDCSkill

skill = USDCSkill()

# Check balance
balance = skill.get_balance()
print(skill.format_balance_message(balance))

# Send USDC
result = skill.send_usdc("0xRecipientAddress", 50.0)
print(skill.format_send_message(result))
```

### Natural Language Commands

```
"Check my USDC balance"
"Send 100 USDC to 0x123..."
"What's my USDC balance on Base?"
```

## Methods

### get_balance(address=None)
Get USDC balance for address.
- **address**: Optional address (defaults to own)
- **Returns**: Balance data dict

### send_usdc(to_address, amount)
Send USDC to address.
- **to_address**: Recipient address
- **amount**: Amount in USDC
- **Returns**: Transaction result

### format_balance_message(balance_data)
Format balance for display.

### format_send_message(send_result)
Format send result for display.

## Network Details

- **Network**: Base Sepolia Testnet
- **Chain ID**: 84532
- **USDC Contract**: 0x036CbD53842c5426634e7929541eC2318f3dCF7e
- **RPC**: https://sepolia.base.org

## Safety

- ✅ Testnet only
- ✅ Never use mainnet keys
- ✅ Verify addresses before sending
- ✅ Check transaction on explorer

## Faucets

Get testnet USDC:
1. https://www.alchemy.com/faucets/base-sepolia (ETH for gas)
2. Circle testnet faucet for USDC

## Explorer

View transactions: https://sepolia.basescan.org
