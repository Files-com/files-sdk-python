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


class InboxRegistration:
    """A inbox registration record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        code: string - Registration cookie code
        name: string - Registrant name
        company: string - Registrant company name
        email: string - Registrant email address
        ip: string - Registrant IP Address
        clickwrap_body: string - Clickwrap text that was shown to the registrant
        form_field_set_id: int64 - Id of associated form field set
        form_field_data: object - Data for form field set with form field ids as keys and user data as values
        inbox_id: int64 - Id of associated inbox
        inbox_recipient_id: int64 - Id of associated inbox recipient
        inbox_title: string - Title of associated inbox
        created_at: date-time - Registration creation date/time
    """

    default_attributes = {
        "code": None,  # string - Registration cookie code
        "name": None,  # string - Registrant name
        "company": None,  # string - Registrant company name
        "email": None,  # string - Registrant email address
        "ip": None,  # string - Registrant IP Address
        "clickwrap_body": None,  # string - Clickwrap text that was shown to the registrant
        "form_field_set_id": None,  # int64 - Id of associated form field set
        "form_field_data": None,  # object - Data for form field set with form field ids as keys and user data as values
        "inbox_id": None,  # int64 - Id of associated inbox
        "inbox_recipient_id": None,  # int64 - Id of associated inbox recipient
        "inbox_title": None,  # string - Title of associated inbox
        "created_at": None,  # date-time - Registration creation date/time
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    code: str | None
    name: str | None
    company: str | None
    email: str | None
    ip: str | None
    clickwrap_body: str | None
    form_field_set_id: int | None
    form_field_data: dict[str, Any] | None
    inbox_id: int | None
    inbox_recipient_id: int | None
    inbox_title: str | None
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
        ) in InboxRegistration.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in InboxRegistration.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class InboxRegistrationResource:
    """InboxRegistration operations that use one client's configuration.

    Get one from a client, such as ``client.inbox_registration``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[InboxRegistration]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        folder_behavior_id - int64 - ID of the associated Inbox. This is required if the user is not a site admin.
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
        if "folder_behavior_id" in params and (
            not isinstance(params["folder_behavior_id"], int)
            or isinstance(params["folder_behavior_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: folder_behavior_id must be an int"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            InboxRegistration, "GET", "/inbox_registrations", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[InboxRegistration]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> InboxRegistration:
        """A new InboxRegistration with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = InboxRegistration(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = InboxRegistrationResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[InboxRegistration]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    folder_behavior_id - int64 - ID of the associated Inbox. This is required if the user is not a site admin.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[InboxRegistration]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> InboxRegistration:
    return InboxRegistration(*args, **kwargs)
