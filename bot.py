#!/usr/bin/python3


import logging
import requests
import json

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from conf import BOT_TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def get_shortened_url(url):
    if "http" not in str(url):
        url = "https://" + url
    api_response = json.loads(requests.get(f"https://ulvis.net/API/write/get?url={url}").text)
    short_url = api_response.get('data', "Error").get('url')
    return(short_url)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /shorten <URL> to shorten an URL")

async def shorten_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shortens the provided URL."""
    user_submitted_url = context.args[0]
    await update.message.reply_text(f"Shortening {user_submitted_url}...")
    shortened_url = get_shortened_url(user_submitted_url)
    await update.message.reply_text(f"Here's your shortened URL: {shortened_url}")
    
def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("shorten", shorten_url))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()