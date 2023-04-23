from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater
from config import BOT_TOKEN, PORT, HEROKU_WEBHOOK_URL

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

def handle_message(update, context):
    message = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

if __name__ == '__main__':
    updater = Updater(token=BOT_TOKEN, use_context=True)
    updater.bot.setWebhook(HEROKU_WEBHOOK_URL, allowed_updates=['message'])
    bot = telegram.Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher(bot, None)
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    app.run(debug=True, host='0.0.0.0', port=PORT)

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
