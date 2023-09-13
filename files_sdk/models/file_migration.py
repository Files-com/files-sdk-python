import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class FileMigration:
    default_attributes = {
        "id": None,  # int64 - File migration ID
        "path": None,  # string - Source path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "dest_path": None,  # string - Destination path
        "files_moved": None,  # int64 - Number of files processed
        "files_total": None,  # int64 - Deprecated: used to return a count of the applicable files.  Currently returns 0 always.  On remote servers, it is not possible to reliably determine the number of affected files for every migration operation.
        "operation": None,  # string - The type of operation
        "region": None,  # string - Region
        "status": None,  # string - Status
        "log_url": None,  # string - Link to download the log file for this migration.
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
        ) in FileMigration.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in FileMigration.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   id (required) - int64 - File Migration ID.
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET", "/file_migrations/{id}".format(id=params["id"]), params, options
    )
    return FileMigration(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


def new(*args, **kwargs):
    return FileMigration(*args, **kwargs)
