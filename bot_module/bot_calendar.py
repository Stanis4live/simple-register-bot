import datetime
from router_config import router
from aiogram import types, F
from keyboards import create_calendar, CalendarCallbackData, ScheduleData, create_schedule_keyboard, DayData, RU_MONTHS, \
    create_services_keyboard, confirmation_keyboard
from aiogram.fsm.context import FSMContext


@router.callback_query(CalendarCallbackData.filter(F.action == "prev"))
async def calendar_prev(query: types.CallbackQuery, callback_data: CalendarCallbackData):
    month = callback_data.month
    year = callback_data.year
    markup = create_calendar(int(year), int(month))
    await query.message.edit_text("Выберите дату:", reply_markup=markup)


@router.callback_query(CalendarCallbackData.filter(F.action == "next"))
async def calendar_next(query: types.CallbackQuery, callback_data: CalendarCallbackData):
    month = callback_data.month
    year = callback_data.year
    markup = create_calendar(int(year), int(month))
    await query.message.edit_text("Выберите дату:", reply_markup=markup)


@router.callback_query(F.data == "back_to_services")
async def back_to_services(query: types.CallbackQuery):
    await query.message.edit_text("Выберите услугу:", reply_markup=create_services_keyboard())


@router.callback_query(ScheduleData.filter(F.action == "record"))
async def schedule_hour_selected(query: types.CallbackQuery, callback_data: ScheduleData, state: FSMContext):
    hour = callback_data.hour
    await state.update_data(time=f"{hour}:00")
    user_data = await state.get_data()
    service_name = user_data.get("service")
    selected_date = user_data.get("date")
    selected_time = user_data.get("time")
    await query.message.edit_text(
        f"Подтвердите запись:\n"
        f"Услуга - {service_name}\n"
        f"Дата - {selected_date}\n"
        f"Время - {selected_time}\n"
        f"Стоимость: ХХХХ р.",
        reply_markup=confirmation_keyboard()
    )


@router.callback_query(DayData.filter(F.action == "day"))
async def calendar_day_selected(query: types.CallbackQuery, callback_data: CalendarCallbackData, state: FSMContext):
    day = callback_data.day
    month = callback_data.month
    year = callback_data.year
    await state.update_data(date=f"{day} {RU_MONTHS[month]} {year} года")
    markup = create_schedule_keyboard(day)
    await query.message.edit_text(f"Выбрано {day} {RU_MONTHS[month]} {year} года. Выберите время:", reply_markup=markup)


@router.callback_query(F.data == "back_to_calendar")
async def back_to_calendar_callback(query: types.CallbackQuery):
    current_date = datetime.date.today()
    markup = create_calendar(current_date.year, current_date.month)
    await query.message.edit_text("Выберите дату:", reply_markup=markup)


