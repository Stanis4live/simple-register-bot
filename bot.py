from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
import os
import asyncio
from channels.db import database_sync_to_async


TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itregul1.settings')

import django
django.setup()

from users.models import User

router = Router()


@database_sync_to_async
def is_user_registered(user_id: int) -> bool:
    return User.objects.filter(telegram_id=user_id).exists()


@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id

    if await is_user_registered(user_id):
        await message.answer("Вы уже зарегистрированы в системе.")
        return

    agreement_text = """Я даю свое согласие
ООО «ИТ-Регул» на обработку моих персональных данных. Согласие касается фамилии, имени, номера сотового телефона,
а также сведений использования данного бота.
Я даю согласие на хранение всех вышеназванных данных на электронных носителях. Также данным согласием я разрешаю сбор
моих персональных данных, их хранение, систематизацию, обновление, использование (в т.ч. передачу третьим лицам для
обмена информацией), а также осуществление любых иных действий, предусмотренных действующим законом Российской Федерации.
До моего сведения доведено, что ООО «ИТ-Регул» гарантирует обработку моих персональных данных в соответствии с
действующим законодательством Российской Федерации. Срок действия данного согласия не ограничен. Согласие может быть
отозвано в любой момент по моему письменному заявлению.
Подтверждаю, что, давая согласие, я действую без принуждения, по собственной воле и в своих интересах.

    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Принять", callback_data='accept_agreement')]])
    await message.answer(agreement_text, reply_markup=keyboard)


@router.callback_query()
async def accept_agreement(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Спасибо за принятие пользовательского соглашения...")


dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






