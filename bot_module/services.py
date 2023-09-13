from aiogram import types, F
from keyboards import services_keyboard, subservices_1_keyboard, subservices_2_keyboard
from router_config import router


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


