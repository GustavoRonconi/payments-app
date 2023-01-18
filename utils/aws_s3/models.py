import typing

from pydantic import BaseModel


class S3Bucket(BaseModel):
    name: str


class S3Object(BaseModel):
    key: str


class S3Information(BaseModel):
    object: S3Object
    bucket: S3Bucket


class S3Record(BaseModel):
    s3: S3Information


class S3Event(BaseModel):
    Records: typing.List[S3Record]
