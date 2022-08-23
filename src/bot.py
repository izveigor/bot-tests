import os

from telegram import Bot

bot = Bot(os.environ.get("TELEGRAM_TOKEN"))
