import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
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


class SyncRun:
    """A sync run record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - SyncRun ID
        body: string - Log or summary body for this run
        bytes_synced: int64 - Total bytes synced in this run
        compared_files: int64 - Number of files compared
        compared_folders: int64 - Number of folders compared
        completed_at: date-time - When this run was completed
        created_at: date-time - When this run was created
        dest_remote_server_type: string - Destination remote server type, if any
        dry_run: boolean - Whether this run was a dry run (no actual changes made)
        errored_files: int64 - Number of files that errored
        estimated_bytes_count: int64 - Estimated bytes count for this run
        event_errors: array(string) - Array of errors encountered during the run
        log_url: string - Link to external log file.
        runtime: double - Total runtime in seconds
        site_id: int64 - Site ID
        workspace_id: int64 - Workspace ID
        src_remote_server_type: string - Source remote server type, if any
        status: string - Status of the sync run (success, failure, partial_failure, in_progress, skipped)
        successful_files: int64 - Number of files successfully synced
        sync_id: int64 - ID of the Sync this run belongs to
        sync_name: string - Name of the Sync this run belongs to
        updated_at: date-time - When this run was last updated
        live_transfers: array(object) - Array of in-progress file transfers with progress data. Only present when the sync run status is in_progress.
    """

    default_attributes = {
        "id": None,  # int64 - SyncRun ID
        "body": None,  # string - Log or summary body for this run
        "bytes_synced": None,  # int64 - Total bytes synced in this run
        "compared_files": None,  # int64 - Number of files compared
        "compared_folders": None,  # int64 - Number of folders compared
        "completed_at": None,  # date-time - When this run was completed
        "created_at": None,  # date-time - When this run was created
        "dest_remote_server_type": None,  # string - Destination remote server type, if any
        "dry_run": None,  # boolean - Whether this run was a dry run (no actual changes made)
        "errored_files": None,  # int64 - Number of files that errored
        "estimated_bytes_count": None,  # int64 - Estimated bytes count for this run
        "event_errors": None,  # array(string) - Array of errors encountered during the run
        "log_url": None,  # string - Link to external log file.
        "runtime": None,  # double - Total runtime in seconds
        "site_id": None,  # int64 - Site ID
        "workspace_id": None,  # int64 - Workspace ID
        "src_remote_server_type": None,  # string - Source remote server type, if any
        "status": None,  # string - Status of the sync run (success, failure, partial_failure, in_progress, skipped)
        "successful_files": None,  # int64 - Number of files successfully synced
        "sync_id": None,  # int64 - ID of the Sync this run belongs to
        "sync_name": None,  # string - Name of the Sync this run belongs to
        "updated_at": None,  # date-time - When this run was last updated
        "live_transfers": None,  # array(object) - Array of in-progress file transfers with progress data. Only present when the sync run status is in_progress.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    body: str | None
    bytes_synced: int | None
    compared_files: int | None
    compared_folders: int | None
    completed_at: str | None
    created_at: str | None
    dest_remote_server_type: str | None
    dry_run: bool | None
    errored_files: int | None
    estimated_bytes_count: int | None
    event_errors: builtins.list[str] | None
    log_url: str | None
    runtime: float | None
    site_id: int | None
    workspace_id: int | None
    src_remote_server_type: str | None
    status: str | None
    successful_files: int | None
    sync_id: int | None
    sync_name: str | None
    updated_at: str | None
    live_transfers: builtins.list[dict[str, Any]] | None

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
        for attribute, default_value in SyncRun.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SyncRun.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class SyncRunResource:
    """SyncRun operations that use one client's configuration.

    Get one from a client, such as ``client.sync_run``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SyncRun]:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id`, `sync_id`, `created_at` or `status`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `status`, `dry_run`, `workspace_id`, `src_remote_server_type`, `dest_remote_server_type` or `sync_id`. Valid field combinations are `[ status, created_at ]`, `[ workspace_id, created_at ]`, `[ src_remote_server_type, created_at ]`, `[ dest_remote_server_type, created_at ]`, `[ sync_id, created_at ]`, `[ workspace_id, status ]`, `[ src_remote_server_type, status ]`, `[ dest_remote_server_type, status ]`, `[ sync_id, status ]`, `[ workspace_id, src_remote_server_type ]`, `[ workspace_id, dest_remote_server_type ]`, `[ workspace_id, sync_id ]`, `[ workspace_id, status, created_at ]`, `[ src_remote_server_type, status, created_at ]`, `[ dest_remote_server_type, status, created_at ]`, `[ sync_id, status, created_at ]`, `[ workspace_id, src_remote_server_type, created_at ]`, `[ workspace_id, dest_remote_server_type, created_at ]`, `[ workspace_id, sync_id, created_at ]`, `[ workspace_id, src_remote_server_type, status ]`, `[ workspace_id, dest_remote_server_type, status ]`, `[ workspace_id, sync_id, status ]`, `[ workspace_id, src_remote_server_type, status, created_at ]`, `[ workspace_id, dest_remote_server_type, status, created_at ]` or `[ workspace_id, sync_id, status, created_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_gt must be an dict"
            )
        if "filter_gteq" in params and not isinstance(
            params["filter_gteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_gteq must be an dict"
            )
        if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_lt must be an dict"
            )
        if "filter_lteq" in params and not isinstance(
            params["filter_lteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_lteq must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(SyncRun, "GET", "/sync_runs", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SyncRun]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SyncRun:
        """Parameters:
        id (required) - int64 - Sync Run ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> SyncRun:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/sync_runs/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, SyncRun)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SyncRun:
        """The same as find()."""
        return self.find(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SyncRun:
        """A new SyncRun with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = SyncRun(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SyncRunResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SyncRun]:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id`, `sync_id`, `created_at` or `status`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `status`, `dry_run`, `workspace_id`, `src_remote_server_type`, `dest_remote_server_type` or `sync_id`. Valid field combinations are `[ status, created_at ]`, `[ workspace_id, created_at ]`, `[ src_remote_server_type, created_at ]`, `[ dest_remote_server_type, created_at ]`, `[ sync_id, created_at ]`, `[ workspace_id, status ]`, `[ src_remote_server_type, status ]`, `[ dest_remote_server_type, status ]`, `[ sync_id, status ]`, `[ workspace_id, src_remote_server_type ]`, `[ workspace_id, dest_remote_server_type ]`, `[ workspace_id, sync_id ]`, `[ workspace_id, status, created_at ]`, `[ src_remote_server_type, status, created_at ]`, `[ dest_remote_server_type, status, created_at ]`, `[ sync_id, status, created_at ]`, `[ workspace_id, src_remote_server_type, created_at ]`, `[ workspace_id, dest_remote_server_type, created_at ]`, `[ workspace_id, sync_id, created_at ]`, `[ workspace_id, src_remote_server_type, status ]`, `[ workspace_id, dest_remote_server_type, status ]`, `[ workspace_id, sync_id, status ]`, `[ workspace_id, src_remote_server_type, status, created_at ]`, `[ workspace_id, dest_remote_server_type, status, created_at ]` or `[ workspace_id, sync_id, status, created_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SyncRun]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SyncRun:
    """Parameters:
    id (required) - int64 - Sync Run ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SyncRun:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def new(*args, **kwargs) -> SyncRun:
    return SyncRun(*args, **kwargs)
