import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SessionAvailableSite:
    default_attributes = {
        "id": None,  # int64 - Site Id
        "name": None,  # string - Site name
        "domain": None,  # string - Custom domain
        "subdomain": None,  # string - Site subdomain
        "logo": None,  # Image - Branded logo
        "color2_top": None,  # string - Top bar background color
        "folder_permissions_groups_only": None,  # boolean - If true, permissions for this site must be bound to a group (not a user).
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
        ) in SessionAvailableSite.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SessionAvailableSite.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return SessionAvailableSite(*args, **kwargs)
