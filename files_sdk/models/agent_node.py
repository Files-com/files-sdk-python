import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AgentNode:
    """A agent node record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        node_id: string - Stable Agent installation ID
        name: string - Customer-configured Agent node name
        hostname: string - Hostname reported by the Agent
        availability_role: string - Configured traffic preference
        status: string - Whether this node currently has an available Agent instance
        is_default: boolean - Whether this node is the current default route for new unscoped work
        direct_transfer_available: boolean - Whether the proxy recently validated a direct connection to this Agent node. False means direct transfers are enabled but not currently available; null means disabled or unsupported.
        last_seen_at: date-time - Most recent successful node observation
        instances: array(object) - Current Agent processes for this node
    """

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

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    node_id: str | None
    name: str | None
    hostname: str | None
    availability_role: str | None
    status: str | None
    is_default: bool | None
    direct_transfer_available: bool | None
    last_seen_at: str | None
    instances: builtins.list[dict[str, Any]] | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

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

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> AgentNode:
    return AgentNode(*args, **kwargs)
