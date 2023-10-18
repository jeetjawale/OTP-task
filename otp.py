import random
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv
import os
import re

# Regular expression pattern for email validation
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

# Load environment variables from .env file
load_dotenv('.env')

# Generate a 6-digit OTP
def generateotp():
    return str(random.randint(100000, 999999))

# Send OTP over email using SMTP
def sendotpovermail(email, otp):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'jyjawale2003@gmail.com'
    smtp_password = os.getenv('SMTP_PASSWORD')  # Retrieve SMTP password from environment

    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        msg = f'Subject: {subject}\n\n{message}'
        server.sendmail(smtp_username, email, msg)
        server.quit()
        print('OTP sent successfully via email!')
    except Exception as e:
        print(f'Error sending OTP via email: {str(e)}')

# Send OTP over mobile using Twilio
def sendotpovermobile(phone_number, otp):
    twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')  # Retrieve Account SID from environment
    twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')    # Retrieve Auth Token from environment

    if twilio_account_sid is None or twilio_auth_token is None:
        print("Twilio credentials not found in the .env file.")
        return

    try:
        client = Client(twilio_account_sid, twilio_auth_token)
        message = client.messages.create(
            to=phone_number,
            from_='+15418358453',  # Replace with your Twilio phone number
            body=f'Your OTP is: {otp}'
        )
        print('OTP sent successfully via Twilio!')
    except Exception as e:
        print(f'Error sending OTP via Twilio: {str(e)}')

# Validate an email address
def validateemail(email):
    return re.match(email_pattern, email) is not None

# User input for email
email = input('Enter your email address: ')
if validateemail(email):
    otp = generateotp()
    sendotpovermail(email, otp)
else:
    print('Invalid email address!')

# Validate a mobile number
def validatemobile(mobile):
    return len(mobile) == 10 and mobile.isdigit()

# User input for mobile number (Twilio)
use_twilio = input('Do you want to send OTP via Twilio? (yes/no): ')
if use_twilio.lower() == 'yes':
    mobile = input('Enter your mobile number: ')
    if validatemobile(mobile):
        sendotpovermobile('+91' + mobile, otp)
    else:
        print('Invalid mobile number!')








