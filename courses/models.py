from django.db import models
from django.conf import settings

class Course(models.Model):
    """
    Курс: владелец — автор (User), права доступа строятся вокруг него.
    """
    title = models.CharField("Название курса", max_length=255)
    description = models.TextField("Описание", blank=True)

    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Урок: принадлежит курсу, владельцем считается author курса.
    """
    course = models.ForeignKey(
        Course,                 # <-- Course уже определён выше, поэтому тут нет ошибки
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Курс"
    )
    title = models.CharField("Название урока", max_length=255)
    content = models.TextField("Контент урока", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    video_url = models.URLField("Ссылка на видео", blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.course.title} — {self.title}"

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name="Курс"
    )
    created_at = models.DateTimeField(
        "Дата подписки",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ('user', 'course')  # защита от дублей на уровне БД

    def __str__(self):
        return f"{self.user.email} → {self.course.title}"