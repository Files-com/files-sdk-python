import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AgentNodeConnection:
    default_attributes = {
        "mode": None,  # string - How the Agent process uses this proxy connection
        "status": None,  # string - Whether this connection was observed recently and has not disconnected
        "last_seen_at": None,  # date-time - Most recent successful observation for this connection
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
        ) in AgentNodeConnection.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AgentNodeConnection.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return AgentNodeConnection(*args, **kwargs)
