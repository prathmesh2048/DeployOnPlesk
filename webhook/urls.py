from django.urls import path
from .api import StripeWebhook, PaypalWebhook

urlpatterns = [
    path('stripe', StripeWebhook.as_view()),
    path('paypal', PaypalWebhook.as_view()),
]
