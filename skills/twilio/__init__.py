"""
📱 NANBA TWILIO SKILL
=====================
Send SMS and make calls using Twilio API

Setup:
1. Get SID and Auth Token from Twilio Console
2. Set environment variables or pass to constructor
3. Use phone number must be purchased from Twilio
"""

import os
from typing import Optional, Dict, List

try:
    from twilio.rest import Client
except ImportError:
    raise ImportError("Install twilio: pip install twilio")


class TwilioSkill:
    """
    Twilio integration for SMS and voice calls
    """
    
    def __init__(self, 
                 account_sid: Optional[str] = None,
                 auth_token: Optional[str] = None,
                 from_number: Optional[str] = None):
        """
        Initialize Twilio client
        
        Args:
            account_sid: Twilio Account SID
            auth_token: Twilio Auth Token
            from_number: Twilio phone number (with country code)
        """
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = from_number or os.getenv('TWILIO_FROM_NUMBER')
        
        if not self.account_sid or not self.auth_token:
            raise ValueError(
                "Twilio credentials required. "
                "Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN env vars "
                "or pass to constructor"
            )
        
        self.client = Client(self.account_sid, self.auth_token)
        self.message_history = []
    
    def send_sms(self, to_number: str, message: str) -> Dict:
        """
        Send SMS message
        
        Args:
            to_number: Recipient phone number (with country code, e.g., +1234567890)
            message: Message text (max 1600 characters)
            
        Returns:
            Dict with message details
        """
        try:
            if not self.from_number:
                return {'success': False, 'error': 'From number not configured'}
            
            # Validate message length
            if len(message) > 1600:
                message = message[:1597] + "..."
            
            # Send message
            twilio_message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            result = {
                'success': True,
                'message_sid': twilio_message.sid,
                'status': twilio_message.status,
                'to': to_number,
                'from': self.from_number,
                'body': message[:100] + "..." if len(message) > 100 else message,
                'price': twilio_message.price,
                'direction': twilio_message.direction
            }
            
            self.message_history.append(result)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'to': to_number
            }
    
    def send_bulk_sms(self, to_numbers: List[str], message: str) -> List[Dict]:
        """
        Send SMS to multiple recipients
        
        Args:
            to_numbers: List of phone numbers
            message: Message text
            
        Returns:
            List of results for each number
        """
        results = []
        for number in to_numbers:
            result = self.send_sms(number, message)
            results.append(result)
        return results
    
    def make_call(self, to_number: str, twiml_url: Optional[str] = None) -> Dict:
        """
        Make voice call
        
        Args:
            to_number: Recipient phone number
            twiml_url: URL to TwiML instructions (optional)
            
        Returns:
            Dict with call details
        """
        try:
            if not self.from_number:
                return {'success': False, 'error': 'From number not configured'}
            
            # Default TwiML - simple message
            if not twiml_url:
                twiml = '<Response><Say>This is a call from Nanba AI assistant.</Say></Response>'
            else:
                twiml = None
            
            # Make call
            if twiml:
                call = self.client.calls.create(
                    twiml=twiml,
                    to=to_number,
                    from_=self.from_number
                )
            else:
                call = self.client.calls.create(
                    url=twiml_url,
                    to=to_number,
                    from_=self.from_number
                )
            
            return {
                'success': True,
                'call_sid': call.sid,
                'status': call.status,
                'to': to_number,
                'from': self.from_number,
                'duration': call.duration
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'to': to_number
            }
    
    def check_message_status(self, message_sid: str) -> Dict:
        """
        Check status of sent message
        
        Args:
            message_sid: Message SID from send_sms
            
        Returns:
            Message status details
        """
        try:
            message = self.client.messages(message_sid).fetch()
            return {
                'success': True,
                'sid': message.sid,
                'status': message.status,
                'to': message.to,
                'from': message.from_,
                'body': message.body[:100] if message.body else "",
                'date_sent': str(message.date_sent),
                'price': message.price,
                'error_message': message.error_message
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_balance(self) -> Dict:
        """
        Get Twilio account balance
        
        Returns:
            Balance information
        """
        try:
            balance = self.client.balance.fetch()
            return {
                'success': True,
                'balance': balance.balance,
                'currency': balance.currency
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_phone_numbers(self) -> List[Dict]:
        """
        List purchased phone numbers
        
        Returns:
            List of phone numbers
        """
        try:
            numbers = self.client.incoming_phone_numbers.list()
            return [
                {
                    'sid': num.sid,
                    'phone_number': num.phone_number,
                    'friendly_name': num.friendly_name,
                    'capabilities': {
                        'voice': num.capabilities['voice'],
                        'sms': num.capabilities['sms'],
                        'mms': num.capabilities['mms']
                    }
                }
                for num in numbers
            ]
        except Exception as e:
            return [{'error': str(e)}]
    
    def format_sms_report(self, result: Dict) -> str:
        """Format SMS result for display"""
        if result.get('success'):
            return f"""✅ SMS Sent Successfully!

To: {result['to']}
From: {result['from']}
Status: {result['status']}
Message SID: {result['message_sid']}
Price: {result.get('price', 'N/A')} USD

Message: {result['body']}"""
        else:
            return f"""❌ SMS Failed

Error: {result.get('error', 'Unknown error')}
To: {result.get('to', 'N/A')}"""


# Convenience functions
def send_sms_quick(to_number: str, message: str) -> str:
    """Quick SMS send"""
    skill = TwilioSkill()
    result = skill.send_sms(to_number, message)
    return skill.format_sms_report(result)


if __name__ == "__main__":
    print("📱 Nanba Twilio Skill")
    print("Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER")
    print("\nExample usage:")
    print("  skill = TwilioSkill()")
    print("  result = skill.send_sms('+1234567890', 'Hello from Nanba!')")
    print("  print(skill.format_sms_report(result))")
