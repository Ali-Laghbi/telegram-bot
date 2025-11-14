import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..db import AsyncSessionLocal, StoredMessage, User
from ..config import MEDIA_DIR

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    async with AsyncSessionLocal() as session:
        obj = await session.get(User, user.id)
        if not obj:
            obj = User(id=user.id, username=user.username, first_name=user.first_name)
            session.add(obj)
        else:
            obj.username = user.username
            obj.first_name = user.first_name
        await session.commit()

    keyboard = [
        [InlineKeyboardButton("🔥 الميزات", callback_data="menu_features")],
        [InlineKeyboardButton("📤 أرسل رسالة", callback_data="menu_send")],
    ]
    await update.message.reply_text(
        f"أهلًا {user.first_name or ''} 👋\nمرحبًا في البوت.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("استخدم /start أو أرسل رسالة.")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    async with AsyncSessionLocal() as session:
        msg = StoredMessage(user_id=user.id, content=text)
        session.add(msg)
        await session.commit()

    await update.message.reply_text("تم حفظ رسالتك بنجاح ✓")
