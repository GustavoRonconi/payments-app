import pytest

from payments_service.handlers import S3CsvSplitHandler

s3_events = [
    {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": "payments-consolidation/individual/rafael.correia/2019-5-23_9-44-43.csv"
                    },
                    "bucket": {"name": "olist-adminapp"},
                },
            }
        ]
    },
    {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": "controller-consolidation/individual/francesco.cruz/2021-10-1_17-31-20.csv"
                    },
                    "bucket": {"name": "olist-adminapp"},
                }
            }
        ]
    },
]


@pytest.fixture
def s3_csv_split_handler():
    return S3CsvSplitHandler()
