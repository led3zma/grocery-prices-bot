from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

MENU = '*Opciones*\n/listar\n/registrar\n/buscar'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    await menu(update, context)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, MENU, parse_mode=ParseMode.MARKDOWN)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu(update, context)
