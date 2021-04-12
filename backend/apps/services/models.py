from django.db import models
# Create your models here.


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