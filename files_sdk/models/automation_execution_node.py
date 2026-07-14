import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AutomationExecutionNode:
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


def new(*args, **kwargs):
    return AutomationExecutionNode(*args, **kwargs)
