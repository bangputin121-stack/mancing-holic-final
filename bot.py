import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Gunakan try-except agar jika database error, bot tidak langsung CRASH
try:
    from database import Database
    HAS_DB = True
except ImportError:
    HAS_DB = False
    print("PERINGATAN: File database.py bermasalah atau kelas Database tidak ditemukan!")

from handlers.start import start_handler, register_handler

# Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    
    if not token:
        print("ERROR: BOT_TOKEN kosong!")
    else:
        # 1. Bangun Aplikasi
        application = ApplicationBuilder().token(token).build()

        # 2. Inisialisasi Database hanya jika filenya benar
        if HAS_DB:
            try:
                application.bot_data['db'] = Database()
            except Exception as e:
                print(f"Gagal inisialisasi Database: {e}")

        # 3. Daftarkan Perintah Utama
        application.add_handler(CommandHandler('start', start_handler))
        application.add_handler(CallbackQueryHandler(register_handler, pattern="^register$"))

        # 4. Nyalakan
        print("--- MESIN BOT SUDAH AKTIF ---")
        application.run_polling()
