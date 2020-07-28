import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Action:
    default_attributes = {
        'id': None,     # int64 - Action ID
        'path': None,     # string - Path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'when': None,     # date-time - Action occurrence date/time
        'destination': None,     # string - The destination path for this action, if applicable
        'display': None,     # string - Friendly displayed output
        'ip': None,     # string - IP Address that performed this action
        'source': None,     # string - The source path for this action, if applicable
        'targets': None,     # array - Targets
        'user_id': None,     # int64 - User ID
        'username': None,     # string - Username
        'action': None,     # string - Type of action
        'failure_type': None,     # string - Failure type.  If action was a user login or session failure, why did it fail?
        'interface': None,     # string - Interface on which this action occurred.
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Action.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Action.default_attributes if getattr(self, k, None) is not None}


def new(*args, **kwargs):
    return Action(*args, **kwargs)