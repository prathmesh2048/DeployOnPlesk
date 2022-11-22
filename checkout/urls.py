from django.urls import path
from .api import StripeCheckout, PaypalCheckout, CheckoutPlan, ReadCheckout, CreateCheckout
from .restAPI import StripeRestCheckout, PaypalRestCheckout

urlpatterns = [
    path('stripe', StripeRestCheckout.as_view()),
    path('paypal', PaypalRestCheckout.as_view()),
    path('checkout-stripe', StripeCheckout.as_view()),
    path('checkout-paypal', PaypalCheckout.as_view()),
    path('plan', CheckoutPlan.as_view()),
    path('read/<str:id>', ReadCheckout.as_view()),
    path('create', CreateCheckout.as_view()),
]
