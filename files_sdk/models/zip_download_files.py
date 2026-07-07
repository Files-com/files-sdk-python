import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ZipDownloadFiles:
    default_attributes = {
        "site_id": None,  # int64 - Site Id
        "user_id": None,  # int64 - User Id
        "bundle_id": None,  # int64 - Bundle Id
        "bundle_registration_id": None,  # int64 - Bundle Registration Id
        "files": None,  # array(object) - A list of file names, sizes, and signed download URLs.
        "cursor": None,  # string - Cursor for fetching more files in subsequent requests.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in ZipDownloadFiles.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ZipDownloadFiles.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return ZipDownloadFiles(*args, **kwargs)
