import telegram
from telegram.ext import Updater, MessageHandler, filters
from telegram.ext import CommandHandler
from dictionary import get_info
import queue
from config import BOT_TOKEN

updater = Updater(BOT_TOKEN, use_context=True, update_queue=queue.Queue())
dispatcher = updater.dispatcher


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Hello there. Provide any English word and I will give you a bunch "
                                                   "of information about it.")


# obtain the information of the word provided and format before presenting.
def get_word_info(update, context):
    # get the word info
    word_info = get_info(update.message.text)

    # If the user provides an invalid English word, return the custom response from get_info() and exit the function
    if word_info.__class__ is str:
        update.message.reply_text(word_info)
        return

    # get the word the user provided
    word = word_info['word']

    # get the origin of the word
    origin = word_info['origin']
    meanings = '\n'

    synonyms = ''
    definition = ''
    example = ''
    antonyms = ''

    # a word may have several meanings. We'll use this counter to track each of the meanings provided from the response
    meaning_counter = 1

    for word_meaning in word_info['meanings']:
        meanings += 'Meaning ' + str(meaning_counter) + ':\n'

        for word_definition in word_meaning['definitions']:
            # extract the each of the definitions of the word
            definition = word_definition['definition']

            # extract each example for the respective definition
            if 'example' in word_definition:
                example = word_definition['example']

            # extract the collection of synonyms for the word based on the definition
            for word_synonym in word_definition['synonyms']:
                synonyms += word_synonym + ', '

            # extract the antonyms of the word based on the definition
            for word_antonym in word_definition['antonyms']:
                antonyms += word_antonym + ', '

        meanings += 'Definition: ' + definition + '\n\n'
        meanings += 'Example: ' + example + '\n\n'
        meanings += 'Synonym: ' + synonyms + '\n\n'
        meanings += 'Antonym: ' + antonyms + '\n\n\n'

        meaning_counter += 1

    # format the data into a string
    message = f"Word: {word}\n\nOrigin: {origin}\n{meanings}"

    update.message.reply_text(message)

# run the start function when the user invokes the /start command 
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message 
# that is not a command.
dispatcher.add_handler(MessageHandler(filters.text, get_word_info))
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
