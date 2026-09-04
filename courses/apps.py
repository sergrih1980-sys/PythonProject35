from django.apps import AppConfig
import os
import stripe

def charge_payment(amount, token):
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        raise RuntimeError("STRIPE_SECRET_KEY не задан")


    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
