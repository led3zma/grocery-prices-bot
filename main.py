import logging
import os

import models
import conversation_states
from db import Base, engine
from handlers import end_conversation_to_menu, list_products, menu, register_product_name, register_product_price, register_product_store, register_products, search_products, start, help

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

load_dotenv()

Base.metadata.create_all(bind=engine)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).build()

    # TODO: #2 Refactor the inclusion of command handlers using `add_handlers`
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler('registrar', register_products)],
        states={
            conversation_states.REGISTER_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               register_product_name)
            ],
            conversation_states.REGISTER_PRICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               register_product_price)
            ],
            conversation_states.REGISTER_STORE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               register_product_store)
            ]
        },
        fallbacks=[CommandHandler("cancel", end_conversation_to_menu)]
    ))
    application.add_handler(CommandHandler('listar', list_products))
    application.add_handler(CommandHandler('buscar', search_products))

    application.run_polling()
