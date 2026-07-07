import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class CrashReport:
    default_attributes = {
        "id": None,  # int64 - Crash Report ID
        "build": None,  # string
        "platform": None,  # string
        "product_name": None,  # string
        "version": None,  # string
        "comment": None,  # string
        "email": None,  # string
        "platform_version": None,  # string
        "release_channel": None,  # string
        "dump_file": None,  # file
        "log_file": None,  # file
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in CrashReport.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in CrashReport.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The CrashReport object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   build (required) - string
#   platform (required) - string
#   product_name (required) - string
#   version (required) - string
#   comment - string
#   email - string
#   platform_version - string
#   release_channel - string
#   dump_file - file
#   log_file - file
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "build" in params and not isinstance(params["build"], str):
        raise InvalidParameterError("Bad parameter: build must be an str")
    if "platform" in params and not isinstance(params["platform"], str):
        raise InvalidParameterError("Bad parameter: platform must be an str")
    if "product_name" in params and not isinstance(
        params["product_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: product_name must be an str"
        )
    if "version" in params and not isinstance(params["version"], str):
        raise InvalidParameterError("Bad parameter: version must be an str")
    if "comment" in params and not isinstance(params["comment"], str):
        raise InvalidParameterError("Bad parameter: comment must be an str")
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "platform_version" in params and not isinstance(
        params["platform_version"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: platform_version must be an str"
        )
    if "release_channel" in params and not isinstance(
        params["release_channel"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: release_channel must be an str"
        )
    if "build" not in params:
        raise MissingParameterError("Parameter missing: build")
    if "platform" not in params:
        raise MissingParameterError("Parameter missing: platform")
    if "product_name" not in params:
        raise MissingParameterError("Parameter missing: product_name")
    if "version" not in params:
        raise MissingParameterError("Parameter missing: version")
    response, options = Api.send_request(
        "POST", "/crash_reports", params, options
    )
    return CrashReport(response.data, options)


def new(*args, **kwargs):
    return CrashReport(*args, **kwargs)
