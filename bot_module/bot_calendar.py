import datetime
from router_config import router
from aiogram import types, F
from keyboards import create_calendar, CalendarCallbackData, ScheduleData, create_schedule_keyboard, DayData, RU_MONTHS, \
    create_services_keyboard


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
async def schedule_hour_selected(query: types.CallbackQuery, callback_data: ScheduleData):
    hour = callback_data.hour
    # Здесь вы можете сохранить выбранное время и перейти к следующему этапу
    # await query.message.edit_text(f"Вы выбрали {hour}:00. Подтвердите запись или вернитесь назад.",
    #                               reply_markup=confirmation_keyboard)


@router.callback_query(DayData.filter(F.action == "day"))
async def calendar_day_selected(query: types.CallbackQuery, callback_data: CalendarCallbackData):
    day = callback_data.day
    month = callback_data.month
    year = callback_data.year
    # Здесь вы можете сохранить выбранную дату и перейти к расписанию
    markup = create_schedule_keyboard(day)
    await query.message.edit_text(f"Выбрано {day} {RU_MONTHS[month]} {year} года. Выберите время:", reply_markup=markup)


@router.callback_query(F.data == "back_to_calendar")
async def back_to_calendar_callback(query: types.CallbackQuery):
    current_date = datetime.date.today()
    markup = create_calendar(current_date.year, current_date.month)
    await query.message.edit_text("Выберите дату:", reply_markup=markup)


