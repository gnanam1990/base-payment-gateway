# API Documentation

## Base URL
```
https://api.yourdomain.com/api
```

## Authentication
No authentication required for public endpoints.

## Endpoints

### Create Payment
```http
POST /payment/create
```

**Request Body:**
```json
{
  "merchantAddress": "0x...",
  "amount": 100,
  "token": "0x...",
  "metadata": "Order #123"
}
```

**Response:**
```json
{
  "success": true,
  "paymentId": "uuid",
  "paymentHash": "0x...",
  "contractAddress": "0x..."
}
```

### Verify Payment
```http
POST /payment/verify
```

**Request Body:**
```json
{
  "paymentHash": "0x..."
}
```

**Response:**
```json
{
  "success": true,
  "payment": {
    "payer": "0x...",
    "merchant": "0x...",
    "amount": "100",
    "status": "completed"
  }
}
```

### Get Merchant Balance
```http
GET /merchant/{address}/balance?token={tokenAddress}
```

**Response:**
```json
{
  "merchant": "0x...",
  "token": "ETH",
  "balance": "1.5"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 404 | Payment not found |
| 500 | Internal server error |
