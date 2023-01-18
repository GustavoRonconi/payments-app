from utils.aws_s3.client import S3Client

from payments_api.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_DEFAULT_REGION,
    AWS_SECRET_ACCESS_KEY,
    AWS_ENDPOINT_URL,
)

s3_client = S3Client(
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION,
    endpoint_url=AWS_ENDPOINT_URL,
)
