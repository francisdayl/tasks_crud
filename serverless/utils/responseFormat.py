import json


class ResponseFormat:
    def __init__(
        self,
        status_code: int = 200,
        body: dict = {},
        headers: dict = {"Content-Type": "application/json"},
        isBase64Encoded: bool = False,
    ):
        self.status_code = status_code
        self.body = body
        self.headers = headers
        self.isBase64Encoded = isBase64Encoded

    def to_json(self):
        return {
            "statusCode": self.status_code,
            "body": json.dumps(self.body) if self.body else {},
            "headers": self.headers,
            "isBase64Encoded": self.isBase64Encoded,
        }

    def to_dict(self):
        return {
            "statusCode": self.status_code,
            "body": self.body if self.body else {},
            "headers": self.headers,
            "isBase64Encoded": self.isBase64Encoded,
        }
