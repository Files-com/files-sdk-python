import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Preview:
    default_attributes = {
        'id': None,     # int64 - Preview ID
        'status': None,     # string - Preview status.  Can be invalid, not_generated, generating, complete, or file_too_large
        'download_uri': None,     # string - Link to download preview
        'type': None,     # string - Preview status.  Can be invalid, not_generated, generating, complete, or file_too_large
        'size': None,     # int64 - Preview size
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Preview.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Preview.default_attributes}

