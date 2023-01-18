import os

import pytest
from moto import mock_s3
from olist_aws.s3.client import S3Client
from rest_framework.reverse import reverse

from apps.payments_api.serializers import (
    PaymentsFileItemSerializer,
    PaymentsFileRetrieveSerializer,
    PaymentsFileSerializer,
)
from tests.payments_api.factories import PaymentsFileFactory, PaymentsFileItemFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def batch_file_instance():
    return PaymentsFileFactory()


@pytest.fixture
def batch_file_item_instance():
    return PaymentsFileItemFactory()


@pytest.fixture
def batch_file_serializer():
    return PaymentsFileSerializer


@pytest.fixture
def batch_file_retrieve_serializer():
    return PaymentsFileRetrieveSerializer


@pytest.fixture
def batch_file_item_serializer():
    return PaymentsFileItemSerializer


@pytest.fixture
def batch_file_api():
    return reverse("payments_api:batch-files-list")


@pytest.fixture
def batch_file_item_api():
    return reverse("payments_api:batch-file-items-list")


@pytest.fixture
def batch_file_upload_api():
    return reverse("payments_api:batch-files-upload-list")


@pytest.fixture
def batch_file_detail_api(batch_file_instance):
    return reverse("payments_api:batch-files-detail", args=[batch_file_instance.id])


@pytest.fixture
def batch_file_item_detail_api(batch_file_item_instance):
    return reverse("payments_api:batch-file-items-detail", args=[batch_file_item_instance.id])


@pytest.fixture
def batch_file_data():
    return {
        "origin": "origin",
        "type": "type",
        "url": "http://localhost:5000",
        "requester": "requester",
        "checksum": "hash",
        "status": "created",
        "total": 10,
        "items_done": 3,
        "items_failed": 2,
    }


@pytest.fixture
def batch_file_item_data(batch_file_instance):
    return {
        "batch_file": batch_file_instance.id,
        "index": 1,
        "data": {"data_key": "data-data"},
        "status": "created",
        "error": {"error_key": "error-data"},
    }


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"  # pragma: allowlist secret
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"  # pragma: allowlist secret
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def s3_client(aws_credentials):
    with mock_s3():
        yield S3Client("testing", "testing", region_name="us-east-1")
