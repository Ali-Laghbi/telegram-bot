import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("ضع TELEGRAM_BOT_TOKEN في متغيرات البيئة")

DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data.db"))
MEDIA_DIR = os.getenv("MEDIA_DIR", str(BASE_DIR / "media"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ADMIN_IDS = {int(i) for i in os.getenv("ADMIN_IDS", "").split(",") if i}
