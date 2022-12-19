import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class UsageSnapshot:
    default_attributes = {
        'id': None,     # int64 - Usage snapshot ID
        'start_at': None,     # date-time - Usage snapshot start date/time
        'end_at': None,     # date-time - Usage snapshot end date/time
        'high_water_user_count': None,     # double - Highest user count number in time period
        'current_storage': None,     # double - Current total Storage Usage GB as of end date (not necessarily high water mark, which is used for billing)
        'high_water_storage': None,     # double - Highest Storage Usage GB recorded in time period (used for billing)
        'usage_by_top_level_dir': None,     # object - Storage Usage - map of root folders to their usage as of end date (not necessarily high water mark, which is used for billing)
        'root_storage': None,     # double - Storage Usage for root folder as of end date (not necessarily high water mark, which is used for billing)
        'deleted_files_counted_in_minimum': None,     # double - Storage Usage for files that are deleted but uploaded within last 30 days as of end date (not necessarily high water mark, which is used for billing)
        'deleted_files_storage': None,     # double - Storage Usage for files that are deleted but retained as backups as of end date (not necessarily high water mark, which is used for billing)
        'total_billable_usage': None,     # double - Storage + Transfer Usage - Total Billable amount
        'total_billable_transfer_usage': None,     # double - Transfer usage for period - Total Billable amount
        'bytes_sent': None,     # double - Transfer Usage for period - Outbound GB from Files Native Storage
        'sync_bytes_received': None,     # double - Transfer Usage for period - Inbound GB to Remote Servers (Sync/Mount)
        'sync_bytes_sent': None,     # double - Transfer Usage for period - Outbound GB from Remote Servers (Sync/Mount)
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in UsageSnapshot.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in UsageSnapshot.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(UsageSnapshot,"GET", "/usage_snapshots", params, options)

def all(params = None, options = None):
    list(params, options)

def new(*args, **kwargs):
    return UsageSnapshot(*args, **kwargs)