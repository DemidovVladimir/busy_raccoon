import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TEQUILA_API = os.getenv('TEQUILA_API')
TEQUILA_API_KEY = os.getenv('TEQUILA_API_KEY')