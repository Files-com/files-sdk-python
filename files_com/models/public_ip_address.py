import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class PublicIpAddress:
    default_attributes = {
        'ip_address': None,     # string - The public IP address.
        'server_name': None,     # string - The name of the frontend server.
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in PublicIpAddress.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in PublicIpAddress.default_attributes}

