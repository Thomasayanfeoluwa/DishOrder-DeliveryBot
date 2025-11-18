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
            with smtplib.SMTP(self.smtp_address, 587) as connection:  
                connection.starttls()
                connection.login(self.email, self.email_password)
                for email in email_list:
                    connection.sendmail( 
                        from_addr=self.email,
                        to_addrs=email,
                        msg=f"Subject:New Delivery Order!\n\n{email_body}".encode('utf-8')
                    )
                    print(f"Email sent to: {email}")
            return True
        except Exception as e:
            print(f"Email failed: {e}")
            return False
        
    

    def notify_owner(self, order_details, customer_info, total_amount, order_images=None):
        """
        Enhanced notification with order images
        """
        # Base notification message
        notification_message = f"""
    🚨 **NEW CUSTOMER ORDER** 🚨

    👤 **CUSTOMER DETAILS:**
    📛 Name: {customer_info.get('name', 'Not provided')}
    📞 Phone: {customer_info.get('phone', 'Not provided')}
    📍 Address: {customer_info.get('address', 'Not provided')}

    💰 **ORDER TOTAL:** ₦{total_amount:,.2f}

    📦 **ORDER DETAILS:**
    {order_details}
    """
        
        # Add image references if available
        if order_images:
            notification_message += "\n\n📸 **ORDER IMAGES:**\n"
            for img_url in order_images:
                notification_message += f"- {img_url}\n"
        
        notification_message += "\n📍 **ACTION REQUIRED:** Please prepare this order immediately!"
        
        # Send notifications
        self.send_sms(notification_message[:160])  # SMS limited
        self.send_whatsapp(notification_message)
        
        # Enhanced email with images
        owner_emails = os.environ.get("OWNER_EMAILS", "").split(',')
        if owner_emails and owner_emails[0]:
            email_body = f"""
    New order received!

    CUSTOMER INFORMATION:
    Name: {customer_info.get('name', 'Not provided')}
    Phone: {customer_info.get('phone', 'Not provided')}
    Address: {customer_info.get('address', 'Not provided')}

    ORDER TOTAL: ₦{total_amount:,.2f}

    ORDER DETAILS:
    {order_details}

    ORDER IMAGES:
    {chr(10).join(order_images) if order_images else 'No images available'}

    Please prepare this order immediately!
            """
            self.send_emails(owner_emails, email_body)