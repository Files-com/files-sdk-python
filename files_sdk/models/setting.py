import builtins  # noqa: F401
from files_sdk.models.settings import Settings
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Setting:
    default_attributes = {}

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Setting.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Setting.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def languages(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    Api.send_request("GET", "/settings/languages", params, options)


def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request("GET", "/settings", params, options)
    return Settings(response.data, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   domain (required) - string
def get_domain(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "domain" in params and not isinstance(params["domain"], str):
        raise InvalidParameterError("Bad parameter: domain must be an str")
    if "domain" not in params:
        raise MissingParameterError("Parameter missing: domain")
    response, options = Api.send_request(
        "GET", "/settings/domain", params, options
    )
    return Settings(response.data, options)


def new(*args, **kwargs):
    return Setting(*args, **kwargs)
