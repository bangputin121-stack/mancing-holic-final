import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

# Import database dan semua fitur dari folder handlers
from database import Database
from handlers.start import start_handler, register_handler
from handlers.fishing import fishing_handler, fishing_callback
from handlers.shop import shop_handler, shop_callback
from handlers.profile import profile_handler

# Setup Logging agar kamu bisa lihat error di Railway dengan jelas
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    # 1. Ambil Token dari tab Variables Railway
    token = os.getenv("BOT_TOKEN")
    
    if not token:
        print("ERROR: BOT_TOKEN tidak ditemukan di Variables Railway!")
    else:
        # 2. Bangun Aplikasi Bot
        application = ApplicationBuilder().token(token).build()

        # 3. Inisialisasi Database
        application.bot_data['db'] = Database()

        # 4. DAFTARKAN SEMUA PERINTAH (Handlers)
        # Perintah Dasar
        application.add_handler(CommandHandler('start', start_handler))
        application.add_handler(CommandHandler('profil', profile_handler))
        
        # Perintah Mancing
        application.add_handler(CommandHandler('fishing', fishing_handler))
        application.add_handler(CallbackQueryHandler(fishing_callback, pattern="^fish_"))
        
        # Perintah Toko/Shop
        application.add_handler(CommandHandler('shop', shop_handler))
        application.add_handler(CallbackQueryHandler(shop_callback, pattern="^buy_"))
        
        # Handler untuk pendaftaran user baru
        application.add_handler(CallbackQueryHandler(register_handler, pattern="^register$"))

        # 5. NYALAKAN BOT
        print("--- MESIN MANCING HOLIC SUDAH AKTIF ---")
        application.run_polling()
