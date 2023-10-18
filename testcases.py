import unittest
from unittest.mock import patch
from otp import generateotp, sendotpovermail, sendotpovermobile, validateemail, validatemobile
import os

class TestOTP(unittest.TestCase):

    def test_generateotp(self):
        otp = generateotp()
        self.assertIsInstance(otp, str)
        self.assertRegex(otp, r'^\d{6}$')

    @patch('smtplib.SMTP')
    def test_sendotpovermail(self, mock_smtp):
        email = 'test@example.com'
        otp = '123456'
        sendotpovermail(email, otp)
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once_with('jyjawale2003@gmail.com', os.getenv('SMTP_PASSWORD'))
        mock_smtp.return_value.sendmail.assert_called_once_with('jyjawale2003@gmail.com', email, f'Subject: Your OTP\n\nYour OTP is: {otp}')
        mock_smtp.return_value.quit.assert_called_once()

    @patch('twilio.rest.Client')
    def test_sendotpovermobile(self, mock_client):
        phone_number = '+919876543210'
        otp = '123456'
        sendotpovermobile(phone_number, otp)
        mock_client.assert_called_once_with(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        mock_client.return_value.messages.create.assert_called_once_with(to=phone_number, from_='+15418358453', body=f'Your OTP is: {otp}')

    def test_validateemail(self):
        valid_email = 'test@example.com'
        invalid_email = 'test@.com'
        self.assertTrue(validateemail(valid_email))
        self.assertFalse(validateemail(invalid_email))

    def test_validatemobile(self):
        valid_mobile = '9876543210'
        invalid_mobile = '123456789'
        self.assertTrue(validatemobile(valid_mobile))
        self.assertFalse(validatemobile(invalid_mobile))

if __name__ == '__main__':
    unittest.main()