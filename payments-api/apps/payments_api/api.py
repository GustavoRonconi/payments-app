import time
from http import HTTPStatus

import pandas as pd
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ViewSet, ModelViewSet

from .exceptions import CharsetNotUtf8Exception, FileTypeNotCsvException
from .serializers import PaymentsFileUploadSerializer, PaymentDebtSerializer
from payments_api.settings import CSV_DELIMITER, PAYMENTS_API_BUCKET
from payments_api.clients import s3_client
from apps.payments_api.models import PaymentDebt


class PaymentDbtView(ModelViewSet):
    http_method_names: list[str] = ["post"]
    permission_classes = (IsAuthenticated,)
    queryset = PaymentDebt.objects.all().order_by("debt_id")
    serializer_class = PaymentDebtSerializer


class PaymentsFileUploadView(ViewSet):
    http_method_names: list[str] = ["post", "options"]
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = PaymentsFileUploadSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request: Request) -> Response:
        serializer = PaymentsFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_uploaded = request.data.get("file")
        origin = request.data.get("origin")
        batch_type = request.data.get("type")
        requester = request.data.get("requester")
        filename = file_uploaded.name

        if not filename.endswith(".csv") or file_uploaded.content_type != "text/csv":
            raise FileTypeNotCsvException()
        if request.data.encoding != "utf-8":
            raise CharsetNotUtf8Exception()

        new_filename = f"{filename[:-4]}_{round(time.time()*1000)}.csv"

        file_dataframe = pd.read_csv(file_uploaded.file, sep=None, engine="python")
        file_dataframe.to_csv(f"/tmp/{new_filename}", sep=CSV_DELIMITER, index=False)
        with open(f"/tmp/{new_filename}", "rb") as csvfile:
            s3_client.bucket(PAYMENTS_API_BUCKET).files.upload(
                file_object=csvfile,
                key=f"{origin}/{batch_type}/{requester}/{new_filename}",
            )
        return Response(f"'{filename}' file uploaded", status=HTTPStatus.ACCEPTED)
