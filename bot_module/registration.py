import os
from aiogram import types, F
from aiogram.filters.state import State, StatesGroup
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from channels.db import database_sync_to_async
from bot_module.agreement import AGREEMENT_TEXT
from aiogram.filters import Filter
import logging
from keyboards import create_main_keyboard
from router_config import router


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itregul1.settings')

import django
django.setup()

from users.models import TelegramUser


logger = logging.getLogger(__name__)


class Registration(StatesGroup):
    '''Класс состояний для процесса регистрации.'''
    PhoneNumber = State()
    FirstName = State()
    LastName = State()
    EditingMenu = State()


class IsReg(Filter):
    '''Фильтр для проверки состояний и команды /start.'''
    key = "is_reg"

    async def __call__(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        return current_state is None and message.text != '/start'


@database_sync_to_async
def save_user_to_db(telegram_id, first_name, last_name, phone_number):
    '''Сохраняет данные пользователя в базе данных.'''
    TelegramUser.objects.create(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
    )


@database_sync_to_async
def is_user_registered(user_id: int) -> bool:
    '''Проверяет, зарегистрирован ли пользователь в базе данных.'''
    return TelegramUser.objects.filter(telegram_id=user_id).exists()


@router.message(IsReg())
async def handle_text_messages(message: types.Message):
    '''Обрабатывает текстовые сообщения от пользователей.'''
    user_id = message.from_user.id

    if await is_user_registered(user_id):
        await message.answer("Выберите услугу:", reply_markup=create_main_keyboard())
    else:
        await message.answer("Вы не зарегистрированы в системе. Чтобы начать регистрацию, отправьте команду /start.")


@router.message(Command("start"))
async def start(message: types.Message):
    print('start')
    '''Обрабатывает команду /start и начинает процесс регистрации.'''
    try:
        user_id = message.from_user.id

        if await is_user_registered(user_id):
            await message.answer("Вы уже зарегистрированы в системе.")
            await send_services_keyboard(message)
            return

        agreement_text = AGREEMENT_TEXT
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Принять", callback_data='accept_agreement')]])
        await message.answer(agreement_text, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error in start: {e}")


@router.callback_query(F.data == 'accept_agreement')
async def accept_agreement(callback_query: types.CallbackQuery, state: FSMContext):
    '''Обрабатывает подтверждение пользовательского соглашения.'''
    try:
        user_data = {
            "first_name": callback_query.from_user.first_name,
            "last_name": callback_query.from_user.last_name
        }
        await state.set_data(user_data)
        await state.set_state(Registration.PhoneNumber.state)
        await callback_query.message.edit_text("Пожалуйста, введите ваш номер телефона.")
    except Exception as e:
        await callback_query.message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        print(f"Error in accept_agreement: {e}")


@router.message(Registration.PhoneNumber)
async def get_phone_number(message: types.Message, state: FSMContext):
    '''Получает и сохраняет номер телефона пользователя.'''
    try:
        user_data = await state.get_data()
        phone_number = message.text
        user_data["phone_number"] = phone_number
        await state.set_data(user_data)

        first_name = user_data.get("first_name", "Неизвестное имя")
        last_name = user_data.get("last_name", "Неизвестная фамилия")
        await send_user_data(message, first_name, last_name)
        await state.set_state(Registration.EditingMenu.state)
    except Exception as e:
        await message.answer("Произошла ошибка при обработке вашего номера телефона. Пожалуйста, попробуйте еще раз.")
        print(f"Error in get_phone_number: {e}")


@router.message(Registration.FirstName)
async def get_first_name(message: types.Message, state: FSMContext):
    '''Получает и сохраняет имя пользователя.'''
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
    '''Получает и сохраняет фамилию пользователя.'''
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
    '''Отправляет пользователю его текущие данные.'''
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
    '''Завершает процесс регистрации, сохраняя данные пользователя в базе данных.'''
    user_data = await state.get_data()

    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    phone_number = user_data.get("phone_number", "")
    telegram_id = callback_query.from_user.id

    await save_user_to_db(telegram_id, first_name, last_name, phone_number)
    logger.info(
        f"New user registered: ID={telegram_id}, First Name={first_name}, Last Name={last_name}, Phone={phone_number}")
    await callback_query.message.answer("Регистрация завершена")

    await state.clear()


async def send_services_keyboard(message: types.Message):
    '''Отправляет клавиатуру с кнопкой "Услуги".'''
    await message.answer("Выберите действие:", reply_markup=main_keyboard)

