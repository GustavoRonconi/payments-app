import io

import boto3
import botocore

from .exceptions import DownloadError, FileTypeError, UploadError


class FileUploaderMixin:
    def upload(self, file_object, key, **kwargs):
        """Method to upload a fileobject to a s3 bucket

        :type file_object: io.BytesIO
        :param file_object: file to be uploaded

        :type key: string
        :param key: The name of the key to upload to

        :type key: dictionary
        :param kwargs: Extra options for send to upload_fileobj
        """
        try:
            self.bucket.upload_fileobj(file_object, key, **kwargs)
        except boto3.exceptions.S3UploadFailedError as ex:
            raise UploadError() from ex
        except TypeError as ex:
            msg = "An io.BytesIO object is expected as a file"
            raise FileTypeError(msg) from ex

    def upload_text_stream(self, file_object, key, **kwargs):
        try:
            content = file_object.getvalue().encode("utf-8")
        except AttributeError as ex:
            msg = "An io.StringIO object is expected as a file"
            raise FileTypeError(msg) from ex
        else:
            file_object = io.BytesIO(content)
            self.upload(file_object, key, **kwargs)

    def upload_bytes_stream(self, file_object, key, **kwargs):
        if not isinstance(file_object, bytes):
            msg = "A bytestream is expected"
            raise FileTypeError(msg)
        else:
            file_object = io.BytesIO(file_object)
            self.upload(file_object, key, **kwargs)


class FileDownloaderMixin:
    def download(self, key, **kwargs):
        """Get 'key' and return buffer of io.BytesIO"""
        data = io.BytesIO()

        try:
            self.bucket.download_fileobj(key, data, **kwargs)
        except botocore.exceptions.ClientError as ex:
            raise DownloadError() from ex

        return data

    def download_text_stream(self, key, decode_to="utf-8-sig", **kwargs):
        """Get 'key' and return buffer of io.StringIO"""
        with self.download(key, **kwargs) as buffer:
            content = io.StringIO(buffer.getvalue().decode(decode_to))
        return content


class FilePreSignURLMixin:
    def pre_sign_url_from_file(self, key, expires_in=3600, **kwargs):
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket.name, "Key": key},
            ExpiresIn=expires_in,
            **kwargs,
        )

    def generate_presigned_post_url(self, key, expires_in=3600, **kwargs):
        return self.client.generate_presigned_post(self.bucket.name, key, ExpiresIn=expires_in, **kwargs)


class FileInformationMixin:
    def get_metadata(self, key, **kwargs):
        """Method to get metadata information of a key

        :type key: string
        :param key: The name of the key to get metadata

        :type key: dictionary
        :param kwargs: Extra options for send to head_object

        :rtype: dictionary
        :returns: Dictionary with metadata about key
        """
        return self.client.head_object(
            Bucket=self.bucket.name,
            Key=key,
            **kwargs,
        ).get("Metadata")
