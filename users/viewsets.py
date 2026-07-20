from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .models import Payment
from .serializers import PaymentSerializer, UserSerializer

User = get_user_model()

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer