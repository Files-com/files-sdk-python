import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Auto:
    default_attributes = {
        'dynamic': None,     # object
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Auto.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Auto.default_attributes if getattr(self, k, None) is not None}


def new(*args, **kwargs):
    return Auto(*args, **kwargs)