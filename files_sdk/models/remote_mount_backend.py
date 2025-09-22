import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class RemoteMountBackend:
    default_attributes = {
        "canary_file_path": None,  # string - Path to the canary file used for health checks.
        "enabled": None,  # boolean - True if this backend is enabled.
        "fall": None,  # int64 - Number of consecutive failures before considering the backend unhealthy.
        "health_check_enabled": None,  # boolean - True if health checks are enabled for this backend.
        "health_check_results": None,  # array(object) - Array of recent health check results.
        "health_check_type": None,  # string - Type of health check to perform.
        "id": None,  # int64 - Unique identifier for this backend.
        "interval": None,  # int64 - Interval in seconds between health checks.
        "min_free_cpu": None,  # double - Minimum free CPU percentage required for this backend to be considered healthy.
        "min_free_mem": None,  # double - Minimum free memory percentage required for this backend to be considered healthy.
        "priority": None,  # int64 - Priority of this backend.
        "remote_path": None,  # string - Path on the remote server to treat as the root of this mount.
        "remote_server_id": None,  # int64 - The remote server that this backend is associated with.
        "remote_server_mount_id": None,  # int64 - The mount ID of the Remote Server Mount that this backend is associated with.
        "rise": None,  # int64 - Number of consecutive successes before considering the backend healthy.
        "status": None,  # string - Status of this backend.
        "undergoing_maintenance": None,  # boolean - True if this backend is undergoing maintenance.
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
        ) in RemoteMountBackend.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in RemoteMountBackend.default_attributes
            if getattr(self, k, None) is not None
        }

    # Reset backend status to healthy
    def reset_status(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "POST",
            "/remote_mount_backends/{id}/reset_status".format(id=params["id"]),
            params,
            self.options,
        )

    # Parameters:
    #   enabled - boolean - True if this backend is enabled.
    #   fall - int64 - Number of consecutive failures before considering the backend unhealthy.
    #   health_check_enabled - boolean - True if health checks are enabled for this backend.
    #   health_check_type - string - Type of health check to perform.
    #   interval - int64 - Interval in seconds between health checks.
    #   min_free_cpu - double - Minimum free CPU percentage required for this backend to be considered healthy.
    #   min_free_mem - double - Minimum free memory percentage required for this backend to be considered healthy.
    #   priority - int64 - Priority of this backend.
    #   remote_path - string - Path on the remote server to treat as the root of this mount.
    #   rise - int64 - Number of consecutive successes before considering the backend healthy.
    #   canary_file_path - string - Path to the canary file used for health checks.
    #   remote_server_id - int64 - The remote server that this backend is associated with.
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "fall" in params and not isinstance(params["fall"], int):
            raise InvalidParameterError("Bad parameter: fall must be an int")
        if "health_check_type" in params and not isinstance(
            params["health_check_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: health_check_type must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], int):
            raise InvalidParameterError(
                "Bad parameter: interval must be an int"
            )
        if "priority" in params and not isinstance(params["priority"], int):
            raise InvalidParameterError(
                "Bad parameter: priority must be an int"
            )
        if "remote_path" in params and not isinstance(
            params["remote_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: remote_path must be an str"
            )
        if "rise" in params and not isinstance(params["rise"], int):
            raise InvalidParameterError("Bad parameter: rise must be an int")
        if "canary_file_path" in params and not isinstance(
            params["canary_file_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: canary_file_path must be an str"
            )
        if "remote_server_id" in params and not isinstance(
            params["remote_server_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: remote_server_id must be an int"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/remote_mount_backends/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "DELETE",
            "/remote_mount_backends/{id}".format(id=params["id"]),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            new_obj = self.update(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            return True
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `remote_server_mount_id`.
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
    return ListObj(
        RemoteMountBackend, "GET", "/remote_mount_backends", params, options
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Remote Mount Backend ID.
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
        "GET",
        "/remote_mount_backends/{id}".format(id=params["id"]),
        params,
        options,
    )
    return RemoteMountBackend(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   enabled - boolean - True if this backend is enabled.
#   fall - int64 - Number of consecutive failures before considering the backend unhealthy.
#   health_check_enabled - boolean - True if health checks are enabled for this backend.
#   health_check_type - string - Type of health check to perform.
#   interval - int64 - Interval in seconds between health checks.
#   min_free_cpu - double - Minimum free CPU percentage required for this backend to be considered healthy.
#   min_free_mem - double - Minimum free memory percentage required for this backend to be considered healthy.
#   priority - int64 - Priority of this backend.
#   remote_path - string - Path on the remote server to treat as the root of this mount.
#   rise - int64 - Number of consecutive successes before considering the backend healthy.
#   canary_file_path (required) - string - Path to the canary file used for health checks.
#   remote_server_mount_id (required) - int64 - The mount ID of the Remote Server Mount that this backend is associated with.
#   remote_server_id (required) - int64 - The remote server that this backend is associated with.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "enabled" in params and not isinstance(params["enabled"], bool):
        raise InvalidParameterError("Bad parameter: enabled must be an bool")
    if "fall" in params and not isinstance(params["fall"], int):
        raise InvalidParameterError("Bad parameter: fall must be an int")
    if "health_check_enabled" in params and not isinstance(
        params["health_check_enabled"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: health_check_enabled must be an bool"
        )
    if "health_check_type" in params and not isinstance(
        params["health_check_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: health_check_type must be an str"
        )
    if "interval" in params and not isinstance(params["interval"], int):
        raise InvalidParameterError("Bad parameter: interval must be an int")
    if "min_free_cpu" in params and not isinstance(
        params["min_free_cpu"], float
    ):
        raise InvalidParameterError(
            "Bad parameter: min_free_cpu must be an float"
        )
    if "min_free_mem" in params and not isinstance(
        params["min_free_mem"], float
    ):
        raise InvalidParameterError(
            "Bad parameter: min_free_mem must be an float"
        )
    if "priority" in params and not isinstance(params["priority"], int):
        raise InvalidParameterError("Bad parameter: priority must be an int")
    if "remote_path" in params and not isinstance(params["remote_path"], str):
        raise InvalidParameterError(
            "Bad parameter: remote_path must be an str"
        )
    if "rise" in params and not isinstance(params["rise"], int):
        raise InvalidParameterError("Bad parameter: rise must be an int")
    if "canary_file_path" in params and not isinstance(
        params["canary_file_path"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: canary_file_path must be an str"
        )
    if "remote_server_mount_id" in params and not isinstance(
        params["remote_server_mount_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: remote_server_mount_id must be an int"
        )
    if "remote_server_id" in params and not isinstance(
        params["remote_server_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: remote_server_id must be an int"
        )
    if "canary_file_path" not in params:
        raise MissingParameterError("Parameter missing: canary_file_path")
    if "remote_server_mount_id" not in params:
        raise MissingParameterError(
            "Parameter missing: remote_server_mount_id"
        )
    if "remote_server_id" not in params:
        raise MissingParameterError("Parameter missing: remote_server_id")
    response, options = Api.send_request(
        "POST", "/remote_mount_backends", params, options
    )
    return RemoteMountBackend(response.data, options)


# Reset backend status to healthy
def reset_status(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "POST",
        "/remote_mount_backends/{id}/reset_status".format(id=params["id"]),
        params,
        options,
    )


# Parameters:
#   enabled - boolean - True if this backend is enabled.
#   fall - int64 - Number of consecutive failures before considering the backend unhealthy.
#   health_check_enabled - boolean - True if health checks are enabled for this backend.
#   health_check_type - string - Type of health check to perform.
#   interval - int64 - Interval in seconds between health checks.
#   min_free_cpu - double - Minimum free CPU percentage required for this backend to be considered healthy.
#   min_free_mem - double - Minimum free memory percentage required for this backend to be considered healthy.
#   priority - int64 - Priority of this backend.
#   remote_path - string - Path on the remote server to treat as the root of this mount.
#   rise - int64 - Number of consecutive successes before considering the backend healthy.
#   canary_file_path - string - Path to the canary file used for health checks.
#   remote_server_id - int64 - The remote server that this backend is associated with.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "enabled" in params and not isinstance(params["enabled"], bool):
        raise InvalidParameterError("Bad parameter: enabled must be an bool")
    if "fall" in params and not isinstance(params["fall"], int):
        raise InvalidParameterError("Bad parameter: fall must be an int")
    if "health_check_enabled" in params and not isinstance(
        params["health_check_enabled"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: health_check_enabled must be an bool"
        )
    if "health_check_type" in params and not isinstance(
        params["health_check_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: health_check_type must be an str"
        )
    if "interval" in params and not isinstance(params["interval"], int):
        raise InvalidParameterError("Bad parameter: interval must be an int")
    if "min_free_cpu" in params and not isinstance(
        params["min_free_cpu"], float
    ):
        raise InvalidParameterError(
            "Bad parameter: min_free_cpu must be an float"
        )
    if "min_free_mem" in params and not isinstance(
        params["min_free_mem"], float
    ):
        raise InvalidParameterError(
            "Bad parameter: min_free_mem must be an float"
        )
    if "priority" in params and not isinstance(params["priority"], int):
        raise InvalidParameterError("Bad parameter: priority must be an int")
    if "remote_path" in params and not isinstance(params["remote_path"], str):
        raise InvalidParameterError(
            "Bad parameter: remote_path must be an str"
        )
    if "rise" in params and not isinstance(params["rise"], int):
        raise InvalidParameterError("Bad parameter: rise must be an int")
    if "canary_file_path" in params and not isinstance(
        params["canary_file_path"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: canary_file_path must be an str"
        )
    if "remote_server_id" in params and not isinstance(
        params["remote_server_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: remote_server_id must be an int"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/remote_mount_backends/{id}".format(id=params["id"]),
        params,
        options,
    )
    return RemoteMountBackend(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "DELETE",
        "/remote_mount_backends/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return RemoteMountBackend(*args, **kwargs)
