import io
from collections import OrderedDict
from unittest import mock

import pytest

from payments_service.clients import S3CustomClient


@pytest.fixture
def s3_custom_client():
    return S3CustomClient("key", "secret", **{"region_name": "us-xablau-1"})

