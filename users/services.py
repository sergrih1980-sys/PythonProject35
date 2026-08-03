import stripe
from django.conf import settings
from django.db import transaction

from users.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(name: str) -> dict:
    product = stripe.Product.create(name=name)
    return product

def create_stripe_price(product_id: str, amount_cents: int, currency: str = 'rub') -> dict:
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount_cents,  # в копейках
        currency=currency.lower(),
    )
    return price

def create_checkout_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    session = stripe.CheckoutSession.create(
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session

def create_payment_session(user, course, amount, session=None):
    """
    Создаёт продукт, цену и сессию в Stripe, сохраняет платёж в БД.
    Возвращает dict с данными сессии.
    """
    amount_cents = int(round(float(amount) * 100))  # безопасное округление
    name = f"Курс: {course.title}"

    # Вызовы Stripe (в тестах их будем мокать)
    product = create_stripe_product(name)
    price = create_stripe_price(product["id"], amount_cents)
    session = create_checkout_session(
        price["id"],
        success_url=f"/payment-success/?session_id={session['id']}",
        cancel_url="/payment-cancel/"
    )

    with transaction.atomic():
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=amount,
            stripe_product_id=product["id"],
            stripe_price_id=price["id"],
            stripe_session_id=session["id"],
            checkout_url=session["url"],
            status='pending',
        )

    return {
        "payment_id": payment.id,
        "checkout_url": session["url"],
        "session_id": session["id"],
    }