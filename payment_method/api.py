from helper import helper
from .serializers import PaymentMethodSerializer, PaymentCredSerializer, PublicCredsSerializer
from .models import Payment_Method, PaymentCreds
from rest_framework.generics import ListAPIView, UpdateAPIView


# Read Payyment Methods
# get
# /v1/payment_method/read
class ReadPaymentMethods(ListAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def list(self, request):
        if request.user.is_superuser:
            queryset = Payment_Method.objects.all()
        else:
            queryset = Payment_Method.objects.filter(status=True)

        return helper.createResponse(
            helper.message.MODULE_LIST("Payment Methods"),
            {
                "payment_methods": PaymentMethodSerializer(queryset, many=True).data,
                "payment_creds": PaymentCredSerializer(PaymentCreds.objects.all(), many=True).data
            },
        )


# Update Payment Methods
# put
# /v1/payment_method/update/<str:id>
class UpdatePaymentMethod(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request, id):
        helper.check_parameters(request, ["status"])
        payment_method = helper.checkRecord(
            id, Payment_Method, "Payment Method")

        payment_method.status = helper.toBool(request.data["status"])
        payment_method.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("Payment method", "updated")
        )


# Read Public Creds
# get
# /v1/payment_method/read-public
class ReadPublicPaymentMethods(ListAPIView):
    def list(self, request):
        queryset = Payment_Method.objects.filter(status=True)

        return helper.createResponse(
            helper.message.MODULE_LIST("Payment Methods"),
            {
                "payment_methods": PaymentMethodSerializer(queryset, many=True).data,
                "payment_creds": PublicCredsSerializer(PaymentCreds.objects.filter(is_private=False), many=True).data
            },
        )


# Update Payment Creds
# put
# /v1/payment_method/creds/update
class UpdatePaymentCreds(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request):
        creds = request.data
        keys = creds.keys()

        for key in keys:
            obj = PaymentCreds.objects.get(key=key)
            obj.value = creds[key]
            obj.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE(
                "Payment Credentials", "updated")
        )
