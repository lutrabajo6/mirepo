import os
from telegram.ext import Application, MessageHandler, filters

async def get_id(update, context):
    print(f"Nombre: {update.effective_user.first_name} | ID: {update.effective_user.id}")

import asyncio

# SEGURIDAD: el token ya NO se escribe en este archivo.
# Configura la variable de entorno TELEGRAM_BOT_TOKEN antes de ejecutar este script.
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def run():
    if not TOKEN:
        raise RuntimeError(
            "La variable de entorno TELEGRAM_BOT_TOKEN no está definida. "
            "Configúrala antes de ejecutar obtener_ids.py."
        )
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, get_id))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass

asyncio.run(run())

