import datetime
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import calendar


class CalendarCallbackData(CallbackData, prefix='calendar'):
    action: str
    year: int
    month: int


class DayData(CallbackData, prefix='day'):
    action: str
    year: int
    month: int
    day: int


class ScheduleData(CallbackData, prefix='schedule'):
    action: str
    hour: int


RU_MONTHS = [
    "", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]


# Клавиатура для главного меню
services_button = types.InlineKeyboardButton(text="Услуги", callback_data="show_services")
main_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[services_button]])

# Клавиатура для меню услуг
service1_button = types.InlineKeyboardButton(text="Услуга 1", callback_data="service_1")
service2_button = types.InlineKeyboardButton(text="Услуга 2", callback_data="service_2")
services_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[service1_button], [service2_button]])

# Клавиатуры для подуслуг
subservice1_1_button = types.InlineKeyboardButton(text="Подуслуга 1.1", callback_data="subservice_1_1")
subservice1_2_button = types.InlineKeyboardButton(text="Подуслуга 1.2", callback_data="subservice_1_2")
subservices_1_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[subservice1_1_button], [subservice1_2_button]])

subservice2_1_button = types.InlineKeyboardButton(text="Подуслуга 2.1", callback_data="subservice_2_1")
subservice2_2_button = types.InlineKeyboardButton(text="Подуслуга 2.2", callback_data="subservice_2_2")
subservices_2_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[subservice2_1_button], [subservice2_2_button]])


def create_calendar(year, month):
    month_year_button = InlineKeyboardButton(text=f"{RU_MONTHS[month]} {year}", callback_data="ignore")

    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    week_days_buttons = [InlineKeyboardButton(text=day, callback_data="ignore") for day in week_days]

    month_days = calendar.monthcalendar(year, month)
    days_buttons = []
    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                # row.append(InlineKeyboardButton(text=str(day), callback_data=f"calendar-day-{day}"))
                day_data = DayData(action="day", year=year, month=month, day=day).pack()
                row.append(InlineKeyboardButton(text=str(day), callback_data=day_data))
        days_buttons.append(row)

    # Кнопки навигации
    current_date = datetime.date.today()
    if year == current_date.year and month == current_date.month:
        prev_button = InlineKeyboardButton(text=" ", callback_data="ignore")
    else:
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        prev_data = CalendarCallbackData(action="prev", year=prev_year, month=prev_month).pack()
        prev_button = InlineKeyboardButton(text="<", callback_data=prev_data)

    back_button = InlineKeyboardButton(text="Назад", callback_data="calendar-back")
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    next_data = CalendarCallbackData(action="next", year=next_year, month=next_month).pack()
    next_button = InlineKeyboardButton(text=">", callback_data=next_data)

    calendar_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [month_year_button],
        week_days_buttons,
        *days_buttons,
        [prev_button, back_button, next_button]
    ])

    return calendar_keyboard


def create_schedule_keyboard(selected_date):
    hours = list(range(9, 18))
    schedule_buttons = []

    for hour in hours:
        time_range = f"{hour}:00 - {hour + 1}:00"
        hour_data = ScheduleData(action="record", hour=hour).pack()
        button = InlineKeyboardButton(text=time_range, callback_data=hour_data)
        schedule_buttons.append([button])

    back_button = InlineKeyboardButton(text="Назад", callback_data="back_to_calendar")
    schedule_buttons.append([back_button])

    return InlineKeyboardMarkup(inline_keyboard=schedule_buttons)
