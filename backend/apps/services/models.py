from django.db import models
# Create your models here.
from backend.apps.accounts.models import CompanyUser, Employee


class Region(models.Model):
    name = models.CharField("Наименование", max_length=50)

    class Meta:
        verbose_name = "Область"
        verbose_name_plural = "Области"

    def __str__(self):
        return f"{self.name}"


class District(models.Model):
    name = models.CharField("Наименование", max_length=50)
    region = models.ForeignKey(
        Region, verbose_name="Регион", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"

    def __str__(self):
        return f"{self.name}"


class Locality(models.Model):
    name = models.CharField("Наименование", max_length=50)
    district = models.ForeignKey(
        District, verbose_name="Район", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенные пункты"

    def __str__(self):
        return f"{self.name}"


#Заказ на сервис
class Order(models.Model):
    company = models.ForeignKey(
        CompanyUser,
        verbose_name="Компания исполнитель",
        on_delete=models.SET_NULL,
        null=True
    ) # Исполнитель
    performer_employee = models.ForeignKey(
        Employee,
        verbose_name="Сотрудник исполнитель",
        on_delete=models.SET_NULL,
        null=True
    )
    email = models.EmailField()
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=10)
    locality = models.ForeignKey(
        Locality,
        verbose_name="Город назначения",
        on_delete=models.SET_NULL,
        null=True
    )
    address = models.CharField("Улица и Номер дома", max_length=255)
    date = models.DateTimeField(verbose_name="Дата и время бронирования")


    created = models.DateTimeField(verbose_name="Время создания заказа", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Время обновления бро", auto_now=True)

