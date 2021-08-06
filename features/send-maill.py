import smtplib
import os
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
FILE_ATTACHMENT = './media/safety.doc'

def send(client_add,content_file):
    # init email 
    msg = EmailMessage()
    msg['Subject'] = "Nice to meet U"

    msg['From'] = EMAIL_ADDRESS
    msg['To'] = client_add
    msg.set_content('You are the fucking asshole!')

    # read file 
    with open(FILE_ATTACHMENT,'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
