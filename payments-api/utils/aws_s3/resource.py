import boto3


class BaseResource:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, **kwargs):
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._resource = boto3.resource(
            "s3",
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            **kwargs,
        )
        self._client = boto3.client(
            "s3",
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
            **kwargs,
        )

    @property
    def boto3_resource(self):
        return self._resource

    @property
    def boto3_client(self):
        return self._client
