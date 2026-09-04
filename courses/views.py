from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import StandardResultsSetPagination
from .tasks import send_course_update_notification
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Course.objects.none()

        if user.groups.filter(name='moderator').exists() or user.is_superuser:
            return Course.objects.all()

        return Course.objects.filter(author=user)

    def perform_create(self, serializer):
        user = self.request.user
        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and not user.is_superuser:
            raise PermissionDenied("Создавать курсы могут только модераторы и суперпользователи.")
        serializer.save(author=user)

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user

        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and instance.author != user:
            raise PermissionDenied("Вы можете редактировать только свои курсы.")

        updated = serializer.save()

        # Сбор изменённых полей
        old_data = {f.name: getattr(instance, f.name) for f in instance._meta.fields}
        new_data = {f.name: getattr(updated, f.name) for f in updated._meta.fields}
        changed_fields = [
            f for f in old_data.keys()
            if old_data[f] != new_data[f]
        ]

        if changed_fields:
            send_course_update_notification.delay(
                course_id=updated.id,
                course_title=updated.title,
                updated_fields=changed_fields,
            )

        return updated

    def perform_destroy(self, instance):
        user = self.request.user
        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and instance.author != user:
            raise PermissionDenied("Вы можете удалять только свои курсы.")
        instance.delete()

    def get_permissions(self):
        if self.action == 'create':
            return [IsModerator()]
        return [permissions.IsAuthenticated()]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Lesson.objects.none()

        if user.groups.filter(name='moderator').exists() or user.is_superuser:
            return Lesson.objects.all()

        return Lesson.objects.filter(course__author=user)

    def perform_create(self, serializer):
        user = self.request.user
        is_moderator = user.groups.filter(name='moderator').exists()
        if not is_moderator and not user.is_superuser:
            raise PermissionDenied("Создавать уроки могут только модераторы и суперпользователи.")
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


class ToggleSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        user = request.user

        subs_item = Subscription.objects.filter(user=user, course=course).first()

        if subs_item:
            subs_item.delete()
            message = "Подписка удалена"
            status_code = status.HTTP_200_OK
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)