import chainlit as cl
from fastapi import Request
from chainlit.server import app as fastapi_app
import json
import os
import re
import time
from src.loader import order_request, messages
from twilio.twiml.messaging_response import MessagingResponse
from src.notification import NotificationManager
from services.image_service import DishImageService
from services.payment_service import PaystackService

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize services
notification_manager = NotificationManager()
image_service = DishImageService()
payment_service = PaystackService()

# Store user information and notification status
user_sessions = {}

@cl.on_chat_start
async def start_chat():
    """Send welcome message immediately when chat starts"""
    welcome_message = """
# Welcome to DishDelivery Nigerian Restaurant! 🍽️🇳🇬

**How you dey!** Welcome to DishDelivery - your number one spot for authentic Nigerian cuisine! 

## How to Order
1. **Browse our menu** - Tell me what you'd like to eat
2. **Provide delivery details** - Name, phone, address
3. **Get confirmation** - We'll calculate your total
4. **Complete payment** - Secure payment via Paystack
5. **Receive your order** - Delivered to your doorstep!

*Minimum delivery: ₦1,500*

**Ready to order?** Just tell me what you'd like!

🍛 **Popular Dishes:**
- Jollof Rice with Chicken
- Pounded Yam with Egusi Soup  
- Fried Rice with Beef
- Suya with drinks
"""
    await cl.Message(content=welcome_message).send()

def is_final_confirmation(response):
    """
    STRICT check for FINAL order confirmation
    Only returns True for the actual final confirmation message
    """
    # Must contain ORDER CONFIRMED
    if "ORDER CONFIRMED" not in response.upper():
        return False
    
    # Must NOT contain any phrases asking for more information
    exclusion_phrases = [
        "please provide", "not provided", "is this correct?", 
        "can you provide", "i need", "let me get", "confirm again",
        "would you like", "do you have", "can you please"
    ]
    
    response_lower = response.lower()
    for phrase in exclusion_phrases:
        if phrase in response_lower:
            return False
    
    # Must contain customer information section
    if "customer information" not in response_lower and "name:" not in response_lower:
        return False
    
    # Must contain total amount
    if "total: ₦" not in response_lower:
        return False
    
    return True

def extract_customer_info_from_response(response):
    """Extract customer details from LLM response"""
    customer_info = {
        'name': None,
        'phone': None,
        'address': None,
        'email': None
    }
    
    lines = response.split('\n')
    for line in lines:
        line_lower = line.lower()
        
        # Look for name
        if 'name:' in line_lower and 'customer' not in line_lower:
            name_parts = line.split(':')
            if len(name_parts) > 1:
                name = name_parts[1].strip()
                if name and name not in ['(please provide your name)', 'not provided']:
                    customer_info['name'] = name
        
        # Look for phone
        if 'phone:' in line_lower:
            phone_parts = line.split(':')
            if len(phone_parts) > 1:
                phone_str = phone_parts[1].strip()
                # Extract Nigerian phone numbers
                phone_match = re.search(r'(\+?234[789][01]\d{8}|0[789][01]\d{8}|\d{11})', phone_str)
                if phone_match:
                    customer_info['phone'] = phone_match.group()
                elif phone_str and phone_str not in ['(please provide your phone number)', 'not provided']:
                    customer_info['phone'] = phone_str
        
        # Look for address
        if 'address:' in line_lower:
            address_parts = line.split(':')
            if len(address_parts) > 1:
                address = address_parts[1].strip()
                if address and address not in ['(please provide your address)', 'not provided', 'delivery']:
                    customer_info['address'] = address
        
        # Look for email
        if 'email:' in line_lower:
            email_parts = line.split(':')
            if len(email_parts) > 1:
                email = email_parts[1].strip()
                if email and '@' in email:
                    customer_info['email'] = email
    
    return customer_info

def extract_total_amount(response):
    """Extract total order amount"""
    total_amount = 0.0
    total_line = [line for line in response.split('\n') if 'total: ₦' in line.lower()]
    
    if total_line:
        try:
            amount_str = re.search(r'₦?([\d,]+\.?\d*)', total_line[0])
            if amount_str:
                total_amount = float(amount_str.group(1).replace(',', ''))
        except:
            total_amount = 0.0
    
    return total_amount

def format_customer_info(customer_session):
    """Format customer information for notifications"""
    return {
        'name': customer_session.get('name', 'Not provided'),
        'phone': customer_session.get('phone', 'Not provided'),
        'address': customer_session.get('address', 'Not provided'),
        'email': customer_session.get('email', 'Not provided')
    }

@cl.on_message 
async def main(message: cl.Message):
    user_id = message.id
    
    # Initialize user session if not exists
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'name': None,
            'phone': None,
            'address': None,
            'email': None,
            'notification_sent': False,
            'payment_processed': False
        }
    
    # Extract customer info from user message
    user_info = extract_customer_info_from_response(message.content)
    for key in ['name', 'phone', 'address', 'email']:
        if user_info[key]:
            user_sessions[user_id][key] = user_info[key]
    
    # Add user message to conversation
    messages.append({"role": "user", "content": message.content})
    
    # Get LLM response
    response = order_request(messages)
    
    # Add assistant response to conversation
    messages.append({"role": "assistant", "content": response})
    
    # Extract customer info from current response and update session
    current_customer_info = extract_customer_info_from_response(response)
    for key in ['name', 'phone', 'address', 'email']:
        if current_customer_info[key]:
            user_sessions[user_id][key] = current_customer_info[key]
    
    # Check if this is menu browsing or order discussion - SHOW IMAGES
    if any(keyword in response.lower() for keyword in ['menu', 'dish', 'soup', 'rice', 'chicken', 'beef', 'fish', 'plantain', 'drink']):
        # Show dish images when discussing menu items
        dish_images = image_service.get_images_for_order(response)
        
        if dish_images:
            # Create image elements
            elements = []
            for img_url in dish_images:
                elements.append(cl.Image(name="Dish Image", display="inline", url=img_url))
            
            # Send message with images
            await cl.Message(content=response, elements=elements).send()
            return
    
    # Check if this is the FINAL confirmation (STRICT check)
    if (is_final_confirmation(response) and 
        not user_sessions[user_id]['notification_sent'] and
        user_sessions[user_id]['phone'] is not None):  # Must have phone at minimum
        
        total_amount = extract_total_amount(response)
        
        if total_amount > 0:
            # Mark notification as sent to prevent duplicates
            user_sessions[user_id]['notification_sent'] = True
            
            customer_info = user_sessions[user_id]
            
            # Get order images for manager notification
            order_images = image_service.get_images_for_order(response)
            
            # Create clean order summary (remove conversational parts)
            order_lines = []
            in_order_section = False
            for line in response.split('\n'):
                clean_line = line.strip()
                if 'ORDER CONFIRMED' in clean_line.upper():
                    in_order_section = True
                if in_order_section and clean_line and not clean_line.startswith('How you dey'):
                    if any(indicator in clean_line.lower() for indicator in ['-', '•', '*', 'item', 'total:']):
                        order_lines.append(clean_line)
            
            order_summary = '\n'.join(order_lines) if order_lines else "Full details in system"
            
            # Format manager notification
            manager_message = f"""
🚨 **NEW CUSTOMER ORDER** 🚨

👤 **CUSTOMER DETAILS:**
📛 Name: {customer_info['name'] or 'Not provided'}
📞 Phone: {customer_info['phone'] or 'Not provided'}
📍 Address: {customer_info['address'] or 'Not provided'}

💰 **ORDER TOTAL:** ₦{total_amount:,.2f}

📦 **ORDER SUMMARY:**
{order_summary}

📍 **ACTION REQUIRED:** 
Please prepare this order immediately and contact the customer for delivery confirmation!
"""
            
            # Send SINGLE notification to manager
            print("🔄 SENDING FINAL ORDER NOTIFICATION...")
            notification_manager.send_sms(manager_message)
            notification_manager.send_whatsapp(manager_message)
            
            # Send email to owner
            owner_emails = os.environ.get("OWNER_EMAILS", "").split(',')
            if owner_emails and owner_emails[0]:
                email_subject = f"🆕 FINAL ORDER - ₦{total_amount:,.2f} - {customer_info['name'] or 'Customer'}"
                notification_manager.send_emails(owner_emails, manager_message)
            
            # Generate payment link for customer
            payment_response = payment_service.initiate_payment(
                email=customer_info.get('email', 'customer@example.com'),
                amount=total_amount,
                reference=f"DD{user_id}{int(time.time())}",
                metadata={
                    "customer_name": customer_info.get('name'),
                    "phone": customer_info.get('phone'),
                    "address": customer_info.get('address')
                }
            )
            
            if payment_response.get('status'):
                payment_url = payment_response['data']['authorization_url']
                
                # Send payment message to user
                payment_message = f"""
💰 **Payment Required**

Your order total: **₦{total_amount:,.2f}**

Please complete your payment using this secure link:
{payment_url}

📍 **After payment, we'll immediately prepare your order!**
⏰ Delivery time: 30-45 minutes
                """
                
                await cl.Message(content=payment_message).send()
            else:
                error_message = "Payment system temporarily unavailable. Please try again in a few minutes or contact us directly."
                await cl.Message(content=error_message).send()

    # Send normal response without images
    await cl.Message(content=response).send()

@fastapi_app.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    from_number = form.get("From")
    message_body = form.get("Body")
    print(f"📱 WhatsApp message from {from_number}: {message_body}")

    # Use phone number as user ID for WhatsApp
    user_id = from_number
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'name': None,
            'phone': from_number,  # Set phone from WhatsApp number
            'address': None,
            'email': None,
            'notification_sent': False,
            'payment_processed': False
        }
    else:
        user_sessions[user_id]['phone'] = from_number

    # Create message and process
    user_message = cl.Message(content=message_body)
    await main(user_message)

    # Reply to customer
    resp = MessagingResponse()
    resp.message("Thank you! Your order is being processed. We'll contact you shortly.")
    return str(resp)



























# import chainlit as cl
# from fastapi import Request
# from chainlit.server import app as fastapi_app
# import json
# import os
# import re
# from src.loader import order_request, messages
# from twilio.twiml.messaging_response import MessagingResponse
# from src.notification import NotificationManager

# # Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

# # Initialize notification manager
# notification_manager = NotificationManager()

# # Store user information globally
# user_sessions = {}

# @cl.on_chat_start
# async def start_chat():
#     """Send welcome message immediately when chat starts"""
#     welcome_message = """
# # Welcome to DishDelivery Nigerian Restaurant! 🍽️🇳🇬

# **How you dey!** Welcome to DishDelivery - your number one spot for authentic Nigerian cuisine! 

# ## How to Order
# 1. **Browse our menu** - We have everything from traditional soups to delicious rice dishes
# 2. **Place your order** - Just tell me what you'd like to eat  
# 3. **Choose delivery or pickup** - We'll bring it to you or have it ready for pickup
# 4. **Get confirmation** - We'll calculate your total and confirm your order

# *Minimum delivery: ₦1,500*

# **Ready to order?** Just tell me what you'd like!
# """
#     await cl.Message(content=welcome_message).send()

# @cl.on_message 
# async def main(message: cl.Message):
#     # Store user info if provided
#     user_id = message.id
#     if user_id not in user_sessions:
#         user_sessions[user_id] = {
#             'phone': None,
#             'address': None,
#             'name': None
#         }
    
#     # Extract phone number from message
#     phone_match = re.search(r'(\+?234|0)[789][01]\d{8}', message.content)
#     if phone_match:
#         user_sessions[user_id]['phone'] = phone_match.group()
    
#     # Look for address indicators
#     if any(keyword in message.content.lower() for keyword in ['address', 'location', 'street', 'house', 'deliver']):
#         user_sessions[user_id]['address'] = message.content
    
#     # Look for name
#     if 'my name is' in message.content.lower():
#         name_match = re.search(r'my name is (\w+ \w+)', message.content.lower())
#         if name_match:
#             user_sessions[user_id]['name'] = name_match.group(1).title()
    
#     # Add user message to conversation
#     messages.append({"role": "user", "content": message.content})
    
#     # Get LLM response
#     response = order_request(messages)
    
#     # Add assistant response to conversation
#     messages.append({"role": "assistant", "content": response})
    
#     # Check if order is confirmed and send notifications
#     if "ORDER CONFIRMED" in response or "Total: ₦" in response:
#         # Extract total amount from response
#         total_line = [line for line in response.split('\n') if 'Total:' in line]
#         total_amount = 0.0
        
#         if total_line:
#             try:
#                 amount_str = re.search(r'₦?[\d,]+\.?\d*', total_line[0])
#                 if amount_str:
#                     total_amount = float(amount_str.group().replace('₦', '').replace(',', ''))
#             except:
#                 total_amount = 0.0
        
#         # Send notifications with CUSTOMER INFORMATION
#         if total_amount > 0:
#             user_info = user_sessions[user_id]
            
#             # Format manager notification
#             manager_message = f"""
# 🚨 **NEW CUSTOMER ORDER** 🚨

# 👤 **Customer Details:**
# Name: {user_info['name'] or 'Not provided'}
# Phone: {user_info['phone'] or 'Not provided'}
# Address: {user_info['address'] or 'Not provided'}

# 💰 **Order Total:** ₦{total_amount:,.2f}

# 📦 **Order Details:**
# {response}

# 📍 **Action Required:** 
# Please prepare this order and contact customer for delivery!
# """
            
#             # Send SMS to manager
#             notification_manager.send_sms(manager_message)
            
#             # Send WhatsApp to manager  
#             notification_manager.send_whatsapp(manager_message)
            
#             # Send Email to manager
#             owner_emails = os.environ.get("OWNER_EMAILS", "").split(',')
#             if owner_emails and owner_emails[0]:
#                 email_subject = f"New Order - ₦{total_amount:,.2f} - {user_info['name'] or 'Customer'}"
#                 notification_manager.send_emails(owner_emails, manager_message)

#     # Send response to user
#     await cl.Message(content=response).send()

# @fastapi_app.post("/whatsapp/webhook")
# async def whatsapp_webhook(request: Request):
#     form = await request.form()
#     from_number = form.get("From")
#     message_body = form.get("Body")
#     print(f"Received WhatsApp message from {from_number}: {message_body}")

#     # Store customer phone from WhatsApp
#     user_id = from_number
#     if user_id not in user_sessions:
#         user_sessions[user_id] = {
#             'phone': from_number,
#             'address': None,
#             'name': None
#         }
#     else:
#         user_sessions[user_id]['phone'] = from_number

#     # Wrap form data into a Chainlit Message object
#     user_message = cl.Message(content=message_body)

#     # Call your existing Chainlit handler
#     await main(user_message)

#     # Reply to customer
#     resp = MessagingResponse()
#     resp.message("Thank you! Your order is being processed. We'll contact you shortly.")
#     return str(resp)