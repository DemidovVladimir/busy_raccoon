import os
import requests
from flask import Flask

app = Flask(__name__)


@app.route('/')
def get_info():

    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format('file')

    response = requests.get(url)

# return a custom response if an invalid word is provided
    if response.status_code == 404:
        error_response = 'We are not able to provide any information about your word. Please confirm that the word is ' \
                         'spelled correctly or try the search again at a later time.'
        return error_response

    data = response.json()[0]

    print(data)
    return data


get_info()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

# import handlers
# from telegram.ext import (
#     CommandHandler, ConversationHandler, MessageHandler,
#     filters, CallbackQueryHandler, ApplicationBuilder, Updater
# )
# from config import BOT_TOKEN

# def main():
#     # app = ApplicationBuilder().token(BOT_TOKEN).build()
#     updater = Updater(token=BOT_TOKEN, use_context=True)#
    
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', handlers.start)],
#         states={
#             handlers.BOT_SCHEDULER: [
#                 CallbackQueryHandler(handlers.bot_scheduler),
#                 MessageHandler(filters.ALL, handlers.bot_scheduler_set)
#             ],
#             handlers.BOT_CONFIG: [
#                 CallbackQueryHandler(handlers.bot_config),
#                 MessageHandler(filters.ALL, handlers.bot_reply)
#             ]
#         },
#         fallbacks=[CommandHandler('cancel', handlers.cancel)],
#         allow_reentry=True
#     )
#     updater.add_handler(conv_handler)
#     updater.add_handler(CommandHandler("unset", handlers.unset))
#     updater.add_error_handler(handlers.error)

#     updater.start_webhook()

#     updater.run_polling()

# if __name__ == '__main__':
#     main()
