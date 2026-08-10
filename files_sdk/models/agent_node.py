import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AgentNode:
    default_attributes = {
        "node_id": None,  # string - Stable Agent installation ID
        "name": None,  # string - Customer-configured Agent node name
        "hostname": None,  # string - Hostname reported by the Agent
        "availability_role": None,  # string - Configured traffic preference
        "status": None,  # string - Whether this node currently has an available Agent instance
        "is_default": None,  # boolean - Whether this node is the current default route for new unscoped work
        "direct_transfer_available": None,  # boolean - Whether the proxy recently validated a direct connection to this Agent node. False means direct transfers are enabled but not currently available; null means disabled or unsupported.
        "last_seen_at": None,  # date-time - Most recent successful node observation
        "instances": None,  # array(object) - Current Agent processes for this node
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in AgentNode.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AgentNode.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return AgentNode(*args, **kwargs)
