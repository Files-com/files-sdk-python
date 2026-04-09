import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SyncRunLiveTransfer:
    default_attributes = {
        "path": None,  # string - The file path being transferred. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "status": None,  # string - Status of this individual transfer
        "bytes_copied": None,  # int64 - Bytes transferred so far
        "bytes_total": None,  # int64 - Total bytes of the file being transferred
        "percentage": None,  # double - Transfer progress from 0.0 to 1.0
        "eta": None,  # string - Estimated time remaining (human-readable)
        "started_at": None,  # string - When this individual transfer started
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
        ) in SyncRunLiveTransfer.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SyncRunLiveTransfer.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return SyncRunLiveTransfer(*args, **kwargs)
