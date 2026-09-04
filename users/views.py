from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import viewsets
from stripe import StripeError

from courses.models import Course
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer
from .services import create_checkout_session, create_stripe_price, create_stripe_product, create_payment_session


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

class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        amount_raw = request.data.get('amount')

        # Валидация наличия полей
        if not course_id or amount_raw is None:
            return Response(
                {"error": "course_id и amount обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Валидация amount
        try:
            amount = float(amount_raw)
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {"error": "amount должен быть положительным числом"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, pk=course_id)

        try:
            result = create_payment_session(request.user, course, amount)
            return Response(result, status=status.HTTP_201_CREATED)
        except StripeError as e:
            # Логирование + понятный ответ
            return Response(
                {"error": "Ошибка при создании платёжной сессии", "details": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )