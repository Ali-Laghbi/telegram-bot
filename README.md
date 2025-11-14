# Telegram Pro Bot — Ready to deploy (from iPad)

هذا مشروع جاهز للنشر ليجعل بوت تليجرام يعمل 24/7. يناسب منصات: Render, Railway, Fly.io أو VPS.

## خطوات سريعة للنشر من الآيباد (سهل)
1. قم بتحميل هذا الأرشيف إلى جهازك الآيباد وافتح تطبيق **Working Copy** أو **a-Shell**.
2. افتح الملف `.env` وضع `TELEGRAM_BOT_TOKEN` (لا تشارك التوكن).
3. **خيار A — نشر عبر Render (أسهل):**
   - أنشئ حساب في https://render.com
   - أنشئ Web Service جديد من GitHub أو اختر "Deploy manually" وارفع الملفات.
   - في Settings > Environment > Add Environment Variable: `TELEGRAM_BOT_TOKEN` مع قيمته.
   - اضبط build command إن لزم: `pip install -r requirements.txt`
   - اضف start command: `python app/bot.py`
   - ابدأ النشر. البوت سيعمل باستمرار (Render يدعم خدمات 24/7 في خطط مدفوعة؛ الخطة المجانية قد توقف).
   (مرجع: Render docs: https://render.com/docs/free). 

## خيار B — نشر عبر Railway (مناسب للمشاريع الصغيرة)
- سجّل في https://railway.com وقم بربط المستودع.
- أضف Environment Variable بنفس الاسم.
- نشر التطبيق كـ service (Railway يسهل الإعداد). Railway يقدم ساعات مجانية في طبقات معينة.
(مرجع: https://railway.com).

## خيار C — Fly.io (أفضل من ناحية التكلفة/التحكم لكنه يحتاج معرفة بسيطة)
- اتبع دليل Fly: https://fly.io/docs/python/
- يتطلب تثبيت CLI وبعض أوامر `fly launch`.
(مرجع: https://fly.io)

## ملاحظات مهمة
- لا تضع التوكن داخل المستودع العام.
- لعمل بوت قابل للانتشار: فكّر في استخدام قاعدة PostgreSQL بدل SQLite عند ترقية.
- إن احتجت، أجهز لك خطوة بخطوة نشر Render من الآيباد مع لقطات شاشة وأوامر مفصّلة.

---

## الملفات داخل المشروع
- app/bot.py  — الكود الرئيسي
- requirements.txt
- Dockerfile
- .env.example
