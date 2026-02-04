# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report security vulnerabilities to the repository owner privately.

DO NOT create a public issue for security bugs.

## Security Measures

- ReentrancyGuard on all payment functions
- Ownable pattern for administrative functions
- Input validation on all endpoints
- Rate limiting to prevent abuse
- No storage of private keys in code

## Best Practices

1. Never commit `.env` files
2. Use hardware wallets for deployment
3. Verify contracts on Basescan
4. Monitor contract activity
5. Keep dependencies updated
