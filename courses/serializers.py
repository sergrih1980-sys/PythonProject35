from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_only_youtube_com


class CourseSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()

    class Meta:
        model = Course
        # author здесь нет — он заполняется автоматически
        fields = ['id', 'title', 'description', 'author_email', 'created_at', 'updated_at']

    def get_author_email(self, obj):
        return obj.author.email if obj.author else None

    def get_is_subscribed(self, obj):
        """
        Возвращает True, если текущий пользователь (request.user) подписан на курс.
        Если пользователь не авторизован — False.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.subscribers.filter(user=request.user).exists()


class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'course_title',
            'title', 'content', 'video_url', 'order', 'created_at'
        ]
        extra_kwargs = {
            # Ссылки в контенте урока
            'content': {'validators': [validate_only_youtube_com]},
            # Ссылка в отдельном поле video_url
            'video_url': {'validators': [validate_only_youtube_com]},
        }