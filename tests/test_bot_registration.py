import sys
sys.path.append('/home/stas/PycharmProjects/itregul1/bot_module')
from django.test import TestCase
import asyncio
from unittest.mock import Mock, patch, ANY, AsyncMock
from aiogram import types
def mock_include_router(*args, **kwargs):
    pass

from unittest.mock import patch

with patch('aiogram.dispatcher.router.Router.include_router', mock_include_router):
    from bot_module.bot import Registration, get_phone_number


class BotTests(TestCase):
    def test_get_phone_number(self):
        '''Тестирование процесса получения номера телефона от пользователя.
        Проверяет, что после отправки номера телефона пользователю показывается его имя и фамилия.'''
        mock_message = Mock(spec=types.Message)
        mock_message.from_user = Mock(spec=types.User)
        mock_message.from_user.id = 12345
        mock_message.text = "+1234567890"
        mock_message.answer = AsyncMock()

        mock_state = AsyncMock()
        mock_state.set_data = AsyncMock()
        mock_state.set_state = AsyncMock()
        mock_state.get_data = AsyncMock(return_value={
            "first_name": "John",
            "last_name": "Doe"
        })
        mock_state.get_state = AsyncMock(return_value=Registration.PhoneNumber.state)

        asyncio.run(get_phone_number(mock_message, mock_state))

        mock_message.answer.assert_called_with(ANY, reply_markup=ANY)  # проверка, что был вызван метод answer



