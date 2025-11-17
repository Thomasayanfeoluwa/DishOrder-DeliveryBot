import smtplib
import os
from twilio.rest import Client


class NotificationManager:

    def __init__(self):
        # Retrieve environment variables
        self.smtp_address = os.environ.get("EMAIL_PROVIDER_SMTP_ADDRESS", "smtp.gmail.com")
        self.email = os.environ.get("MANAGER_EMAIL")
        self.email_password = os.environ.get("MANAGER_EMAIL_PASSWORD")
        self.twilio_virtual_number = os.environ.get("TWILIO_VIRTUAL_NUMBER")
        self.twilio_verified_number = os.environ.get("TWILIO_VERIFIED_NUMBER")
        self.whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")
        
        # Initialize Twilio Client only if credentials exist
        twilio_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        twilio_token = os.environ.get("TWILIO_AUTH_TOKEN")

        if twilio_sid and twilio_token:
            self.client = Client(twilio_sid, twilio_token)
            print("Twilio client initialized successfully")
        else:
            self.client = None
            print("Twilio credentials not found. SMS/WhatsApp disabled.")


    def send_sms(self, message_body):
        """Send SMS notification"""
        if not self.client:
            print("SMS failed: Twilio client not initialized")
            return False
            
        try:
            message = self.client.messages.create(
                from_=self.twilio_virtual_number,
                body=message_body,
                to=self.twilio_verified_number
            )
            print(f"SMS sent. SID: {message.sid}")
            return True
        except Exception as e:
            print(f"SMS failed: {e}")
            return False

    def send_whatsapp(self, message_body):
        """Send WhatsApp message"""
        if not self.client:
            print("WhatsApp failed: Twilio client not initialized")
            return False
            
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.whatsapp_number}',
                body=message_body,
                to=f'whatsapp:{self.twilio_verified_number}'
            )
            print(f"WhatsApp sent. SID: {message.sid}")
            return True
        except Exception as e:
            print(f"WhatsApp failed: {e}")
            return False

    def send_emails(self, email_list, email_body):
        """Send email notifications"""
        if not self.email or not self.email_password:
            print("Email failed: Email credentials not configured")
            return False
            
        try:
            with smtplib.SMTP(self.smtp_address) as connection:  # FIXED: Use 'connection' not 'self.connection'
                connection.starttls()
                connection.login(self.email, self.email_password)
                for email in email_list:
                    connection.sendmail(  # FIXED: Use 'connection' not 'self.connection'
                        from_addr=self.email,
                        to_addrs=email,
                        msg=f"Subject:New Delivery Order!\n\n{email_body}".encode('utf-8')
                    )
                    print(f"Email sent to: {email}")
            return True
        except Exception as e:
            print(f"Email failed: {e}")
            return False