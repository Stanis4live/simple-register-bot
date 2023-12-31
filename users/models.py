from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.first_name