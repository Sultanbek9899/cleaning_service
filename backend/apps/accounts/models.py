from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email")

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CompanyUser(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)
    company_name = models.CharField("Название", max_length=255, db_index=True)
    logo = models.ImageField(verbose_name="Лого", upload_to='company_logo/', null=True, blank=True)
    phone_number = models.CharField(
        "Номер телефона", max_length=10, null=True)
    activity_localities = models.ManyToManyField(
        "services.Locality",
        verbose_name="Населенные пункты деятельности",

    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    first_name = None
    last_name = None
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['-created']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        unique_together = ("email", "company_name")

    def __str__(self):
        return f'{self.company_name}'


class Employee(models.Model):
    WORK_STATUS_BUSY = 'busy'
    WORK_STATUS_VACANT = 'vacant'
    WORK_STATUS_FREE_DAY = 'free_day'
    WORK_STATUS_CHOICES = (
        (WORK_STATUS_BUSY, "Занят"),
        (WORK_STATUS_FREE_DAY, "Выходной"),
        (WORK_STATUS_VACANT, "Свободен"),
    )
    full_name = models.CharField("Ф.И.О", max_length=255, )
    photo = models.ImageField("Фото сотрудника", upload_to="employees_photos", null=True, blank=True)
    work_status = models.CharField("Статус сотрудника", max_length=10, choices=WORK_STATUS_CHOICES)
    age = models.PositiveSmallIntegerField("Возраст", null=True, blank=True)
    company = models.ForeignKey(
        CompanyUser,
        verbose_name="Компания",
        related_name="employees",
        on_delete=models.SET_NULL,
        null=True,
    )
    phone_number = models.CharField("Номер телефона", max_length=10, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f'{self.full_name}'


class EventCalendar(models.Model):
    employee = models.ForeignKey(
        Employee,
        verbose_name="Сотрудник",
        on_delete=models.CASCADE,
        db_index=True
    )
    booking = models.ForeignKey('services.Booking', verbose_name="Бронь", on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="Время начала брони", db_index=True)
    end_time = models.DateTimeField(verbose_name="Время конца брони", db_index=True)

    class Meta:
        verbose_name = "Бронь сотрудника"
        verbose_name_plural = "Брони сотрудника"
