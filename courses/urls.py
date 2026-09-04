from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, ToggleSubscriptionView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:course_id>/subscribe/', ToggleSubscriptionView.as_view(), name='toggle-subscription'),
]