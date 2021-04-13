from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
from backend.apps.services.models import Locality


class Employee(models.Model):
    WORK_STATUS_BUSY = 'busy'
    WORK_STATUS_VACANT = 'vacant'
    WORK_STATUS_FREE_DAY = 'free_day'

    full_name = models.CharField("Ф.И.О", max_length=255, )
    photo = models.ImageField("Фото сотрудника", upload_to="employees_photos", null=True, blank=True)
    work_status = models.CharField("Статус сотрудника", max_length=10)
    age = models.PositiveSmallIntegerField("Возраст", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f'{self.full_name}'


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
    email = models.EmailField("Email", unique=True)
    company_name = models.CharField("Название", max_length=255, db_index=True)
    logo = models.ImageField(verbose_name="Лого", upload_to='company_logo/', null=True, blank=True)
    phone_number = models.CharField(
        "Номер телефона", max_length=10, null=True)
    employees = models.ManyToManyField(Employee, verbose_name="Сотрудники")
    activity_localities = models.ManyToManyField(
        Locality,
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

