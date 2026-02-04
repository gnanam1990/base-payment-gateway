# Nanba Base Payment Gateway

🚀 **A complete payment gateway solution for the Base ecosystem**

[![CI/CD](https://github.com/gnanam1990/base-payment-gateway/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/gnanam1990/base-payment-gateway/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Base](https://img.shields.io/badge/Base-Sepolia-blue.svg)](https://base.org)

Built by **Nanba** for **k Я Λ T 0 Ƨ**

---

## 📋 Overview

This project provides a **complete payment infrastructure** for the Base blockchain, featuring:

- ✅ **Smart Contract** - Multi-token payment gateway on Base
- ✅ **Backend API** - REST API with Stripe integration
- ✅ **Frontend** - React dApp with wallet connection
- ✅ **Dual Payment Support** - Crypto (Base) + Fiat (Stripe)

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend API    │────▶│  Smart Contract │
│   (React)       │     │   (Node.js)      │     │  (Base L2)      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────────┐
│   Rainbow Kit   │     │   Stripe API     │
│   (Wallet)      │     │   (Fiat)         │
└─────────────────┘     └──────────────────┘
```

---

## 📁 Project Structure

```
base-payment-project/
├── contracts/           # Smart contracts (Hardhat)
│   ├── NanbaPaymentGateway.sol
│   ├── hardhat.config.js
│   └── scripts/
│
├── backend/            # Backend API (Express)
│   ├── server.js
│   └── package.json
│
├── frontend/           # Frontend (React)
│   ├── src/
│   └── package.json
│
└── docs/              # Documentation
```

---

## 🚀 Quick Start

### 1. Smart Contract

```bash
cd contracts
npm install
cp .env.example .env
# Add your PRIVATE_KEY and BASESCAN_API_KEY
npx hardhat compile
npx hardhat run scripts/deploy.js --network baseSepolia
```

### 2. Backend

```bash
cd backend
npm install
cp .env.example .env
# Add your environment variables
npm run dev
```

### 3. Frontend

```bash
cd frontend
npm install
npm start
```

---

## ✨ Features

### Smart Contract

| Feature | Description |
|---------|-------------|
| **Multi-Token** | Support USDC, ETH, and any ERC20 |
| **Platform Fees** | Configurable (default 2.5%) |
| **Refunds** | Merchant/Owner can refund |
| **Withdrawals** | Merchants withdraw anytime |
| **Events** | Full event emission for tracking |

### Backend API

| Endpoint | Description |
|----------|-------------|
| `POST /api/payment/create` | Create crypto payment |
| `POST /api/payment/verify` | Verify on-chain payment |
| `POST /api/stripe/create-intent` | Create Stripe payment |
| `GET /api/merchant/:address/balance` | Check merchant balance |

### Frontend

- 🔗 Wallet connection (RainbowKit)
- 💳 Stripe payment integration
- 📊 Payment dashboard
- 📜 Transaction history

---

## 🔧 Configuration

### Environment Variables

#### Contracts (.env)
```
PRIVATE_KEY=your_wallet_private_key
BASE_SEPOLIA_RPC=https://sepolia.base.org
BASE_MAINNET_RPC=https://mainnet.base.org
BASESCAN_API_KEY=your_basescan_key
```

#### Backend (.env)
```
PORT=3001
CONTRACT_ADDRESS=your_deployed_contract
BASE_SEPOLIA_RPC=https://sepolia.base.org
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

#### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:3001
REACT_APP_CONTRACT_ADDRESS=your_contract_address
REACT_APP_STRIPE_PUBLIC_KEY=pk_test_...
```

---

## 🛡️ Security

- ✅ ReentrancyGuard on all external functions
- ✅ Ownable pattern for admin functions
- ✅ Rate limiting on API
- ✅ Helmet.js for HTTP headers
- ✅ Input validation on all endpoints

---

## 📊 Payment Flow

### Crypto Payment
```
1. Customer clicks "Pay with Crypto"
2. Frontend connects wallet
3. Approve token spend
4. Call processPayment()
5. Backend verifies on-chain
6. Payment complete!
```

### Stripe Payment
```
1. Customer clicks "Pay with Card"
2. Frontend loads Stripe elements
3. Customer enters card details
4. Stripe processes payment
5. Webhook confirms success
6. Payment complete!
```

---

## 🌐 Networks

| Network | Chain ID | Status |
|---------|----------|--------|
| Base Sepolia | 84532 | ✅ Testnet |
| Base Mainnet | 8453 | ✅ Production |

---

## 📝 License

MIT License - Built by Nanba 🐾

---

## 🙏 Credits

- **Base** - Coinbase L2 blockchain
- **OpenZeppelin** - Smart contract libraries
- **RainbowKit** - Wallet connection
- **Stripe** - Fiat payments

---

**Ready to accept payments on Base!** 🚀
