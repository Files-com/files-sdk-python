import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PublicUrl:
    default_attributes = {
        "http-code": None,  # int64 - Response HTTP code
        "type": None,  # string - A short string representing which error happened, if any
        "http_headers": None,  # object - Headers to include with the response
        "body": None,  # string - Body of the response, if a folder listing was requested
        "download_uri": None,  # string - Signed URL allowing access to the requested file
        "internal_download_uri": None,  # string - For use with internal services and should also be with headers and socks_ips
        "redirect": None,  # string - URL where this request should be redirected, if necessary
        "mime_type": None,  # string - Used for response content-type
        "site_id": None,  # int64 - Site id
        "remote_server_id": None,  # int64 - Used for internal bandwidth tracking
        "headers": None,  # object - Used for internal url management
        "socks_ips": None,  # array(string) - Used for internal url management
        "true_path": None,  # string - The actual path of the file or folder being accessed. Used for caching.
        "cache_for_seconds": None,  # int64 - Indicates how long the response should be cached, in seconds.
        "hostname": None,  # string - Hostname used to request the publicly shared resource.
        "path": None,  # string - Path of the resource being requested.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in PublicUrl.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PublicUrl.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        new_obj = create(self.path, self.get_attributes(), self.options)
        self.set_attributes(new_obj.get_attributes())
        return True


# Parameters:
#   hostname (required) - string - Hostname used to request the publicly shared resource.
#   path (required) - string - Path of the resource being requested.
def create(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "hostname" not in params:
        raise MissingParameterError("Parameter missing: hostname")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request(
        "POST", "/public_urls", params, options
    )
    return PublicUrl(response.data, options)


def new(*args, **kwargs):
    return PublicUrl(*args, **kwargs)
