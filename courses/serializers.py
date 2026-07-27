from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()

    class Meta:
        model = Course
        # author здесь нет — он заполняется автоматически
        fields = ['id', 'title', 'description', 'author_email', 'created_at', 'updated_at']

    def get_author_email(self, obj):
        return obj.author.email if obj.author else None


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'order', 'created_at']