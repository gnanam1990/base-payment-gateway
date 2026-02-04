# API Documentation

## Authentication

All API endpoints require authentication via API key.

```bash
Authorization: Bearer YOUR_API_KEY
```

## Base URL

```
https://api.nanbapay.com/v1
```

## Endpoints

### POST /payments

Create a new payment.

**Request:**
```json
{
  "amount": "100.00",
  "currency": "ETH",
  "recipient": "0x...",
  "callback_url": "https://yoursite.com/webhook"
}
```

**Response:**
```json
{
  "payment_id": "pay_123",
  "status": "pending",
  "payment_url": "https://pay.nanbapay.com/pay_123"
}
```

### GET /payments/{id}

Get payment status.

**Response:**
```json
{
  "payment_id": "pay_123",
  "status": "completed",
  "amount": "100.00",
  "tx_hash": "0x..."
}
```

## Webhooks

Webhooks are sent to your callback URL when payment status changes.

**Payload:**
```json
{
  "event": "payment.completed",
  "payment_id": "pay_123",
  "data": { ... }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Payment Not Found |
| 500 | Internal Server Error |
