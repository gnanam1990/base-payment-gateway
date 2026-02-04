require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const { ethers } = require('ethers');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Contract ABI (simplified)
const CONTRACT_ABI = [
  "function processPayment(address _merchant, uint256 _amount, address _token, string _paymentId, string _metadata) returns (bytes32)",
  "function processEthPayment(address _merchant, string _paymentId, string _metadata) payable returns (bytes32)",
  "function getPayment(bytes32 _paymentHash) view returns (tuple(address payer, address merchant, uint256 amount, address token, string paymentId, string metadata, uint8 status, uint256 timestamp))",
  "function merchantBalances(address _merchant, address _token) view returns (uint256)",
  "event PaymentCreated(bytes32 indexed paymentHash, address indexed payer, address indexed merchant, uint256 amount, address token, string paymentId)"
];

// Initialize provider
const provider = new ethers.JsonRpcProvider(
  process.env.BASE_SEPOLIA_RPC || "https://sepolia.base.org"
);

const contract = new ethers.Contract(
  process.env.CONTRACT_ADDRESS,
  CONTRACT_ABI,
  provider
);

// In-memory store (use MongoDB in production)
const payments = new Map();
const merchants = new Map();

// ==================== ROUTES ====================

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Get contract info
app.get('/api/contract/info', async (req, res) => {
  try {
    res.json({
      address: process.env.CONTRACT_ADDRESS,
      network: 'base-sepolia',
      platformFee: '2.5%'
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create payment intent (crypto)
app.post('/api/payment/create', async (req, res) => {
  try {
    const { merchantAddress, amount, token, metadata } = req.body;
    
    if (!merchantAddress || !amount) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    const paymentId = uuidv4();
    const paymentHash = ethers.keccak256(
      ethers.toUtf8Bytes(JSON.stringify({
        merchant: merchantAddress,
        amount,
        token: token || 'ETH',
        paymentId,
        timestamp: Date.now()
      }))
    );
    
    const payment = {
      paymentId,
      paymentHash,
      merchantAddress,
      amount,
      token: token || 'ETH',
      metadata: metadata || '',
      status: 'pending',
      createdAt: new Date().toISOString()
    };
    
    payments.set(paymentId, payment);
    
    res.json({
      success: true,
      paymentId,
      paymentHash,
      contractAddress: process.env.CONTRACT_ADDRESS,
      amount,
      merchantAddress
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Verify payment (after blockchain confirmation)
app.post('/api/payment/verify', async (req, res) => {
  try {
    const { paymentHash } = req.body;
    
    const payment = await contract.getPayment(paymentHash);
    
    if (payment.timestamp === 0n) {
      return res.status(404).json({ error: 'Payment not found' });
    }
    
    const statusMap = ['pending', 'completed', 'refunded', 'failed'];
    
    res.json({
      success: true,
      payment: {
        payer: payment.payer,
        merchant: payment.merchant,
        amount: ethers.formatEther(payment.amount),
        token: payment.token,
        paymentId: payment.paymentId,
        status: statusMap[payment.status],
        timestamp: Number(payment.timestamp)
      }
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get merchant balance
app.get('/api/merchant/:address/balance', async (req, res) => {
  try {
    const { address } = req.params;
    const { token } = req.query;
    
    const balance = await contract.merchantBalances(
      address,
      token || ethers.ZeroAddress
    );
    
    res.json({
      merchant: address,
      token: token || 'ETH',
      balance: ethers.formatEther(balance)
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Stripe payment integration
app.post('/api/stripe/create-intent', async (req, res) => {
  try {
    const { amount, currency = 'usd', metadata } = req.body;
    
    const paymentIntent = await stripe.paymentIntents.create({
      amount: amount * 100, // Convert to cents
      currency,
      metadata: {
        ...metadata,
        integration: 'nanba-payment-gateway'
      }
    });
    
    res.json({
      clientSecret: paymentIntent.client_secret,
      paymentIntentId: paymentIntent.id
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Webhook for Stripe
app.post('/webhook/stripe', express.raw({type: 'application/json'}), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  
  try {
    const event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
    
    if (event.type === 'payment_intent.succeeded') {
      console.log('✅ Stripe payment succeeded:', event.data.object.id);
      // Process successful payment
    }
    
    res.json({ received: true });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Get payment history
app.get('/api/payments/:merchantAddress', (req, res) => {
  const { merchantAddress } = req.params;
  
  const merchantPayments = Array.from(payments.values())
    .filter(p => p.merchantAddress.toLowerCase() === merchantAddress.toLowerCase())
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  
  res.json({
    merchant: merchantAddress,
    total: merchantPayments.length,
    payments: merchantPayments
  });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`⛓️  Contract: ${process.env.CONTRACT_ADDRESS || 'not configured'}`);
});

module.exports = app;
