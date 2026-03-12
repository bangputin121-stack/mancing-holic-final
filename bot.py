import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Import file yang baru kita buat
from database import Database

# Setup Logging
logging.basicConfig(level=logging.INFO)

# --- HANDLERS ---
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data['db']
    user = update.effective_user
    player = db.get_player(user.id)

    if player:
        await update.message.reply_text(f"🎣 Halo {user.first_name}! Kamu sudah terdaftar.")
    else:
        keyboard = [[InlineKeyboardButton("📥 Daftar Sekarang", callback_data="register")]]
        await update.message.reply_text("Selamat datang! Klik daftar:", reply_markup=InlineKeyboardMarkup(keyboard))

async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    db = context.bot_data['db']
    user = update.effective_user
    
    if db.register_player(user.id, user.username, user.full_name):
        await query.edit_message_text("✅ Pendaftaran Berhasil!")
    else:
        await query.edit_message_text("kamu sudah terdaftar!")

if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    
    application = ApplicationBuilder().token(token).build()
    
    # Inisialisasi Database ke dalam bot
    application.bot_data['db'] = Database()

    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CallbackQueryHandler(register_handler, pattern="^register$"))

    print("--- MESIN BOT AKTIF ---")
    application.run_polling()
