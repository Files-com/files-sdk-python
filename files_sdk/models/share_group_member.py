import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ShareGroupMember:
    default_attributes = {
        "name": None,  # string - Name of the share group member
        "company": None,  # string - Company of the share group member
        "email": None,  # string - Email of the share group member
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
        ) in ShareGroupMember.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in ShareGroupMember.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return ShareGroupMember(*args, **kwargs)
