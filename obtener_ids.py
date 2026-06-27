from telegram.ext import Application, MessageHandler, filters

async def get_id(update, context):
    print(f"Nombre: {update.effective_user.first_name} | ID: {update.effective_user.id}")

import asyncio
async def run():
    app = Application.builder().token("8296395464:AAHx7_EYV0FqFSfbEv4XLdzk-KUl7sT4vcs").build()
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

