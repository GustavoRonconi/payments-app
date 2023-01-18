import csv
import itertools


from utils.aws_s3.client import S3Client

from payments_service.config import settings
from payments_service.models import PaymentDebt

import aiohttp
import asyncio

s3_client_options = {
    "region_name": settings.AWS_DEFAULT_REGION,
    "endpoint_url": settings.AWS_ENDPOINT_URL,
}


class PaymentsApiClient:
    def __init__(self, token, url) -> None:
        self.token = token
        self.url = url

    def _generate_chunks(self, data):
        iterable = iter(data)
        while chunk := tuple(itertools.islice(iterable, settings.CHUNK_SIZE)):
            yield chunk

    async def post(self, session, payment_debt):
        async with session.post(
            url=f"{self.url}/payment-debt/", json=payment_debt.__dict__
        ) as response:
            return response

    async def post_all(self, payments_debts):
        all_responses = []
        async with aiohttp.ClientSession(
            headers={"Authorization": "Bearer {}".format(self.token)}
        ) as session:
            for chunk in self._generate_chunks(payments_debts):
                responses = await asyncio.gather(
                    *[self.post(session, payment_debt) for payment_debt in chunk],
                    return_exceptions=True,
                )
                all_responses.extend(responses)

        return all_responses


class S3CustomClient(S3Client):
    CSV_DELIMITER = ","

    def get_lines_from_csv(self, bucket_name, object_key):
        bucket = self.bucket(bucket_name)
        with bucket.files.download_text_stream(object_key) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.CSV_DELIMITER)
            for line in reader:
                yield PaymentDebt(**line)


s3_client = S3CustomClient(
    settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, **s3_client_options
)

payments_api_client = PaymentsApiClient(settings.TOKEN, settings.PAYMENTS_API_URL)
