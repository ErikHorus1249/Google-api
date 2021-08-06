from Google import Create_Service

CLIENT_FILE = 'credentials/credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/gmail.labels']

service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)


