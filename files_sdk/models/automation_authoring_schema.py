import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AutomationAuthoringSchema:
    default_attributes = {
        "definition_schema": None,  # object - JSON Schema for active Automation v2 graph definitions.
        "error_families": None,  # array(object) - Typed error families accepted by Automation v2 on_error rules.
        "nodes": None,  # array(object) - Active Automation v2 node authoring metadata.
        "schema_url": None,  # string - Stable public URL for the Automation v2 graph definition JSON Schema.
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
        ) in AutomationAuthoringSchema.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AutomationAuthoringSchema.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return AutomationAuthoringSchema(*args, **kwargs)
