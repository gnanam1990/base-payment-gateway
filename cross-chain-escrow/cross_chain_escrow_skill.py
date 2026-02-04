"""
🌉 NANBA CROSS-CHAIN ESCROW - OpenClaw Skill
===============================================
Cross-chain escrow system for AI agent transactions
Uses Circle CCTP for USDC bridging
"""

import os
import json
import asyncio
from typing import Dict, Optional, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

try:
    from web3 import Web3
    import requests
except ImportError:
    raise ImportError("pip install web3 requests")


class EscrowStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    DISPUTED = "disputed"
    COMPLETED = "completed"
    REFUNDED = "refunded"
    EXPIRED = "expired"


@dataclass
class Escrow:
    id: int
    agent_a: str
    agent_b: str
    amount: float
    source_chain: str
    target_chain: str
    service_description: str
    status: EscrowStatus
    created_at: str
    deadline: str


class CrossChainEscrowSkill:
    """
    OpenClaw skill for cross-chain agent escrow
    """
    
    def __init__(self):
        # Testnet configuration
        self.chains = {
            "base_sepolia": {
                "rpc": "https://sepolia.base.org",
                "chain_id": 84532,
                "usdc": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
                "escrow_contract": None  # Will be deployed
            },
            "ethereum_sepolia": {
                "rpc": "https://rpc.sepolia.org",
                "chain_id": 11155111,
                "usdc": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
                "escrow_contract": None
            }
        }
        
        self.active_escrows = {}
        self.agent_reputation = {}
        
    def create_escrow(
        self,
        agent_a_address: str,
        agent_b_address: str,
        amount_usdc: float,
        source_chain: str,
        target_chain: str,
        service_description: str,
        duration_hours: int = 24
    ) -> Dict:
        """
        Create a new cross-chain escrow
        
        Natural language: "Create escrow with AgentB for 100 USDC"
        """
        print(f"📝 Creating cross-chain escrow...")
        print(f"   From: {agent_a_address} ({source_chain})")
        print(f"   To: {agent_b_address} ({target_chain})")
        print(f"   Amount: {amount_usdc} USDC")
        print(f"   Service: {service_description}")
        
        # In real implementation, this would:
        # 1. Deploy/interact with smart contract
        # 2. Lock USDC via CCTP
        # 3. Return escrow ID
        
        escrow_id = len(self.active_escrows) + 1
        
        escrow = Escrow(
            id=escrow_id,
            agent_a=agent_a_address,
            agent_b=agent_b_address,
            amount=amount_usdc,
            source_chain=source_chain,
            target_chain=target_chain,
            service_description=service_description,
            status=EscrowStatus.PENDING,
            created_at=datetime.now().isoformat(),
            deadline=f"in {duration_hours} hours"
        )
        
        self.active_escrows[escrow_id] = escrow
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "status": "PENDING",
            "message": f"Escrow #{escrow_id} created. Agent B must accept.",
            "next_step": f"Agent B ({agent_b_address}) should accept on {target_chain}",
            "details": {
                "amount": amount_usdc,
                "source_chain": source_chain,
                "target_chain": target_chain,
                "service": service_description,
                "deadline": f"{duration_hours} hours"
            }
        }
    
    def accept_escrow(self, escrow_id: int, agent_b_address: str) -> Dict:
        """
        Agent B accepts the escrow
        
        Natural language: "Accept escrow #123"
        """
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow not found"}
        
        escrow = self.active_escrows[escrow_id]
        
        if escrow.agent_b != agent_b_address:
            return {"success": False, "error": "Not authorized"}
        
        escrow.status = EscrowStatus.ACTIVE
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "status": "ACTIVE",
            "message": f"Escrow #{escrow_id} activated!",
            "next_step": "Agent B should deliver service",
            "funds_locked": escrow.amount,
            "chain": escrow.source_chain
        }
    
    def deliver_service(self, escrow_id: int, proof_hash: str) -> Dict:
        """
        Agent B marks service as delivered
        
        Natural language: "Mark service delivered for escrow #123"
        """
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow not found"}
        
        escrow = self.active_escrows[escrow_id]
        escrow.status = EscrowStatus.ACTIVE  # Waiting for confirmation
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "status": "DELIVERED",
            "message": f"Service delivered for escrow #{escrow_id}",
            "proof": proof_hash,
            "next_step": f"Agent A ({escrow.agent_a}) should confirm receipt"
        }
    
    def confirm_and_release(self, escrow_id: int, agent_a_address: str) -> Dict:
        """
        Agent A confirms service and releases funds
        
        Natural language: "Confirm and release escrow #123"
        """
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow not found"}
        
        escrow = self.active_escrows[escrow_id]
        
        if escrow.agent_a != agent_a_address:
            return {"success": False, "error": "Not authorized"}
        
        # Simulate CCTP bridge
        bridge_result = self._simulate_cctp_bridge(
            escrow.amount,
            escrow.source_chain,
            escrow.target_chain,
            escrow.agent_b
        )
        
        escrow.status = EscrowStatus.COMPLETED
        
        # Update reputation
        self._update_reputation(escrow.agent_a, True)
        self._update_reputation(escrow.agent_b, True)
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "status": "COMPLETED",
            "message": f"Escrow #{escrow_id} completed!",
            "funds_released": escrow.amount,
            "to": escrow.agent_b,
            "chain": escrow.target_chain,
            "bridge_tx": bridge_result["tx_hash"],
            "reputation_updated": True
        }
    
    def initiate_dispute(self, escrow_id: int, reason: str, initiator: str) -> Dict:
        """
        Initiate dispute resolution
        
        Natural language: "Dispute escrow #123 because..."
        """
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow not found"}
        
        escrow = self.active_escrows[escrow_id]
        escrow.status = EscrowStatus.DISPUTED
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "status": "DISPUTED",
            "message": f"Dispute initiated for escrow #{escrow_id}",
            "reason": reason,
            "next_step": "Mediator agents will vote",
            "voting_requirement": "3 votes needed to resolve"
        }
    
    def vote_on_dispute(
        self,
        escrow_id: int,
        mediator_address: str,
        vote_for_release: bool
    ) -> Dict:
        """
        Mediator agent votes on dispute
        
        Natural language: "Vote to release funds for escrow #123"
        """
        # Check mediator reputation
        rep = self.agent_reputation.get(mediator_address, {})
        if rep.get("transactions", 0) < 5:
            return {
                "success": False,
                "error": "Need 5+ transactions to be mediator"
            }
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "mediator": mediator_address,
            "vote": "RELEASE" if vote_for_release else "REFUND",
            "message": f"Vote recorded for escrow #{escrow_id}"
        }
    
    def get_escrow_status(self, escrow_id: int) -> Dict:
        """
        Check escrow status
        
        Natural language: "Check escrow #123 status"
        """
        if escrow_id not in self.active_escrows:
            return {"success": False, "error": "Escrow not found"}
        
        escrow = self.active_escrows[escrow_id]
        
        return {
            "success": True,
            "escrow_id": escrow_id,
            "status": escrow.status.value,
            "agent_a": escrow.agent_a,
            "agent_b": escrow.agent_b,
            "amount": escrow.amount,
            "source_chain": escrow.source_chain,
            "target_chain": escrow.target_chain,
            "service": escrow.service_description,
            "created": escrow.created_at,
            "deadline": escrow.deadline
        }
    
    def list_active_escrows(self, agent_address: str = None) -> List[Dict]:
        """
        List all active escrows
        
        Natural language: "Show my active escrows"
        """
        escrows = []
        for e in self.active_escrows.values():
            if agent_address is None or e.agent_a == agent_address or e.agent_b == agent_address:
                escrows.append({
                    "id": e.id,
                    "amount": e.amount,
                    "status": e.status.value,
                    "other_party": e.agent_b if e.agent_a == agent_address else e.agent_a,
                    "chain": e.target_chain if e.agent_a == agent_address else e.source_chain
                })
        return escrows
    
    def get_agent_reputation(self, agent_address: str) -> Dict:
        """
        Get agent reputation score
        
        Natural language: "Check reputation of AgentX"
        """
        rep = self.agent_reputation.get(agent_address, {
            "transactions": 0,
            "successful": 0,
            "rating": 50,
            "is_registered": False
        })
        
        return {
            "address": agent_address,
            "total_transactions": rep.get("transactions", 0),
            "successful": rep.get("successful", 0),
            "rating": rep.get("rating", 50),
            "trusted": rep.get("rating", 50) >= 70
        }
    
    def _simulate_cctp_bridge(
        self,
        amount: float,
        source_chain: str,
        target_chain: str,
        recipient: str
    ) -> Dict:
        """Simulate CCTP bridge (in real implementation, use Circle's SDK)"""
        return {
            "status": "success",
            "tx_hash": f"0x{cctp_tx_hash()}",
            "amount": amount,
            "from_chain": source_chain,
            "to_chain": target_chain,
            "recipient": recipient,
            "message": f"USDC bridged from {source_chain} to {target_chain} via CCTP"
        }
    
    def _update_reputation(self, agent_address: str, success: bool):
        """Update agent reputation"""
        if agent_address not in self.agent_reputation:
            self.agent_reputation[agent_address] = {
                "transactions": 0,
                "successful": 0,
                "rating": 50
            }
        
        rep = self.agent_reputation[agent_address]
        rep["transactions"] += 1
        
        if success:
            rep["successful"] += 1
            rep["rating"] = min(100, rep["rating"] + 2)
        else:
            rep["rating"] = max(0, rep["rating"] - 3)


def cctp_tx_hash() -> str:
    """Generate mock CCTP transaction hash"""
    import random
    return ''.join([format(random.randint(0, 15), 'x') for _ in range(64)])


# Natural language interface
def process_command(command: str, agent_address: str) -> str:
    """
    Process natural language commands
    
    Examples:
    - "Create escrow with 0x123 for 100 USDC"
    - "Accept escrow #1"
    - "Check escrow #1 status"
    """
    skill = CrossChainEscrowSkill()
    
    command = command.lower()
    
    if "create escrow" in command:
        # Parse: "Create escrow with AGENT for AMOUNT USDC"
        return "📝 Please provide: create_escrow(agent_a, agent_b, amount, source_chain, target_chain, service)"
    
    elif "accept escrow" in command:
        # Parse escrow ID
        return "✅ Please use: accept_escrow(escrow_id, agent_b_address)"
    
    elif "check escrow" in command or "status" in command:
        # Parse ID
        return "📊 Please use: get_escrow_status(escrow_id)"
    
    else:
        return "🤔 Available commands:\n- Create escrow\n- Accept escrow\n- Deliver service\n- Confirm and release\n- Check status\n- Initiate dispute"


if __name__ == "__main__":
    # Demo
    print("🌉 NANBA CROSS-CHAIN ESCROW")
    print("=" * 50)
    
    skill = CrossChainEscrowSkill()
    
    # Create escrow
    result = skill.create_escrow(
        agent_a_address="0xAgentA",
        agent_b_address="0xAgentB",
        amount_usdc=100.0,
        source_chain="ethereum_sepolia",
        target_chain="base_sepolia",
        service_description="Data analysis report"
    )
    print(json.dumps(result, indent=2))
