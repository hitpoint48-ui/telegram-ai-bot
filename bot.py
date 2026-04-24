import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Логи (очень помогает в Render)
logging.basicConfig(level=logging.INFO)

# Берём ключи ИЗ ENV (Render)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка (чтобы сразу видеть ошибку)
if not TELEGRAM_TOKEN:
    raise Exception("TELEGRAM_TOKEN is missing in Render ENV")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY is missing in Render ENV")

client = OpenAI(api_key=OPENAI_API_KEY)

# Обработка сообщений
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Отвечай кратко и по-человечески."},
                {"role": "user", "content": user_text}
            ]
        )

        await update.message.reply_text(response.choices[0].message.content)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Запуск бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot started...")
app.run_polling()
