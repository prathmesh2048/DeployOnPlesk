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
class StripeCheckout(CreateAPIView):
    def post(self, request):
        helper.check_parameters(
            request, ['checkout_id'])
        body = request.data

        checkout = helper.checkRecord(
            body['checkout_id'], Checkout, "Order")

        data = {
            "metadata": helper.json.loads(checkout.metadata),
            "email": checkout.email,
            "amount":  checkout.amount,
            'return_url': checkout.return_url
        }

        try:
            stripe_secret = PaymentCreds.objects.get(key='STRIPE_SECRET')
        except Exception:
            raise helper.exception.ParseError(
                helper.message.MODULE_INVALID('Payment'))

        response = helper.payment.stripe_api(data, stripe_secret.value)

        checkout.payment_id = response['id']
        checkout.save()

        return helper.createResponse(
            helper.message.CHECKOUT_SUCCESSFUL,
            {
                "url": checkout.payment_id
            }
        )


# Paypal checkout
# post
# /v1/checkout/paypal
class PaypalCheckout(CreateAPIView):
    def post(self, request):
        helper.check_parameters(
            request, ['checkout_id'])
        body = request.data

        checkout = helper.checkRecord(
            body['checkout_id'], Checkout, "Order")

        data = {
            "metadata": helper.json.loads(checkout.metadata),
            "email": checkout.email,
            "amount":  checkout.amount,
            'return_url': checkout.return_url
        }

        paypal_client_id = PaymentCreds.objects.get(key='PAYPAL_CLIENT_ID')
        paypal_secret = PaymentCreds.objects.get(key='PAYPAL_SECRET')

        id, url = helper.payment.paypal_api(
            data, paypal_client_id.value, paypal_secret.value)

        checkout.payment_id = id
        checkout.save()

        return helper.createResponse(
            helper.message.CHECKOUT_SUCCESSFUL,
            {
                "url": url
            }
        )


# Checkout plan
# post
# /v1/checkout/plan
class CheckoutPlan(CreateAPIView):
    def post(self, request):
        helper.check_parameters(request, ['payment_method', 'plan', 'email'])
        body = request.data

        payment_method = Payment_Method.objects.get(id=body['payment_method'])
        plan = Plan.objects.get(id=body['plan'])

        data = {
            "email": body['email'],
            "metadata": [],
            "amount":  plan.price,
            'return_url': helper.settings.DOMAIN_NAME
        }

        if payment_method.code == "stripe":
            stripe_secret = PaymentCreds.objects.get(key='STRIPE_SECRET')
            stripe_secret = stripe_secret.value

            response = helper.payment.stripe_api(data, stripe_secret)
            hosted_url = response['id']

        else:
            paypal_client_id = PaymentCreds.objects.get(key='PAYPAL_CLIENT_ID')
            paypal_secret = PaymentCreds.objects.get(key='PAYPAL_SECRET')
            paypal_client_id = paypal_client_id.value
            paypal_secret = paypal_secret.value

            id, url = helper.payment.paypal_api(
                data, paypal_client_id, paypal_secret)

            hosted_url = url

        return helper.createResponse(
            helper.message.CHECKOUT_SUCCESSFUL,
            {
                "url": hosted_url
            }
        )


# Create Checkout
# post
# /v1/checkout/create
class CreateCheckout(CreateAPIView):
    def post(self, request):
        helper.check_parameters(
            request, ['api_key', 'email', 'amount', 'return_url', 'webhook_url', 'metadata'])
        body = request.data

        if body['api_key'] != helper.settings.API_SECRET:
            raise helper.exception.PermissionDenied()

        data = {
            "metadata": body['metadata'],
            "email": body['email'],
            "amount":  body['amount'],
            'return_url': body['return_url']
        }

        checkout = Checkout.objects.create(
            metadata=helper.json.dumps(body['metadata']),
            email=body['email'],
            amount=body['amount'],
            return_url=body['return_url'],
            webhook_url=body['webhook_url']
        )
        checkout.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE('Order', 'created'),
            {
                "url": helper.settings.DOMAIN_NAME + '/checkout/' + str(checkout.id)
            }
        )


# Read Checkout
# get
# /v1/checkout/read
class ReadCheckout(ListAPIView):
    def list(self, request, id):
        try:
            checkout = Checkout.objects.get(payment_id=id)
        except Exception:
            checkout = helper.checkRecord(id, Checkout, "order")
        # data = serializers.serialize("json", checkout)

        return helper.createResponse(
            helper.message.MODULE_LIST('order'),
            {
                "order": CheckoutSerializer(checkout).data
            }
        )
