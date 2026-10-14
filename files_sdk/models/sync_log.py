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


class SyncLog:
    """A sync log record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        timestamp: date-time - Start Time of Action. Deprecrated: Use created_at.
        sync_id: int64 - Sync ID
        external_event_id: int64 - External Event ID used by legacy syncs
        sync_run_id: int64 - Sync Run ID
        error_type: string - Error type, if applicable
        message: string - Message
        operation: string - Operation type
        path: string - File path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        size: int64 - File size
        file_type: string - File type
        status: string - Status
        created_at: date-time - Start Time of Action
    """

    default_attributes = {
        "timestamp": None,  # date-time - Start Time of Action. Deprecrated: Use created_at.
        "sync_id": None,  # int64 - Sync ID
        "external_event_id": None,  # int64 - External Event ID used by legacy syncs
        "sync_run_id": None,  # int64 - Sync Run ID
        "error_type": None,  # string - Error type, if applicable
        "message": None,  # string - Message
        "operation": None,  # string - Operation type
        "path": None,  # string - File path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "size": None,  # int64 - File size
        "file_type": None,  # string - File type
        "status": None,  # string - Status
        "created_at": None,  # date-time - Start Time of Action
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    timestamp: str | None
    sync_id: int | None
    external_event_id: int | None
    sync_run_id: int | None
    error_type: str | None
    message: str | None
    operation: str | None
    path: str | None
    size: int | None
    file_type: str | None
    status: str | None
    created_at: str | None

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
        for attribute, default_value in SyncLog.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SyncLog.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class SyncLogResource:
    """SyncLog operations that use one client's configuration.

    Get one from a client, such as ``client.sync_log``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SyncLog]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 1000, 1,000 or less is recommended).
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `external_event_id`, `operation`, `status`, `sync_id`, `created_at` or `sync_run_id`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
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
        return ListObj(SyncLog, "GET", "/sync_logs", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SyncLog]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SyncLog:
        """A new SyncLog with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = SyncLog(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SyncLogResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SyncLog]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 1000, 1,000 or less is recommended).
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `external_event_id`, `operation`, `status`, `sync_id`, `created_at` or `sync_run_id`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ external_event_id ]`, `[ operation ]`, `[ status ]`, `[ sync_id ]`, `[ created_at ]`, `[ sync_run_id ]`, `[ external_event_id, operation ]`, `[ external_event_id, status ]`, `[ external_event_id, sync_id ]`, `[ external_event_id, created_at ]`, `[ external_event_id, sync_run_id ]`, `[ operation, status ]`, `[ operation, sync_id ]`, `[ operation, created_at ]`, `[ operation, sync_run_id ]`, `[ status, sync_id ]`, `[ status, created_at ]`, `[ status, sync_run_id ]`, `[ sync_id, created_at ]`, `[ sync_id, sync_run_id ]`, `[ created_at, sync_run_id ]`, `[ external_event_id, operation, status ]`, `[ external_event_id, operation, sync_id ]`, `[ external_event_id, operation, created_at ]`, `[ external_event_id, operation, sync_run_id ]`, `[ external_event_id, status, sync_id ]`, `[ external_event_id, status, created_at ]`, `[ external_event_id, status, sync_run_id ]`, `[ external_event_id, sync_id, created_at ]`, `[ external_event_id, sync_id, sync_run_id ]`, `[ external_event_id, created_at, sync_run_id ]`, `[ operation, status, sync_id ]`, `[ operation, status, created_at ]`, `[ operation, status, sync_run_id ]`, `[ operation, sync_id, created_at ]`, `[ operation, sync_id, sync_run_id ]`, `[ operation, created_at, sync_run_id ]`, `[ status, sync_id, created_at ]`, `[ status, sync_id, sync_run_id ]`, `[ status, created_at, sync_run_id ]`, `[ sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id ]`, `[ external_event_id, operation, status, created_at ]`, `[ external_event_id, operation, status, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at ]`, `[ external_event_id, operation, sync_id, sync_run_id ]`, `[ external_event_id, operation, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at ]`, `[ external_event_id, status, sync_id, sync_run_id ]`, `[ external_event_id, status, created_at, sync_run_id ]`, `[ external_event_id, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at ]`, `[ operation, status, sync_id, sync_run_id ]`, `[ operation, status, created_at, sync_run_id ]`, `[ operation, sync_id, created_at, sync_run_id ]`, `[ status, sync_id, created_at, sync_run_id ]`, `[ external_event_id, operation, status, sync_id, created_at ]`, `[ external_event_id, operation, status, sync_id, sync_run_id ]`, `[ external_event_id, operation, status, created_at, sync_run_id ]`, `[ external_event_id, operation, sync_id, created_at, sync_run_id ]`, `[ external_event_id, status, sync_id, created_at, sync_run_id ]`, `[ operation, status, sync_id, created_at, sync_run_id ]` or `[ external_event_id, operation, status, sync_id, created_at, sync_run_id ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SyncLog]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> SyncLog:
    return SyncLog(*args, **kwargs)
