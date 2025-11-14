# app/bot.py
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, func

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("Set TELEGRAM_BOT_TOKEN in .env")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Simple SQLite DB (async)
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data.db"))
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StoredMessage(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # add/update user (simple)
    async with AsyncSessionLocal() as session:
        obj = await session.get(User, user.id)
        if not obj:
            obj = User(id=user.id, username=user.username, first_name=user.first_name, language_code=user.language_code)
            session.add(obj)
        else:
            obj.username = user.username
            obj.first_name = user.first_name
            obj.language_code = user.language_code
        await session.commit()

    keyboard = [
        [InlineKeyboardButton("🔥 الميزات", callback_data="features")],
        [InlineKeyboardButton("📤 أرسل رسالة", callback_data="send")],
    ]
    await update.message.reply_text(f"أهلًا {user.first_name or ''} 👋\nمرحبًا في البوت الاحترافي.", reply_markup=InlineKeyboardMarkup(keyboard))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أوامر:\n/start\n/help\n/profile\n\nيمكنك إرسال رسالة لأرشفتها.")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"👤 @{user.username or '-'}\nID: {user.id}\nالاسم: {user.first_name or '-'}")

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "features":
        await q.edit_message_text("ميزات:\n- رسائل تفاعلية\n- حفظ بيانات\n- تشغيل 24/7")
    elif q.data == "send":
        await q.edit_message_text("أرسل الآن نصًا وسيتم حفظه.")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    async with AsyncSessionLocal() as session:
        m = StoredMessage(user_id=user.id, content=text)
        session.add(m)
        await session.commit()
    await update.message.reply_text("تم حفظ الرسالة ✅")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = update.message.photo
    if not photos:
        return
    Path(BASE_DIR / "media").mkdir(exist_ok=True)
    photo = photos[-1]
    file = await context.bot.get_file(photo.file_id)
    path = BASE_DIR / "media" / f"{photo.file_id}.jpg"
    await file.download_to_drive(str(path))
    await update.message.reply_text("تم استلام الصورة وحفظها ✅")

async def run():
    await init_db()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    logger.info("Bot started (polling)...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
