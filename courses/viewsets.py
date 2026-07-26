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

        if user.groups.filter(name='moderator').exists():
            return Course.objects.all()


        return Course.objects.filter(author=user)


    def perform_create(self, serializer):
        user = self.request.user
        if not user.groups.filter(name='moderator').exists() and not user.is_superuser:
            raise PermissionDenied("Создавать курсы могут только модераторы и суперпользователи.")
        serializer.save(author=user)

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user

        if not user.groups.filter(name='moderator').exists() and instance.author != user:
            raise PermissionDenied("Вы можете редактировать только свои курсы.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if not user.groups.filter(name='moderator').exists() and instance.author != user:
            raise PermissionDenied("Вы можете удалять только свои курсы.")
        instance.delete()

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permission_classes = [IsModerator]
        return [permission() for permission in permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Lesson.objects.none()

        if user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()

        # Обычный пользователь видит все уроки.
        # Если нужно только свои (по автору курса) — фильтруй по course.author
        return Lesson.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if not user.groups.filter(name='moderator').exists() and not user.is_superuser:
            raise PermissionDenied("Создавать уроки могут только модераторы и суперпользователи.")
        # Автор курса обычно уже задан в course, поэтому просто сохраняем
        serializer.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user
        course_author = instance.course.author

        if not user.groups.filter(name='moderator').exists() and course_author != user:
            raise PermissionDenied("Вы можете редактировать только уроки своих курсов.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        course_author = instance.course.author

        if not user.groups.filter(name='moderator').exists() and course_author != user:
            raise PermissionDenied("Вы можете удалять только уроки своих курсов.")
        instance.delete()

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permission_classes = [IsModerator]
        return [permission() for permission in permission_classes]