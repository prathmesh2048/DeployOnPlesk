from django.db import models


class Payment_Method(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True, default=None)
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payment_methods"


class PaymentCreds(models.Model):
    id = models.AutoField(primary_key=True)
    payment_method = models.ForeignKey(
        Payment_Method, on_delete=models.CASCADE)
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=200)
    is_private = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment_creds"
