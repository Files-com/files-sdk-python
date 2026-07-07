import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SyncApiUsageSnapshotReport:
    default_attributes = {
        "start_time": None,  # date-time - start time of statistics collection
        "end_time": None,  # date-time - end time of statistics collection
        "uuid": None,  # string - Unique ID for this entry
        "auth_cache_hits": None,  # int64 - Numbers of hits of the authentication cache
        "auth_cache_misses": None,  # int64 - Numbers of misses of the authentication cache
        "auth_api_requests_for_sftp": None,  # int64 - A count of api authentications requests for SFTP
        "auth_api_requests_for_ftp": None,  # int64 - A count of api authentications requests for FTP
        "auth_api_requests_for_dav": None,  # int64 - A count of api authentications requests for DAV
        "auth_api_requests_for_desktop": None,  # int64 - A count of api authentications requests for Desktop
        "auth_api_requests_for_restapi": None,  # int64 - A count of api authentications requests for Restapi
        "number_of_sync_api_usage_snapshots": None,  # int64 - A count of the number of api usage logs
        "sync_api_usage_snapshots": None,  # array(object) - A list of all the api usage logs
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
        ) in SyncApiUsageSnapshotReport.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SyncApiUsageSnapshotReport.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The SyncApiUsageSnapshotReport object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   start_time - string - start time of statistics collection
#   end_time - string - end time of statistics collection
#   uuid - string - Unique ID for this entry
#   auth_cache_hits - int64 - Numbers of hits of the authentication cache
#   auth_cache_misses - int64 - Numbers of misses of the authentication cache
#   auth_api_requests_for_sftp - int64 - A count of api authentications requests for SFTP
#   auth_api_requests_for_ftp - int64 - A count of api authentications requests for FTP
#   auth_api_requests_for_dav - int64 - A count of api authentications requests for DAV
#   auth_api_requests_for_desktop - int64 - A count of api authentications requests for Desktop
#   auth_api_requests_for_restapi - int64 - A count of api authentications requests for Restapi
#   number_of_sync_api_usage_snapshots - int64 - A count of the number of api usage logs
#   sync_api_usage_snapshots - array(object)
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "start_time" in params and not isinstance(params["start_time"], str):
        raise InvalidParameterError("Bad parameter: start_time must be an str")
    if "end_time" in params and not isinstance(params["end_time"], str):
        raise InvalidParameterError("Bad parameter: end_time must be an str")
    if "uuid" in params and not isinstance(params["uuid"], str):
        raise InvalidParameterError("Bad parameter: uuid must be an str")
    if "auth_cache_hits" in params and not isinstance(
        params["auth_cache_hits"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: auth_cache_hits must be an int"
        )
    if "auth_cache_misses" in params and not isinstance(
        params["auth_cache_misses"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: auth_cache_misses must be an int"
        )
    if "auth_api_requests_for_sftp" in params and not isinstance(
        params["auth_api_requests_for_sftp"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: auth_api_requests_for_sftp must be an int"
        )
    if "auth_api_requests_for_ftp" in params and not isinstance(
        params["auth_api_requests_for_ftp"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: auth_api_requests_for_ftp must be an int"
        )
    if "auth_api_requests_for_dav" in params and not isinstance(
        params["auth_api_requests_for_dav"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: auth_api_requests_for_dav must be an int"
        )
    if "auth_api_requests_for_desktop" in params and not isinstance(
        params["auth_api_requests_for_desktop"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: auth_api_requests_for_desktop must be an int"
        )
    if "auth_api_requests_for_restapi" in params and not isinstance(
        params["auth_api_requests_for_restapi"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: auth_api_requests_for_restapi must be an int"
        )
    if "number_of_sync_api_usage_snapshots" in params and not isinstance(
        params["number_of_sync_api_usage_snapshots"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: number_of_sync_api_usage_snapshots must be an int"
        )
    if "sync_api_usage_snapshots" in params and not isinstance(
        params["sync_api_usage_snapshots"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: sync_api_usage_snapshots must be an list"
        )
    response, options = Api.send_request(
        "POST", "/sync_api_usage_snapshot_reports", params, options
    )
    return SyncApiUsageSnapshotReport(response.data, options)


def new(*args, **kwargs):
    return SyncApiUsageSnapshotReport(*args, **kwargs)
