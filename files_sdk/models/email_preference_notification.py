import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class EmailPreferenceNotification:
    default_attributes = {
        "id": None,  # int64 - Email preferences ID
        "path": None,  # string - Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "send_interval": None,  # string - The time interval that notifications are aggregated to.  Can be five_minutes, fifteen_minutes, hourly, or daily
        "unsubscribed": None,  # boolean - Is unsubscribed?
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in EmailPreferenceNotification.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in EmailPreferenceNotification.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return EmailPreferenceNotification(*args, **kwargs)
