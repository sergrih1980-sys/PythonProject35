from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Course.objects.none()

        if user.groups.filter(name='moderator').exists() or user.is_superuser:
            return Course.objects.all()

        return Course.objects.filter(author=user)

    def perform_create(self, serializer):
        user = self.request.user
        # Проверка: создавать могут только модераторы и суперпользователи
        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and not user.is_superuser:
            raise PermissionDenied("Создавать курсы могут только модераторы и суперпользователи.")

        # АВТОМАТИЧЕСКАЯ привязка автора из запроса
        serializer.save(author=user)

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user

        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and instance.author != user:
            raise PermissionDenied("Вы можете редактировать только свои курсы.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and instance.author != user:
            raise PermissionDenied("Вы можете удалять только свои курсы.")
        instance.delete()

    def get_permissions(self):
        if self.action == 'create':
            # Только модераторы/суперпользователи могут создавать
            return [IsModerator()]
        return [permissions.IsAuthenticated()]


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Lesson.objects.none()

        if user.groups.filter(name='moderator').exists() or user.is_superuser:
            return Lesson.objects.all()

        # Обычный пользователь видит только уроки своих курсов
        return Lesson.objects.filter(course__author=user)

    def perform_create(self, serializer):
        user = self.request.user
        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and not user.is_superuser:
            raise PermissionDenied("Создавать уроки могут только модераторы и суперпользователи.")

        # Автор не нужен: он уже есть у курса
        serializer.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user
        course_author = instance.course.author

        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and course_author != user:
            raise PermissionDenied("Вы можете редактировать только уроки своих курсов.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        course_author = instance.course.author

        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and course_author != user:
            raise PermissionDenied("Вы можете удалять только уроки своих курсов.")
        instance.delete()

    def get_permissions(self):
        if self.action == 'create':
            return [IsModerator()]
        return [permissions.IsAuthenticated()]