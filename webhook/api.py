from django.core import serializers
from rest_framework.generics import CreateAPIView
from stripe import log
from payment_method.models import PaymentCreds
from helper import helper
from checkout.models import Checkout
import paypalrestsdk

# STRIPE WEBHOOK
# post
# /v1/webhook/stripe


class StripeWebhook(CreateAPIView):
    def post(self, request):
        request_data = request.data
        data = request_data["data"]
        
        print(data)
        print(request_data)

        data_object = data["object"]
        if data_object['payment_status'] == 'paid':
            try:
                obj = Checkout.objects.get(payment_id=data_object['id'])
                data = {
                    "api_key": helper.settings.API_SECRET,
                    "payment_method": "stripe",
                    "metadata": obj.metadata
                }
                helper.request.post(obj.webhook_url, params=data)
            except Exception:
                pass

        return helper.createResponse(
            helper.message.MODULE_STORE_SUCCESS('Data')
        )


# PAYPAL WEBHOOK
# post
# /v1/webhook/paypal
class PaypalWebhook(CreateAPIView):
    def post(self, request):
        helper.check_parameters(request, ['PayerID', 'paymentId'])
        request_data = request.data
        try:
            obj = Checkout.objects.get(payment_id=request_data['paymentId'])
            paypal_client_id = PaymentCreds.objects.get(key='PAYPAL_CLIENT_ID')
            paypal_secret = PaymentCreds.objects.get(key='PAYPAL_SECRET')
            paypal_client_id = paypal_client_id.value
            paypal_secret = paypal_secret.value

            paypalrestsdk.configure({
                "mode": helper.settings.PAYPAL_MODE,  # sandbox or live
                "client_id": paypal_client_id,
                "client_secret": paypal_secret
            })

            payment = paypalrestsdk.Payment.find(request_data['paymentId'])

            if payment.execute({"payer_id": request_data['PayerID']}):
                print("Payment execute successfully")
            else:
                print(payment.error)

            if payment['state'] == "approved":
                data = {
                    "api_key": helper.settings.API_SECRET,
                    "payment_method": "paypal",
                    "metadata": obj.metadata
                }

                helper.request.post(
                    obj.webhook_url, params=data
                )

            return helper.createResponse(
                helper.message.MODULE_STORE_SUCCESS('Data'),
                {
                    "url": obj.return_url
                }
            )

        except Exception as e:
            print(e)
            raise helper.exception.ParseError(
                helper.message.PAYMENT_FAILD
            )
