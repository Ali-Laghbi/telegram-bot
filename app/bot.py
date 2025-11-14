import logging
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from .handlers import general, callbacks, admin
from .db import init_db
from .config import TELEGRAM_TOKEN, LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

async def run():
    await init_db()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", general.start))
    app.add_handler(CommandHandler("help", general.help_cmd))
    app.add_handler(CommandHandler("stats", admin.stats))

    app.add_handler(CallbackQueryHandler(callbacks.callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, general.text_handler))

    logger.info("Bot started…")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(run())
