import base64
import hashlib
import hmac
import json

from .exceptions import S3InvalidPolicy


class BucketSigner:
    def __init__(self, bucket, access_key, secret_key, max_upload_size):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        self.max_upload_size = max_upload_size

    def sign_request(self, request_payload):
        headers = request_payload.get("headers", None)

        if headers:
            response_data = self.sign_headers(headers)
        else:
            if not self.is_valid_policy(request_payload):
                raise S3InvalidPolicy("Policy tampered with client-side before sending it off")
            response_data = self.sign_policy_document(request_payload)

        return response_data

    def is_valid_policy(self, policy_document):
        bucket = ""
        parsed_max_size = 0

        for condition in policy_document["conditions"]:
            if isinstance(condition, list) and condition[0] == "content-length-range":
                parsed_max_size = condition[2]
            else:
                if condition.get("bucket", None):
                    bucket = condition["bucket"]

        return bucket == self.bucket and parsed_max_size == self.max_upload_size

    def sign_policy_document(self, policy_document):
        policy = base64.b64encode(json.dumps(policy_document).encode("utf-8"))
        signature = base64.b64encode(hmac.new(self.secret_key.encode("utf-8"), policy, hashlib.sha1).digest())
        return {"policy": policy.decode("utf-8"), "signature": signature.decode("utf-8")}

    def sign_headers(self, headers):
        signature = base64.b64encode(
            hmac.new(self.secret_key.encode("utf-8"), headers.encode("utf-8"), hashlib.sha1).digest()
        )
        return {"signature": signature.decode("utf-8")}
