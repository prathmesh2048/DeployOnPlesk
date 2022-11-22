from rest_framework.generics import CreateAPIView, ListAPIView
from django.core import serializers
from .models import Checkout
from .serializers import CheckoutSerializer
from payment_method.models import PaymentCreds, Payment_Method
from plan.models import Plan
from helper import helper


# Stripe Checkout
# post
# /v1/checkout/stripe
class StripeRestCheckout(CreateAPIView):
    def post(self, request):
        helper.check_parameters(
            request, ['api_key', 'email', 'amount', 'return_url', 'webhook_url', 'metadata'])
        body = request.data

        if body['api_key'] != helper.settings.API_SECRET:
            raise helper.exception.PermissionDenied()

        data = {
            "metadata": helper.json.loads(body['metadata']),
            "email": body['email'],
            "amount":  body['amount'],
            'return_url': body['return_url']
        }

        try:
            stripe_secret = PaymentCreds.objects.get(key='STRIPE_SECRET')
        except Exception:
            raise helper.exception.ParseError(
                helper.message.MODULE_INVALID('Payment'))

        response = helper.payment.stripe_api(data, stripe_secret.value)

        checkout = Checkout.objects.create(
            payment_id=response['id'],
            email=body['email'],
            amount=body['amount'],
            return_url=body['return_url'],
            webhook_url=body['webhook_url'],
            metadata=body['metadata']
        )
        checkout.save()

        return helper.createResponse(
            helper.message.CHECKOUT_SUCCESSFUL,
            {
                "url": helper.settings.DASHBOARD_DOMAIN_NAME + '/checkout/stripe/' + checkout.payment_id
            }
        )


# Paypal checkout
# post
# /v1/checkout/paypal
class PaypalRestCheckout(CreateAPIView):
    def post(self, request):
        helper.check_parameters(
            request, ['api_key', 'email', 'amount', 'return_url', 'webhook_url', 'metadata'])
        body = request.data

        if body['api_key'] != helper.settings.API_SECRET:
            raise helper.exception.PermissionDenied()

        paypal_client_id = PaymentCreds.objects.get(key='PAYPAL_CLIENT_ID')
        paypal_secret = PaymentCreds.objects.get(key='PAYPAL_SECRET')

        data = {
            "metadata": body['metadata'],
            "email": body['email'],
            "amount":  body['amount'],
            'return_url': body['return_url']
        }

        id, url = helper.payment.paypal_api(
            data, paypal_client_id.value, paypal_secret.value)

        checkout = Checkout.objects.create(
            payment_id=id,
            email=body['email'],
            amount=body['amount'],
            return_url=body['return_url'],
            webhook_url=body['webhook_url'],
            url=url,
            metadata=helper.json.dumps(body['metadata'])
        )
        checkout.save()

        return helper.createResponse(
            helper.message.CHECKOUT_SUCCESSFUL,
            {
                "url": helper.settings.DASHBOARD_DOMAIN_NAME + '/redirect/' + str(checkout.id)
            }
        )
