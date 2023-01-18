from loafer.ext.aws.routes import SNSQueueRoute

from payments_service.config import settings
from payments_service.handlers import PaymentsDebtHandler

provider_options = {
    "endpoint_url": settings.AWS_ENDPOINT_URL,
    "region_name": settings.AWS_DEFAULT_REGION,
    "options": {
        "MaxNumberOfMessages": 10,
        "WaitTimeSeconds": settings.WAIT_TIME_SECONDS,
    },
}


routes = (
    SNSQueueRoute(
        settings.PAYMENTS_DEBT_QUEUE,
        provider_options=provider_options,
        handler=PaymentsDebtHandler(),
    ),
)
