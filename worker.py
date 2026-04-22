import asyncio
from queue import get_job
from downloader import download_with_retry
from utils import safe_delete

async def worker_loop(bot):
    while True:
        job = await get_job()

        if not job:
            await asyncio.sleep(1)
            continue

        chat_id, url, context = job

        try:
            file_path = download_with_retry(url)

            if file_path:
                await context.bot.send_document(chat_id, open(file_path, "rb"))
                safe_delete(file_path)
            else:
                await context.bot.send_message(chat_id, "Download failed ❌")

        except Exception as e:
            await context.bot.send_message(chat_id, f"Error: {e}")