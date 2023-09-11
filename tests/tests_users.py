from django.test import TestCase
from users.models import TelegramUser


class TelegramUserModelTest(TestCase):

    def test_create_and_retrieve_user(self):
        '''Тестирование процесса создания и извлечения пользователя из базы данных.
        Проверяет, что после создания пользователя его данные можно корректно извлечь из базы данных.'''
        TelegramUser.objects.create(
            telegram_id=12345,
            first_name="John",
            last_name="Doe",
            phone_number="+1234567890"
        )

        saved_user = TelegramUser.objects.get(telegram_id=12345)
        self.assertEqual(saved_user.first_name, "John")
        self.assertEqual(saved_user.last_name, "Doe")
        self.assertEqual(saved_user.phone_number, "+1234567890")



