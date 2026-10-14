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


class AutomationExecutionNode:
    """A automation execution node record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        node_id: string - Node ID from the pinned Automation definition.
        node_type: string - Node type.
        status: string - Node status.
        run_stage: string - Current node execution stage.
        reused: boolean - Whether this node reused persisted output from an earlier run.
        successful_operations: int64 - Count of successful operations in this node.
        failed_operations: int64 - Count of failed operations in this node.
        started_at: date-time - When this node started.
        completed_at: date-time - When this node completed.
        duration_ms: int64 - Node runtime in milliseconds.
        inputs: array(object) - Ordered inbound edge references.
        outputs: object - Output counts, item kinds, and typed-error summaries by outlet.
        input_items: object - Materialized input items currently available, grouped by inlet.
        output_items: object - Materialized output items grouped by outlet.
    """

    default_attributes = {
        "node_id": None,  # string - Node ID from the pinned Automation definition.
        "node_type": None,  # string - Node type.
        "status": None,  # string - Node status.
        "run_stage": None,  # string - Current node execution stage.
        "reused": None,  # boolean - Whether this node reused persisted output from an earlier run.
        "successful_operations": None,  # int64 - Count of successful operations in this node.
        "failed_operations": None,  # int64 - Count of failed operations in this node.
        "started_at": None,  # date-time - When this node started.
        "completed_at": None,  # date-time - When this node completed.
        "duration_ms": None,  # int64 - Node runtime in milliseconds.
        "inputs": None,  # array(object) - Ordered inbound edge references.
        "outputs": None,  # object - Output counts, item kinds, and typed-error summaries by outlet.
        "input_items": None,  # object - Materialized input items currently available, grouped by inlet.
        "output_items": None,  # object - Materialized output items grouped by outlet.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    node_id: str | None
    node_type: str | None
    status: str | None
    run_stage: str | None
    reused: bool | None
    successful_operations: int | None
    failed_operations: int | None
    started_at: str | None
    completed_at: str | None
    duration_ms: int | None
    inputs: builtins.list[dict[str, Any]] | None
    outputs: dict[str, Any] | None
    input_items: dict[str, Any] | None
    output_items: dict[str, Any] | None

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
        ) in AutomationExecutionNode.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AutomationExecutionNode.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> AutomationExecutionNode:
    return AutomationExecutionNode(*args, **kwargs)
