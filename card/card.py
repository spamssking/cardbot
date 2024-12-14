import logging
import requests
import pandas as pd
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, filters, ContextTypes
import random
import urllib.parse
import time


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

token = '7815620289:AAHQfLKzAJlwcSAWvpnadv5C-JJNY7CTFUI'
WAITING_FOR_REPLY = 1

def fetch_username(token):
    global user_info  # Declare global here, before using `user_info`
    global username
    
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)
    logger.info(f"API Response: {response.text}")  # Log the raw response for debugging

    data = response.json()
    username
    if data.get('ok') and data.get('result'):
        for update in data['result']:
            if 'message' in update:
                chat = update['message']['chat']
                chat_id = chat.get('id')
                username = chat.get('username')

                return username
        return username
    return username

birthday_cards = {
    "Premium": {
        "url": "https://paystack.com/buy/premium-card-tptqic"
    },
    "Basic": {
        "url": "https://Paystack.shop/kard-design-birthday-card"
    }
}

polaroid_cards = {
    "Premium": {
        "url": "https://paystack.com/buy/premium-card-jozdyv"
    },
    "Basic": {
        "url": "https://paystack.shop/kard-design"
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    name = update.message.from_user.first_name
    await update.message.reply_text(
    f"Hey {name},\n"
    "Would you like to get a /Birthday card or /Polaroid Photo Card"
)
    #time.sleep(10)
    #await update.message.reply_text("Okay. Thats nice")
    return WAITING_FOR_REPLY
    
    
async def Birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Okay. Thats nice")
    keyboard = [
        [InlineKeyboardButton("Premium", callback_data="brand_Premium")],
        [InlineKeyboardButton("Basic", callback_data="brand_Basic")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select Premium for a customized card or Basic to browse through the catalog:", reply_markup=reply_markup)

# Polaroid command
async def Polaroid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Okay. Thats nice")
    
    keyboard = [
        [InlineKeyboardButton("Premium", callback_data="brand_Premium")],
        [InlineKeyboardButton("Basic", callback_data="brand_Basic")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select Premium for a customized card or Basic to browse through the catalog:", reply_markup=reply_markup)

# Handle brand selection
async def handle_brand_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Get the brand name from callback data (e.g., brand_Premium)
    brand = query.data.split("_")[1]

    # Determine which category the brand belongs to (birthday_cards or polaroid_cards)
    brand_info = None
    if brand in birthday_cards:
        brand_info = birthday_cards[brand]
    elif brand in polaroid_cards:
        brand_info = polaroid_cards[brand]

    # If the brand is found in either dictionary, send a button that links to the website
    if brand_info:
        keyboard = [
            [InlineKeyboardButton("Visit Website", url=brand_info['url'])],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Here is the {brand} card. Click below to visit the website:",
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text("Sorry, this brand is not available.")
        
async def inactivity_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    await update.message.reply_text(f"Hey {username}, you seem to be inactive. Please let me know if you'd like to continue with a /Birthday card or /Polaroid Photo Card.")
    return WAITING_FOR_REPLY


async def main():
    application = ApplicationBuilder().token(token).build()
    
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_FOR_REPLY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, inactivity_timeout)
            ]
        },
        fallbacks=[]
    )

    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('Birthday', Birthday))
    application.add_handler(CommandHandler('Polaroid', Polaroid))
    #application.add_handler(CommandHandler('pay', pay))
    application.add_handler(CallbackQueryHandler(handle_brand_selection, pattern=r"^brand_"))
    #application.add_handler(CallbackQueryHandler(handle_product_purchase, pattern=r"^buy_"))
    #application.add_handler(PreCheckoutQueryHandler(precheckout_callback)) 
    #application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    #application.add_handler(CommandHandler('visits', visits))  # To show visit counts

    # Start the bot using the internal event loop
    await application.run_polling()

# If running as a script, run the bot without using asyncio.run()
if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()  # Apply nest_asyncio

    # Directly start the bot by calling `main()` without asyncio.run()
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())