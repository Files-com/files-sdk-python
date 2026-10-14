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


class InboundS3Log:
    """A inbound s3 log record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        path: string - Request Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        client_ip: string - Client IP
        operation: string - S3 Operation Type
        status: string - HTTP Status Code
        aws_access_key: string - AWS Access Key ID
        error_message: string - Error message, if applicable
        error_type: string - Error type, if applicable
        duration_ms: int64 - Duration (in milliseconds)
        request_id: string - Request ID
        user_agent: string - User Agent
        created_at: date-time - Start Time of Request
    """

    default_attributes = {
        "path": None,  # string - Request Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "client_ip": None,  # string - Client IP
        "operation": None,  # string - S3 Operation Type
        "status": None,  # string - HTTP Status Code
        "aws_access_key": None,  # string - AWS Access Key ID
        "error_message": None,  # string - Error message, if applicable
        "error_type": None,  # string - Error type, if applicable
        "duration_ms": None,  # int64 - Duration (in milliseconds)
        "request_id": None,  # string - Request ID
        "user_agent": None,  # string - User Agent
        "created_at": None,  # date-time - Start Time of Request
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    path: str | None
    client_ip: str | None
    operation: str | None
    status: str | None
    aws_access_key: str | None
    error_message: str | None
    error_type: str | None
    duration_ms: int | None
    request_id: str | None
    user_agent: str | None
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
        for (
            attribute,
            default_value,
        ) in InboundS3Log.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in InboundS3Log.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class InboundS3LogResource:
    """InboundS3Log operations that use one client's configuration.

    Get one from a client, such as ``client.inbound_s3_log``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[InboundS3Log]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 1000, 1,000 or less is recommended).
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `operation`, `status`, `path`, `client_ip` or `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `operation`, `status`, `path` or `client_ip`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
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
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
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
            InboundS3Log, "GET", "/inbound_s3_logs", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[InboundS3Log]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> InboundS3Log:
        """A new InboundS3Log with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = InboundS3Log(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = InboundS3LogResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[InboundS3Log]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 1000, 1,000 or less is recommended).
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `operation`, `status`, `path`, `client_ip` or `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `operation`, `status`, `path` or `client_ip`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ operation ]`, `[ status ]`, `[ path ]`, `[ client_ip ]`, `[ created_at ]`, `[ operation, status ]`, `[ operation, path ]`, `[ operation, client_ip ]`, `[ operation, created_at ]`, `[ status, path ]`, `[ status, client_ip ]`, `[ status, created_at ]`, `[ path, client_ip ]`, `[ path, created_at ]`, `[ client_ip, created_at ]`, `[ operation, status, path ]`, `[ operation, status, client_ip ]`, `[ operation, status, created_at ]`, `[ operation, path, client_ip ]`, `[ operation, path, created_at ]`, `[ operation, client_ip, created_at ]`, `[ status, path, client_ip ]`, `[ status, path, created_at ]`, `[ status, client_ip, created_at ]`, `[ path, client_ip, created_at ]`, `[ operation, status, path, client_ip ]`, `[ operation, status, path, created_at ]`, `[ operation, status, client_ip, created_at ]`, `[ operation, path, client_ip, created_at ]` or `[ status, path, client_ip, created_at ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[InboundS3Log]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> InboundS3Log:
    return InboundS3Log(*args, **kwargs)
