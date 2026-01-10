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

# Data Flow
User Interaction → Streamlit Interface → Groq LLM Processing
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
├── 📁 images/                       # Images folder
│   └── images                       # Local dish images 
├── app.py                           # Main Chainlit application entry point
├── chainlit.md                      # Web interface content and welcome page
|__ dashboard.py                     # Streamlit Web interface
├── .env                             # Environment variables (create this)
├── .env.example                     # Environment variables template
├── requirements.txt                 # Python dependencies
├── README.md                        # This file



# 🔧 Technology Stack #

Component	Technology	Purpose
Frontend	Streamlit	Interactive chat interface
Backend	Python 3.10+	Application logic
AI/LLM	Groq API (Llama 3.3 70B)	Natural language order processing
Payments	Paystack API	Secure Nigerian payment processing
Notifications	Twilio API	SMS & WhatsApp alerts
Email	SMTP (Gmail)	Email notifications to owners
Image Hosting	ImgBB	Free CDN for dish photos

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
conda create -m Carebot python=3.10 -y

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
streamlit run dashboard.py

# The app will be available at: [http://localhost:8000](https://dishorder-deliverybot-de2jdgxfjjvy5rkeevgz23.streamlit.app/)
📋 Core Components Documentation
🎯 dashboard.py
Purpose: Orchestrates the entire order processing workflow


Issues: Create a GitHub issue for bugs
Discussions: Use GitHub discussions for questions
Email: Contact ayanfeoluwadegoke@gmail.com




![WhatsApp Image 2025-11-20 at 12 52 20_8aa6140d](https://github.com/user-attachments/assets/421c66e2-f3f4-4ba1-b62b-8354e045cbee)

![WhatsApp Image 2025-11-20 at 12 52 20_7dbe052c](https://github.com/user-attachments/assets/371384b6-798f-46ea-b2ba-e8ae7d9adad8)

<img width="1142" height="614" alt="Screenshot (122)" src="https://github.com/user-attachments/assets/82e030fe-2893-491b-abdb-2f9611916ea1" />






