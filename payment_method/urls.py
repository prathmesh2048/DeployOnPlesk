from django.urls import path
from .api import ReadPaymentMethods, UpdatePaymentMethod, ReadPublicPaymentMethods, UpdatePaymentCreds


urlpatterns = [
    path('read', ReadPaymentMethods.as_view()),
    path('read-public', ReadPublicPaymentMethods.as_view()),
    path('update/<str:id>', UpdatePaymentMethod.as_view()),
    path('creds/update', UpdatePaymentCreds.as_view()),
]
