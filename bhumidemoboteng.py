import logging
import os
import datetime
from imagedectection import *
from telegram import Update, constants, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ConversationHandler , ContextTypes, CommandHandler, MessageHandler, filters
from airtable import *
from barcode import get_barcode_from_url
ADDREFRIGERANT, REFRIGERANTAMOUNT, CREATEREFRIGERANT,BARCODE, APPLIANCEPHOTO, SIGNATUREPHOTO = range(6)
chatContext = {}
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def addRefrigerant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    context.user_data['userId'] = get_first_record_username(baseId, api, tableProviders, username)[2]
    keyboard = [
        [InlineKeyboardButton('R22', callback_data='R22')],
        [InlineKeyboardButton('R134A', callback_data='R134A')],
        [InlineKeyboardButton('R32', callback_data='R32')],
        [InlineKeyboardButton('R410A', callback_data='R410A')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('<b>Please choose your refrigerant:</b>', parse_mode='HTML', reply_markup=reply_markup)
    return REFRIGERANTAMOUNT


async def RefrigerantAmount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #gets the refrigerant type from the previous step
    query = update.callback_query
    await query.answer()
    context.user_data['refrigerant_type'] = query.data
    await context.bot.send_message(chat_id=update.effective_chat.id, text="How much refrigerant in KG do you have in the cyclinder?")
    return CREATEREFRIGERANT


async def CreateRefrigerant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """refrigerantaccount."""
    context.user_data['amount'] = update.message.text
    print("Userdata amount is:  " + context.user_data['amount'])
    result = insert_new_refrigerant(baseId, api, tableManagement, providerId= context.user_data['userId'], refrigerantType= context.user_data['refrigerant_type'], amountKG= int(context.user_data['amount']))
    print(result)
    context.chat_data['refrigerant_id'] = result['fields']['RefrigerantID']
    await update.message.reply_text('<b>Amount noted.\n'
                                    'Please upload a photo of the barcode</b>',
                                    parse_mode='HTML')
    return BARCODE

async def storeBarcode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo."""
    
    photo_file = await update.message.photo[-1].get_file()
    # Correctly store the file_id of the uploaded photo for later use
    context.user_data['barcode_photo'] = photo_file.file_id  # Preserve this line
    barcode = get_barcode_from_url(photo_file.file_path)
    if barcode == False:
        await update.message.reply_text('<b>Your image does not appear to be a barcode, please try again!</b>', parse_mode='HTML'
        )
        return BARCODE
    print("Barcode is: " + barcode)
    result = update_refrigerant(baseId, api, tableManagement, context.chat_data['refrigerant_id'], {"BarcodePhoto": [{"url": photo_file.file_path}],"BarcodeText": barcode})
    print(result)
    await update.message.reply_text('<b>Photo uploaded successfully.Next upload a photo of the appliance</b>', parse_mode='HTML'
        )
    return APPLIANCEPHOTO


async def storeAppliancePhoto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo."""
    photo_file = await update.message.photo[-1].get_file()
    # Correctly store the file_id of the uploaded photo for later use
    context.user_data['appliance_photo'] = photo_file.file_id  # Preserve this line
    result = update_refrigerant(baseId, api, tableManagement, context.chat_data['refrigerant_id'], {"AppliancePhoto": [{"url": photo_file.file_path}]})
    print(result)
    await update.message.reply_text('<b>Photo uploaded successfully.Next upload a photo of the signature</b>', parse_mode='HTML'
    )
    return SIGNATUREPHOTO

async def storeSignaturePhoto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo."""
    photo_file = await update.message.photo[-1].get_file()
    # Correctly store the file_id of the uploaded photo for later use
    context.user_data['signature_photo'] = photo_file.file_id  # Preserve this line
    result = update_refrigerant(baseId, api, tableManagement, context.chat_data['refrigerant_id'], {"SignaturePhoto": [{"url": photo_file.file_path}]})
    print(result)
    await update.message.reply_text('<b>Photo uploaded successfully.Thank you. Refrigerant successfully created. Use the /addrefrigerant command to add another refrigerant.</b>', parse_mode='HTML'
    )
    return ConversationHandler.END



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Bhumi Recycler Bot! Use the menu to see all commands this bot can do.")



async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    decline_keyboard = KeyboardButton(text="Decline", request_location=True)
    contact_keyboard = KeyboardButton(text="Send Contact Info", request_contact=True)
    custom_keyboard = [[  contact_keyboard, decline_keyboard]] 
    regist_reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    username = update.message.from_user.username
    id = update.message.from_user.id
    print(update.message)
    x = get_first_record_username(baseId, api, tableProviders, id)
    print("x:")
    print(x)
    if x[0] == 0:
        insert_provider_telegram_username(baseId, api, tableProviders, str(id), update.message.from_user.first_name +"" + update.message.from_user.last_name,update.message.from_user.language_code)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are now registered in our database. Please provide your contact number by clicking the button below.", reply_markup=regist_reply_markup)
    elif x[1] == False:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are already registered in our database. Please provide your phone number by clicking the button below.", reply_markup=regist_reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are already registered in our database.")
   
    

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("contact handler")
    print(update.message)
    phone_number = update.message.contact.phone_number
    id = update.message.from_user.id
    update_provider_telegram_phoneNumber(baseId, api, tableProviders, update.message.from_user.id, phone_number)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Phone Number Updated", parse_mode='HTML')


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Sorry, I didn't understand that command. Please open the menu and use one of the commands.</b>", parse_mode='HTML')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to talk to you again soon.')
    return ConversationHandler.END

async def switchtopic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bye! Hope to talk to you again soon.')
    await update.message.reply_text('Bye2! Hope to talk to you again soon.')

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ["Telegram_Bot_TOKEN"]).build()
    

    application.add_handler(MessageHandler(filters.CONTACT, contact))
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    switch_handler = CommandHandler('switchtopic', switchtopic)
    application.add_handler(switch_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addrefrigerant', addRefrigerant)],
        states={
            REFRIGERANTAMOUNT: [CallbackQueryHandler(RefrigerantAmount)],
            CREATEREFRIGERANT: [MessageHandler(filters.TEXT, CreateRefrigerant)],
            BARCODE: [MessageHandler(filters.PHOTO, storeBarcode),
                      CallbackQueryHandler(storeBarcode)],
            APPLIANCEPHOTO: [MessageHandler(filters.PHOTO, storeAppliancePhoto)],
            SIGNATUREPHOTO: [MessageHandler(filters.PHOTO, storeSignaturePhoto)]
                            },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    register_handler = CommandHandler('register', register)
    application.add_handler(register_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.run_polling()