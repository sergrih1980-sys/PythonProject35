from rest_framework import generics
from .models import Lesson
from .serializers import LessonSerializer
from rest_framework import viewsets
from django.db.models import Count
from .models import Course
from .serializers import CourseSerializer


# Список уроков + создание нового
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

# Получение, обновление, удаление одного урока
class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = (
        Course.objects
        .prefetch_related('lessons')          # подгружаем все уроки одним запросом
        .annotate(lessons_count=Count('lessons'))  # считаем количество в БД
    )
    serializer_class = CourseSerializer