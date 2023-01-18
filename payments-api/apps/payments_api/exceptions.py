from rest_framework.exceptions import ValidationError


class FileTypeNotCsvException(ValidationError):
    default_detail = "Uploaded file must be '.csv'"


class CharsetNotUtf8Exception(ValidationError):
    default_detail = "Uploaded file must have 'UTF-8' charset"
