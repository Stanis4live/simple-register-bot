from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название услуги")

    def __str__(self):
        return self.name


class SubService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="subservices", verbose_name="Услуга")
    name = models.CharField(max_length=255, verbose_name="Название подуслуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey('users.TelegramUser', on_delete=models.CASCADE, verbose_name="Пользователь")
    subservice = models.ForeignKey(SubService, on_delete=models.CASCADE, verbose_name="Подуслуга")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")

    def __str__(self):
        return f"{self.user} - {self.subservice.name} - {self.date} {self.time}"
