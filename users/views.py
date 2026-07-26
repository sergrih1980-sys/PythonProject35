
from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    # select_related нужен, чтобы не было N+1 запросов к БД
    queryset = Payment.objects.all().select_related('user', 'paid_course', 'paid_lesson')
    serializer_class = PaymentSerializer

    # Настройка фильтрации
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PaymentFilter

    # Настройка сортировки
    ordering_fields = ['paid_at', 'amount']
    ordering = ['-paid_at']


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"detail": "Пользователь успешно зарегистрирован"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)