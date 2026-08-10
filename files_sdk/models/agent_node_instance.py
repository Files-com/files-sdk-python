import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AgentNodeInstance:
    default_attributes = {
        "instance_id": None,  # string - Ephemeral ID for this running Agent process
        "process_state": None,  # string - Role of this process during an Agent update
        "status": None,  # string - Whether this process has an available proxy connection
        "is_default": None,  # boolean - Whether this process receives new unscoped work for its node
        "agent_version": None,  # string - Agent version reported by this process
        "last_seen_at": None,  # date-time - Most recent successful observation for this process
        "connections": None,  # array(object) - Proxy connections observed for this process
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
        ) in AgentNodeInstance.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AgentNodeInstance.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return AgentNodeInstance(*args, **kwargs)
