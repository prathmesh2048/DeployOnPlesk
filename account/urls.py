from django.urls import path
from .api import (
    AdminLogin,
    UpdatePassword,
    CheckAccess,
)


urlpatterns = [
    path("admin-login", AdminLogin.as_view()),
    path("update-password", UpdatePassword().as_view()),
    path("access", CheckAccess.as_view()),
]
