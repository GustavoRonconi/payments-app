from .bucket import Bucket
from .resource import BaseResource


class S3Client(BaseResource):
    """
    Client to manipulate actions on S3.

    Example for downloading files:

    s3_client = S3Client('my_access_key_id', 'my_secret_access_key')
    s3_client.bucket('my_bucket').files.download('file')
    """

    def bucket(self, bucket_name):
        return Bucket(bucket_name, resource=self.boto3_resource, client=self.boto3_client)
