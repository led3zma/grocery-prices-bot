from enum import Enum

import conversation_states

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

MENU = '*Opciones*\n/listar\n/registrar\n/buscar'
NAVIGATION_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('Prev', callback_data='1'),
        InlineKeyboardButton('Next', callback_data='2')
    ]
])
RESPONSE_MENU = ReplyKeyboardMarkup(
    [['1', '2', '3']],
    one_time_keyboard=True,
    input_field_placeholder='Select one'
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    await menu(update, context)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, MENU, parse_mode=ParseMode.MARKDOWN)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu(update, context)


async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, '*Listing...(WIP)*', parse_mode=ParseMode.MARKDOWN)


async def register_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(update.effective_chat.id, '*Introduce la descripción del producto...(WIP)*', parse_mode=ParseMode.MARKDOWN)
    return conversation_states.REGISTER_NAME


async def register_product_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['new_product_name'] = update.message.text.upper()
    await update.message.reply_text('Ingresa el precio para el producto...')
    return conversation_states.REGISTER_PRICE


async def register_product_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['new_product_price'] = update.message.text.upper()
    await update.message.reply_text('¿En qué tienda viste este producto a este precio?')
    return conversation_states.REGISTER_STORE


async def register_product_store(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['new_product_store'] = update.message.text.upper()
    data = '\n'.join(
        [f'{key} - {value}' for key, value in context.user_data.items()
         if key in ['new_product_name', 'new_product_price', 'new_product_store']]
    )
    del context.user_data['new_product_name']
    del context.user_data['new_product_price']
    del context.user_data['new_product_store']
    await update.message.reply_text(f'Guardado!\n{data}')
    return ConversationHandler.END


async def search_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, '*Introduce el producto a buscar...(WIP)*', parse_mode=ParseMode.MARKDOWN)
    return conversation_states.SEARCH_NAME


async def search_product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('*Listando...*', parse_mode=ParseMode.MARKDOWN, reply_markup=NAVIGATION_MENU)
    await update.message.reply_text('*Selecciona uno...*', parse_mode=ParseMode.MARKDOWN, reply_markup=RESPONSE_MENU)
    return conversation_states.SEARCH_DETAILS


async def get_product_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('*Detalles (WIP)...*', parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def end_conversation_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu(update, context)
    return ConversationHandler.END
