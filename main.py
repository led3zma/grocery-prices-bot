import logging
import os

import models
from db import Base, engine
from handlers import list_products, menu, register_products, search_products, start, help

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

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
    application.add_handler(CommandHandler('listar', list_products))
    application.add_handler(CommandHandler('registrar', register_products))
    application.add_handler(CommandHandler('buscar', search_products))

    application.run_polling()
