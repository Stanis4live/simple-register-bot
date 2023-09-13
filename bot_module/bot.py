from aiogram import Bot, Dispatcher, types, F, Router
from decouple import config
import os
import asyncio
import logging
from registration import router, save_user_to_db, is_user_registered, handle_text_messages, start

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("../bot_logs.log", 'a', 'utf-8')])

logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itregul1.settings')

import django
django.setup()



dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
