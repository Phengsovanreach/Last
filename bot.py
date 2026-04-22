from telegram import Update
from telegram.ext import ContextTypes
from queue import add_job

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("V12 Bot Ready 🚀 Send link")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await add_job((update.message.chat_id, url, context))
    await update.message.reply_text("Added to queue ⏳")