import json
import threading
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

TOKEN = "7408316421:AAFqxaB39EtKCepdAO-8X-4uJMna92OfecM"
bot = Bot(token=TOKEN)
app = Flask(__name__)

REQUIRED_CHANNELS = [
    ("@ffprivatesensi", "STAR NODE-1"),
    ("@webmakerhu", "STAR NODE-2"),
    ("@botclubhu", "STAR NODE-3")
]

# 🟢 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif_url = "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif"
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation=gif_url)

    keyboard = [
        [InlineKeyboardButton(name, url=f"https://t.me/{channel[1:]}")]
        for channel, name in REQUIRED_CHANNELS
    ]
    keyboard.append([InlineKeyboardButton("✅ I Have Joined", callback_data="check_join")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚨 ACCESS REQUIRED 🚨\n\n"
        "⚠️ Join All STAR NODES To Unlock The Bot Features!\n\n"
        "👨‍💻 Developer Node: @teamtoxic009",
        reply_markup=reply_markup
    )

# ✅ Callback for button
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # 🔴 Real check later
    user_joined = True

    if user_joined:
        await query.edit_message_text("✅ ACCESS GRANTED. Use /register to continue.")
    else:
        await query.edit_message_text("🚫 ACCESS DENIED. Join all STAR NODES!")

# ✅ Telegram Bot Application
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(check_join))

# ✅ Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

# ✅ Root check
@app.route('/')
def home():
    return "Star Bot is Running ✅"

# ✅ Start Flask + Bot
def run():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run).start()
