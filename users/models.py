from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя: вход по email, дополнительные поля."""

    username = None  # отключаем username
    email = models.EmailField("email address", unique=True)

    phone = models.CharField("телефон", max_length=20, blank=True)
    city = models.CharField("город", max_length=100, blank=True)
    avatar = models.ImageField("аватар", upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"  # по чему логиниться
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
