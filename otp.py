import smtplib
from twilio.rest import Client
import math
import random

account_sid = "AC72f0a54b0fa300722c44c88847dc4ce3"
auth_token = "7441917e6d04f7d9da7b6514fa5a41cc"

inputNO = '+15418358453'
sendNo = '+919869366902'
# send to sms
client = Client(account_sid, auth_token)
data = "0123456789"
leng = len(data)
otp = ""

for i in range(6):
    otp += data[math.floor(random.random()*leng)]

message = client.messages.create(
    body="Your 6 digit OTP is "+otp,

    from_=inputNO,
    to=sendNo
)

print(message.body)
# send to email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()  # transfer layer security
server.login('jyjawale2003@gmail.com', 'qtbwgpqawlsxwcxc')
msg = 'Your 6 digit OTP is '+str(otp)
server.sendmail('jyjawale2003@gmail.com', 'jeetjawale07@gmail.com', msg)
server.quit()