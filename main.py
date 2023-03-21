import handlers
from telegram.ext import (
    CommandHandler, CallbackContext,
    ConversationHandler, MessageHandler,
    filters, Updater, CallbackQueryHandler, ApplicationBuilder
)
from config import TOKEN

app = ApplicationBuilder().token(TOKEN).build()
print(app)

def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={
            handlers.CHOOSING: [
                MessageHandler(
                    filters.ALL, handlers.choose
                )
            ],
            handlers.CLASS_STATE: [
                CallbackQueryHandler(handlers.classer)
            ],
            handlers.SME_DETAILS: [
                MessageHandler(
                    filters.ALL, handlers.business_details
                )
            ],
            handlers.SME_CAT: [
                CallbackQueryHandler(handlers.business_details_update)
            ],
            handlers.ADD_PRODUCTS: [
                CallbackQueryHandler(handlers.add_product),
                MessageHandler(filters.ALL, handlers.product_info)
            ],
            handlers.CHOOSE_PREF: [
                CallbackQueryHandler(handlers.customer_pref)
            ],
            handlers.SHOW_STOCKS: [
                CallbackQueryHandler(handlers.show_products)
            ],
            handlers.POST_VIEW_PRODUCTS: [
                CallbackQueryHandler(handlers.post_view_products)
            ]
        },
        fallbacks=[CommandHandler('cancel', handlers.cancel)],
        allow_reentry=True
    )
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()