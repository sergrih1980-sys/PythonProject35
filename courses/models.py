from django.db import models
from django.conf import settings


class Course(models.Model):
    """Курс: название, превью, описание."""

    title = models.CharField("название курса", max_length=255)
    preview = models.ImageField(
        "превью курса", upload_to="course_previews/", blank=True, null=True
    )
    description = models.TextField("описание курса", blank=True)

    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Урок: название, описание, превью, ссылка на видео, связь с курсом."""

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="курс"
    )
    title = models.CharField("название урока", max_length=255)
    preview = models.ImageField(
        "превью урока", upload_to="lesson_previews/", blank=True, null=True
    )
    description = models.TextField("описание урока", blank=True)
    video_url = models.URLField("ссылка на видео", max_length=500, blank=True)

    order = models.PositiveIntegerField("порядок в курсе", default=0, db_index=True)

    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("дата обновления", auto_now=True)

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["course", "order"]

    def __str__(self):
        return f"{self.course.title} — {self.title}"
