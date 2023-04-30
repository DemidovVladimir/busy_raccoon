import os
# import dotenv

# dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
MODE = os.getenv('MODE')
TEQUILA_API = os.getenv('TEQUILA_API')
TEQUILA_API_KEY = os.getenv('TEQUILA_API_KEY')
HEROKU_WEBHOOK_URL = os.getenv('HEROKU_WEBHOOK_URL')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
PORT = int(os.getenv('PORT', 8443))