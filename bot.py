import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from database import Database # Pastikan file database.py kamu sudah benar

# --- HANDLER START ---
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = context.bot_data['db']
    user = update.effective_user
    player = db.get_player(user.id)

    if player:
        text = (
            f"🎣 *Selamat Datang Kembali, {user.first_name}!*\n\n"
            f"📊 Level: {player['level']} | 💰 Koin: {player['coins']:,}\n"
            f"🐟 Total Tangkapan: {player['total_fish']}\n\n"
            f"Gunakan /help untuk melihat semua perintah."
        )
        await update.message.reply_text(text, parse_mode='Markdown')
    else:
        text = (
            "🎣 *Selamat Datang di Fishing Game Bot!*\n\n"
            "Klik tombol di bawah untuk mulai!"
        )
        keyboard = [[InlineKeyboardButton("📥 Daftar Sekarang", callback_data="register")]]
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# --- HANDLER REGISTER ---
async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    db = context.bot_data['db']
    user = update.effective_user

    if db.get_player(user.id):
        await query.edit_message_text("✅ Kamu sudah terdaftar!")
        return

    success = db.register_player(user.id, user.username, user.full_name)
    if success:
        await query.edit_message_text("✅ *Pendaftaran Berhasil!* Gunakan /fishing untuk mulai.", parse_mode='Markdown')
    else:
        await query.edit_message_text("❌ Gagal mendaftar.")

# --- MAIN BLOCK ---
if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN") 
    
    # 1. Bangun aplikasinya
    application = ApplicationBuilder().token(token).build()

    # 2. Masukkan database ke bot_data agar bisa diakses handler
    application.bot_data['db'] = Database()

    # 3. Hubungkan perintah
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CallbackQueryHandler(register_handler, pattern="^register$"))

    # 4. Nyalakan!
    print("--- MESIN BOT MULAI DINYALAKAN ---")
    application.run_polling()
