import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from config import BOT_TOKEN

telegram_bot_token = BOT_TOKEN

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello there. Provide any English word and I will give you a bunch "
                                                   "of information about it.")


# obtain the information of the word provided and format before presenting.
def get_word_info(update, context):
    # get the word info
    word_info = ['test', 'test2', 'test3', 'test4', 'test5', 'test6']

    # If the user provides an invalid English word, return the custom response from get_info() and exit the function
    if word_info.__class__ is str:
        update.message.reply_text(word_info)
        return

    # format the data into a string
    message = f"Word: may work or not"

    update.message.reply_text(message)

# run the start function when the user invokes the /start command 
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message 
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_word_info))
updater.start_polling()

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
