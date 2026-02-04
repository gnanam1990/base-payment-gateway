#!/bin/bash
# Quick setup script for development environment

echo "🌙 Nanba Payment Gateway - Quick Setup"
echo "======================================"

# Check Node.js version
node_version=$(node -v 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "❌ Node.js not found. Please install Node.js v18+"
    exit 1
fi

echo "✅ Node.js version: $node_version"

# Setup contracts
echo ""
echo "📦 Setting up smart contracts..."
cd contracts
npm install
npx hardhat compile
cd ..

# Setup backend
echo ""
echo "⚙️  Setting up backend..."
cd backend
npm install
cd ..

# Setup frontend
echo ""
echo "🎨 Setting up frontend..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. cd contracts && cp .env.example .env"
echo "2. Add your private key to .env"
echo "3. npm run dev (in each directory)"
