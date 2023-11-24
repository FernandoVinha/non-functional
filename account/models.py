from django.db import models
from users.models import User
import uuid

SOURCE = [
    ('bitcoin', 'Bitcoin'),
    ('internal', 'Internal'),
    ('lightning', 'Lightning'),
]

TYPE = [
    ('received', 'Received'),
    ('spent', 'Spent'),
]

class Transfer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=10, choices=SOURCE, default="internal")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    mensagem = models.TextField(blank=True, null=True)
    bitcoin_address = models.CharField(max_length=255, blank=True, null=True)
    lightning_address = models.CharField(max_length=255, blank=True, null=True)
    received = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transfer - ID: {self.id}, User: {self.user}, Status: {self.status}, Amount: {self.valor}"

class PaymentRequest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bitcoin_address = models.CharField(max_length=255)
    lightning_address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=(
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('not_paid', 'Not Paid'),
        ('unconfirmed', 'Unconfirmed')
    ), default='not_paid')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment Request - ID: {self.id}, User: {self.user}, Amount: {self.amount}, Status: {self.payment_status}"
