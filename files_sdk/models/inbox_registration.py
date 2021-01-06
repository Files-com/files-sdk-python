import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class InboxRegistration:
    default_attributes = {
        'code': None,     # string - Registration cookie code
        'name': None,     # string - Registrant name
        'company': None,     # string - Registrant company name
        'email': None,     # string - Registrant email address
        'form_field_set_id': None,     # int64 - Id of associated form field set
        'form_field_data': None,     # string - Data for form field set with form field ids as keys and user data as values
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in InboxRegistration.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in InboxRegistration.default_attributes if getattr(self, k, None) is not None}


def new(*args, **kwargs):
    return InboxRegistration(*args, **kwargs)