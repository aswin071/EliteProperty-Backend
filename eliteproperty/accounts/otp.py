from twilio.rest import Client
from django.conf import settings
from django.core.mail import EmailMessage
from .models import Account
import random


def send_otp(username, email):
   
    otp_no = str(random.randint(1000, 9999))
    
    user = Account.objects.get(email=email)
    user.otp = otp_no
    user.save()
    message = f"""Hi {username},

Thank you for registering with EliteProperty.

Please use the following OTP code to verify your email id: {otp_no}
"""
    email_subject = "Verify your email address"
    email_to = email
    email_instance = EmailMessage(email_subject, message, to=[email_to])
    email_instance.send()