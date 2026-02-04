# SKILL.md - Twilio Integration

## Name
twilio

## Description
Send SMS and make voice calls using Twilio API. Perfect for notifications, alerts, and automated messaging.

## Installation

```bash
pip install twilio python-dotenv
```

## Environment Variables

```bash
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_FROM_NUMBER=your_twilio_phone_number
```

## Usage

### Python API

```python
from skills.twilio import TwilioSkill

# Initialize
skill = TwilioSkill()

# Send SMS
result = skill.send_sms(
    to_number='+1234567890',
    message='Hello from Nanba!'
)
print(skill.format_sms_report(result))

# Make voice call
result = skill.make_call('+1234567890')

# Check account balance
balance = skill.get_balance()
```

### Quick SMS

```python
from skills.twilio import send_sms_quick

report = send_sms_quick('+1234567890', 'Hello!')
print(report)
```

## Methods

### send_sms(to_number, message)
Send SMS to a phone number.
- **to_number**: Recipient with country code (e.g., +1234567890)
- **message**: Text message (max 1600 chars)
- **Returns**: Message details or error

### send_bulk_sms(to_numbers, message)
Send SMS to multiple recipients.
- **to_numbers**: List of phone numbers
- **message**: Text message
- **Returns**: List of results

### make_call(to_number, twiml_url=None)
Make voice call.
- **to_number**: Recipient phone number
- **twiml_url**: URL to voice instructions (optional)
- **Returns**: Call details

### check_message_status(message_sid)
Check delivery status of sent message.
- **message_sid**: Message SID from send_sms
- **Returns**: Status details

### get_balance()
Get Twilio account balance.
- **Returns**: Balance and currency

### list_phone_numbers()
List your Twilio phone numbers.
- **Returns**: List of numbers with capabilities

## Setup Instructions

1. **Create Twilio Account:**
   - Go to https://www.twilio.com/try-twilio
   - Sign up and verify

2. **Get Credentials:**
   - Account SID: From Twilio Console dashboard
   - Auth Token: From Twilio Console dashboard

3. **Buy Phone Number:**
   - Go to Phone Numbers > Manage > Buy a number
   - Choose number with SMS and Voice capabilities

4. **Set Environment Variables:**
   ```bash
   export TWILIO_ACCOUNT_SID=ACxxxxx
   export TWILIO_AUTH_TOKEN=xxxxx
   export TWILIO_FROM_NUMBER=+1xxxxxx
   ```

## Pricing

- SMS: ~$0.0075 per message (US)
- Voice calls: ~$0.013 per minute (US)
- International rates vary
- Check: https://www.twilio.com/pricing

## Examples

### Trading Alert
```python
skill = TwilioSkill()
skill.send_sms('+1234567890', '🚨 BTC dropped 5%! Check your positions.')
```

### Daily Summary
```python
skill = TwilioSkill()
message = """📊 Daily Report:
Portfolio: $12,450 (+2.3%)
Best: ETH +5%
Worst: BTC -1%
"""
skill.send_sms('+1234567890', message)
```

### Bulk Notification
```python
skill = TwilioSkill()
numbers = ['+1234567890', '+1987654321']
skill.send_bulk_sms(numbers, 'System maintenance in 30 minutes.')
```

## Security

- ✅ Never commit credentials to Git
- ✅ Use environment variables
- ✅ Validate phone numbers
- ✅ Check message length (1600 char limit)

## Links

- Twilio Console: https://console.twilio.com
- Documentation: https://www.twilio.com/docs
- Pricing: https://www.twilio.com/pricing
