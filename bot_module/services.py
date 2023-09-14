from aiogram import types, F
from keyboards import create_services_keyboard, subservices_1_keyboard, subservices_2_keyboard, create_calendar
from router_config import router
import datetime
from aiogram.fsm.context import FSMContext


@router.callback_query(F.data == "show_services")
async def show_services(query: types.CallbackQuery):
    await query.message.edit_text("Выберите услугу:", reply_markup=create_services_keyboard())


@router.callback_query(F.data == "service_1")
async def show_subservices_1(query: types.CallbackQuery):
    await query.message.edit_text("Выберите подуслугу для Услуги 1:", reply_markup=subservices_1_keyboard)


@router.callback_query(F.data == "service_2")
async def show_subservices_2(query: types.CallbackQuery):
    await query.message.edit_text("Выберите подуслугу для Услуги 2:", reply_markup=subservices_2_keyboard)


@router.callback_query(F.data == "subservice_1_1")
async def select_subservice_1_1(query: types.CallbackQuery, state: FSMContext):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await state.set_data({"service": "Подуслуга 1.1"})
    markup = create_calendar(current_year, current_month)
    await query.message.edit_text("Выберите дату:", reply_markup=markup)


@router.callback_query(F.data == "subservice_1_2")
async def select_subservice_1_2(query: types.CallbackQuery, state: FSMContext):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await state.set_data({"service": "Подуслуга 1.2"})
    markup = create_calendar(current_year, current_month)
    await query.message.edit_text("Выберите дату:", reply_markup=markup)


@router.callback_query(F.data == "subservice_2_1")
async def select_subservice_2_1(query: types.CallbackQuery, state: FSMContext):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await state.set_data({"service": "Подуслуга 2.1"})
    markup = create_calendar(current_year, current_month)
    await query.message.edit_text("Выберите дату:", reply_markup=markup)


@router.callback_query(F.data == "subservice_2_2")
async def select_subservice_2_2(query: types.CallbackQuery, state: FSMContext):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await state.set_data({"service": "Подуслуга 2.2"})
    markup = create_calendar(current_year, current_month)
    await query.message.edit_text("Выберите дату:", reply_markup=markup)


@router.callback_query(F.data == "confirm_record")
async def confirm_record(query: types.CallbackQuery):
    await query.message.answer("Запись подтверждена!")
    await query.message.answer("Выберите услугу:", reply_markup=create_services_keyboard())