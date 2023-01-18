from django.db import models


class PaymentDebtStatus(models.TextChoices):
    OPEN = "open", "Open"
    PAYED = "payed", "Payed"
