from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.first_name