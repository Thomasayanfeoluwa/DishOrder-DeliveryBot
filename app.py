# import chainlit as cl
# from fastapi import Request
# from chainlit.server import app as fastapi_app
# import json
# import os
# from src.loader import order_request, messages
# from twilio.twiml.messaging_response import MessagingResponse
# from src.notification import NotificationManager

# # Load environment variables FIRST
# from dotenv import load_dotenv
# load_dotenv()  # This loads variables from .env file

# # Initialize notification manager AFTER loading environment
# notification_manager = NotificationManager()

# async def process_order(message_text: str):
#     # Add user message to conversation
#     messages.append({"role": "user", "content": message_text})
    
#     # Get LLM response
#     response = order_request(messages)
    
#     # Add assistant response to conversation
#     messages.append({"role": "assistant", "content": response})
    
#     # Check order and send notifications
#     if "ORDER CONFIRMED" in response or "Total: ₦" in response:
#         # Put your existing notification code here (SMS, WhatsApp, Email)
#         total_line = [line for line in response.split('\n') if 'Total:' in line]
#         total_amount = 0.0
#         if total_line:
#             import re
#             amount_str = re.search(r'₦?[\d,]+\.?\d*', total_line[0])
#             if amount_str:
#                 total_amount = float(amount_str.group().replace('₦', '').replace(',', ''))
#         if total_amount > 0:
#             sms_message = f"New Order: ₦{total_amount:,.2f}\nCheck system for details"
#             notification_manager.send_sms(sms_message)
#             whatsapp_message = f"🆕 NEW ORDER 🆕\nTotal: ₦{total_amount:,.2f}\n{response[:200]}..."
#             notification_manager.send_whatsapp(whatsapp_message)
#             owner_emails = os.environ.get("OWNER_EMAILS", "").split(',')
#             if owner_emails and owner_emails[0]:
#                 email_body = f"New order received:\n\n{response}"
#                 notification_manager.send_emails(owner_emails, email_body)
    
#     return response


# @cl.on_message
# async def main(message: cl.Message):
#     response = await process_order(message.content)
#     await cl.Message(content=response).send()
    
#     # Add assistant response to conversation
#     messages.append({"role": "assistant", "content": response})
    
#     # Check if order is confirmed and send notifications
#     if "ORDER CONFIRMED" in response or "Total: ₦" in response:
#         # Extract total amount from response
#         total_line = [line for line in response.split('\n') if 'Total:' in line]
#         total_amount = 0.0
        
#         if total_line:
#             try:
#                 # Extract number from "Total: ₦5,000" format
#                 import re
#                 amount_str = re.search(r'₦?[\d,]+\.?\d*', total_line[0])
#                 if amount_str:
#                     total_amount = float(amount_str.group().replace('₦', '').replace(',', ''))
#             except:
#                 total_amount = 0.0
        
#         # Send notifications
#         if total_amount > 0:
#             # Send SMS
#             sms_message = f"New Order: ₦{total_amount:,.2f}\nCheck system for details"
#             notification_manager.send_sms(sms_message)
            
#             # Send WhatsApp
#             whatsapp_message = f"🆕 NEW ORDER 🆕\nTotal: ₦{total_amount:,.2f}\n{response[:200]}..."
#             notification_manager.send_whatsapp(whatsapp_message)
            
#             # Send Email
#             owner_emails = os.environ.get("OWNER_EMAILS", "").split(',')
#             if owner_emails and owner_emails[0]:
#                 email_body = f"New order received:\n\n{response}"
#                 notification_manager.send_emails(owner_emails, email_body)

#     # Send response to user
#     await cl.Message(content=response).send()


# @fastapi_app.post("/whatsapp/webhook")
# async def whatsapp_webhook(request: Request):
#     form = await request.form()
#     from_number = form.get("From")
#     message_body = form.get("Body")
#     print(f"Received WhatsApp message from {from_number}: {message_body}")

#     # Wrap form data into a real Chainlit Message object
#     user_message = cl.Message(content=message_body)

#     # Call your existing Chainlit handler
#     await main(user_message)

#     # Reply to Twilio
#     resp = MessagingResponse()
#     resp.message("Message received. Processing your order...")
#     return str(resp)



import chainlit as cl
from fastapi import Request
from chainlit.server import app as fastapi_app
import json
import os
from src.loader import order_request, messages
from twilio.twiml.messaging_response import MessagingResponse
from src.notification import NotificationManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize notification manager
notification_manager = NotificationManager()

# -------------------------------
# Refactored order processing
# -------------------------------
async def process_order(message_text: str):
    # Add user message to conversation
    messages.append({"role": "user", "content": message_text})
    
    # Get LLM response
    response = order_request(messages)
    
    # Add assistant response to conversation
    messages.append({"role": "assistant", "content": response})
    
    # Check order and send notifications
    if "ORDER CONFIRMED" in response or "Total: ₦" in response:
        total_line = [line for line in response.split('\n') if 'Total:' in line]
        total_amount = 0.0
        if total_line:
            import re
            amount_str = re.search(r'₦?[\d,]+\.?\d*', total_line[0])
            if amount_str:
                total_amount = float(amount_str.group().replace('₦', '').replace(',', ''))
        if total_amount > 0:
            sms_message = f"New Order: ₦{total_amount:,.2f}\nCheck system for details"
            notification_manager.send_sms(sms_message)
            whatsapp_message = f"🆕 NEW ORDER 🆕\nTotal: ₦{total_amount:,.2f}\n{response[:200]}..."
            notification_manager.send_whatsapp(whatsapp_message)
            owner_emails = os.environ.get("OWNER_EMAILS", "").split(',')
            if owner_emails and owner_emails[0]:
                email_body = f"New order received:\n\n{response}"
                notification_manager.send_emails(owner_emails, email_body)
    
    return response

# -------------------------------
# Chainlit handler
# -------------------------------
@cl.on_message
async def main(message: cl.Message):
    response = await process_order(message.content)
    await cl.Message(content=response).send()

# -------------------------------
# Twilio WhatsApp webhook
# -------------------------------
@fastapi_app.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    from_number = form.get("From")
    message_body = form.get("Body")
    print(f"Received WhatsApp message from {from_number}: {message_body}")

    # Call the refactored function directly (no cl.Message)
    response_text = await process_order(message_body)

    # Reply to Twilio
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)
