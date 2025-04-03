import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class UsageByTopLevelDir:
    default_attributes = {
        "dir": None,  # string - Directory name
        "size": None,  # int64 - Usage
        "count": None,  # int64 - File count
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
        ) in UsageByTopLevelDir.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in UsageByTopLevelDir.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return UsageByTopLevelDir(*args, **kwargs)
