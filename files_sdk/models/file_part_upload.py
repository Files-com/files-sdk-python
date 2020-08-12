import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FilePartUpload:
    default_attributes = {
        'send': None,     # object - Content-Type and File to send
        'action': None,     # string - Type of upload
        'ask_about_overwrites': None,     # boolean - If false, rename conflicting files instead of asking for overwrite confirmation
        'available_parts': None,     # string - Currently unused
        'expires': None,     # string - Currently unused
        'headers': None,     # object - Additional upload headers
        'http_method': None,     # string - Upload method, usually POST
        'next_partsize': None,     # string - Currently unused
        'parallel_parts': None,     # boolean - If true, parts may be uploaded in parallel
        'parameters': None,     # string - Additional upload parameters
        'part_number': None,     # string - Currently unused
        'partsize': None,     # string - Currently unused
        'path': None,     # string - Upload path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'ref': None,     # string - Reference name for this upload part
        'upload_uri': None,     # string - URI to upload this part to
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FilePartUpload.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FilePartUpload.default_attributes if getattr(self, k, None) is not None}


def new(*args, **kwargs):
    return FilePartUpload(*args, **kwargs)