import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Status:
    default_attributes = {
        'code': None,     # int64 - Status http code
        'message': None,     # string - Error message
        'status': None,     # string - Status message
        'data': None,     # Additional data
        'errors': None,     # array - A list of api errors
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Status.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Status.default_attributes if getattr(self, k, None) is not None}


def new(*args, **kwargs):
    return Status(*args, **kwargs)