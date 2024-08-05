import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class OutboundConnectionLog:
    default_attributes = {
        "timestamp": None,  # date-time - Start Time of Action
        "path": None,  # string - Remote Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "client_ip": None,  # string - End User IP
        "src_remote_server_id": None,  # string - Source Remote Server ID
        "dest_remote_server_id": None,  # string - Destination Remote Server ID
        "operation": None,  # string - Operation Type
        "error_message": None,  # string - Error message, if applicable
        "error_operation": None,  # string - Error operation, if applicable
        "error_type": None,  # string - Error type, if applicable
        "status": None,  # string - Status
        "duration_ms": None,  # int64 - Duration (in milliseconds)
        "bytes_uploaded": None,  # int64 - Data Length in Bytes. Present for upload actions that transfer data.
        "bytes_downloaded": None,  # int64 - Data Length in Bytes. Present for download actions that transfer data.
        "list_count": None,  # int64 - Number of entries returned for a folder list action.
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
        ) in OutboundConnectionLog.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in OutboundConnectionLog.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `start_date`, `end_date`, `operation`, `status`, `src_remote_server_id`, `dest_remote_server_id`, `path` or `client_ip`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ operation ]`, `[ status ]`, `[ src_remote_server_id ]`, `[ dest_remote_server_id ]`, `[ path ]`, `[ client_ip ]`, `[ start_date, end_date ]`, `[ start_date, operation ]`, `[ start_date, status ]`, `[ start_date, src_remote_server_id ]`, `[ start_date, dest_remote_server_id ]`, `[ start_date, path ]`, `[ start_date, client_ip ]`, `[ end_date, operation ]`, `[ end_date, status ]`, `[ end_date, src_remote_server_id ]`, `[ end_date, dest_remote_server_id ]`, `[ end_date, path ]`, `[ end_date, client_ip ]`, `[ operation, status ]`, `[ operation, src_remote_server_id ]`, `[ operation, dest_remote_server_id ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ status, src_remote_server_id ]`, `[ status, dest_remote_server_id ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ src_remote_server_id, dest_remote_server_id ]`, `[ src_remote_server_id, path ]`, `[ src_remote_server_id, client_ip ]`, `[ dest_remote_server_id, path ]`, `[ dest_remote_server_id, client_ip ]`, `[ path, client_ip ]`, `[ start_date, end_date, operation ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, src_remote_server_id ]`, `[ start_date, end_date, dest_remote_server_id ]`, `[ start_date, end_date, path ]`, `[ start_date, end_date, client_ip ]`, `[ start_date, operation, status ]`, `[ start_date, operation, src_remote_server_id ]`, `[ start_date, operation, dest_remote_server_id ]`, `[ start_date, operation, path ]`, `[ start_date, operation, client_ip ]`, `[ start_date, status, src_remote_server_id ]`, `[ start_date, status, dest_remote_server_id ]`, `[ start_date, status, path ]`, `[ start_date, status, client_ip ]`, `[ start_date, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, src_remote_server_id, path ]`, `[ start_date, src_remote_server_id, client_ip ]`, `[ start_date, dest_remote_server_id, path ]`, `[ start_date, dest_remote_server_id, client_ip ]`, `[ start_date, path, client_ip ]`, `[ end_date, operation, status ]`, `[ end_date, operation, src_remote_server_id ]`, `[ end_date, operation, dest_remote_server_id ]`, `[ end_date, operation, path ]`, `[ end_date, operation, client_ip ]`, `[ end_date, status, src_remote_server_id ]`, `[ end_date, status, dest_remote_server_id ]`, `[ end_date, status, path ]`, `[ end_date, status, client_ip ]`, `[ end_date, src_remote_server_id, dest_remote_server_id ]`, `[ end_date, src_remote_server_id, path ]`, `[ end_date, src_remote_server_id, client_ip ]`, `[ end_date, dest_remote_server_id, path ]`, `[ end_date, dest_remote_server_id, client_ip ]`, `[ end_date, path, client_ip ]`, `[ operation, status, src_remote_server_id ]`, `[ operation, status, dest_remote_server_id ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, src_remote_server_id, dest_remote_server_id ]`, `[ operation, src_remote_server_id, path ]`, `[ operation, src_remote_server_id, client_ip ]`, `[ operation, dest_remote_server_id, path ]`, `[ operation, dest_remote_server_id, client_ip ]`, `[ operation, path, client_ip ]`, `[ status, src_remote_server_id, dest_remote_server_id ]`, `[ status, src_remote_server_id, path ]`, `[ status, src_remote_server_id, client_ip ]`, `[ status, dest_remote_server_id, path ]`, `[ status, dest_remote_server_id, client_ip ]`, `[ status, path, client_ip ]`, `[ src_remote_server_id, dest_remote_server_id, path ]`, `[ src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ src_remote_server_id, path, client_ip ]`, `[ dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status ]`, `[ start_date, end_date, operation, src_remote_server_id ]`, `[ start_date, end_date, operation, dest_remote_server_id ]`, `[ start_date, end_date, operation, path ]`, `[ start_date, end_date, operation, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id ]`, `[ start_date, end_date, status, dest_remote_server_id ]`, `[ start_date, end_date, status, path ]`, `[ start_date, end_date, status, client_ip ]`, `[ start_date, end_date, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, end_date, src_remote_server_id, path ]`, `[ start_date, end_date, src_remote_server_id, client_ip ]`, `[ start_date, end_date, dest_remote_server_id, path ]`, `[ start_date, end_date, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, path, client_ip ]`, `[ start_date, operation, status, src_remote_server_id ]`, `[ start_date, operation, status, dest_remote_server_id ]`, `[ start_date, operation, status, path ]`, `[ start_date, operation, status, client_ip ]`, `[ start_date, operation, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, operation, src_remote_server_id, path ]`, `[ start_date, operation, src_remote_server_id, client_ip ]`, `[ start_date, operation, dest_remote_server_id, path ]`, `[ start_date, operation, dest_remote_server_id, client_ip ]`, `[ start_date, operation, path, client_ip ]`, `[ start_date, status, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, status, src_remote_server_id, path ]`, `[ start_date, status, src_remote_server_id, client_ip ]`, `[ start_date, status, dest_remote_server_id, path ]`, `[ start_date, status, dest_remote_server_id, client_ip ]`, `[ start_date, status, path, client_ip ]`, `[ start_date, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, src_remote_server_id, path, client_ip ]`, `[ start_date, dest_remote_server_id, path, client_ip ]`, `[ end_date, operation, status, src_remote_server_id ]`, `[ end_date, operation, status, dest_remote_server_id ]`, `[ end_date, operation, status, path ]`, `[ end_date, operation, status, client_ip ]`, `[ end_date, operation, src_remote_server_id, dest_remote_server_id ]`, `[ end_date, operation, src_remote_server_id, path ]`, `[ end_date, operation, src_remote_server_id, client_ip ]`, `[ end_date, operation, dest_remote_server_id, path ]`, `[ end_date, operation, dest_remote_server_id, client_ip ]`, `[ end_date, operation, path, client_ip ]`, `[ end_date, status, src_remote_server_id, dest_remote_server_id ]`, `[ end_date, status, src_remote_server_id, path ]`, `[ end_date, status, src_remote_server_id, client_ip ]`, `[ end_date, status, dest_remote_server_id, path ]`, `[ end_date, status, dest_remote_server_id, client_ip ]`, `[ end_date, status, path, client_ip ]`, `[ end_date, src_remote_server_id, dest_remote_server_id, path ]`, `[ end_date, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ end_date, src_remote_server_id, path, client_ip ]`, `[ end_date, dest_remote_server_id, path, client_ip ]`, `[ operation, status, src_remote_server_id, dest_remote_server_id ]`, `[ operation, status, src_remote_server_id, path ]`, `[ operation, status, src_remote_server_id, client_ip ]`, `[ operation, status, dest_remote_server_id, path ]`, `[ operation, status, dest_remote_server_id, client_ip ]`, `[ operation, status, path, client_ip ]`, `[ operation, src_remote_server_id, dest_remote_server_id, path ]`, `[ operation, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ operation, src_remote_server_id, path, client_ip ]`, `[ operation, dest_remote_server_id, path, client_ip ]`, `[ status, src_remote_server_id, dest_remote_server_id, path ]`, `[ status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ status, src_remote_server_id, path, client_ip ]`, `[ status, dest_remote_server_id, path, client_ip ]`, `[ src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status, src_remote_server_id ]`, `[ start_date, end_date, operation, status, dest_remote_server_id ]`, `[ start_date, end_date, operation, status, path ]`, `[ start_date, end_date, operation, status, client_ip ]`, `[ start_date, end_date, operation, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, end_date, operation, src_remote_server_id, path ]`, `[ start_date, end_date, operation, src_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, dest_remote_server_id, path ]`, `[ start_date, end_date, operation, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, path, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, end_date, status, src_remote_server_id, path ]`, `[ start_date, end_date, status, src_remote_server_id, client_ip ]`, `[ start_date, end_date, status, dest_remote_server_id, path ]`, `[ start_date, end_date, status, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, status, path, client_ip ]`, `[ start_date, end_date, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, end_date, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, src_remote_server_id, path, client_ip ]`, `[ start_date, end_date, dest_remote_server_id, path, client_ip ]`, `[ start_date, operation, status, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, operation, status, src_remote_server_id, path ]`, `[ start_date, operation, status, src_remote_server_id, client_ip ]`, `[ start_date, operation, status, dest_remote_server_id, path ]`, `[ start_date, operation, status, dest_remote_server_id, client_ip ]`, `[ start_date, operation, status, path, client_ip ]`, `[ start_date, operation, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, operation, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, operation, src_remote_server_id, path, client_ip ]`, `[ start_date, operation, dest_remote_server_id, path, client_ip ]`, `[ start_date, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, status, src_remote_server_id, path, client_ip ]`, `[ start_date, status, dest_remote_server_id, path, client_ip ]`, `[ start_date, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ end_date, operation, status, src_remote_server_id, dest_remote_server_id ]`, `[ end_date, operation, status, src_remote_server_id, path ]`, `[ end_date, operation, status, src_remote_server_id, client_ip ]`, `[ end_date, operation, status, dest_remote_server_id, path ]`, `[ end_date, operation, status, dest_remote_server_id, client_ip ]`, `[ end_date, operation, status, path, client_ip ]`, `[ end_date, operation, src_remote_server_id, dest_remote_server_id, path ]`, `[ end_date, operation, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ end_date, operation, src_remote_server_id, path, client_ip ]`, `[ end_date, operation, dest_remote_server_id, path, client_ip ]`, `[ end_date, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ end_date, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ end_date, status, src_remote_server_id, path, client_ip ]`, `[ end_date, status, dest_remote_server_id, path, client_ip ]`, `[ end_date, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ operation, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ operation, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ operation, status, src_remote_server_id, path, client_ip ]`, `[ operation, status, dest_remote_server_id, path, client_ip ]`, `[ operation, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, end_date, operation, status, src_remote_server_id, path ]`, `[ start_date, end_date, operation, status, src_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, status, dest_remote_server_id, path ]`, `[ start_date, end_date, operation, status, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, status, path, client_ip ]`, `[ start_date, end_date, operation, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, end_date, operation, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, src_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, end_date, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id, path, client_ip ]`, `[ start_date, end_date, status, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, operation, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, operation, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, operation, status, src_remote_server_id, path, client_ip ]`, `[ start_date, operation, status, dest_remote_server_id, path, client_ip ]`, `[ start_date, operation, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ end_date, operation, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ end_date, operation, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ end_date, operation, status, src_remote_server_id, path, client_ip ]`, `[ end_date, operation, status, dest_remote_server_id, path, client_ip ]`, `[ end_date, operation, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ end_date, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ operation, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, end_date, operation, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, status, src_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, operation, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]` or `[ end_date, operation, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `operation`, `status`, `src_remote_server_id`, `dest_remote_server_id` or `path`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ operation ]`, `[ status ]`, `[ src_remote_server_id ]`, `[ dest_remote_server_id ]`, `[ path ]`, `[ client_ip ]`, `[ start_date, end_date ]`, `[ start_date, operation ]`, `[ start_date, status ]`, `[ start_date, src_remote_server_id ]`, `[ start_date, dest_remote_server_id ]`, `[ start_date, path ]`, `[ start_date, client_ip ]`, `[ end_date, operation ]`, `[ end_date, status ]`, `[ end_date, src_remote_server_id ]`, `[ end_date, dest_remote_server_id ]`, `[ end_date, path ]`, `[ end_date, client_ip ]`, `[ operation, status ]`, `[ operation, src_remote_server_id ]`, `[ operation, dest_remote_server_id ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ status, src_remote_server_id ]`, `[ status, dest_remote_server_id ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ src_remote_server_id, dest_remote_server_id ]`, `[ src_remote_server_id, path ]`, `[ src_remote_server_id, client_ip ]`, `[ dest_remote_server_id, path ]`, `[ dest_remote_server_id, client_ip ]`, `[ path, client_ip ]`, `[ start_date, end_date, operation ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, src_remote_server_id ]`, `[ start_date, end_date, dest_remote_server_id ]`, `[ start_date, end_date, path ]`, `[ start_date, end_date, client_ip ]`, `[ start_date, operation, status ]`, `[ start_date, operation, src_remote_server_id ]`, `[ start_date, operation, dest_remote_server_id ]`, `[ start_date, operation, path ]`, `[ start_date, operation, client_ip ]`, `[ start_date, status, src_remote_server_id ]`, `[ start_date, status, dest_remote_server_id ]`, `[ start_date, status, path ]`, `[ start_date, status, client_ip ]`, `[ start_date, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, src_remote_server_id, path ]`, `[ start_date, src_remote_server_id, client_ip ]`, `[ start_date, dest_remote_server_id, path ]`, `[ start_date, dest_remote_server_id, client_ip ]`, `[ start_date, path, client_ip ]`, `[ end_date, operation, status ]`, `[ end_date, operation, src_remote_server_id ]`, `[ end_date, operation, dest_remote_server_id ]`, `[ end_date, operation, path ]`, `[ end_date, operation, client_ip ]`, `[ end_date, status, src_remote_server_id ]`, `[ end_date, status, dest_remote_server_id ]`, `[ end_date, status, path ]`, `[ end_date, status, client_ip ]`, `[ end_date, src_remote_server_id, dest_remote_server_id ]`, `[ end_date, src_remote_server_id, path ]`, `[ end_date, src_remote_server_id, client_ip ]`, `[ end_date, dest_remote_server_id, path ]`, `[ end_date, dest_remote_server_id, client_ip ]`, `[ end_date, path, client_ip ]`, `[ operation, status, src_remote_server_id ]`, `[ operation, status, dest_remote_server_id ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, src_remote_server_id, dest_remote_server_id ]`, `[ operation, src_remote_server_id, path ]`, `[ operation, src_remote_server_id, client_ip ]`, `[ operation, dest_remote_server_id, path ]`, `[ operation, dest_remote_server_id, client_ip ]`, `[ operation, path, client_ip ]`, `[ status, src_remote_server_id, dest_remote_server_id ]`, `[ status, src_remote_server_id, path ]`, `[ status, src_remote_server_id, client_ip ]`, `[ status, dest_remote_server_id, path ]`, `[ status, dest_remote_server_id, client_ip ]`, `[ status, path, client_ip ]`, `[ src_remote_server_id, dest_remote_server_id, path ]`, `[ src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ src_remote_server_id, path, client_ip ]`, `[ dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status ]`, `[ start_date, end_date, operation, src_remote_server_id ]`, `[ start_date, end_date, operation, dest_remote_server_id ]`, `[ start_date, end_date, operation, path ]`, `[ start_date, end_date, operation, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id ]`, `[ start_date, end_date, status, dest_remote_server_id ]`, `[ start_date, end_date, status, path ]`, `[ start_date, end_date, status, client_ip ]`, `[ start_date, end_date, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, end_date, src_remote_server_id, path ]`, `[ start_date, end_date, src_remote_server_id, client_ip ]`, `[ start_date, end_date, dest_remote_server_id, path ]`, `[ start_date, end_date, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, path, client_ip ]`, `[ start_date, operation, status, src_remote_server_id ]`, `[ start_date, operation, status, dest_remote_server_id ]`, `[ start_date, operation, status, path ]`, `[ start_date, operation, status, client_ip ]`, `[ start_date, operation, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, operation, src_remote_server_id, path ]`, `[ start_date, operation, src_remote_server_id, client_ip ]`, `[ start_date, operation, dest_remote_server_id, path ]`, `[ start_date, operation, dest_remote_server_id, client_ip ]`, `[ start_date, operation, path, client_ip ]`, `[ start_date, status, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, status, src_remote_server_id, path ]`, `[ start_date, status, src_remote_server_id, client_ip ]`, `[ start_date, status, dest_remote_server_id, path ]`, `[ start_date, status, dest_remote_server_id, client_ip ]`, `[ start_date, status, path, client_ip ]`, `[ start_date, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, src_remote_server_id, path, client_ip ]`, `[ start_date, dest_remote_server_id, path, client_ip ]`, `[ end_date, operation, status, src_remote_server_id ]`, `[ end_date, operation, status, dest_remote_server_id ]`, `[ end_date, operation, status, path ]`, `[ end_date, operation, status, client_ip ]`, `[ end_date, operation, src_remote_server_id, dest_remote_server_id ]`, `[ end_date, operation, src_remote_server_id, path ]`, `[ end_date, operation, src_remote_server_id, client_ip ]`, `[ end_date, operation, dest_remote_server_id, path ]`, `[ end_date, operation, dest_remote_server_id, client_ip ]`, `[ end_date, operation, path, client_ip ]`, `[ end_date, status, src_remote_server_id, dest_remote_server_id ]`, `[ end_date, status, src_remote_server_id, path ]`, `[ end_date, status, src_remote_server_id, client_ip ]`, `[ end_date, status, dest_remote_server_id, path ]`, `[ end_date, status, dest_remote_server_id, client_ip ]`, `[ end_date, status, path, client_ip ]`, `[ end_date, src_remote_server_id, dest_remote_server_id, path ]`, `[ end_date, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ end_date, src_remote_server_id, path, client_ip ]`, `[ end_date, dest_remote_server_id, path, client_ip ]`, `[ operation, status, src_remote_server_id, dest_remote_server_id ]`, `[ operation, status, src_remote_server_id, path ]`, `[ operation, status, src_remote_server_id, client_ip ]`, `[ operation, status, dest_remote_server_id, path ]`, `[ operation, status, dest_remote_server_id, client_ip ]`, `[ operation, status, path, client_ip ]`, `[ operation, src_remote_server_id, dest_remote_server_id, path ]`, `[ operation, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ operation, src_remote_server_id, path, client_ip ]`, `[ operation, dest_remote_server_id, path, client_ip ]`, `[ status, src_remote_server_id, dest_remote_server_id, path ]`, `[ status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ status, src_remote_server_id, path, client_ip ]`, `[ status, dest_remote_server_id, path, client_ip ]`, `[ src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status, src_remote_server_id ]`, `[ start_date, end_date, operation, status, dest_remote_server_id ]`, `[ start_date, end_date, operation, status, path ]`, `[ start_date, end_date, operation, status, client_ip ]`, `[ start_date, end_date, operation, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, end_date, operation, src_remote_server_id, path ]`, `[ start_date, end_date, operation, src_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, dest_remote_server_id, path ]`, `[ start_date, end_date, operation, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, path, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, end_date, status, src_remote_server_id, path ]`, `[ start_date, end_date, status, src_remote_server_id, client_ip ]`, `[ start_date, end_date, status, dest_remote_server_id, path ]`, `[ start_date, end_date, status, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, status, path, client_ip ]`, `[ start_date, end_date, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, end_date, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, src_remote_server_id, path, client_ip ]`, `[ start_date, end_date, dest_remote_server_id, path, client_ip ]`, `[ start_date, operation, status, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, operation, status, src_remote_server_id, path ]`, `[ start_date, operation, status, src_remote_server_id, client_ip ]`, `[ start_date, operation, status, dest_remote_server_id, path ]`, `[ start_date, operation, status, dest_remote_server_id, client_ip ]`, `[ start_date, operation, status, path, client_ip ]`, `[ start_date, operation, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, operation, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, operation, src_remote_server_id, path, client_ip ]`, `[ start_date, operation, dest_remote_server_id, path, client_ip ]`, `[ start_date, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, status, src_remote_server_id, path, client_ip ]`, `[ start_date, status, dest_remote_server_id, path, client_ip ]`, `[ start_date, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ end_date, operation, status, src_remote_server_id, dest_remote_server_id ]`, `[ end_date, operation, status, src_remote_server_id, path ]`, `[ end_date, operation, status, src_remote_server_id, client_ip ]`, `[ end_date, operation, status, dest_remote_server_id, path ]`, `[ end_date, operation, status, dest_remote_server_id, client_ip ]`, `[ end_date, operation, status, path, client_ip ]`, `[ end_date, operation, src_remote_server_id, dest_remote_server_id, path ]`, `[ end_date, operation, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ end_date, operation, src_remote_server_id, path, client_ip ]`, `[ end_date, operation, dest_remote_server_id, path, client_ip ]`, `[ end_date, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ end_date, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ end_date, status, src_remote_server_id, path, client_ip ]`, `[ end_date, status, dest_remote_server_id, path, client_ip ]`, `[ end_date, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ operation, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ operation, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ operation, status, src_remote_server_id, path, client_ip ]`, `[ operation, status, dest_remote_server_id, path, client_ip ]`, `[ operation, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status, src_remote_server_id, dest_remote_server_id ]`, `[ start_date, end_date, operation, status, src_remote_server_id, path ]`, `[ start_date, end_date, operation, status, src_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, status, dest_remote_server_id, path ]`, `[ start_date, end_date, operation, status, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, status, path, client_ip ]`, `[ start_date, end_date, operation, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, end_date, operation, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, src_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, end_date, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id, path, client_ip ]`, `[ start_date, end_date, status, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, operation, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, operation, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, operation, status, src_remote_server_id, path, client_ip ]`, `[ start_date, operation, status, dest_remote_server_id, path, client_ip ]`, `[ start_date, operation, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ end_date, operation, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ end_date, operation, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ end_date, operation, status, src_remote_server_id, path, client_ip ]`, `[ end_date, operation, status, dest_remote_server_id, path, client_ip ]`, `[ end_date, operation, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ end_date, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ operation, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status, src_remote_server_id, dest_remote_server_id, path ]`, `[ start_date, end_date, operation, status, src_remote_server_id, dest_remote_server_id, client_ip ]`, `[ start_date, end_date, operation, status, src_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, status, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, operation, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, end_date, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`, `[ start_date, operation, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]` or `[ end_date, operation, status, src_remote_server_id, dest_remote_server_id, path, client_ip ]`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    return ListObj(
        OutboundConnectionLog,
        "GET",
        "/outbound_connection_logs",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return OutboundConnectionLog(*args, **kwargs)
