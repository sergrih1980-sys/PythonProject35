from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, PaymentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, CreatePaymentView
from .viewsets import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payments/create/', CreatePaymentView.as_view(), name='create-payment'),
]