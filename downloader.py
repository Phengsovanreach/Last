import yt_dlp
import time
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_with_retry(url, retries=3):
    for i in range(retries):
        try:
            ydl_opts = {
                "format": "best",
                "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
                "quiet": True,
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        except Exception as e:
            print(f"Retry {i+1} failed: {e}")
            time.sleep(2)

    return None