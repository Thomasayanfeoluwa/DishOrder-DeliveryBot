# DishDelivery-OrderBot

An intelligent AI-powered Nigerian restaurant ordering system with real-time notifications and payment integration.

# 🚀 Features #

AI-Powered Ordering: Natural language processing for seamless order taking
Multi-Channel Notifications: SMS, WhatsApp, and email alerts for new orders
Secure Payments: Paystack integration for seamless payment processing
Image Display: Professional dish photos for enhanced user experience
Real-time Chat: Interactive ordering via Chainlit web interface
WhatsApp Integration: Order directly through WhatsApp messages
Session Management: Customer data tracking across conversations
Error Handling: Robust error handling and retry mechanisms

# 🏗️ Project Architecture #


System Architecture Diagram
text
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User          │    │   Chainlit       │    │   Groq LLM      │
│   Interface     │◄──►│   Application    │◄──►│   (Llama 3.3)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   WhatsApp      │    │   Session        │    │   Image         │
│   Webhook       │    │   Management     │    │   Service       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Payment       │    │   Notification   │    │   Order         │
│   Service       │    │   Manager        │    │   Processing    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Paystack      │    │   Twilio SMS/    │    │   Email         │
│   API           │    │   WhatsApp       │    │   SMTP          │
└─────────────────┘    └──────────────────┘    └─────────────────┘

# Data Flow

User Interaction → Chainlit Interface → Groq LLM Processing
Order Confirmation → Payment Link Generation → Paystack
Successful Payment → Multi-channel Notifications → Restaurant
Order Fulfillment → Customer Delivery → Completion

# 📁 Complete Project Structure

DishDelivery-OrderBot/
├── 📁 src/                          # Core application logic
│   ├── __init__.py
│   ├── notification.py              # Twilio SMS/WhatsApp & Email notifications
│   ├── loader.py                    # Groq LLM integration and API handling
│   └── prompt.py                    # AI system instructions & complete menu
├── 📁 services/                     # External service integrations
│   ├── __init__.py
│   ├── image_service.py             # Dish image management and URL mapping
│   └── payment_service.py           # Paystack payment integration
├── 📁 assets/                       # Static assets (optional)
│   └── images/                      # Local dish images (if needed)
├── app.py                           # Main Chainlit application entry point
├── chainlit.md                      # Web interface content and welcome page
├── .env                             # Environment variables (create this)
├── .env.example                     # Environment variables template
├── requirements.txt                 # Python dependencies
├── README.md                        # This file



# 🔧 Technology Stack #

Component	Technology	Purpose
Frontend	Chainlit	Interactive chat interface
Backend	Python 3.10+	Application logic
AI/LLM	Groq API (Llama 3.3 70B)	Natural language order processing
Payments	Paystack API	Secure Nigerian payment processing
Notifications	Twilio API	SMS & WhatsApp alerts
Email	SMTP (Gmail)	Email notifications to owners
Image Hosting	ImgBB	Free CDN for dish photos
Web Framework	FastAPI (via Chainlit)	HTTP server and webhooks

# 🛠️ Installation & Setup
Prerequisites
Python 3.10 or higher
Groq API account (free tier available)
Twilio account (trial account available)
Paystack account (test mode available)
Gmail account (for email notifications)

# Step 1: Clone and Setup
bash
# Clone the repository
git clone <repository-url>
cd DishDelivery-OrderBot

# Create virtual environment
python -m venv Carebot

# Activate virtual environment
# On Windows:
Carebot\Scripts\activate
# On macOS/Linux:
source Carebot/bin/activate

# Install dependencies
pip install -r requirements.txt
Step 2: Environment Configuration
Create a .env file in the root directory:

bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Twilio Configuration
TWILIO_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_VIRTUAL_NUMBER=+1234567890
TWILIO_VERIFIED_NUMBER=+2348160568999
TWILIO_WHATSAPP_NUMBER=+14155238886

# Email Configuration
EMAIL_PROVIDER_SMTP_ADDRESS=smtp.gmail.com
MY_EMAIL=your_email@gmail.com
MY_EMAIL_PASSWORD=your_app_password
OWNER_EMAILS=owner1@example.com,owner2@example.com

# Paystack Configuration
PAYSTACK_SECRET_KEY=sk_test_your_secret_key
PAYSTACK_PUBLIC_KEY=pk_test_your_public_key

# Step 3: Obtain API Keys

# Groq API Key
Visit Groq Cloud
Sign up for free account
Generate API key from dashboard
Add to .env file

# Twilio Credentials
Sign up at Twilio
Get Account SID and Auth Token from console
Purchase a phone number or use trial number
Verify your personal number for testing

# Paystack Keys
Register at Paystack
Go to Settings → API Keys & Webhooks
Copy Test Secret Key and Test Public Key

# Gmail App Password
Enable 2FA on your Gmail account
Generate App Password for "Mail"
Use this password in MY_EMAIL_PASSWORD

# Step 4: Run the Application

bash
# Start the application
chainlit run app.py

# Or with clear cache
chainlit run app.py --clear-cache

# The app will be available at: http://localhost:8000
📋 Core Components Documentation
🎯 app.py - Main Application
Purpose: Orchestrates the entire order processing workflow

# Key Functions:
@cl.on_chat_start - Initial welcome message
@cl.on_message - Main message processing handler
main() - Processes user messages and manages order flow
is_final_confirmation() - Detects complete order confirmations
extract_customer_info() - Parses customer details from conversation
WhatsApp webhook integration for messaging

# Flow Control:
User message → LLM processing → Response generation
Customer info extraction → Session storage
Order confirmation detection → Notification triggering
Payment link generation → User redirection

# 🔔 src/notification.py - Notification System
Purpose: Manages all outgoing communications to restaurant owners

# Key Methods:
__init__() - Initializes Twilio client and email settings
send_sms() - Sends SMS alerts to restaurant owners
send_whatsapp() - Sends WhatsApp business messages
send_emails() - Sends detailed email notifications
notify_owner() - Coordinates multi-channel notifications

# Features:
Error handling for failed notifications
Multi-channel redundancy
Structured message formatting
Customer detail inclusion

# 🧠 src/loader.py - AI Integration
Purpose: Handles communication with Groq LLM API

# Key Features:
order_request() - Main LLM communication function
Exponential backoff retry mechanism
Error handling for API failures
Conversation history management
Model configuration (Llama 3.3 70B)

# 📝 src/prompt.py - AI Instructions
Purpose: Contains system instructions and complete menu data

# Contents:
Complete Nigerian restaurant menu with prices
Order confirmation protocols
Customer data collection rules
Conversational style guidelines
Nigerian cultural context integration

# 🖼️ services/image_service.py - Dish Images
Purpose: Manages dish photo display and mapping

# Key Methods:
get_dish_image() - Returns image URL for specific dish
get_images_for_order() - Extracts relevant images from order text
Comprehensive dish-to-image mapping
Image Sources:
Pre-uploaded to ImgBB CDN
Professional food photography
Organized by menu categories

# 💳 services/payment_service.py - Payments
# Purpose: Handles Paystack payment integration

# Key Methods:
initiate_payment() - Generates Paystack payment links
verify_payment() - Confirms payment completion
Secure transaction handling
Webhook integration ready

# 🔌 API Integrations Details
Groq LLM API
Endpoint: https://api.groq.com/openai/v1/chat/completions

# Model: llama-3.3-70b-versatile

# Features: Fast inference, conversational AI, order calculation

# Rate Limits: Generous free tier, suitable for deployment

# Twilio API
# SMS: Programmable Messaging API
# WhatsApp: Business API via Twilio

# Features: Global delivery, delivery receipts, error handling

# Paystack API
Payment Methods: Card, Bank Transfer, USSD, Mobile Money

# Security: PCI DSS compliant, tokenization

# Features: Recurring payments, split payments, verification

# Test Mode: Full functionality without real money

# ImgBB API
Storage: Free image hosting

# CDN: Global content delivery

# Features: No compression, direct links, no watermarks

# 🎮 Usage Examples
# Web Interface Ordering
text
User: "I want Jollof Rice with Chicken and a Coke"
AI: "How you dey! Jollof Rice with Chicken (₦2,500) + Coke (₦200) = ₦2,700. 
     Is this for delivery or pickup?"

User: "Delivery to 123 Main Street, my name is John, phone 08123456789"
AI: "ORDER CONFIRMED ✅
     👤 CUSTOMER INFORMATION:
     📛 Name: John
     📞 Phone: 08123456789
     📍 Address: 123 Main Street
     
     📦 ORDER SUMMARY:
     - Jollof Rice with Chicken: ₦2,500
     - Coke: ₦200
     
     💰 TOTAL: ₦2,700
     
     Please complete payment: [Paystack Link]"
WhatsApp Ordering
text
User: "Hi, I'd like Pounded Yam and Egusi Soup for delivery"
AI: "Welcome! Pounded Yam (₦800) + Egusi Soup (₦2,500) = ₦3,300. 
     Please provide your name, phone number, and delivery address."

User: "My name is Ada, phone 08012345678, address 45 Lagos Street"
AI: "ORDER CONFIRMED ✅
     [Payment Link Sent]
     Thank you! Your order is being processed."

# 🔐 Security Features
Environment Variables: Sensitive data protection
API Key Management: Secure credential storage
Input Validation: User input sanitization
Session Isolation: User data separation
Payment Security: PCI-compliant payment processing
Error Logging: Secure error handling without data exposure

# 📊 Notification Templates
SMS to Restaurant Owner
text

# 🚨 NEW ORDER: ₦12,500
Customer: John - 08123456789
Address: 123 Main Street
Items: Jollof Rice, Chicken, Coke
Prepare immediately!
WhatsApp to Restaurant Owner
text

# 🚨 **NEW CUSTOMER ORDER** 🚨

👤 **CUSTOMER DETAILS:**
📛 Name: John
📞 Phone: 08123456789
📍 Address: 123 Main Street

💰 **ORDER TOTAL:** ₦12,500

📦 **ORDER SUMMARY:**
- Jollof Rice with Chicken: ₦2,500
- Pounded Yam: ₦800
- Egusi Soup: ₦2,500
- Coke: ₦200

📍 **ACTION REQUIRED:** 
Please prepare this order immediately!
Email to Restaurant Team
text
Subject: 🆕 NEW ORDER - ₦12,500 - John

Dear Team,

A new order has been received:

CUSTOMER INFORMATION:
Name: John
Phone: 08123456789
Address: 123 Main Street

ORDER TOTAL: ₦12,500

ORDER DETAILS:
- Jollof Rice with Chicken: ₦2,500
- Pounded Yam: ₦800
- Egusi Soup: ₦2,500
- Coke: ₦200

Please prepare this order immediately and contact the customer for delivery confirmation.

Best regards,
DishDelivery Auto-Notifier
🚀 Deployment Instructions
Local Development
bash
# Development mode with auto-reload
chainlit run app.py --port 8000 --watch
Production Deployment
Option 1: Traditional VPS
bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app

# Setup systemd service
sudo nano /etc/systemd/system/dishdelivery.service
Option 2: Docker Deployment
dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["chainlit", "run", "app.py", "--port", "8000", "--host", "0.0.0.0"]
Option 3: Cloud Platform
Railway: One-click deployment

Heroku: Container-based deployment

AWS EC2: Traditional VM deployment

Google Cloud Run: Serverless container deployment

Production Checklist
Set production environment variables

Configure custom domain with SSL

Setup Paystack webhooks for payment verification

Configure Twilio webhook URLs

Setup monitoring and logging

Configure backup procedures

Performance testing completed

🐛 Troubleshooting Guide
Common Issues and Solutions
Groq API Errors
python
# Symptom: 500 Internal Server Error
# Solution: Add retry logic and error handling
def order_request(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(...)
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return "System busy, please try again"
Twilio Authentication Failures
bash
# Symptom: Error 20003 - Authenticate
# Solution: Verify credentials
TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_auth_token_here
TWILIO_VIRTUAL_NUMBER=+1234567890  # Must be purchased number
Email Delivery Issues
bash
# Symptom: SMTP Authentication Error
# Solution: Use App Password, not regular password
MY_EMAIL=youremail@gmail.com
MY_EMAIL_PASSWORD=abcd efgh ijkl mnop  # 16-character app password
Payment Link Generation Failures
python
# Symptom: Paystack API errors
# Solution: Verify keys and amount format
amount = int(total_amount * 100)  # Convert to kobo
Logs and Debugging
Enable debug logging by adding to app.py:

python
import logging
logging.basicConfig(level=logging.DEBUG)

# 📈 Monitoring and Analytics
# Key Metrics to Track
Orders per day/hour
Average order value
Popular menu items
Payment success rate
Customer acquisition channels
Peak ordering times

# Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

# Development Setup
bash

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# 📄 License
This project is licensed under the MIT License.


# 🆘 Support
# Getting Help
Documentation: Check this README first
Issues: Create a GitHub issue for bugs
Discussions: Use GitHub discussions for questions
Email: Contact ayanfeoluwadegoke@gmail.com
