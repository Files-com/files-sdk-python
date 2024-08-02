import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Action:
    default_attributes = {
        "id": None,  # int64 - Action ID
        "path": None,  # string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "when": None,  # date-time - Action occurrence date/time
        "destination": None,  # string - The destination path for this action, if applicable
        "display": None,  # string - Friendly displayed output
        "ip": None,  # string - IP Address that performed this action
        "source": None,  # string - The source path for this action, if applicable
        "targets": None,  # array(object) - Targets
        "user_id": None,  # int64 - User ID
        "username": None,  # string - Username
        "user_is_from_parent_site": None,  # boolean - true if this change was performed by a user on a parent site.
        "action": None,  # string - Type of action
        "failure_type": None,  # string - Failure type.  If action was a user login or session failure, why did it fail?
        "interface": None,  # string - Interface on which this action occurred.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Action.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Action.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return Action(*args, **kwargs)
