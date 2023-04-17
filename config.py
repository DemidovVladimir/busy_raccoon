import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_SECRET = os.getenv('API_SECRET')
API_KEY = os.getenv('API_KEY')
FAUNA_KEY = os.getenv('FAUNA_KEY')
CLOUD_NAME = os.getenv('CLOUD_NAME')
TEQUILA_API = os.getenv('TEQUILA_API')
TEQUILA_API_KEY = os.getenv('TEQUILA_API_KEY')
MY_EMAIL = os.getenv('MY_EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')