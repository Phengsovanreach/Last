import asyncio
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN, WEBHOOK_URL, PORT
from bot import start, handle_message
from worker import worker_loop

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# ---------------- BOT INIT ----------------
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ---------------- WEBHOOK ----------------
@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"ok": True}

@app.get("/")
async def home():
    return {"status": "V12 STABLE RUNNING"}

# ---------------- STARTUP ----------------
@app.on_event("startup")
async def startup():
    await bot_app.initialize()

    if WEBHOOK_URL:
        await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    asyncio.create_task(worker_loop(bot_app))

# ---------------- RUN ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)