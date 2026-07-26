from rest_framework import viewsets
from .models import Lesson
from users import permissions
from .models import Course
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        - list, retrieve, update, partial_update: любой авторизованный
        - create, destroy: запрещены всем (включая модераторов)
        Если хочешь оставить create/destroy только для суперюзеров — поставь IsAdminUser.
        """
        permission_classes = [permissions.IsAuthenticated]

        if self.action in ['create', 'destroy']:
            # Запрещаем создание и удаление даже модераторам
            permission_classes = []  # либо [permissions.IsAdminUser], если нужно оставить админам

        return [permission() for permission in permission_classes]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]

        if self.action in ['create', 'destroy']:
            permission_classes = []  # или [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]