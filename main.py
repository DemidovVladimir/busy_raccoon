import handlers
from telegram.ext import (
    CommandHandler, ConversationHandler, MessageHandler,
    filters, CallbackQueryHandler, ApplicationBuilder, Updater
)
import queue
from config import BOT_TOKEN, MODE, PORT, HEROKU_APP_NAME, HEROKU_WEBHOOK_URL
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if MODE == 'polling':
    def run(app):
        app.run_polling()
elif MODE == 'webhook':
    def run(updater):
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=BOT_TOKEN, webhook_url=HEROKU_WEBHOOK_URL)
        updater.bot.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            secret_token='SomeTokenGeneratedByOwnerBot',
            webhook_url=HEROKU_WEBHOOK_URL
        )
else:
    logger.error('NO MODE SPECIFIED')
    sys.exit(1)

if __name__ == '__main__':
    logger.info('Starting bot v1...')
    logger.info(HEROKU_WEBHOOK_URL)
    logger.info(HEROKU_APP_NAME)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    updater = Updater(app, update_queue=queue.Queue())

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
    app.add_error_handler(handlers.error)

    if MODE == 'polling':
        run(app)
    elif MODE == 'webhook':
        run(updater)
    else:
        sys.exit(1)
        