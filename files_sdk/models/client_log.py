import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ClientLog:
    default_attributes = {}

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in ClientLog.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ClientLog.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


# Parameters:
#   identifier (required) - string - Client log stream identifier
#   body (required) - string - NDJSON log records
def log(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "identifier" in params and not isinstance(params["identifier"], str):
        raise InvalidParameterError("Bad parameter: identifier must be an str")
    if "body" in params and not isinstance(params["body"], str):
        raise InvalidParameterError("Bad parameter: body must be an str")
    if "identifier" not in params:
        raise MissingParameterError("Parameter missing: identifier")
    if "body" not in params:
        raise MissingParameterError("Parameter missing: body")
    Api.send_request("POST", "/client_logs/log", params, options)


def new(*args, **kwargs):
    return ClientLog(*args, **kwargs)
