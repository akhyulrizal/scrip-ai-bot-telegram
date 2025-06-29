import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


TELEGRAM_TOKEN = "isi dengan token bot" # isi dengan token dari bot
OPENROUTER_API_KEY = "isi dengan api ai" # isi dengan api dari open router
OPENROUTER_MODEL = "openrouter/auto"  

logging.basicConfig(level=logging.INFO)

async def ai_reply(message: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://t.me/your_bot_username",  # optional, bisa disesuaikan
        "X-Title": "TelegramBot"
    }
    data = {
    "model": OPENROUTER_MODEL,
    "messages": [{"role": "user", "content": message}],
    "max_tokens": 500  #  batas token 
}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"❌ Gagal: {response.status_code} - {response.text}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya bot AI Siap Membantu Pertanyaan Anda, Silahkan Kirimkan Pertanyaan anda")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    ai_response = await ai_reply(user_message)
    await update.message.reply_text(ai_response)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot Telegram OpenRouter sedang berjalan...")
    app.run_polling()
