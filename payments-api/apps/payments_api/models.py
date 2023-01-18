from django.db import models
from apps.payments_api.choices import PaymentDebtStatus


class PaymentDebt(models.Model):
    serializer = "apps.payments_api.serializers.PaymentDebtSerializer"

    debt_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    government_id = models.BigIntegerField()
    email = models.EmailField()
    debt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    debt_due_date = models.DateField()
    status = models.CharField(
        max_length=32, choices=PaymentDebtStatus.choices, default=PaymentDebtStatus.OPEN
    )
