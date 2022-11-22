from rest_framework.serializers import ModelSerializer
from .models import Payment_Method, PaymentCreds


class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = Payment_Method
        fields = "__all__"


class PaymentCredSerializer(ModelSerializer):
    class Meta:
        model = PaymentCreds
        fields = "__all__"


class PublicCredsSerializer(ModelSerializer):
    class Meta:
        model = PaymentCreds
        fields = ['key', 'payment_method', 'value']
