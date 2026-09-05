import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Course, Lesson, Subscription
from .serializers import LessonSerializer

User = get_user_model()


class CoursesAPITest(APITestCase):
    def setUp(self):
        # Группы
        self.moderator_group, _ = Group.objects.get_or_create(name='moderator')

        # Пользователи
        # Обычный пользователь
        self.user = User.objects.create_user(
            email='test@test.com',
            password='pass'
        )

        # Модератор: только email и пароль, без username
        self.moderator = User.objects.create_user(
            email='mod@example.com',
            password='pass'
        )
        self.moderator.groups.add(self.moderator_group)

        # Суперпользователь: тоже без username
        self.superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='pass'
        )

        # Курсы
        self.course_by_user = Course.objects.create(
            title='Course by user',
            description='User course',
            author=self.user
        )
        self.course_by_mod = Course.objects.create(
            title='Course by mod',
            description='Mod course',
            author=self.moderator
        )

        # Уроки
        self.lesson_by_user = Lesson.objects.create(
            title='Lesson by user',
            content='Content',
            course=self.course_by_user
        )
        self.lesson_by_mod = Lesson.objects.create(
            title='Lesson by mod',
            content='Content',
            course=self.course_by_mod
        )

    # -----------------------------
    # CRUD Lessons (LessonViewSet)
    # -----------------------------

    def test_list_lessons_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        results = data['results']
        self.assertIn(self.lesson_by_user.id, [r['id'] for r in results])
        self.assertNotIn(self.lesson_by_mod.id, [r['id'] for r in results])

    def test_list_lessons_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        ids = [r['id'] for r in data['results']]
        self.assertIn(self.lesson_by_user.id, ids)
        self.assertIn(self.lesson_by_mod.id, ids)

    def test_create_lesson_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "New lesson",
            "content": "Content",
            "course": self.course_by_user.id
        }
        response = self.client.post(
            '/api/lessons/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_moderator_allowed(self):
        self.client.force_authenticate(user=self.moderator)
        payload = {
            "title": "New lesson by mod",
            "content": "Content",
            "course": self.course_by_mod.id
        }
        response = self.client.post(
            '/api/lessons/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_id = response.data['id']
        lesson = Lesson.objects.get(id=created_id)
        self.assertEqual(lesson.title, payload['title'])
        self.assertEqual(lesson.course.id, payload['course'])

    def test_update_lesson_own_course_allowed(self):
        self.client.force_authenticate(user=self.moderator)
        payload = {"title": "Updated title"}
        response = self.client.patch(
            f'/api/lessons/{self.lesson_by_mod.id}/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Lesson.objects.get(id=self.lesson_by_mod.id).title,
            payload['title']
        )

    def test_delete_lesson_own_course_allowed(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f'/api/lessons/{self.lesson_by_mod.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson_by_mod.id).exists())

    def test_debug_check(self):
        response = self.client.get('/debug/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "OK")