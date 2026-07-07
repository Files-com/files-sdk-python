import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Release:
    default_attributes = {
        "version": None,  # string - Native release version
        "description": None,  # string - Native release description
        "native_release_packages": None,  # array(object) - A list of native release packages
        "title": None,  # string - Native release title
        "product": None,  # string - Native release product
        "version_major": None,  # int64
        "version_minor": None,  # int64
        "version_patch": None,  # int64
        "version_build": None,  # int64
        "oem": None,  # string
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Release.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Release.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The Release object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   product - string
#   platform - string
#   architecture - string
#   ext - string
def get_latest(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "product" in params and not isinstance(params["product"], str):
        raise InvalidParameterError("Bad parameter: product must be an str")
    if "platform" in params and not isinstance(params["platform"], str):
        raise InvalidParameterError("Bad parameter: platform must be an str")
    if "architecture" in params and not isinstance(
        params["architecture"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: architecture must be an str"
        )
    if "ext" in params and not isinstance(params["ext"], str):
        raise InvalidParameterError("Bad parameter: ext must be an str")
    response, options = Api.send_request(
        "GET", "/releases/latest", params, options
    )
    return Release(response.data, options)


# Parameters:
#   title - string
#   description - string
#   version_major - int64
#   version_minor - int64
#   version_patch - int64
#   version_build - int64
#   oem - string
#   product - string
#   native_release_packages - array(object)
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "title" in params and not isinstance(params["title"], str):
        raise InvalidParameterError("Bad parameter: title must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "version_major" in params and not isinstance(
        params["version_major"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: version_major must be an int"
        )
    if "version_minor" in params and not isinstance(
        params["version_minor"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: version_minor must be an int"
        )
    if "version_patch" in params and not isinstance(
        params["version_patch"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: version_patch must be an int"
        )
    if "version_build" in params and not isinstance(
        params["version_build"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: version_build must be an int"
        )
    if "oem" in params and not isinstance(params["oem"], str):
        raise InvalidParameterError("Bad parameter: oem must be an str")
    if "product" in params and not isinstance(params["product"], str):
        raise InvalidParameterError("Bad parameter: product must be an str")
    if "native_release_packages" in params and not isinstance(
        params["native_release_packages"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: native_release_packages must be an list"
        )
    response, options = Api.send_request("POST", "/releases", params, options)
    return Release(response.data, options)


def new(*args, **kwargs):
    return Release(*args, **kwargs)
