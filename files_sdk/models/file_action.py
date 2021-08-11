import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FileAction:
    default_attributes = {
        'status': None,     # string - Status of file operation. Possible values: completed, enqueued.
        'file_migration_id': None,     # int64 - If status is enqueued, this is the id of the FileMigration to check for status updates.
        'path': None,
        'destination': None,
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FileAction.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FileAction.default_attributes if getattr(self, k, None) is not None}


def new(*args, **kwargs):
    return FileAction(*args, **kwargs)