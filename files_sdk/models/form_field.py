import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FormField:
    default_attributes = {
        'id': None,     # int64 - Form field id
        'label': None,     # string - Label to be displayed
        'required': None,     # boolean - Is this a required field?
        'help_text': None,     # string - Help text to be displayed
        'field_type': None,     # string - Type of Field
        'options_for_select': None,     # string - Options to display for radio and dropdown
        'default_option': None,     # string - Default option for radio and dropdown
        'form_field_set_id': None,     # int64 - Form field set id
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FormField.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FormField.default_attributes if getattr(self, k, None) is not None}


def new(*args, **kwargs):
    return FormField(*args, **kwargs)