from rest_framework.serializers import ModelSerializer
from .models import Checkout


class CheckoutSerializer(ModelSerializer):
    class Meta:
        model = Checkout
        fields = "__all__"
