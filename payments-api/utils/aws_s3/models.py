import typing

from simple_model import Model


class S3Bucket(Model):
    name: str


class S3Object(Model):
    key: str


class S3Information(Model):
    object: S3Object
    bucket: S3Bucket


class S3Record(Model):
    s3: S3Information


class S3Event(Model):
    Records: typing.List[S3Record]
