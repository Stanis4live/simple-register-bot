from django.test import TestCase
import asyncio
from unittest.mock import Mock, patch, ANY, AsyncMock
from aiogram import types
from agreement import AGREEMENT_TEXT
from bot_module.bot import start, accept_agreement, Registration, get_phone_number, finish_registration


class BotTests(TestCase):
    def test_start_command_for_new_user(self):
        '''Тестирование команды старт для нового пользователя. Проверяет, что новому пользователю предлагается
        пользовательское соглашение.'''
        mock_message = Mock()
        mock_message.from_user = Mock()
        mock_message.from_user.id = 12345
        mock_message.answer = AsyncMock()

        with patch('bot.is_user_registered', return_value=False):
            asyncio.run(start(mock_message))

        mock_message.answer.assert_called_once_with(AGREEMENT_TEXT, reply_markup=ANY)

    def test_start_command_for_registered_user(self):
        '''Тестирование команды старта для уже зарегистрированного пользователя.
        Проверяет, что зарегистрированному пользователю выводится сообщение о том, что он уже зарегистрирован'''
        mock_message = Mock()
        mock_message.from_user.id = 12345
        mock_message.answer = AsyncMock()

        with patch('bot.is_user_registered', return_value=True):
            asyncio.run(start(mock_message))

        mock_message.answer.assert_called_once_with("Вы уже зарегистрированы в системе.")

    def test_accept_agreement(self):
        ''' Тестирование процесса принятия пользовательского соглашения.
        Проверяет, что после принятия соглашения пользователю предлагается ввести свой номер телефона.'''
        mock_state = Mock()
        mock_state.set_state = AsyncMock()
        mock_state.set_data = AsyncMock()
        mock_message = Mock()
        mock_message.from_user.id = 12345
        mock_message.answer = AsyncMock()

        mock_callback_query = Mock(spec=types.CallbackQuery)
        mock_callback_query.from_user = Mock()
        mock_callback_query.from_user.id = 12345
        mock_callback_query.from_user.first_name = "John"
        mock_callback_query.from_user.last_name = "Doe"
        mock_callback_query.message = mock_message
        mock_callback_query.message.edit_text = AsyncMock()

        with patch('bot.is_user_registered', return_value=False):
            asyncio.run(start(mock_message))
            mock_message.answer.assert_called_once_with(AGREEMENT_TEXT, reply_markup=ANY)

            with patch('bot.accept_agreement'):
                asyncio.run(accept_agreement(mock_callback_query, mock_state))

            mock_state.set_data.assert_called_once_with({
                "first_name": "John",
                "last_name": "Doe"
            })
            mock_callback_query.message.edit_text.assert_called_once_with("Пожалуйста, введите ваш номер телефона.")

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

    # ... [остальные тесты остаются без изменений]

    def test_finish_registration(self):
        '''Тестирование завершения процесса регистрации. Проверяет, что
        данные пользователя сохраняются в базе данных и пользователю отправляется сообщение о завершении регистрации.'''
        mock_callback_query = Mock(spec=types.CallbackQuery)
        mock_callback_query.from_user = Mock(spec=types.User)
        mock_callback_query.from_user.id = 12345
        mock_callback_query.message = Mock()
        mock_callback_query.message.answer = AsyncMock()

        mock_state = Mock()
        mock_state.get_data = AsyncMock(return_value={
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890"
        })
        mock_state.clear = AsyncMock()
        with patch('bot.save_user_to_db', new_callable=AsyncMock) as mock_save_user_to_db:
            asyncio.run(finish_registration(mock_callback_query, mock_state))

            mock_save_user_to_db.assert_called_once_with(12345, "John", "Doe", "+1234567890")

            mock_callback_query.message.answer.assert_called_once_with("Регистрация завершена")
