# Deployment Guide

## Prerequisites

- Node.js v18+
- Git
- Base Sepolia ETH (for testing)

## Step 1: Smart Contract Deployment

### 1.1 Install dependencies
```bash
cd contracts
npm install
```

### 1.2 Configure environment
```bash
cp .env.example .env
# Edit .env with your private key
```

### 1.3 Deploy to Base Sepolia
```bash
npx hardhat run scripts/deploy.js --network baseSepolia
```

### 1.4 Verify contract
```bash
npx hardhat verify --network baseSepolia CONTRACT_ADDRESS
```

## Step 2: Backend Deployment

### 2.1 Install dependencies
```bash
cd backend
npm install
```

### 2.2 Configure environment
```bash
cp .env.example .env
# Add your contract address and Stripe keys
```

### 2.3 Start server
```bash
npm start
```

## Step 3: Frontend Deployment

### 3.1 Install dependencies
```bash
cd frontend
npm install
```

### 3.2 Build for production
```bash
npm run build
```

### 3.3 Deploy to Vercel/Netlify
```bash
npx vercel --prod
```

## Environment Variables

### Contracts
- `PRIVATE_KEY`: Deployer wallet private key
- `BASE_SEPOLIA_RPC`: Base Sepolia RPC URL
- `BASESCAN_API_KEY`: For contract verification

### Backend
- `CONTRACT_ADDRESS`: Deployed contract address
- `STRIPE_SECRET_KEY`: Stripe API key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook secret

### Frontend
- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_CONTRACT_ADDRESS`: Contract address
- `REACT_APP_STRIPE_PUBLIC_KEY`: Stripe public key
