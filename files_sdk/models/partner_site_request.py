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


class PartnerSiteRequest:
    """A partner site request record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Partner Site Request ID
        host_partner_id: int64 - Host Partner ID
        guest_site_url: string - Guest Site URL
        status: string - Request status (pending, approved, rejected)
        host_site_name: string - Host Site Name
        pairing_key: string - Pairing key used to approve this request on the Guest Site
        created_at: date-time - Request creation date/time
        updated_at: date-time - Request last updated date/time
    """

    default_attributes = {
        "id": None,  # int64 - Partner Site Request ID
        "host_partner_id": None,  # int64 - Host Partner ID
        "guest_site_url": None,  # string - Guest Site URL
        "status": None,  # string - Request status (pending, approved, rejected)
        "host_site_name": None,  # string - Host Site Name
        "pairing_key": None,  # string - Pairing key used to approve this request on the Guest Site
        "created_at": None,  # date-time - Request creation date/time
        "updated_at": None,  # date-time - Request last updated date/time
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    host_partner_id: int | None
    guest_site_url: str | None
    status: str | None
    host_site_name: str | None
    pairing_key: str | None
    created_at: str | None
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
        ) in PartnerSiteRequest.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PartnerSiteRequest.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

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
            "/partner_site_requests/" + path_value(params["id"]),
            params,
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns. One that already has an id cannot be updated, and raises
        NotImplementedError."""
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The PartnerSiteRequest object doesn't support updates."
            )
        else:
            new_obj = PartnerSiteRequestResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class PartnerSiteRequestResource:
    """PartnerSiteRequest operations that use one client's configuration.

    Get one from a client, such as ``client.partner_site_request``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[PartnerSiteRequest]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `host_partner_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `host_partner_id`.
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
        operation = Operation.start(self._scope, options)
        return ListObj(
            PartnerSiteRequest,
            "GET",
            "/partner_site_requests",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[PartnerSiteRequest]:
        """The same as list()."""
        return self.list(params, options)

    def find_by_pairing_key(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        pairing_key (required) - string - Pairing key for the partner site request
        """
        params = copy_params(params)
        if "pairing_key" in params and not isinstance(
            params["pairing_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: pairing_key must be an str"
            )
        if "pairing_key" not in params:
            raise MissingParameterError("Parameter missing: pairing_key")
        operation = Operation.start(self._scope, options)
        operation.request(
            "GET", "/partner_site_requests/find_by_pairing_key", params
        )

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PartnerSiteRequest:
        """Parameters:
        host_partner_id (required) - int64 - Host Partner ID to link with
        guest_site_url (required) - string - Guest Site URL to link to
        """
        params = copy_params(params)
        if "host_partner_id" in params and (
            not isinstance(params["host_partner_id"], int)
            or isinstance(params["host_partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: host_partner_id must be an int"
            )
        if "guest_site_url" in params and not isinstance(
            params["guest_site_url"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: guest_site_url must be an str"
            )
        if "host_partner_id" not in params:
            raise MissingParameterError("Parameter missing: host_partner_id")
        if "guest_site_url" not in params:
            raise MissingParameterError("Parameter missing: guest_site_url")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/partner_site_requests", params)
        return operation.decode_model(response, PartnerSiteRequest)

    def reject(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        pairing_key (required) - string - Pairing key for the partner site request
        """
        params = copy_params(params)
        if "pairing_key" in params and not isinstance(
            params["pairing_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: pairing_key must be an str"
            )
        if "pairing_key" not in params:
            raise MissingParameterError("Parameter missing: pairing_key")
        operation = Operation.start(self._scope, options)
        operation.request("POST", "/partner_site_requests/reject", params)

    def approve(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        pairing_key (required) - string - Pairing key for the partner site request
        partner_id - int64 - ID of an existing Partner on this site, with the host role, that represents the requesting organization. The connection binds to that Partner and makes it host_and_guest. When omitted, a guest Partner named after the host site is created.
        """
        params = copy_params(params)
        if "pairing_key" in params and not isinstance(
            params["pairing_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: pairing_key must be an str"
            )
        if "partner_id" in params and (
            not isinstance(params["partner_id"], int)
            or isinstance(params["partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_id must be an int"
            )
        if "pairing_key" not in params:
            raise MissingParameterError("Parameter missing: pairing_key")
        operation = Operation.start(self._scope, options)
        operation.request("POST", "/partner_site_requests/approve", params)

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
            "/partner_site_requests/" + path_value(params["id"]),
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
    ) -> PartnerSiteRequest:
        """A new PartnerSiteRequest with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = PartnerSiteRequest(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = PartnerSiteRequestResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[PartnerSiteRequest]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `host_partner_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `host_partner_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[PartnerSiteRequest]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find_by_pairing_key(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    pairing_key (required) - string - Pairing key for the partner site request
    """
    _legacy_resource.find_by_pairing_key(params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PartnerSiteRequest:
    """Parameters:
    host_partner_id (required) - int64 - Host Partner ID to link with
    guest_site_url (required) - string - Guest Site URL to link to
    """
    return _legacy_resource.create(params, options)


def reject(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    pairing_key (required) - string - Pairing key for the partner site request
    """
    _legacy_resource.reject(params, options)


def approve(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    pairing_key (required) - string - Pairing key for the partner site request
    partner_id - int64 - ID of an existing Partner on this site, with the host role, that represents the requesting organization. The connection binds to that Partner and makes it host_and_guest. When omitted, a guest Partner named after the host site is created.
    """
    _legacy_resource.approve(params, options)


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


def new(*args, **kwargs) -> PartnerSiteRequest:
    return PartnerSiteRequest(*args, **kwargs)
