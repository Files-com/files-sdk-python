class Error(Exception):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super(Error, self).__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:
                http_body = (
                    "<Could not decode body as utf-8. "
                )

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.response = None

    def __str__(self):
        msg = ""
        if self.http_status:
            msg += "HTTP {} ".format(self.http_status)
        msg += self._message
        return msg

class APIConnectionError(Error):
    pass

class APIError(Error):
    pass

class AuthenticationError(Error):
    pass

class InvalidRequestError(Error):
    pass

class NotImplementedError(Error):
    pass

class PermissionsError(Error):
    pass

class RateLimitError(Error):
    pass

class TooManyRequestsError(Error):
    pass

class ValidationError(Error):
    pass


class InvalidParameterError(InvalidRequestError):
    pass

class MissingParameterError(InvalidRequestError):
    pass