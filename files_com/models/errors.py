import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Errors:
    default_attributes = {
        'fields': None,     # array - A list of fields where errors occur
        'messages': None,     # array - A list of error messages
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Errors.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Errors.default_attributes}

