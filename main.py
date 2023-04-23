import handlers
from telegram.ext import (
    CommandHandler, ConversationHandler, MessageHandler,
    filters, CallbackQueryHandler, ApplicationBuilder
)
from config import BOT_TOKEN

app = ApplicationBuilder().token(BOT_TOKEN).build()

def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={
            handlers.BOT_SCHEDULER: [
                CallbackQueryHandler(handlers.bot_scheduler),
                MessageHandler(filters.ALL, handlers.bot_scheduler_set)
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
