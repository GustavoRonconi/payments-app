from .mixins import FileDownloaderMixin, FileInformationMixin, FilePreSignURLMixin, FileUploaderMixin


class FileHandler(
    FileDownloaderMixin,
    FileUploaderMixin,
    FilePreSignURLMixin,
    FileInformationMixin,
):
    def __init__(self, bucket, client):
        self.bucket = bucket
        self.client = client


class Bucket:
    """Manipulate bucket actions on S3. You need use bucket with S3Client."""

    def __init__(self, bucket_name, resource, client):
        bucket = resource.Bucket(bucket_name)
        self.files = FileHandler(bucket=bucket, client=client)
