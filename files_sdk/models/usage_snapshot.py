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


class UsageSnapshot:
    """A usage snapshot record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Usage snapshot ID
        start_at: date-time - Usage snapshot start date/time
        end_at: date-time - Usage snapshot end date/time
        high_water_user_count: int64 - Highest user count number in time period
        transformation_credits_usage: int64 - Total Transformation and AI credits used in this usage period. Updated daily. Does not include credits consumed today.
        current_storage: int64 - Current total Storage Usage GB as of end date (not necessarily high water mark, which is used for billing)
        high_water_storage: int64 - Highest Storage Usage GB recorded in time period (used for billing)
        root_storage: int64 - Storage Usage for root folder as of end date (not necessarily high water mark, which is used for billing)
        deleted_files_counted_in_minimum: int64 - Storage Usage for files that are deleted but uploaded within last 30 days as of end date (not necessarily high water mark, which is used for billing)
        deleted_files_storage: int64 - Storage Usage for files that are deleted but retained as backups as of end date (not necessarily high water mark, which is used for billing)
        total_billable_usage: int64 - Storage + Transfer Usage - Total Billable amount
        total_billable_transfer_usage: int64 - Transfer usage for period - Total Billable amount
        bytes_sent: int64 - Transfer Usage for period - Outbound GB from Files Native Storage
        sync_bytes_received: int64 - Transfer Usage for period - Inbound GB to Remote Servers (Sync/Mount)
        sync_bytes_sent: int64 - Transfer Usage for period - Outbound GB from Remote Servers (Sync/Mount)
        usage_by_top_level_dir: array(object) - Storage Usage - map of root folders to their usage as of end date (not necessarily high water mark, which is used for billing)
    """

    default_attributes = {
        "id": None,  # int64 - Usage snapshot ID
        "start_at": None,  # date-time - Usage snapshot start date/time
        "end_at": None,  # date-time - Usage snapshot end date/time
        "high_water_user_count": None,  # int64 - Highest user count number in time period
        "transformation_credits_usage": None,  # int64 - Total Transformation and AI credits used in this usage period. Updated daily. Does not include credits consumed today.
        "current_storage": None,  # int64 - Current total Storage Usage GB as of end date (not necessarily high water mark, which is used for billing)
        "high_water_storage": None,  # int64 - Highest Storage Usage GB recorded in time period (used for billing)
        "root_storage": None,  # int64 - Storage Usage for root folder as of end date (not necessarily high water mark, which is used for billing)
        "deleted_files_counted_in_minimum": None,  # int64 - Storage Usage for files that are deleted but uploaded within last 30 days as of end date (not necessarily high water mark, which is used for billing)
        "deleted_files_storage": None,  # int64 - Storage Usage for files that are deleted but retained as backups as of end date (not necessarily high water mark, which is used for billing)
        "total_billable_usage": None,  # int64 - Storage + Transfer Usage - Total Billable amount
        "total_billable_transfer_usage": None,  # int64 - Transfer usage for period - Total Billable amount
        "bytes_sent": None,  # int64 - Transfer Usage for period - Outbound GB from Files Native Storage
        "sync_bytes_received": None,  # int64 - Transfer Usage for period - Inbound GB to Remote Servers (Sync/Mount)
        "sync_bytes_sent": None,  # int64 - Transfer Usage for period - Outbound GB from Remote Servers (Sync/Mount)
        "usage_by_top_level_dir": None,  # array(object) - Storage Usage - map of root folders to their usage as of end date (not necessarily high water mark, which is used for billing)
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    start_at: str | None
    end_at: str | None
    high_water_user_count: int | None
    transformation_credits_usage: int | None
    current_storage: int | None
    high_water_storage: int | None
    root_storage: int | None
    deleted_files_counted_in_minimum: int | None
    deleted_files_storage: int | None
    total_billable_usage: int | None
    total_billable_transfer_usage: int | None
    bytes_sent: int | None
    sync_bytes_received: int | None
    sync_bytes_sent: int | None
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
        ) in UsageSnapshot.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in UsageSnapshot.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class UsageSnapshotResource:
    """UsageSnapshot operations that use one client's configuration.

    Get one from a client, such as ``client.usage_snapshot``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UsageSnapshot]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
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
        operation = Operation.start(self._scope, options)
        return ListObj(
            UsageSnapshot, "GET", "/usage_snapshots", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UsageSnapshot]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UsageSnapshot:
        """A new UsageSnapshot with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = UsageSnapshot(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = UsageSnapshotResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UsageSnapshot]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UsageSnapshot]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> UsageSnapshot:
    return UsageSnapshot(*args, **kwargs)
