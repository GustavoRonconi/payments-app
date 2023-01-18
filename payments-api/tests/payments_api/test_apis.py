from unittest import mock

import pytest
from freezegun import freeze_time
from rest_framework import status
from rest_framework.response import Response

from apps.payments_api.choices import PaymentsFileItemStatus, PaymentsFileStatus
from payments_api import settings
from tests.payments_api.factories import PaymentsFileFactory, PaymentsFileItemFactory

pytestmark = pytest.mark.django_db


def test_batch_file_api_unauthorized_client_raises_forbidden(batch_file_api, unauthorized_client_api):
    response = unauthorized_client_api.get(batch_file_api)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("method", ["delete", "put", "patch"])
def test_batch_file_api_when_raises_method_not_allowed(batch_file_api, method, auth_client_api):
    response = auth_client_api.generic(method=method, path=batch_file_api)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_batch_file_detail_api_unauthorized_client_raises_forbidden(
    batch_file_detail_api, unauthorized_client_api
):
    response = unauthorized_client_api.get(batch_file_detail_api)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("method", ["delete", "put", "patch", "post"])
def test_batch_file_detail_api_when_raises_method_not_allowed(batch_file_detail_api, method, auth_client_api):
    response = auth_client_api.generic(method=method, path=batch_file_detail_api)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_batch_file_api_when_get_returns_objects(batch_file_api, auth_client_api):
    payments_api = PaymentsFileFactory.create_batch(3)
    response = auth_client_api.get(batch_file_api)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3
    results = response.data["results"]
    assert results[0]["id"] == str(payments_api[0].id)
    assert results[1]["id"] == str(payments_api[1].id)
    assert results[2]["id"] == str(payments_api[2].id)


@mock.patch("apps.payments_api.serializers.PreSignedUrlField.to_representation")
def test_batch_file_detail_api_when_get_returns_object(
    pre_sign_url_from_file_mock, batch_file_detail_api, auth_client_api, batch_file_instance
):
    pre_sign_url_from_file_mock.return_value = batch_file_instance.url
    response = auth_client_api.get(batch_file_detail_api)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(batch_file_instance.id)
    assert response.data["origin"] == batch_file_instance.origin
    assert response.data["type"] == batch_file_instance.type
    assert response.data["url"] == batch_file_instance.url
    assert response.data["requester"] == batch_file_instance.requester
    assert response.data["checksum"] == batch_file_instance.checksum
    assert response.data["status"] == str(batch_file_instance.status)


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
def test_batch_file_api_returns_400_when_required_field_is_missing(
    batch_file_api, auth_client_api, batch_file_data, field
):
    del batch_file_data[field]
    response = auth_client_api.post(batch_file_api, data=batch_file_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {field: ["This field is required."]}


def test_batch_file_api_returns_400_when_invalid_status_is_given(
    batch_file_api, auth_client_api, batch_file_data
):
    batch_file_data["status"] = "invalid"
    response = auth_client_api.post(batch_file_api, data=batch_file_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"status": ['"invalid" is not a valid choice.']}


@pytest.mark.parametrize(
    "choice",
    [
        "created",
        "done",
    ],
)
def test_batch_file_api_when_status_success(batch_file_api, auth_client_api, batch_file_data, choice):
    batch_file_data["status"] = choice
    response = auth_client_api.post(batch_file_api, data=batch_file_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == choice


def test_batch_file_api_when_post_returns_object(batch_file_api, auth_client_api, batch_file_data):
    response = auth_client_api.post(batch_file_api, data=batch_file_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] is not None
    assert response.data["created_at"] is not None
    assert response.data["updated_at"] is not None
    assert response.data["origin"] == batch_file_data["origin"]
    assert response.data["type"] == batch_file_data["type"]
    assert response.data["url"] == batch_file_data["url"]
    assert response.data["requester"] == batch_file_data["requester"]
    assert response.data["checksum"] == batch_file_data["checksum"]
    assert response.data["status"] == batch_file_data["status"]


@pytest.mark.parametrize(
    "fields_to_change, expected_status",
    [
        ({}, status.HTTP_303_SEE_OTHER),
        ({"requester": "new_requester"}, status.HTTP_303_SEE_OTHER),
        ({"checksum": "new_hash"}, status.HTTP_201_CREATED),
    ],
)
def test_batch_file_api_creating_two_payments_api(
    batch_file_api, auth_client_api, batch_file_data, fields_to_change, expected_status
):
    first_response = auth_client_api.post(batch_file_api, data=batch_file_data)
    assert first_response.status_code == status.HTTP_201_CREATED

    second_response = auth_client_api.post(batch_file_api, data=batch_file_data | fields_to_change)
    assert second_response.status_code == expected_status


def test_batch_file_item_api_unauthorized_client_raises_forbidden(
    batch_file_item_api, unauthorized_client_api
):
    response = unauthorized_client_api.get(batch_file_item_api)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("method", ["delete", "put", "patch"])
def test_batch_file_item_api_when_raises_method_not_allowed(batch_file_item_api, method, auth_client_api):
    response = auth_client_api.generic(method=method, path=batch_file_item_api)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_batch_file_item_detail_api_unauthorized_client_raises_forbidden(
    batch_file_item_detail_api, unauthorized_client_api
):
    response = unauthorized_client_api.get(batch_file_item_detail_api)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("method", ["delete", "put", "post"])
def test_batch_file_item_detail_api_when_raises_method_not_allowed(
    batch_file_item_detail_api, method, auth_client_api
):
    response = auth_client_api.generic(method=method, path=batch_file_item_detail_api)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_batch_file_item_api_returns_a_list_of_items_when_requested(batch_file_item_api, auth_client_api):
    batch_file_items = PaymentsFileItemFactory.create_batch(3)
    response = auth_client_api.get(batch_file_item_api)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3
    results = response.data["results"]
    assert results[0]["id"] == str(batch_file_items[0].id)
    assert results[1]["id"] == str(batch_file_items[1].id)
    assert results[2]["id"] == str(batch_file_items[2].id)


def test_batch_file_item_detail_api_returns_a_batch_file_item_when_requested(
    batch_file_item_detail_api, auth_client_api, batch_file_item_instance, batch_file_instance
):
    response = auth_client_api.get(batch_file_item_detail_api)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(batch_file_item_instance.id)
    assert response.data["batch_file"] == batch_file_item_instance.batch_file.id
    assert response.data["index"] == batch_file_item_instance.index
    assert response.data["data"] == batch_file_item_instance.data
    assert response.data["status"] == str(batch_file_item_instance.status)


@pytest.mark.parametrize(
    "field",
    ["batch_file", "index", "data"],
)
def test_batch_file_item_api_returns_400_when_required_field_is_missing(
    batch_file_item_api, auth_client_api, batch_file_item_data, field
):
    del batch_file_item_data[field]
    response = auth_client_api.post(batch_file_item_api, data=batch_file_item_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {field: ["This field is required."]}


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
def test_batch_file_item_api_returns_400_when_given_a_field_with_invalid_value(
    batch_file_item_api, auth_client_api, batch_file_item_data, field, value, error
):
    batch_file_item_data[field] = value
    response = auth_client_api.post(batch_file_item_api, data=batch_file_item_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {field: [error]}


@pytest.mark.parametrize(
    "choice",
    [
        "created",
        "done",
        "failed",
    ],
)
def test_batch_file_item_api_returns_201_when_a_valid_status_is_given(
    batch_file_item_api, auth_client_api, batch_file_item_data, choice
):
    batch_file_item_data["status"] = choice
    response = auth_client_api.post(batch_file_item_api, data=batch_file_item_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == choice


def test_batch_file_item_api_returns_the_created_batch_file_item_on_success(
    batch_file_item_api, auth_client_api, batch_file_item_data
):
    response = auth_client_api.post(batch_file_item_api, data=batch_file_item_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] is not None
    assert response.data["created_at"] is not None
    assert response.data["updated_at"] is not None
    assert response.data["batch_file"] == batch_file_item_data["batch_file"]
    assert response.data["index"] == batch_file_item_data["index"]
    assert response.data["data"] == batch_file_item_data["data"]
    assert response.data["status"] == batch_file_item_data["status"]


@pytest.mark.parametrize(
    "fields_to_change, expected_status",
    [
        ({}, status.HTTP_303_SEE_OTHER),
        ({"data": {"data_key_2": "data-data-2"}}, status.HTTP_303_SEE_OTHER),
        ({"index": 2}, status.HTTP_201_CREATED),
    ],
)
def test_batch_file_item_api_creating_two_batch_file_items(
    batch_file_item_api, auth_client_api, batch_file_item_data, fields_to_change, expected_status
):
    first_response = auth_client_api.post(batch_file_item_api, data=batch_file_item_data)
    assert first_response.status_code == status.HTTP_201_CREATED

    second_response = auth_client_api.post(batch_file_item_api, data=batch_file_item_data | fields_to_change)
    assert second_response.status_code == expected_status


def test_batch_file_item_api_patch_returns_the_updated_batch_file_item_on_success(
    batch_file_item_detail_api, auth_client_api, batch_file_item_instance
):
    updated_item = auth_client_api.patch(
        batch_file_item_detail_api, data={"id": batch_file_item_instance.id, "status": "done"}
    )

    assert updated_item.status_code == status.HTTP_200_OK
    assert updated_item.data["id"] is not None
    assert updated_item.data["created_at"] is not None
    assert updated_item.data["updated_at"] is not None
    assert updated_item.data["batch_file"] == batch_file_item_instance.batch_file.id
    assert updated_item.data["index"] == batch_file_item_instance.index
    assert updated_item.data["data"] == batch_file_item_instance.data
    assert updated_item.data["status"] == "done"


def assert_expected_api_response(api_response: Response, expected_items: list[object]) -> None:
    response_items_ids = [item["id"] for item in api_response.data["results"]]
    for expected_item in expected_items:
        assert str(expected_item.id) in response_items_ids
    assert len(response_items_ids) == len(expected_items)


@pytest.mark.parametrize(
    "time_field",
    ["created_at", "updated_at"],
)
def test_batch_file_api_filter_by_created_at(batch_file_api, auth_client_api, time_field):
    with freeze_time("2022-10-01"):
        batch_file_first_date_1 = PaymentsFileFactory()
        batch_file_first_date_2 = PaymentsFileFactory()
        batch_file_first_date_3 = PaymentsFileFactory()
    with freeze_time("2022-10-02"):
        batch_file_second_date_1 = PaymentsFileFactory()
        batch_file_second_date_2 = PaymentsFileFactory()
    with freeze_time("2022-10-03"):
        batch_file_third_date = PaymentsFileFactory()

    response_1 = auth_client_api.get(batch_file_api, {f"{time_field}__date__range": "2022-10-01,2022-10-01"})
    assert_expected_api_response(
        response_1, [batch_file_first_date_1, batch_file_first_date_2, batch_file_first_date_3]
    )

    response_2 = auth_client_api.get(batch_file_api, {f"{time_field}__date__range": "2022-10-01,2022-10-02"})
    assert_expected_api_response(
        response_2,
        [
            batch_file_first_date_1,
            batch_file_first_date_2,
            batch_file_first_date_3,
            batch_file_second_date_1,
            batch_file_second_date_2,
        ],
    )

    response_3 = auth_client_api.get(batch_file_api, {f"{time_field}__range": "2022-10-02,2022-10-04"})
    assert_expected_api_response(
        response_3,
        [
            batch_file_second_date_1,
            batch_file_second_date_2,
            batch_file_third_date,
        ],
    )


@pytest.mark.parametrize(
    "field, value_1, value_2, value_3",
    [
        ("status", PaymentsFileStatus.CREATED, PaymentsFileStatus.DONE, PaymentsFileStatus.FAILED),
        ("origin", "origin_1", "origin_2", "origin_3"),
        ("type", "type_1", "type_2", "type_3"),
    ],
)
def test_batch_file_api_filter_by_status(batch_file_api, auth_client_api, field, value_1, value_2, value_3):
    batch_file_value_1_instance_1 = PaymentsFileFactory(**{field: value_1})
    batch_file_value_1_instance_2 = PaymentsFileFactory(**{field: value_1})
    batch_file_value_1_instance_3 = PaymentsFileFactory(**{field: value_1})
    batch_file_value_2_instance_1 = PaymentsFileFactory(**{field: value_2})
    batch_file_value_2_instance_2 = PaymentsFileFactory(**{field: value_2})
    batch_file_value_3 = PaymentsFileFactory(**{field: value_3})

    response_1 = auth_client_api.get(batch_file_api, {field: value_1})
    assert_expected_api_response(
        response_1,
        [batch_file_value_1_instance_1, batch_file_value_1_instance_2, batch_file_value_1_instance_3],
    )

    response_2 = auth_client_api.get(batch_file_api, {field: value_2})
    assert_expected_api_response(response_2, [batch_file_value_2_instance_1, batch_file_value_2_instance_2])

    response_3 = auth_client_api.get(batch_file_api, {f"{field}__in": f"{value_1},{value_3}"})
    assert_expected_api_response(
        response_3,
        [
            batch_file_value_1_instance_1,
            batch_file_value_1_instance_2,
            batch_file_value_1_instance_3,
            batch_file_value_3,
        ],
    )


def test_batch_file_item_api_filter_by_batch_file(batch_file_item_api, auth_client_api):
    batch_file_1 = PaymentsFileFactory()
    batch_file_2 = PaymentsFileFactory()
    batch_file_1_item_1 = PaymentsFileItemFactory(batch_file=batch_file_1)
    batch_file_1_item_2 = PaymentsFileItemFactory(batch_file=batch_file_1)
    batch_file_1_item_3 = PaymentsFileItemFactory(batch_file=batch_file_1)
    batch_file_2_item_1 = PaymentsFileItemFactory(batch_file=batch_file_2)
    batch_file_2_item_2 = PaymentsFileItemFactory(batch_file=batch_file_2)

    response_1 = auth_client_api.get(batch_file_item_api, {"batch_file": batch_file_1.id})
    assert_expected_api_response(response_1, [batch_file_1_item_1, batch_file_1_item_2, batch_file_1_item_3])

    response_2 = auth_client_api.get(batch_file_item_api, {"batch_file": batch_file_2.id})
    assert_expected_api_response(response_2, [batch_file_2_item_1, batch_file_2_item_2])


def test_batch_file_item_api_filter_by_status(batch_file_item_api, auth_client_api):
    batch_file_item_created_1 = PaymentsFileItemFactory(status=PaymentsFileItemStatus.CREATED)
    batch_file_item_created_2 = PaymentsFileItemFactory(status=PaymentsFileItemStatus.CREATED)
    batch_file_item_created_3 = PaymentsFileItemFactory(status=PaymentsFileItemStatus.CREATED)
    batch_file_item_done_1 = PaymentsFileItemFactory(status=PaymentsFileItemStatus.DONE)
    batch_file_item_done_2 = PaymentsFileItemFactory(status=PaymentsFileItemStatus.DONE)
    PaymentsFileItemFactory(status=PaymentsFileItemStatus.FAILED)

    response_1 = auth_client_api.get(batch_file_item_api, {"status": PaymentsFileItemStatus.CREATED})
    assert_expected_api_response(
        response_1, [batch_file_item_created_1, batch_file_item_created_2, batch_file_item_created_3]
    )

    response_2 = auth_client_api.get(batch_file_item_api, {"status": PaymentsFileItemStatus.DONE})
    assert_expected_api_response(response_2, [batch_file_item_done_1, batch_file_item_done_2])


def test_batch_file_upload_api_unauthorized_client_raises_forbidden(
    batch_file_upload_api, unauthorized_client_api
):
    response = unauthorized_client_api.get(batch_file_upload_api)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("method", ["get", "delete", "put", "patch"])
def test_batch_file_upload_api_when_raises_method_not_allowed(batch_file_upload_api, method, auth_client_api):
    response = auth_client_api.generic(method=method, path=batch_file_upload_api)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@freeze_time("2022-10-01")
@mock.patch("apps.payments_api.api.s3_client")
def test_payments_api_upload__returns_202_on_success(
    mock_s3_client: mock.MagicMock, s3_client, batch_file_upload_api, auth_client_api
):
    bucket = settings.PAYMENTOS_API_BUCKET
    s3_client.boto3_client.create_bucket(Bucket=bucket)
    mock_s3_client.bucket = s3_client.bucket

    with open("/tmp/test.csv", "wb") as test_file:
        test_file.write(b"col_1,col_2,col_3,col_4")
    with open("/tmp/test.csv", "rb") as test_file:
        response = auth_client_api.post(
            batch_file_upload_api,
            data={
                "file": test_file,
                "origin": "origin_value",
                "type": "type_value",
                "requester": "requester_value",
            },
            format="multipart",
        )

    assert response.status_code == status.HTTP_202_ACCEPTED

    get_object_response = s3_client.boto3_client.get_object(
        Bucket=bucket, Key="origin_value/type_value/requester_value/test_1664582400000.csv"
    )
    file_data = get_object_response["Body"].read().decode("utf-8")
    assert file_data == "col_1;col_2;col_3;col_4\n"


def test_payments_api_upload_returns_400_when_file_is_not_csv(batch_file_upload_api, auth_client_api):
    with open("/tmp/test.txt", "wb") as test_file:
        test_file.write(b"col_1,col_2,col_3,col_4")
    with open("/tmp/test.txt", "rb") as test_file:
        response = auth_client_api.post(
            batch_file_upload_api,
            data={
                "file": test_file,
                "origin": "origin_value",
                "type": "type_value",
                "requester": "requester_value",
            },
            format="multipart",
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data[0]) == "Uploaded file must be '.csv'"


@freeze_time("2022-10-01")
@mock.patch("apps.payments_api.api.settings")
@mock.patch("apps.payments_api.api.s3_client")
def test_payments_api_upload_alters_separator_to_settings_csv_delimiter_value(
    mock_s3_client, mock_settings, s3_client, batch_file_upload_api, auth_client_api
):
    bucket = settings.PAYMENTOS_API_BUCKET
    s3_client.boto3_client.create_bucket(Bucket=bucket)
    mock_s3_client.bucket = s3_client.bucket

    mock_settings.CSV_DELIMITER = "\t"
    mock_settings.PAYMENTOS_API_BUCKET = bucket
    with open("/tmp/test.csv", "wb") as test_file:
        test_file.write(b"col_1,col_2,col_3,col_4")
    with open("/tmp/test.csv", "rb") as test_file:
        response = auth_client_api.post(
            batch_file_upload_api,
            data={
                "file": test_file,
                "origin": "origin_value",
                "type": "type_value",
                "requester": "requester_value",
            },
            format="multipart",
        )

    assert response.status_code == status.HTTP_202_ACCEPTED

    get_object_response = s3_client.boto3_client.get_object(
        Bucket=bucket, Key="origin_value/type_value/requester_value/test_1664582400000.csv"
    )
    file_data = get_object_response["Body"].read().decode("utf-8")
    assert file_data == "col_1\tcol_2\tcol_3\tcol_4\n"
