"""
💰 NANBA USDC SKILL
===================
OpenClaw skill for USDC testnet operations

Supports:
- Base Sepolia testnet
- Balance checks
- Transfers
- CCTP cross-chain (testnet)
"""

import os
from typing import Optional, Dict, Any
from decimal import Decimal

try:
    from web3 import Web3
except ImportError:
    raise ImportError("Install web3: pip install web3")

# Base Sepolia testnet config
BASE_SEPOLIA_RPC = "https://sepolia.base.org"
BASE_SEPOLIA_CHAIN_ID = 84532

# USDC contract on Base Sepolia (testnet)
USDC_CONTRACT = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"  # Circle testnet USDC

# Minimal USDC ABI (balanceOf + transfer)
USDC_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]


class USDCSkill:
    """
    USDC operations for OpenClaw - TESTNET ONLY
    """
    
    def __init__(self, private_key: Optional[str] = None):
        """
        Initialize USDC skill
        
        Args:
            private_key: Testnet private key (NO MAINNET KEYS!)
        """
        self.private_key = private_key or os.getenv('TESTNET_PRIVATE_KEY')
        if not self.private_key:
            raise ValueError(
                "TESTNET_PRIVATE_KEY required. "
                "Use testnet only - NEVER mainnet keys!"
            )
        
        # Connect to Base Sepolia
        self.w3 = Web3(Web3.HTTPProvider(BASE_SEPOLIA_RPC))
        
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Base Sepolia")
        
        # Setup account
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.address = self.account.address
        
        # USDC contract
        self.usdc = self.w3.eth.contract(
            address=Web3.to_checksum_address(USDC_CONTRACT),
            abi=USDC_ABI
        )
        
        # Get decimals (USDC = 6)
        self.decimals = self.usdc.functions.decimals().call()
    
    def get_balance(self, address: Optional[str] = None) -> Dict[str, Any]:
        """
        Get USDC balance
        
        Args:
            address: Address to check (default: own address)
            
        Returns:
            Balance info
        """
        addr = address or self.address
        
        try:
            balance_raw = self.usdc.functions.balanceOf(
                Web3.to_checksum_address(addr)
            ).call()
            
            balance = Decimal(balance_raw) / Decimal(10 ** self.decimals)
            
            return {
                'address': addr,
                'balance': float(balance),
                'raw_balance': balance_raw,
                'network': 'Base Sepolia Testnet',
                'contract': USDC_CONTRACT
            }
        except Exception as e:
            return {'error': str(e), 'address': addr}
    
    def send_usdc(self, to_address: str, amount: float) -> Dict[str, Any]:
        """
        Send USDC to address
        
        Args:
            to_address: Recipient address
            amount: Amount in USDC (e.g., 50.5)
            
        Returns:
            Transaction result
        """
        try:
            # Convert amount to wei-like units
            amount_raw = int(amount * (10 ** self.decimals))
            
            # Build transaction
            tx = self.usdc.functions.transfer(
                Web3.to_checksum_address(to_address),
                amount_raw
            ).build_transaction({
                'from': self.address,
                'nonce': self.w3.eth.get_transaction_count(self.address),
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price,
                'chainId': BASE_SEPOLIA_CHAIN_ID
            })
            
            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'from': self.address,
                'to': to_address,
                'amount': amount,
                'network': 'Base Sepolia Testnet',
                'explorer': f"https://sepolia.basescan.org/tx/{tx_hash.hex()}"
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def format_balance_message(self, balance_data: Dict) -> str:
        """Format balance for display"""
        if 'error' in balance_data:
            return f"❌ Error: {balance_data['error']}"
        
        return f"""💰 USDC Balance

Address: {balance_data['address']}
Balance: {balance_data['balance']:.2f} USDC
Network: {balance_data['network']}
Contract: {balance_data['contract']}

🧪 Testnet Only"""
    
    def format_send_message(self, send_result: Dict) -> str:
        """Format send result for display"""
        if not send_result.get('success'):
            return f"❌ Transfer Failed: {send_result.get('error')}"
        
        return f"""✅ USDC Transfer Sent!

From: {send_result['from']}
To: {send_result['to']}
Amount: {send_result['amount']:.2f} USDC
Network: {send_result['network']}

🔗 Transaction: {send_result['tx_hash']}
🔍 Explorer: {send_result['explorer']}

🧪 Testnet Only"""


# Convenience functions
def check_usdc_balance(address: Optional[str] = None) -> str:
    """Quick balance check"""
    skill = USDCSkill()
    balance = skill.get_balance(address)
    return skill.format_balance_message(balance)


def send_usdc(to_address: str, amount: float) -> str:
    """Quick send"""
    skill = USDCSkill()
    result = skill.send_usdc(to_address, amount)
    return skill.format_send_message(result)
