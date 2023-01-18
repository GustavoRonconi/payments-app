import logging

from utils.aws_s3.models import S3Event
from utils.services import AsyncModelHandler

from payments_service.clients import s3_client, payments_api_client

logger = logging.getLogger(__name__)


class PaymentsDebtHandler(AsyncModelHandler):
    model_class = S3Event

    def log_result(self, responses):
        for response in responses:
            if getattr(response, "status", 500) != 201:
                logger.error("some records were not inserted")
                raise Exception()

    async def process(self, s3_event: S3Event, **kwargs) -> bool:
        try:
            first_record = s3_event.Records[0]
            bucket_name = first_record.s3.bucket.name
            object_key = first_record.s3.object.key

            payments_debts = s3_client.get_lines_from_csv(bucket_name, object_key)
            responses = await payments_api_client.post_all(payments_debts)
            self.log_result(responses)
        except Exception as e:
            logger.error(f"error processing file: {object_key}")
            raise e

        return True
