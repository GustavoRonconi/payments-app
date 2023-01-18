from unittest import mock

import pytest
from rest_framework.exceptions import ValidationError

pytestmark = pytest.mark.django_db


def test_batch_file_serializer(batch_file_serializer, batch_file_data):
    serializer = batch_file_serializer(data=batch_file_data)
    assert serializer.is_valid()
    assert serializer.validated_data == batch_file_data


@pytest.mark.parametrize(
    "field",
    [
        "origin",
        "type",
        "url",
        "requester",
        "checksum",
    ],
)
def test_batch_file_serializer_required_fields(batch_file_serializer, batch_file_data, field):
    del batch_file_data[field]
    serializer = batch_file_serializer(data=batch_file_data)
    assert not serializer.is_valid()
    assert len(serializer.errors) == 1
    assert serializer.errors[field] == ["This field is required."]


@pytest.mark.parametrize(
    "choice",
    [
        "created",
        "done",
        "failed",
        "partially_failed",
    ],
)
def test_batch_file_serializer_status_choices(batch_file_serializer, batch_file_data, choice):
    batch_file_data["status"] = choice
    serializer = batch_file_serializer(data=batch_file_data)
    assert serializer.is_valid()
    assert serializer.validated_data == batch_file_data


def test_batch_file_serializer_invalid_status_choice(batch_file_serializer, batch_file_data):
    batch_file_data["status"] = "invalid"
    serializer = batch_file_serializer(data=batch_file_data)
    assert not serializer.is_valid()
    assert len(serializer.errors) == 1
    assert serializer.errors["status"] == ['"invalid" is not a valid choice.']


def test_batch_file_retrieve_serializer_when_url_s3_invalid(batch_file_retrieve_serializer, batch_file_data):
    batch_file_data["url"] = "http://invalid.com"
    serializer = batch_file_retrieve_serializer(data=batch_file_data)
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid()
        serializer.data

    assert excinfo.value.detail[0] == "Invalid S3 URL"


@mock.patch("olist_aws.s3.bucket.FileHandler.pre_sign_url_from_file")
@pytest.mark.parametrize(
    "url, expected, presigned",
    [
        ("http://s3.amazonaws.com/bucket/key", "http://s3.amazonaws.com/bucket/key", False),
        ("http://bucket.s3.amazonaws.com/key", "http://s3.amazonaws.com/bucket/key?chave=123", True),
    ],
    ids=[
        "default_url",
        "token_url",
    ],
)
def test_batch_file_retrieve_serializer_when_url_s3_valid(
    mock_pre_sign_url_from_file, batch_file_retrieve_serializer, batch_file_data, url, expected, presigned
):
    mock_pre_sign_url_from_file.return_value = "http://s3.amazonaws.com/bucket/key?chave=123"
    batch_file_data["url"] = url
    serializer = batch_file_retrieve_serializer(data=batch_file_data)
    assert serializer.is_valid()
    assert serializer.data["url"] == expected
    assert mock_pre_sign_url_from_file.called == presigned


def test_batch_file_item_serializer(batch_file_item_serializer, batch_file_item_data, batch_file_instance):
    serializer = batch_file_item_serializer(data=batch_file_item_data)
    assert serializer.is_valid()

    batch_file_item_data["batch_file"] = batch_file_instance
    assert serializer.validated_data == batch_file_item_data


@pytest.mark.parametrize(
    "field",
    ["batch_file", "index", "data"],
)
def test_batch_file_item_serializer_required_fields(batch_file_item_serializer, batch_file_item_data, field):
    del batch_file_item_data[field]
    serializer = batch_file_item_serializer(data=batch_file_item_data)

    assert not serializer.is_valid()
    assert len(serializer.errors) == 1
    assert serializer.errors[field] == ["This field is required."]


@pytest.mark.parametrize(
    "choice",
    [
        "created",
        "done",
        "failed",
    ],
)
def test_batch_file_item_serializer_status_choices(
    batch_file_item_serializer, batch_file_item_data, batch_file_instance, choice
):
    batch_file_item_data["status"] = choice
    serializer = batch_file_item_serializer(data=batch_file_item_data)
    assert serializer.is_valid()

    batch_file_item_data["batch_file"] = batch_file_instance
    assert serializer.validated_data == batch_file_item_data


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("status", "invalid", '"invalid" is not a valid choice.'),
        ("batch_file", "invalid", "“invalid” is not a valid UUID."),
        (
            "batch_file",
            "15cc9b47-c90b-426d-b4db-a5aa93bfcd78",
            'Invalid pk "15cc9b47-c90b-426d-b4db-a5aa93bfcd78" - object does not exist.',
        ),
    ],
)
def test_batch_file_item_serializer_invalid_status_choice(
    batch_file_item_serializer, batch_file_item_data, field, value, error
):
    batch_file_item_data[field] = value
    serializer = batch_file_item_serializer(data=batch_file_item_data)
    assert not serializer.is_valid()
    assert len(serializer.errors) == 1
    assert serializer.errors[field] == [error]
