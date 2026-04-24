import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("8644438760:AAGdf9vAA0ICvHsO1hyLh2RGPySEmwj9fPk")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Отвечай кратко, по-человечески, без формальностей."},
            {"role": "user", "content": user_text}
        ]
    )

    await update.message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
