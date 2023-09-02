from tgbot import dp
from req_analyse import check_changes
import asyncio
import os

# WEBHOOK
import logging
from aiogram.utils.executor import start_webhook

# webhook
WEBHOOK_HOST = 'https://fibot.info:8443'  # Укажите URL-адрес вашего сервера (https://your.domain)
WEBHOOK_PATH = f"/bot"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver
WEBAPP_HOST = '91.239.232.129'  # Укажите IP
WEBAPP_PORT = 8443  # Укажите порт

async def on_startup(dp):
    await dp.bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(check_changes())


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    import ssl
    current_dir = os.path.dirname(os.path.abspath(__file__))
    certfile_path = os.path.join(current_dir, 'cert.pem')
    keyfile_path = os.path.join(current_dir, 'privkey.pem')
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        ssl_context=context
    )

# POLLING
"""
from aiogram import executor


async def on_startup(dp):
    asyncio.create_task(check_changes())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

"""
