import handlers
from telegram.ext import (
    CommandHandler, CallbackContext,
    ConversationHandler, MessageHandler,
    filters, Updater, CallbackQueryHandler, ApplicationBuilder
)
from config import BOT_TOKEN

app = ApplicationBuilder().token(BOT_TOKEN).build()

def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={
            handlers.BOT_START: [
                CallbackQueryHandler(handlers.bot_start)
            ],
            handlers.BOT_CONFIG: [
                CallbackQueryHandler(handlers.bot_config),
                MessageHandler(filters.ALL, handlers.bot_reply)
            ]
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel)],
        allow_reentry=True
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("unset", handlers.unset))
    app.run_polling()

if __name__ == '__main__':
    main()
