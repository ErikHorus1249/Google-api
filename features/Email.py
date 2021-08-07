from email import message
from http import server
from Google import Create_Service
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

CLIENT_SECRET_FILE = 'credentials/client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


emailmasg = "hello my friend"
mineMessage = MIMEMultipart()
mineMessage['to'] = 'tuananh1421999@gmail.com'
mineMessage['subject'] = 'Hello'
mineMessage.attach(MIMEText(emailmasg, 'plain'))
raw_string = base64.urlsafe_b64encode(mineMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)

