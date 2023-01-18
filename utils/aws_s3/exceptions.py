class S3InvalidPolicy(Exception):
    """A exception for policy tampered with client-side before sending it off"""


class DownloadError(Exception):
    """Download error exception"""


class UploadError(Exception):
    """Upload error exception"""


class FileTypeError(TypeError):
    """Upload file type error"""
