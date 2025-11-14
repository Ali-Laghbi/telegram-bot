from telegram import Update
from telegram.ext import ContextTypes
from ..config import ADMIN_IDS
from ..db import AsyncSessionLocal

def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("ليس لديك صلاحية لاستخدام هذا الأمر.")
            return
        return await func(update, context)
    return wrapper

@admin_only
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with AsyncSessionLocal() as session:
        count = (await session.execute("SELECT COUNT(*) FROM users")).scalar()
    await update.message.reply_text(f"📊 عدد المستخدمين: {count}")
