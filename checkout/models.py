from django.db import models
import uuid


class Checkout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    amount = models.FloatField()
    payment_id = models.CharField(max_length=400, null=True, blank=True)
    return_url = models.CharField(max_length=400)
    webhook_url = models.CharField(max_length=400)
    url = models.URLField(blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "checkout"
