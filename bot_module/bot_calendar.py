from router_config import router
from aiogram import types, F
from keyboards import create_calendar, CalendarCallbackData, ScheduleData, create_schedule_keyboard, DayData


@router.callback_query(F.data == 'calendar')
# @router.message(F.text.startswith('calendar'))
async def debug_callback(query: types.CallbackQuery):
    print(f"Received callback data: {type(query.data)}")


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


@router.callback_query(ScheduleData.filter(F.action == "record"))
async def schedule_hour_selected(query: types.CallbackQuery, callback_data: ScheduleData):
    hour = callback_data.hour
    # Здесь вы можете сохранить выбранное время и перейти к следующему этапу
    # await query.message.edit_text(f"Вы выбрали {hour}:00. Подтвердите запись или вернитесь назад.",
    #                               reply_markup=confirmation_keyboard)


@router.callback_query(DayData.filter(F.action == "day"))
async def calendar_day_selected(query: types.CallbackQuery, callback_data: CalendarCallbackData):
    day = callback_data.day
    # Здесь вы можете сохранить выбранную дату и перейти к расписанию
    markup = create_schedule_keyboard(day)
    await query.message.edit_text(f"Выбрано {day} число. Выберите время:", reply_markup=markup)




# from aiogram import types
# from keyboards import create_calendar
# from router_config import router
#
# @router.message(Command("calendar"))
# async def send_calendar(message: types.Message):
#     markup = create_calendar(2023, 9)
#     await message.answer("Выберите дату:", reply_markup=markup)

# Здесь вы также можете добавить обработчики для callback-запросов, чтобы обрабатывать выбор даты и навигацию по месяцам.
