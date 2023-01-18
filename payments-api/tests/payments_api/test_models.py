import pytest

from olist_django.actions.exceptions import ImpossibleTransitionException
from olist_django.sns.django_utils import validate_sns_publish_with_count_detail

import payments_api.settings as settings
from apps.payments_api.choices import PaymentsFileItemStatus
from tests.payments_api.factories import PaymentsFileFactory, PaymentsFileItemFactory

pytestmark = pytest.mark.django_db


@validate_sns_publish_with_count_detail({f"{settings.SNS_PREFIX}batch_file__created": 1})
def test_batch_file_model(batch_file_data):
    batch_file = PaymentsFileFactory(**batch_file_data)

    assert str(batch_file) == f"PaymentsFile {batch_file.id}"
    assert batch_file.origin == batch_file_data["origin"]
    assert batch_file.type == batch_file_data["type"]
    assert batch_file.url == batch_file_data["url"]
    assert batch_file.requester == batch_file_data["requester"]
    assert batch_file.checksum == batch_file_data["checksum"]
    assert batch_file.status == batch_file_data["status"]
    assert batch_file.total == batch_file_data["total"]
    assert batch_file.items_done == batch_file_data["items_done"]
    assert batch_file.items_failed == batch_file_data["items_failed"]


@validate_sns_publish_with_count_detail({f"{settings.SNS_PREFIX}batch_file_item__created": 1})
def test_batch_file_item_model(batch_file_item_data, batch_file_instance):
    batch_file_item_data["batch_file"] = batch_file_instance
    batch_file_item = PaymentsFileItemFactory(**batch_file_item_data)

    assert str(batch_file_item) == f"PaymentsFileItem {batch_file_item.id}"
    assert batch_file_item.batch_file == batch_file_instance
    assert batch_file_item.index == batch_file_item_data["index"]
    assert batch_file_item.data == batch_file_item_data["data"]
    assert batch_file_item.status == batch_file_item_data["status"]
    assert batch_file_item.error == batch_file_item_data["error"]


@validate_sns_publish_with_count_detail(
    {
        f"{settings.SNS_PREFIX}batch_file_item__created": 1,
        f"{settings.SNS_PREFIX}batch_file_item__updated": 1,
        f"{settings.SNS_PREFIX}batch_file_item__done": 1,
    }
)
def test_batch_file_item_model_publishes_message_when_status_change_to_done(
    batch_file_item_data,
    batch_file_instance,
):
    batch_file_item_data["batch_file"] = batch_file_instance
    batch_file_item = PaymentsFileItemFactory(**batch_file_item_data)

    batch_file_item.status = PaymentsFileItemStatus.DONE
    batch_file_item.save()


@validate_sns_publish_with_count_detail(
    {
        f"{settings.SNS_PREFIX}batch_file_item__created": 1,
        f"{settings.SNS_PREFIX}batch_file_item__updated": 1,
        f"{settings.SNS_PREFIX}batch_file_item__failed": 1,
    }
)
def test_batch_file_item_model_publishes_message_when_status_change_to_failed(
    batch_file_item_data,
    batch_file_instance,
):
    batch_file_item_data["batch_file"] = batch_file_instance
    batch_file_item = PaymentsFileItemFactory(**batch_file_item_data)

    batch_file_item.status = PaymentsFileItemStatus.FAILED
    batch_file_item.save()


@pytest.mark.parametrize(
    "first_status, second_status",
    [
        (PaymentsFileItemStatus.DONE, PaymentsFileItemStatus.FAILED),
        (PaymentsFileItemStatus.FAILED, PaymentsFileItemStatus.DONE),
    ],
)
def test_batch_file_item_model_does_not_update_the_status_when_it_is_different_from_created(
    batch_file_item_data, batch_file_instance, first_status: str, second_status: str
):
    batch_file_item_data["batch_file"] = batch_file_instance
    batch_file_item = PaymentsFileItemFactory(**batch_file_item_data)

    batch_file_item.status = first_status
    batch_file_item.save()

    with pytest.raises(ImpossibleTransitionException):
        batch_file_item.status = second_status
        batch_file_item.save()
