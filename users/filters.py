import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    # Точное совпадение по способу оплаты (cash / transfer и т.п.)
    payment_method = django_filters.CharFilter(field_name='payment_method', lookup_expr='exact')

    # Фильтр по ID курса (?paid_course=1)
    paid_course = django_filters.NumberFilter(field_name='paid_course', lookup_expr='exact')

    # Фильтр по ID урока (?paid_lesson=5)
    paid_lesson = django_filters.NumberFilter(field_name='paid_lesson', lookup_expr='exact')

    class Meta:
        model = Payment
        fields = []