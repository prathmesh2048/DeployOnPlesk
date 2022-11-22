from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField
)
from django.contrib.auth import authenticate
from .models import User
from helper import helper


# Admin Login Serializer
class AdminLoginSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_superuser:
            return user
        raise helper.exception.AuthenticationFailed()