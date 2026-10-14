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


class FormField:
    """A form field record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Form field id
        label: string - Label to be displayed
        required: boolean - Is this a required field?
        help_text: string - Help text to be displayed
        field_type: string - Type of Field
        options_for_select: array(string) - Options to display for radio and dropdown
        default_option: string - Default option for radio and dropdown
        form_field_set_id: int64 - Form field set id
    """

    default_attributes = {
        "id": None,  # int64 - Form field id
        "label": None,  # string - Label to be displayed
        "required": None,  # boolean - Is this a required field?
        "help_text": None,  # string - Help text to be displayed
        "field_type": None,  # string - Type of Field
        "options_for_select": None,  # array(string) - Options to display for radio and dropdown
        "default_option": None,  # string - Default option for radio and dropdown
        "form_field_set_id": None,  # int64 - Form field set id
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    label: str | None
    required: bool | None
    help_text: str | None
    field_type: str | None
    options_for_select: builtins.list[str] | None
    default_option: str | None
    form_field_set_id: int | None

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
        for attribute, default_value in FormField.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FormField.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> FormField:
    return FormField(*args, **kwargs)
