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


class BundleAction:
    """A bundle action record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        action: string - Type of action
        bundle_registration: BundleRegistration - Object that contains bundle registration information
        created_at: date-time - Action occurrence date/time
        destination: string - The destination path for this bundle action, if applicable
        path: string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        source: string - The source path for this bundle action, if applicable
        bundle_registration_id: int64 - Identifier of the associated bundle registration
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
        bundle_registration_name: string - Name of the registrant who performed the action
        bundle_registration_email: string - Email of the registrant
        bundle_registration_ip: string - IP address of the registrant
        form_field_set_id: int64 - Id of associated form field set
        form_field_data: object - Data for form field set with form field ids as keys and user data as values
    """

    default_attributes = {
        "action": None,  # string - Type of action
        "bundle_registration": None,  # BundleRegistration - Object that contains bundle registration information
        "created_at": None,  # date-time - Action occurrence date/time
        "destination": None,  # string - The destination path for this bundle action, if applicable
        "path": None,  # string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "source": None,  # string - The source path for this bundle action, if applicable
        "bundle_registration_id": None,  # int64 - Identifier of the associated bundle registration
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
        "bundle_registration_name": None,  # string - Name of the registrant who performed the action
        "bundle_registration_email": None,  # string - Email of the registrant
        "bundle_registration_ip": None,  # string - IP address of the registrant
        "form_field_set_id": None,  # int64 - Id of associated form field set
        "form_field_data": None,  # object - Data for form field set with form field ids as keys and user data as values
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    action: str | None
    bundle_registration: dict[str, Any] | None
    created_at: str | None
    destination: str | None
    path: str | None
    source: str | None
    bundle_registration_id: int | None
    workspace_id: int | None
    bundle_registration_name: str | None
    bundle_registration_email: str | None
    bundle_registration_ip: str | None
    form_field_set_id: int | None
    form_field_data: dict[str, Any] | None

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
        ) in BundleAction.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in BundleAction.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class BundleActionResource:
    """BundleAction operations that use one client's configuration.

    Get one from a client, such as ``client.bundle_action``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[BundleAction]:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `bundle_registration_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `bundle_id` or `bundle_registration_id`. Valid field combinations are `[ bundle_id, created_at ]`, `[ bundle_registration_id, created_at ]`, `[ bundle_id, bundle_registration_id ]` or `[ bundle_id, bundle_registration_id, created_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
        bundle_id - int64 - Bundle ID
        bundle_registration_id - int64 - Bundle Registration ID
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
        if "bundle_id" in params and (
            not isinstance(params["bundle_id"], int)
            or isinstance(params["bundle_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: bundle_id must be an int"
            )
        if "bundle_registration_id" in params and (
            not isinstance(params["bundle_registration_id"], int)
            or isinstance(params["bundle_registration_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: bundle_registration_id must be an int"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            BundleAction, "GET", "/bundle_actions", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[BundleAction]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> BundleAction:
        """A new BundleAction with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = BundleAction(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = BundleActionResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[BundleAction]:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `bundle_registration_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `bundle_id` or `bundle_registration_id`. Valid field combinations are `[ bundle_id, created_at ]`, `[ bundle_registration_id, created_at ]`, `[ bundle_id, bundle_registration_id ]` or `[ bundle_id, bundle_registration_id, created_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
    bundle_id - int64 - Bundle ID
    bundle_registration_id - int64 - Bundle Registration ID
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[BundleAction]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> BundleAction:
    return BundleAction(*args, **kwargs)
