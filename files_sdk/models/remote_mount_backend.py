import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from decimal import Decimal
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class RemoteMountBackend:
    """A remote mount backend record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        canary_file_path: string - Path to the canary file used for health checks.
        enabled: boolean - True if this backend is enabled.
        fall: int64 - Number of consecutive failures before considering the backend unhealthy.
        health_check_enabled: boolean - True if health checks are enabled for this backend.
        health_check_results: array(object) - Array of recent health check results.
        health_check_type: string - Type of health check to perform.
        id: int64 - Unique identifier for this backend.
        interval: int64 - Interval in seconds between health checks.
        min_free_cpu: decimal - Minimum free CPU percentage required for this backend to be considered healthy.
        min_free_mem: decimal - Minimum free memory percentage required for this backend to be considered healthy.
        priority: int64 - Priority of this backend.
        remote_path: string - Path on the remote server to treat as the root of this mount.
        remote_server_id: int64 - The remote server that this backend is associated with.
        remote_server_mount_id: int64 - The mount ID of the Remote Server Mount that this backend is associated with.
        rise: int64 - Number of consecutive successes before considering the backend healthy.
        status: string - Status of this backend.
        undergoing_maintenance: boolean - True if this backend is undergoing maintenance.
    """

    __decimal_fields = {
        "min_free_cpu",
        "min_free_mem",
    }
    __decimal_array_fields = {}
    default_attributes = {
        "canary_file_path": None,  # string - Path to the canary file used for health checks.
        "enabled": None,  # boolean - True if this backend is enabled.
        "fall": None,  # int64 - Number of consecutive failures before considering the backend unhealthy.
        "health_check_enabled": None,  # boolean - True if health checks are enabled for this backend.
        "health_check_results": None,  # array(object) - Array of recent health check results.
        "health_check_type": None,  # string - Type of health check to perform.
        "id": None,  # int64 - Unique identifier for this backend.
        "interval": None,  # int64 - Interval in seconds between health checks.
        "min_free_cpu": None,  # decimal - Minimum free CPU percentage required for this backend to be considered healthy.
        "min_free_mem": None,  # decimal - Minimum free memory percentage required for this backend to be considered healthy.
        "priority": None,  # int64 - Priority of this backend.
        "remote_path": None,  # string - Path on the remote server to treat as the root of this mount.
        "remote_server_id": None,  # int64 - The remote server that this backend is associated with.
        "remote_server_mount_id": None,  # int64 - The mount ID of the Remote Server Mount that this backend is associated with.
        "rise": None,  # int64 - Number of consecutive successes before considering the backend healthy.
        "status": None,  # string - Status of this backend.
        "undergoing_maintenance": None,  # boolean - True if this backend is undergoing maintenance.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    canary_file_path: str | None
    enabled: bool | None
    fall: int | None
    health_check_enabled: bool | None
    health_check_results: builtins.list[dict[str, Any]] | None
    health_check_type: str | None
    id: int | None
    interval: int | None
    min_free_cpu: Decimal | None
    min_free_mem: Decimal | None
    priority: int | None
    remote_path: str | None
    remote_server_id: int | None
    remote_server_mount_id: int | None
    rise: int | None
    status: str | None
    undergoing_maintenance: bool | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

    def set_attributes(self, attributes):
        # Convert every value before assigning any, so a malformed decimal
        # cannot leave the object partly updated.
        values = {}
        for (
            attribute,
            default_value,
        ) in RemoteMountBackend.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if value is None:
                values[attribute] = None
            elif attribute in RemoteMountBackend.__decimal_fields:
                values[attribute] = Decimal(str(value))
            elif attribute in RemoteMountBackend.__decimal_array_fields:
                values[attribute] = [Decimal(str(v)) for v in (value or [])]
            else:
                values[attribute] = value
        for attribute, value in values.items():
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in RemoteMountBackend.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in RemoteMountBackend.__decimal_fields:
            if k in attrs:
                attrs[k] = str(attrs[k])
        for k in RemoteMountBackend.__decimal_array_fields:
            if k in attrs:
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def reset_status(self, params: dict[str, Any] | None = None) -> None:
        """Reset backend status to healthy"""
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "POST",
            "/remote_mount_backends/"
            + path_value(params["id"])
            + "/reset_status",
            params,
        )

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          enabled - boolean - True if this backend is enabled.
          fall - int64 - Number of consecutive failures before considering the backend unhealthy.
          health_check_enabled - boolean - True if health checks are enabled for this backend.
          health_check_type - string - Type of health check to perform.
          interval - int64 - Interval in seconds between health checks.
          min_free_cpu - double - Minimum free CPU percentage required for this backend to be considered healthy.
          min_free_mem - double - Minimum free memory percentage required for this backend to be considered healthy.
          priority - int64 - Priority of this backend.
          remote_path - string - Path on the remote server to treat as the root of this mount.
          rise - int64 - Number of consecutive successes before considering the backend healthy.
          canary_file_path - string - Path to the canary file used for health checks.
          remote_server_id - int64 - The remote server that this backend is associated with.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "enabled" in params and isinstance(
            params["enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        if "fall" in params and (
            not isinstance(params["fall"], int)
            or isinstance(params["fall"], bool)
        ):
            raise InvalidParameterError("Bad parameter: fall must be an int")
        if "health_check_enabled" in params and isinstance(
            params["health_check_enabled"], (builtins.list, tuple, dict)
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
        if "interval" in params and (
            not isinstance(params["interval"], int)
            or isinstance(params["interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: interval must be an int"
            )
        if "priority" in params and (
            not isinstance(params["priority"], int)
            or isinstance(params["priority"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: priority must be an int"
            )
        if "remote_path" in params and not isinstance(
            params["remote_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: remote_path must be an str"
            )
        if "rise" in params and (
            not isinstance(params["rise"], int)
            or isinstance(params["rise"], bool)
        ):
            raise InvalidParameterError("Bad parameter: rise must be an int")
        if "canary_file_path" in params and not isinstance(
            params["canary_file_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: canary_file_path must be an str"
            )
        if "remote_server_id" in params and (
            not isinstance(params["remote_server_id"], int)
            or isinstance(params["remote_server_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: remote_server_id must be an int"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH",
            "/remote_mount_backends/" + path_value(params["id"]),
            params,
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE",
            "/remote_mount_backends/" + path_value(params["id"]),
            params,
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = RemoteMountBackendResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class RemoteMountBackendResource:
    """RemoteMountBackend operations that use one client's configuration.

    Get one from a client, such as ``client.remote_mount_backend``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[RemoteMountBackend]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `remote_server_mount_id`.
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            RemoteMountBackend,
            "GET",
            "/remote_mount_backends",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[RemoteMountBackend]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteMountBackend:
        """Parameters:
        id (required) - int64 - Remote Mount Backend ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> RemoteMountBackend:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/remote_mount_backends/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, RemoteMountBackend)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteMountBackend:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteMountBackend:
        """Parameters:
        enabled - boolean - True if this backend is enabled.
        fall - int64 - Number of consecutive failures before considering the backend unhealthy.
        health_check_enabled - boolean - True if health checks are enabled for this backend.
        health_check_type - string - Type of health check to perform.
        interval - int64 - Interval in seconds between health checks.
        min_free_cpu - double - Minimum free CPU percentage required for this backend to be considered healthy.
        min_free_mem - double - Minimum free memory percentage required for this backend to be considered healthy.
        priority - int64 - Priority of this backend.
        remote_path - string - Path on the remote server to treat as the root of this mount.
        rise - int64 - Number of consecutive successes before considering the backend healthy.
        canary_file_path (required) - string - Path to the canary file used for health checks.
        remote_server_mount_id (required) - int64 - The mount ID of the Remote Server Mount that this backend is associated with.
        remote_server_id (required) - int64 - The remote server that this backend is associated with.
        """
        params = copy_params(params)
        if "enabled" in params and not isinstance(params["enabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        if "fall" in params and (
            not isinstance(params["fall"], int)
            or isinstance(params["fall"], bool)
        ):
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
        if "interval" in params and (
            not isinstance(params["interval"], int)
            or isinstance(params["interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: interval must be an int"
            )
        if "min_free_cpu" in params and not isinstance(
            params["min_free_cpu"], (float, Decimal, str)
        ):
            raise InvalidParameterError(
                "Bad parameter: min_free_cpu must be one of float, Decimal, str"
            )
        if "min_free_mem" in params and not isinstance(
            params["min_free_mem"], (float, Decimal, str)
        ):
            raise InvalidParameterError(
                "Bad parameter: min_free_mem must be one of float, Decimal, str"
            )
        if "priority" in params and (
            not isinstance(params["priority"], int)
            or isinstance(params["priority"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: priority must be an int"
            )
        if "remote_path" in params and not isinstance(
            params["remote_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: remote_path must be an str"
            )
        if "rise" in params and (
            not isinstance(params["rise"], int)
            or isinstance(params["rise"], bool)
        ):
            raise InvalidParameterError("Bad parameter: rise must be an int")
        if "canary_file_path" in params and not isinstance(
            params["canary_file_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: canary_file_path must be an str"
            )
        if "remote_server_mount_id" in params and (
            not isinstance(params["remote_server_mount_id"], int)
            or isinstance(params["remote_server_mount_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: remote_server_mount_id must be an int"
            )
        if "remote_server_id" in params and (
            not isinstance(params["remote_server_id"], int)
            or isinstance(params["remote_server_id"], bool)
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
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/remote_mount_backends", params)
        return operation.decode_model(response, RemoteMountBackend)

    def reset_status(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Reset backend status to healthy"""
        return self.__reset_status({"id": id}, params, options)

    def __reset_status(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST",
            "/remote_mount_backends/"
            + path_value(params["id"])
            + "/reset_status",
            params,
        )

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteMountBackend:
        """Parameters:
        enabled - boolean - True if this backend is enabled.
        fall - int64 - Number of consecutive failures before considering the backend unhealthy.
        health_check_enabled - boolean - True if health checks are enabled for this backend.
        health_check_type - string - Type of health check to perform.
        interval - int64 - Interval in seconds between health checks.
        min_free_cpu - double - Minimum free CPU percentage required for this backend to be considered healthy.
        min_free_mem - double - Minimum free memory percentage required for this backend to be considered healthy.
        priority - int64 - Priority of this backend.
        remote_path - string - Path on the remote server to treat as the root of this mount.
        rise - int64 - Number of consecutive successes before considering the backend healthy.
        canary_file_path - string - Path to the canary file used for health checks.
        remote_server_id - int64 - The remote server that this backend is associated with.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> RemoteMountBackend:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "enabled" in params and not isinstance(params["enabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        if "fall" in params and (
            not isinstance(params["fall"], int)
            or isinstance(params["fall"], bool)
        ):
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
        if "interval" in params and (
            not isinstance(params["interval"], int)
            or isinstance(params["interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: interval must be an int"
            )
        if "min_free_cpu" in params and not isinstance(
            params["min_free_cpu"], (float, Decimal, str)
        ):
            raise InvalidParameterError(
                "Bad parameter: min_free_cpu must be one of float, Decimal, str"
            )
        if "min_free_mem" in params and not isinstance(
            params["min_free_mem"], (float, Decimal, str)
        ):
            raise InvalidParameterError(
                "Bad parameter: min_free_mem must be one of float, Decimal, str"
            )
        if "priority" in params and (
            not isinstance(params["priority"], int)
            or isinstance(params["priority"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: priority must be an int"
            )
        if "remote_path" in params and not isinstance(
            params["remote_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: remote_path must be an str"
            )
        if "rise" in params and (
            not isinstance(params["rise"], int)
            or isinstance(params["rise"], bool)
        ):
            raise InvalidParameterError("Bad parameter: rise must be an int")
        if "canary_file_path" in params and not isinstance(
            params["canary_file_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: canary_file_path must be an str"
            )
        if "remote_server_id" in params and (
            not isinstance(params["remote_server_id"], int)
            or isinstance(params["remote_server_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: remote_server_id must be an int"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH",
            "/remote_mount_backends/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, RemoteMountBackend)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE",
            "/remote_mount_backends/" + path_value(params["id"]),
            params,
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteMountBackend:
        """A new RemoteMountBackend with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = RemoteMountBackend(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = RemoteMountBackendResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[RemoteMountBackend]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `remote_server_mount_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[RemoteMountBackend]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> RemoteMountBackend:
    """Parameters:
    id (required) - int64 - Remote Mount Backend ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> RemoteMountBackend:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> RemoteMountBackend:
    """Parameters:
    enabled - boolean - True if this backend is enabled.
    fall - int64 - Number of consecutive failures before considering the backend unhealthy.
    health_check_enabled - boolean - True if health checks are enabled for this backend.
    health_check_type - string - Type of health check to perform.
    interval - int64 - Interval in seconds between health checks.
    min_free_cpu - double - Minimum free CPU percentage required for this backend to be considered healthy.
    min_free_mem - double - Minimum free memory percentage required for this backend to be considered healthy.
    priority - int64 - Priority of this backend.
    remote_path - string - Path on the remote server to treat as the root of this mount.
    rise - int64 - Number of consecutive successes before considering the backend healthy.
    canary_file_path (required) - string - Path to the canary file used for health checks.
    remote_server_mount_id (required) - int64 - The mount ID of the Remote Server Mount that this backend is associated with.
    remote_server_id (required) - int64 - The remote server that this backend is associated with.
    """
    return _legacy_resource.create(params, options)


def reset_status(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Reset backend status to healthy"""
    _legacy_resource.reset_status(id, params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> RemoteMountBackend:
    """Parameters:
    enabled - boolean - True if this backend is enabled.
    fall - int64 - Number of consecutive failures before considering the backend unhealthy.
    health_check_enabled - boolean - True if health checks are enabled for this backend.
    health_check_type - string - Type of health check to perform.
    interval - int64 - Interval in seconds between health checks.
    min_free_cpu - double - Minimum free CPU percentage required for this backend to be considered healthy.
    min_free_mem - double - Minimum free memory percentage required for this backend to be considered healthy.
    priority - int64 - Priority of this backend.
    remote_path - string - Path on the remote server to treat as the root of this mount.
    rise - int64 - Number of consecutive successes before considering the backend healthy.
    canary_file_path - string - Path to the canary file used for health checks.
    remote_server_id - int64 - The remote server that this backend is associated with.
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> RemoteMountBackend:
    return RemoteMountBackend(*args, **kwargs)
