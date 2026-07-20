from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment
from courses.serializers import CourseSerializer, LessonSerializer

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    course_title = serializers.SerializerMethodField()
    lesson_title = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email',
            'paid_course', 'course_title',
            'paid_lesson', 'lesson_title',
            'amount', 'payment_method', 'paid_at'
        ]
        read_only_fields = ['paid_at']

    def get_course_title(self, obj):
        if obj.paid_course:
            return obj.paid_course.title
        return None

    def get_lesson_title(self, obj):
        if obj.paid_lesson:
            return obj.paid_lesson.title
        return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Перечисляем только нужные поля (без пароля и username)
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'city',
            'avatar',
            'is_staff',
            'is_active',
        ]

        read_only_fields = ['id', 'is_staff']