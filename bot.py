import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Setup Logging agar kita bisa lihat apa yang terjadi di Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Mancing Mania Berhasil Hidup!")

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Gagal: BOT_TOKEN tidak ditemukan!")
        return

    # Inisialisasi aplikasi dengan cara yang lebih aman untuk Python 3.13
    application = ApplicationBuilder().token(token).build()
    
    # Tambahkan satu perintah tes saja
    application.add_handler(CommandHandler("start", start))

    print("--- MESIN BOT SEDANG COBA DINYALAKAN ---")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Menjaga bot tetap hidup
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
