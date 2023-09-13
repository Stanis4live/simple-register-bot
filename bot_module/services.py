from aiogram import Router, types, F


router = Router()

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


# Обработчики для каждой кнопки
@router.callback_query(F.data == "show_services")
async def show_services(query: types.CallbackQuery):
    print('Here')
    await query.message.edit_text("Выберите услугу:", reply_markup=services_keyboard)


@router.callback_query(F.data == "service_1")
async def show_subservices_1(query: types.CallbackQuery):
    await query.message.edit_text("Выберите подуслугу для Услуги 1:", reply_markup=subservices_1_keyboard)


@router.callback_query(F.data == "service_2")
async def show_subservices_2(query: types.CallbackQuery):
    await query.message.edit_text("Выберите подуслугу для Услуги 2:", reply_markup=subservices_2_keyboard)

# ... (добавьте обработчики для подуслуг, если необходимо выполнить какие-либо действия при их выборе)


