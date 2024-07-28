import logging
import os

from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from airtable import get_first_record_username, table, baseId, api, insert_provider_telegram_username

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Bhumi Recycler Bot! Use the menu to see all commands this bot can do.")


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    print(update.message)
    if get_first_record_username(baseId, api, table, username) == 0:
        insert_provider_telegram_username(baseId, api, table, username, update.message.from_user.first_name +"" + update.message.from_user.last_name,update.message.from_user.language_code)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are now registered in our database.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are already registered in our database.")
   
    



async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Sorry, I didn't understand that command. Please open the menu and use one of the commands.</b>", parse_mode='HTML')


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ["Telegram_Bot_TOKEN"]).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    register_handler = CommandHandler('register', register)
    application.add_handler(register_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.run_polling()