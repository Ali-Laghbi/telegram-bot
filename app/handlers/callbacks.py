from telegram import Update
from telegram.ext import ContextTypes

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d == "menu_features":
        await q.edit_message_text("ميزات البوت:\n- لوحات تفاعلية\n- حفظ رسائل المستخدم\n- يعمل 24 ساعة 🔥")
    elif d == "menu_send":
        await q.edit_message_text("أرسل الآن أي نص وسيتم حفظه ✓")
    else:
        await q.edit_message_text("تم الضغط.")
