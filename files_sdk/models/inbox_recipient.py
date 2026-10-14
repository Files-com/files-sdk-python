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


class InboxRecipient:
    """A inbox recipient record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        company: string - The recipient's company.
        name: string - The recipient's name.
        note: string - A note sent to the recipient with the inbox.
        recipient: string - The recipient's email address.
        sent_at: date-time - When the Inbox was shared with this recipient.
        inbox_id: int64 - Inbox to share.
        share_after_create: boolean - Set to true to share the link with the recipient upon creation.
    """

    default_attributes = {
        "company": None,  # string - The recipient's company.
        "name": None,  # string - The recipient's name.
        "note": None,  # string - A note sent to the recipient with the inbox.
        "recipient": None,  # string - The recipient's email address.
        "sent_at": None,  # date-time - When the Inbox was shared with this recipient.
        "inbox_id": None,  # int64 - Inbox to share.
        "share_after_create": None,  # boolean - Set to true to share the link with the recipient upon creation.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    company: str | None
    name: str | None
    note: str | None
    recipient: str | None
    sent_at: str | None
    inbox_id: int | None
    share_after_create: bool | None

    # Not an attribute of the API's record, but the operations below read it,
    # so set it before calling them.
    id: Any

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
        ) in InboxRecipient.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in InboxRecipient.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns. One that already has an id cannot be updated, and raises
        NotImplementedError."""
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The InboxRecipient object doesn't support updates."
            )
        else:
            new_obj = InboxRecipientResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class InboxRecipientResource:
    """InboxRecipient operations that use one client's configuration.

    Get one from a client, such as ``client.inbox_recipient``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[InboxRecipient]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `has_registrations`.
        inbox_id (required) - int64 - List recipients for the inbox with this ID.
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
        if "inbox_id" in params and (
            not isinstance(params["inbox_id"], int)
            or isinstance(params["inbox_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inbox_id must be an int"
            )
        if "inbox_id" not in params:
            raise MissingParameterError("Parameter missing: inbox_id")
        operation = Operation.start(self._scope, options)
        return ListObj(
            InboxRecipient, "GET", "/inbox_recipients", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[InboxRecipient]:
        """The same as list()."""
        return self.list(params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> InboxRecipient:
        """Parameters:
        inbox_id (required) - int64 - Inbox to share.
        recipient (required) - string - Email address to share this inbox with.
        name - string - Name of recipient.
        company - string - Company of recipient.
        note - string - Note to include in email.
        share_after_create - boolean - Set to true to share the link with the recipient upon creation.
        """
        params = copy_params(params)
        if "inbox_id" in params and (
            not isinstance(params["inbox_id"], int)
            or isinstance(params["inbox_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inbox_id must be an int"
            )
        if "recipient" in params and not isinstance(params["recipient"], str):
            raise InvalidParameterError(
                "Bad parameter: recipient must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "company" in params and not isinstance(params["company"], str):
            raise InvalidParameterError(
                "Bad parameter: company must be an str"
            )
        if "note" in params and not isinstance(params["note"], str):
            raise InvalidParameterError("Bad parameter: note must be an str")
        if "share_after_create" in params and not isinstance(
            params["share_after_create"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: share_after_create must be an bool"
            )
        if "inbox_id" not in params:
            raise MissingParameterError("Parameter missing: inbox_id")
        if "recipient" not in params:
            raise MissingParameterError("Parameter missing: recipient")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/inbox_recipients", params)
        return operation.decode_model(response, InboxRecipient)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> InboxRecipient:
        """A new InboxRecipient with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = InboxRecipient(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = InboxRecipientResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[InboxRecipient]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `has_registrations`.
    inbox_id (required) - int64 - List recipients for the inbox with this ID.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[InboxRecipient]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> InboxRecipient:
    """Parameters:
    inbox_id (required) - int64 - Inbox to share.
    recipient (required) - string - Email address to share this inbox with.
    name - string - Name of recipient.
    company - string - Company of recipient.
    note - string - Note to include in email.
    share_after_create - boolean - Set to true to share the link with the recipient upon creation.
    """
    return _legacy_resource.create(params, options)


def new(*args, **kwargs) -> InboxRecipient:
    return InboxRecipient(*args, **kwargs)
