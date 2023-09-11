from aiogram import Bot, Dispatcher, types, F
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
import os
import asyncio
from channels.db import database_sync_to_async
from agreement import AGREEMENT_TEXT
from aiogram.filters import Filter


TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itregul1.settings')

import django
django.setup()

from users.models import TelegramUser

router = Router()


class Registration(StatesGroup):
    PhoneNumber = State()
    FirstName = State()
    LastName = State()
    EditingMenu = State()


class IsReg(Filter):
    key = "is_reg"

    async def __call__(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        return current_state is None and message.text != '/start'


@database_sync_to_async
def save_user_to_db(telegram_id, first_name, last_name, phone_number):
    TelegramUser.objects.create(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
    )


@database_sync_to_async
def is_user_registered(user_id: int) -> bool:
    return TelegramUser.objects.filter(telegram_id=user_id).exists()


@router.message(IsReg())
async def handle_text_messages(message: types.Message):
    user_id = message.from_user.id

    if await is_user_registered(user_id):
        await message.answer("Вы уже зарегистрированы в системе.")
    else:
        await message.answer("Вы не зарегистрированы в системе. Чтобы начать регистрацию, отправьте команду /start.")


@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id

    if await is_user_registered(user_id):
        await message.answer("Вы уже зарегистрированы в системе.")
        return

    agreement_text = AGREEMENT_TEXT
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Принять", callback_data='accept_agreement')]])
    await message.answer(agreement_text, reply_markup=keyboard)


@router.callback_query(F.data == 'accept_agreement')
async def accept_agreement(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Registration.PhoneNumber.state)
    await callback_query.message.edit_text("Пожалуйста, введите ваш номер телефона.")


@router.message(Registration.PhoneNumber)
async def get_phone_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()

    if current_state == Registration.PhoneNumber.state:
        phone_number = message.text
        await state.set_data({"phone_number": phone_number})
        await state.set_state(Registration.FirstName.state)
        await message.answer("Пожалуйста, введите ваше имя.")


@router.message(Registration.FirstName)
async def get_first_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    first_name = message.text
    user_data["first_name"] = first_name
    await state.set_data(user_data)

    current_state = await state.get_state()

    if current_state == Registration.FirstName.state and not user_data.get("last_name"):
        await state.set_state(Registration.LastName.state)
        await message.answer("Пожалуйста, введите вашу фамилию.")
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Принять", callback_data='accept_first_name')],
                [InlineKeyboardButton(text="Изменить", callback_data='edit_first_name')]
            ]
        )
        await message.answer(f"Имя - {first_name}", reply_markup=keyboard)


@router.message(Registration.LastName)
async def get_last_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    previous_last_name = user_data.get("last_name")

    last_name = message.text
    user_data["last_name"] = last_name
    await state.set_data(user_data)

    first_name = user_data.get("first_name", "Неизвестное имя")

    if not previous_last_name:
        await send_user_data(message, first_name, last_name)
        await state.set_state(Registration.EditingMenu.state)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Принять", callback_data='accept_last_name')],
                [InlineKeyboardButton(text="Изменить", callback_data='edit_last_name')]
            ]
        )
        await message.answer(f"Фамилия - {last_name}", reply_markup=keyboard)


async def send_user_data(message_or_query, first_name, last_name):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Изменить имя", callback_data='edit_first_name')],
            [InlineKeyboardButton(text="Изменить фамилию", callback_data='edit_last_name')],
            [InlineKeyboardButton(text="Завершить редактирование", callback_data='finish_registration')]
        ]
    )

    text = f"Ваша учётная запись:\nИмя - {first_name}\nФамилия - {last_name}"

    if isinstance(message_or_query, types.CallbackQuery):
        await message_or_query.message.edit_text(text, reply_markup=keyboard)
    else:
        await message_or_query.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == 'edit_first_name')
async def edit_first_name_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Registration.FirstName.state)
    await callback_query.message.edit_text("Введите новое имя.")


@router.callback_query(F.data == 'edit_last_name')
async def edit_last_name_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Registration.LastName.state)
    await callback_query.message.edit_text("Введите новую фамилию.")


@router.callback_query(F.data == 'accept_first_name')
async def accept_first_name_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    first_name = user_data.get("first_name", "Неизвестное имя")
    last_name = user_data.get("last_name", "Неизвестная фамилия")

    await send_user_data(callback_query, first_name, last_name)


@router.callback_query(F.data == 'accept_last_name')
async def accept_last_name_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    first_name = user_data.get("first_name", "Неизвестное имя")
    last_name = user_data.get("last_name", "Неизвестная фамилия")

    await send_user_data(callback_query, first_name, last_name)


@router.callback_query(F.data == 'finish_registration')
async def finish_registration(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    phone_number = user_data.get("phone_number", "")
    telegram_id = callback_query.from_user.id

    # Записываем пользователя в базу данных
    await save_user_to_db(telegram_id, first_name, last_name, phone_number)

    # Отправляем сообщение пользователю
    await callback_query.message.answer("Регистрация завершена")

    await state.clear()


dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






