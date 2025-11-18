# services/payment_service.py
import requests
import os
import json
from typing import Dict, Optional

class PaystackService:
    def __init__(self):
        self.secret_key = os.environ.get("PAYSTACK_SECRET_KEY")
        self.public_key = os.environ.get("PAYSTACK_PUBLIC_KEY")
        self.base_url = "https://api.paystack.co"
        
        if not self.secret_key:
            raise ValueError("PAYSTACK_SECRET_KEY environment variable is required")
    
    def initiate_payment(self, email: str, amount: float, reference: str, metadata: Dict = None) -> Dict:
        """
        Initialize Paystack payment and return payment authorization URL
        """
        url = f"{self.base_url}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        # Paystack amounts are in kobo (1 NGN = 100 kobo)
        amount_in_kobo = int(amount * 100)
        
        payload = {
            "email": email,
            "amount": amount_in_kobo,
            "reference": reference,
            "currency": "NGN",
            "metadata": metadata or {},
            "channels": ["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer"]
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get('status'):
                return {
                    "status": True,
                    "message": response_data.get('message', 'Payment initialized successfully'),
                    "data": response_data.get('data', {})
                }
            else:
                return {
                    "status": False,
                    "message": response_data.get('message', 'Failed to initialize payment'),
                    "data": {}
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": False,
                "message": f"Network error: {str(e)}",
                "data": {}
            }
        except Exception as e:
            return {
                "status": False,
                "message": f"Unexpected error: {str(e)}",
                "data": {}
            }
    
    def verify_payment(self, reference: str) -> Dict:
        """
        Verify Paystack payment status using transaction reference
        """
        url = f"{self.base_url}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get('status'):
                transaction_data = response_data.get('data', {})
                
                # Check if payment was successful
                if transaction_data.get('status') == 'success':
                    return {
                        "status": True,
                        "message": "Payment verified successfully",
                        "data": transaction_data
                    }
                else:
                    return {
                        "status": False,
                        "message": f"Payment not successful. Status: {transaction_data.get('status')}",
                        "data": transaction_data
                    }
            else:
                return {
                    "status": False,
                    "message": response_data.get('message', 'Failed to verify payment'),
                    "data": {}
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": False,
                "message": f"Network error: {str(e)}",
                "data": {}
            }
        except Exception as e:
            return {
                "status": False,
                "message": f"Unexpected error: {str(e)}",
                "data": {}
            }
    
    def create_transfer_recipient(self, name: str, account_number: str, bank_code: str) -> Dict:
        """
        Create transfer recipient for disbursements (if needed for refunds)
        """
        url = f"{self.base_url}/transferrecipient"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "type": "nuban",
            "name": name,
            "account_number": account_number,
            "bank_code": bank_code,
            "currency": "NGN"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return response.json()