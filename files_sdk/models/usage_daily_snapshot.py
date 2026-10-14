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


class UsageDailySnapshot:
    """A usage daily snapshot record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - ID of the usage record
        date: date - The date of this usage record
        api_usage_available: boolean - True if the API usage fields `read_api_usage` and `write_api_usage` can be relied upon. If this is false, we suggest hiding that value from any UI.
        read_api_usage: int64 - Read API Calls used on this day. Note: only updated for days before the current day.
        write_api_usage: int64 - Write API Calls used on this day. Note: only updated for days before the current day.
        transformation_credits_usage: int64 - Transformation and AI credits used on this day. Note: only updated for days before the current day.
        user_count: int64 - Number of billable users as of this day.
        current_storage: int64 - GB of Files Native Storage used on this day.
        deleted_files_storage: int64 - GB of Files Native Storage used on this day for files that have been deleted and are stored as backups.
        deleted_files_counted_in_minimum: int64 - GB of Files Native Storage used on this day for files that have been permanently deleted but were uploaded less than 30 days ago, and are still billable.
        root_storage: int64 - GB of Files Native Storage used for the root folder. Included here because this value will not be part of `usage_by_top_level_dir`
        usage_by_top_level_dir: array(object) - Usage broken down by each top-level folder
    """

    default_attributes = {
        "id": None,  # int64 - ID of the usage record
        "date": None,  # date - The date of this usage record
        "api_usage_available": None,  # boolean - True if the API usage fields `read_api_usage` and `write_api_usage` can be relied upon.  If this is false, we suggest hiding that value from any UI.
        "read_api_usage": None,  # int64 - Read API Calls used on this day. Note: only updated for days before the current day.
        "write_api_usage": None,  # int64 - Write API Calls used on this day. Note: only updated for days before the current day.
        "transformation_credits_usage": None,  # int64 - Transformation and AI credits used on this day. Note: only updated for days before the current day.
        "user_count": None,  # int64 - Number of billable users as of this day.
        "current_storage": None,  # int64 - GB of Files Native Storage used on this day.
        "deleted_files_storage": None,  # int64 - GB of Files Native Storage used on this day for files that have been deleted and are stored as backups.
        "deleted_files_counted_in_minimum": None,  # int64 - GB of Files Native Storage used on this day for files that have been permanently deleted but were uploaded less than 30 days ago, and are still billable.
        "root_storage": None,  # int64 - GB of Files Native Storage used for the root folder.  Included here because this value will not be part of `usage_by_top_level_dir`
        "usage_by_top_level_dir": None,  # array(object) - Usage broken down by each top-level folder
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    date: str | None
    api_usage_available: bool | None
    read_api_usage: int | None
    write_api_usage: int | None
    transformation_credits_usage: int | None
    user_count: int | None
    current_storage: int | None
    deleted_files_storage: int | None
    deleted_files_counted_in_minimum: int | None
    root_storage: int | None
    usage_by_top_level_dir: builtins.list[dict[str, Any]] | None

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
        for (
            attribute,
            default_value,
        ) in UsageDailySnapshot.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in UsageDailySnapshot.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class UsageDailySnapshotResource:
    """UsageDailySnapshot operations that use one client's configuration.

    Get one from a client, such as ``client.usage_daily_snapshot``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UsageDailySnapshot]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `date`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `date`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `date`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `date`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `date`.
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
        return ListObj(
            UsageDailySnapshot,
            "GET",
            "/usage_daily_snapshots",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UsageDailySnapshot]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UsageDailySnapshot:
        """A new UsageDailySnapshot with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = UsageDailySnapshot(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = UsageDailySnapshotResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UsageDailySnapshot]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `date`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `date`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `date`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `date`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `date`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UsageDailySnapshot]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> UsageDailySnapshot:
    return UsageDailySnapshot(*args, **kwargs)
