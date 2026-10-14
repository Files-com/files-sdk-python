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


class AgentNodeInstance:
    """A agent node instance record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        instance_id: string - Ephemeral ID for this running Agent process
        process_state: string - Role of this process during an Agent update
        status: string - Whether this process has an available proxy connection
        is_default: boolean - Whether this process receives new unscoped work for its node
        agent_version: string - Agent version reported by this process
        last_seen_at: date-time - Most recent successful observation for this process
        connections: array(object) - Proxy connections observed for this process
    """

    default_attributes = {
        "instance_id": None,  # string - Ephemeral ID for this running Agent process
        "process_state": None,  # string - Role of this process during an Agent update
        "status": None,  # string - Whether this process has an available proxy connection
        "is_default": None,  # boolean - Whether this process receives new unscoped work for its node
        "agent_version": None,  # string - Agent version reported by this process
        "last_seen_at": None,  # date-time - Most recent successful observation for this process
        "connections": None,  # array(object) - Proxy connections observed for this process
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    instance_id: str | None
    process_state: str | None
    status: str | None
    is_default: bool | None
    agent_version: str | None
    last_seen_at: str | None
    connections: builtins.list[dict[str, Any]] | None

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

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> AgentNodeInstance:
    return AgentNodeInstance(*args, **kwargs)
