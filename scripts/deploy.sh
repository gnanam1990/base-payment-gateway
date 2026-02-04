#!/bin/bash
# Deploy script wrapper

NETWORK=${1:-baseSepolia}

echo "🚀 Deploying to $NETWORK..."

cd contracts
npx hardhat run scripts/deploy.js --network $NETWORK

echo "✅ Deployment complete!"
