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


class UserCipherUse:
    """A user cipher use record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - UserCipherUse ID
        user_id: int64 - ID of the user who performed this access
        username: string - Username of the user who performed this access
        protocol_cipher: string - The protocol and cipher employed
        created_at: date-time - The earliest recorded use of this combination of interface and protocol and cipher (for this user)
        insecure: boolean - Is this cipher considered insecure?
        interface: string - The interface accessed
        updated_at: date-time - The most recent use of this combination of interface and protocol and cipher (for this user)
    """

    default_attributes = {
        "id": None,  # int64 - UserCipherUse ID
        "user_id": None,  # int64 - ID of the user who performed this access
        "username": None,  # string - Username of the user who performed this access
        "protocol_cipher": None,  # string - The protocol and cipher employed
        "created_at": None,  # date-time - The earliest recorded use of this combination of interface and protocol and cipher (for this user)
        "insecure": None,  # boolean - Is this cipher considered insecure?
        "interface": None,  # string - The interface accessed
        "updated_at": None,  # date-time - The most recent use of this combination of interface and protocol and cipher (for this user)
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    user_id: int | None
    username: str | None
    protocol_cipher: str | None
    created_at: str | None
    insecure: bool | None
    interface: str | None
    updated_at: str | None

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
        ) in UserCipherUse.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in UserCipherUse.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class UserCipherUseResource:
    """UserCipherUse operations that use one client's configuration.

    Get one from a client, such as ``client.user_cipher_use``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UserCipherUse]:
        """Parameters:
        user_id - int64 - User ID. If provided, will return uses for this user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `updated_at`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `insecure` and `updated_at`. Valid field combinations are `[ insecure, updated_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `updated_at`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `updated_at`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `updated_at`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `updated_at`.
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
        return ListObj(
            UserCipherUse, "GET", "/user_cipher_uses", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UserCipherUse]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UserCipherUse:
        """A new UserCipherUse with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = UserCipherUse(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = UserCipherUseResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UserCipherUse]:
    """Parameters:
    user_id - int64 - User ID. If provided, will return uses for this user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `updated_at`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `insecure` and `updated_at`. Valid field combinations are `[ insecure, updated_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `updated_at`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `updated_at`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `updated_at`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `updated_at`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UserCipherUse]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> UserCipherUse:
    return UserCipherUse(*args, **kwargs)
