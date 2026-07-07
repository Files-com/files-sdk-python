import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PublicHostingSessionPairing:
    default_attributes = {
        "pairing_key": None,  # string - One-time pairing key for the Public Hosting session
        "redirect_uri": None,  # string - Public Hosting URL that exchanges the pairing key for a Public Hosting session cookie
        "expires_at": None,  # date-time - When the pairing key expires
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
        ) in PublicHostingSessionPairing.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PublicHostingSessionPairing.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return PublicHostingSessionPairing(*args, **kwargs)
