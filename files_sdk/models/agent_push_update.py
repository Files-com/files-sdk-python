import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AgentPushUpdate:
    default_attributes = {
        "version": None,  # string - Pushed agent version
        "message": None,  # string - Update accepted or reason
        "current_version": None,  # string - Installed agent version
        "pending_version": None,  # string - Pending agent version or null
        "last_error": None,  # string - Last error message or null
        "error": None,  # string - Error code
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
        ) in AgentPushUpdate.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in AgentPushUpdate.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return AgentPushUpdate(*args, **kwargs)
