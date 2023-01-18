import io
import warnings

import botocore

from .exceptions import DownloadError
from .resource import BaseResource

message = (
    "downloader module was deprecated, use client, "
    "for more information see: https://github.com/olist/olist-aws/pull/15"
)
warnings.warn(message)


class FileDownloader(BaseResource):
    def download(self, bucket, key):
        """Get 'key' from 'bucket' and return buffer of io.BytesIO"""
        data = io.BytesIO()

        try:
            self._resource.Bucket(bucket).download_fileobj(key, data)
        except botocore.exceptions.ClientError as ex:
            raise DownloadError() from ex

        return data

    def download_text_stream(self, bucket, key, decode_to="utf-8-sig"):
        """Get 'key' from 'bucket' and return buffer of io.StringIO"""
        with self.download(bucket, key) as buffer:
            content = io.StringIO(buffer.getvalue().decode(decode_to))
        return content
