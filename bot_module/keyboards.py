from aiogram import types


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