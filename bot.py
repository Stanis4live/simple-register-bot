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


TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itregul1.settings')

import django
django.setup()

from users.models import User

router = Router()


class Registration(StatesGroup):
    PhoneNumber = State()
    FirstName = State()
    LastName = State()
    EditingMenu = State()


@database_sync_to_async
def is_user_registered(user_id: int) -> bool:
    return User.objects.filter(telegram_id=user_id).exists()


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
    first_name = user_data.get("first_name", "Неизвестное имя")
    current_state = await state.get_state()

    if current_state == Registration.LastName.state:
        last_name = message.text
        user_data["last_name"] = last_name
        await state.set_data(user_data)

        await send_user_data(message, first_name, last_name)
        await state.set_state(Registration.EditingMenu.state)


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


@router.callback_query(F.data == 'accept_first_name')
async def accept_first_name_handler(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    first_name = user_data.get("first_name", "Неизвестное имя")
    last_name = user_data.get("last_name", "Неизвестная фамилия")

    await send_user_data(callback_query, first_name, last_name)


dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






