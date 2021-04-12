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
    email = models.EmailField("Email", unique=True)
    company_name = models.CharField("Название компании", max_length=255, null=True, blank=True)
    logo = models.ImageField(verbose_name="Лого компании",upload_to='company_logo/')
    about_me = models.TextField(
        "Краткая информация обо мне", null=True, blank=True)
    locality = models.CharField('Город', max_length=255, null=True, blank=True)
    address = models.CharField('Адрес, улица/дом', max_length=255)
    phone_number = models.CharField(
        "Номер телефона", max_length=255, null=True, blank=True)
    employees_count = models.PositiveSmallIntegerField(verbose_name="Количество сотрудников")
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

    def __str__(self):
        return f'{self.email}'