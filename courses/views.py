from rest_framework import generics
from .models import Lesson
from .serializers import LessonSerializer

# Список уроков + создание нового
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

# Получение, обновление, удаление одного урока
class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer