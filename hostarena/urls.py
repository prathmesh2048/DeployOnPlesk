from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("v1/auth/", include("account.urls")),
    path("v1/plan/", include("plan.urls")),
    path("v1/payment_method/", include("payment_method.urls")),
    path("v1/checkout/", include("checkout.urls")),
    path("v1/webhook/", include("webhook.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
