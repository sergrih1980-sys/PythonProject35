
from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter

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