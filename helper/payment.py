from hostarena.settings import DASHBOARD_DOMAIN_NAME
from . import message, exception
from django.conf import settings
import paypalrestsdk
import stripe
import random


# Generate OTP
def generateOTP(length):
    length -= 1
    return random.randint(int("1" + "0" * length), int("9" + "9" * length))


# STRIPE API
def stripe_api(data, STRIPE_SECRET):
    stripe.api_key = STRIPE_SECRET
    response = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(data['amount']*100),
                    'product_data': {
                        'name': "Checkout",
                    },
                },
                'quantity': 1,

            },
        ],
        customer_email=data['email'],
        mode='payment',
        success_url=DASHBOARD_DOMAIN_NAME + '/stripe',
        cancel_url=DASHBOARD_DOMAIN_NAME,
        metadata=data['metadata']
    )

    print(response)

    return response


# PAYPAL CHECKOUT
def paypal_api(data, client_id, client_secret):
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,  # sandbox or live
        "client_id": client_id,
        "client_secret": client_secret
    })

    payment = paypalrestsdk.Payment(
        {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": DASHBOARD_DOMAIN_NAME + '/checkout/paypal',
                "cancel_url": DASHBOARD_DOMAIN_NAME
            },
            "transactions": [
                {
                    "item_list": {
                        "items": [
                            {
                                "name": "Purchase",
                                "sku": "Hosting Invoice #" + str(generateOTP(4)),
                                "price": data['amount'],
                                "currency": "USD",
                                "quantity": 1
                            }
                        ]
                    },
                    "amount": {
                        "total": data['amount'],
                        "currency": "USD"
                    },
                    "description": "This is the paypal payment."
                }
            ]
        }
    )

    approval_url = ""

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
    else:
        raise exception.ParseError(payment.error)

    if approval_url == "":
        raise exception.ParseError(message.PAYMENT_FAILD)

    return payment.id, approval_url
