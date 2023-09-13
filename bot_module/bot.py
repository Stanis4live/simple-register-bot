from aiogram import Bot, Dispatcher, types
from decouple import config
import os
import asyncio
import logging
from router_config import router


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
from registration import *


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
