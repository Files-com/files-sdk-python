import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ZipListEntry:
    default_attributes = {
        "path": None,  # string - Entry path inside the ZIP. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "size": None,  # int64 - Uncompressed size in bytes.
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
        ) in ZipListEntry.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in ZipListEntry.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return ZipListEntry(*args, **kwargs)
