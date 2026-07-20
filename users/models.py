from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from courses.models import Course, Lesson


class User(AbstractUser):
    """Кастомная модель пользователя: вход по email, дополнительные поля."""

    username = None  # отключаем username
    email = models.EmailField("email address", unique=True)

    phone = models.CharField("телефон", max_length=20, blank=True)
    city = models.CharField("город", max_length=100, blank=True)
    avatar = models.ImageField("аватар", upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"  # по чему логиниться
    REQUIRED_FIELDS = []       # никаких обязательных полей кроме email и пароля

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель платежа: за курс или за урок."""

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_payments'
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lesson_payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='transfer'
    )
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} — {self.amount} ({self.payment_method})"

    class Meta:
        ordering = ['-paid_at']