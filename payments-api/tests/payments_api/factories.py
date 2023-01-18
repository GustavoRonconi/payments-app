import factory

from apps.payments_api.choices import PaymentsFileItemStatus, PaymentsFileStatus
from apps.payments_api.models import PaymentsFile, PaymentsFileItem


class PaymentsFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentsFile

    origin = factory.sequence(lambda n: f"origin_{n}")
    type = factory.sequence(lambda n: f"type_{n}")
    url = factory.sequence(lambda n: f"http://olist-adminapp.s3.amazonaws.com/{n}")
    requester = factory.sequence(lambda n: f"requester 0{n}")
    checksum = factory.sequence(lambda n: f"hash_{n}")
    total = factory.sequence(lambda n: n)
    status = factory.Faker("random_element", elements=PaymentsFileStatus.__members__.values())
    items_done = factory.sequence(lambda n: n)
    items_failed = factory.sequence(lambda n: n)


class PaymentsFileItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentsFileItem

    batch_file = factory.SubFactory(PaymentsFileFactory)
    index = factory.sequence(lambda n: n)
    data = factory.sequence(lambda n: {"data_key": f"data-{n}"})
    status = factory.Faker("random_element", elements=PaymentsFileItemStatus.__members__.values())
    error = factory.sequence(lambda n: {"error_key": f"error-{n}"})
