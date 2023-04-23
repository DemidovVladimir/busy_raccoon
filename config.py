import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
TEQUILA_API = os.getenv('TEQUILA_API')
TEQUILA_API_KEY = os.getenv('TEQUILA_API_KEY')
HEROKU_WEBHOOK_URL = os.getenv('HEROKU_WEBHOOK_URL')
PORT = int(os.getenv('PORT', 5000))