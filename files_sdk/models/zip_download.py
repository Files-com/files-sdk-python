import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ZipDownload:
    default_attributes = {
        "download_uri": None,  # string - URL for downloading the ZIP
        "paths": None,  # array(string)
        "bundle_registration_code": None,  # string
        "encoded_paths": None,  # array(string)
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in ZipDownload.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ZipDownload.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The ZipDownload object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   paths (required) - array(string)
#   bundle_registration_code - string
#   encoded_paths - array(string)
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "paths" in params and not isinstance(params["paths"], builtins.list):
        raise InvalidParameterError("Bad parameter: paths must be an list")
    if "bundle_registration_code" in params and not isinstance(
        params["bundle_registration_code"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_registration_code must be an str"
        )
    if "encoded_paths" in params and not isinstance(
        params["encoded_paths"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: encoded_paths must be an list"
        )
    if "paths" not in params:
        raise MissingParameterError("Parameter missing: paths")
    response, options = Api.send_request(
        "POST", "/zip_downloads", params, options
    )
    return ZipDownload(response.data, options)


def new(*args, **kwargs):
    return ZipDownload(*args, **kwargs)
