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


class CustomDomain:
    """A custom domain record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Custom Domain ID.
        workspace_id: int64 - Workspace ID (0 for the default workspace).
        available_to_all_workspaces: boolean - Allow all workspaces to use this default-workspace Custom Domain.
        outbound_ip_addresses: array(string) - Eligible public IP addresses for Remote Server outbound connections. Empty when this Custom Domain is not eligible for outbound selection.
        domain: string - Customer-owned domain name.
        destination: string - Where this custom domain routes. Can be `site_alias`, `public_hosting`, `s3_endpoint`, or `unassigned` (not routing traffic). Set to `unassigned` automatically when a bound `public_hosting` folder behavior is deleted, and can be set manually via the API for any reason.
        dns_status: string - Current DNS verification status.
        ssl_certificate_id: int64 - Current SSL certificate ID.
        brick_managed: boolean - Is this domain's SSL certificate automatically managed and renewed by Files.com?
        folder_behavior_id: int64 - Public Hosting behavior ID when this domain routes to a specific Public Hosting behavior. Preserved as historical context when `destination` becomes `unassigned`.
        ip_addresses: array(string) - Dedicated public IP addresses allocated to this Custom Domain.
        created_at: date-time - When this Custom Domain was created.
        updated_at: date-time - When this Custom Domain was last updated.
    """

    default_attributes = {
        "id": None,  # int64 - Custom Domain ID.
        "workspace_id": None,  # int64 - Workspace ID (0 for the default workspace).
        "available_to_all_workspaces": None,  # boolean - Allow all workspaces to use this default-workspace Custom Domain.
        "outbound_ip_addresses": None,  # array(string) - Eligible public IP addresses for Remote Server outbound connections. Empty when this Custom Domain is not eligible for outbound selection.
        "domain": None,  # string - Customer-owned domain name.
        "destination": None,  # string - Where this custom domain routes. Can be `site_alias`, `public_hosting`, `s3_endpoint`, or `unassigned` (not routing traffic). Set to `unassigned` automatically when a bound `public_hosting` folder behavior is deleted, and can be set manually via the API for any reason.
        "dns_status": None,  # string - Current DNS verification status.
        "ssl_certificate_id": None,  # int64 - Current SSL certificate ID.
        "brick_managed": None,  # boolean - Is this domain's SSL certificate automatically managed and renewed by Files.com?
        "folder_behavior_id": None,  # int64 - Public Hosting behavior ID when this domain routes to a specific Public Hosting behavior.  Preserved as historical context when `destination` becomes `unassigned`.
        "ip_addresses": None,  # array(string) - Dedicated public IP addresses allocated to this Custom Domain.
        "created_at": None,  # date-time - When this Custom Domain was created.
        "updated_at": None,  # date-time - When this Custom Domain was last updated.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    available_to_all_workspaces: bool | None
    outbound_ip_addresses: builtins.list[str] | None
    domain: str | None
    destination: str | None
    dns_status: str | None
    ssl_certificate_id: int | None
    brick_managed: bool | None
    folder_behavior_id: int | None
    ip_addresses: builtins.list[str] | None
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
        ) in CustomDomain.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in CustomDomain.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          available_to_all_workspaces - boolean - Allow all workspaces to use this default-workspace Custom Domain.
          workspace_id - int64 - Workspace ID (0 for the default workspace).
          destination - string - Where this custom domain routes. Can be `site_alias`, `public_hosting`, `s3_endpoint`, or `unassigned` (not routing traffic). Set to `unassigned` automatically when a bound `public_hosting` folder behavior is deleted, and can be set manually via the API for any reason.
          folder_behavior_id - int64 - Public Hosting behavior ID when this domain routes to a specific Public Hosting behavior.  Preserved as historical context when `destination` becomes `unassigned`.
          ssl_certificate_id - int64 - Current SSL certificate ID.
          domain - string - Customer-owned domain name.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "available_to_all_workspaces" in params and isinstance(
            params["available_to_all_workspaces"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: available_to_all_workspaces must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "folder_behavior_id" in params and (
            not isinstance(params["folder_behavior_id"], int)
            or isinstance(params["folder_behavior_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: folder_behavior_id must be an int"
            )
        if "ssl_certificate_id" in params and (
            not isinstance(params["ssl_certificate_id"], int)
            or isinstance(params["ssl_certificate_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ssl_certificate_id must be an int"
            )
        if "domain" in params and not isinstance(params["domain"], str):
            raise InvalidParameterError("Bad parameter: domain must be an str")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/custom_domains/" + path_value(params["id"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

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
            "DELETE", "/custom_domains/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = CustomDomainResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class CustomDomainResource:
    """CustomDomain operations that use one client's configuration.

    Get one from a client, such as ``client.custom_domain``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[CustomDomain]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `id` or `available_to_all_workspaces`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
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
            CustomDomain, "GET", "/custom_domains", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[CustomDomain]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> CustomDomain:
        """Parameters:
        id (required) - int64 - Custom Domain ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> CustomDomain:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/custom_domains/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, CustomDomain)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> CustomDomain:
        """The same as find()."""
        return self.find(id, params, options)

    def create_allocate_ip(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> CustomDomain:
        """Parameters:
        id (required) - int64 - Custom Domain ID.
        count (required) - int64 - Number of dedicated IP addresses to allocate.
        """
        return self.__create_allocate_ip({"id": id}, params, options)

    def __create_allocate_ip(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> CustomDomain:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "count" in params and (
            not isinstance(params["count"], int)
            or isinstance(params["count"], bool)
        ):
            raise InvalidParameterError("Bad parameter: count must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "count" not in params:
            raise MissingParameterError("Parameter missing: count")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/custom_domains/" + path_value(params["id"]) + "/allocate_ips",
            params,
        )
        return operation.decode_model(response, CustomDomain)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> CustomDomain:
        """Parameters:
        available_to_all_workspaces - boolean - Allow all workspaces to use this default-workspace Custom Domain.
        workspace_id - int64 - Workspace ID (0 for the default workspace).
        destination - string - Where this custom domain routes. Can be `site_alias`, `public_hosting`, `s3_endpoint`, or `unassigned` (not routing traffic). Set to `unassigned` automatically when a bound `public_hosting` folder behavior is deleted, and can be set manually via the API for any reason.
        folder_behavior_id - int64 - Public Hosting behavior ID when this domain routes to a specific Public Hosting behavior.  Preserved as historical context when `destination` becomes `unassigned`.
        ssl_certificate_id - int64 - Current SSL certificate ID.
        domain (required) - string - Customer-owned domain name.
        """
        params = copy_params(params)
        if "available_to_all_workspaces" in params and not isinstance(
            params["available_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: available_to_all_workspaces must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "folder_behavior_id" in params and (
            not isinstance(params["folder_behavior_id"], int)
            or isinstance(params["folder_behavior_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: folder_behavior_id must be an int"
            )
        if "ssl_certificate_id" in params and (
            not isinstance(params["ssl_certificate_id"], int)
            or isinstance(params["ssl_certificate_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ssl_certificate_id must be an int"
            )
        if "domain" in params and not isinstance(params["domain"], str):
            raise InvalidParameterError("Bad parameter: domain must be an str")
        if "domain" not in params:
            raise MissingParameterError("Parameter missing: domain")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/custom_domains", params)
        return operation.decode_model(response, CustomDomain)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> CustomDomain:
        """Parameters:
        available_to_all_workspaces - boolean - Allow all workspaces to use this default-workspace Custom Domain.
        workspace_id - int64 - Workspace ID (0 for the default workspace).
        destination - string - Where this custom domain routes. Can be `site_alias`, `public_hosting`, `s3_endpoint`, or `unassigned` (not routing traffic). Set to `unassigned` automatically when a bound `public_hosting` folder behavior is deleted, and can be set manually via the API for any reason.
        folder_behavior_id - int64 - Public Hosting behavior ID when this domain routes to a specific Public Hosting behavior.  Preserved as historical context when `destination` becomes `unassigned`.
        ssl_certificate_id - int64 - Current SSL certificate ID.
        domain - string - Customer-owned domain name.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> CustomDomain:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "available_to_all_workspaces" in params and not isinstance(
            params["available_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: available_to_all_workspaces must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "folder_behavior_id" in params and (
            not isinstance(params["folder_behavior_id"], int)
            or isinstance(params["folder_behavior_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: folder_behavior_id must be an int"
            )
        if "ssl_certificate_id" in params and (
            not isinstance(params["ssl_certificate_id"], int)
            or isinstance(params["ssl_certificate_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ssl_certificate_id must be an int"
            )
        if "domain" in params and not isinstance(params["domain"], str):
            raise InvalidParameterError("Bad parameter: domain must be an str")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/custom_domains/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, CustomDomain)

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
            "DELETE", "/custom_domains/" + path_value(params["id"]), params
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
    ) -> CustomDomain:
        """A new CustomDomain with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = CustomDomain(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = CustomDomainResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[CustomDomain]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `id` or `available_to_all_workspaces`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[CustomDomain]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> CustomDomain:
    """Parameters:
    id (required) - int64 - Custom Domain ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> CustomDomain:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create_allocate_ip(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> CustomDomain:
    """Parameters:
    id (required) - int64 - Custom Domain ID.
    count (required) - int64 - Number of dedicated IP addresses to allocate.
    """
    return _legacy_resource.create_allocate_ip(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> CustomDomain:
    """Parameters:
    available_to_all_workspaces - boolean - Allow all workspaces to use this default-workspace Custom Domain.
    workspace_id - int64 - Workspace ID (0 for the default workspace).
    destination - string - Where this custom domain routes. Can be `site_alias`, `public_hosting`, `s3_endpoint`, or `unassigned` (not routing traffic). Set to `unassigned` automatically when a bound `public_hosting` folder behavior is deleted, and can be set manually via the API for any reason.
    folder_behavior_id - int64 - Public Hosting behavior ID when this domain routes to a specific Public Hosting behavior.  Preserved as historical context when `destination` becomes `unassigned`.
    ssl_certificate_id - int64 - Current SSL certificate ID.
    domain (required) - string - Customer-owned domain name.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> CustomDomain:
    """Parameters:
    available_to_all_workspaces - boolean - Allow all workspaces to use this default-workspace Custom Domain.
    workspace_id - int64 - Workspace ID (0 for the default workspace).
    destination - string - Where this custom domain routes. Can be `site_alias`, `public_hosting`, `s3_endpoint`, or `unassigned` (not routing traffic). Set to `unassigned` automatically when a bound `public_hosting` folder behavior is deleted, and can be set manually via the API for any reason.
    folder_behavior_id - int64 - Public Hosting behavior ID when this domain routes to a specific Public Hosting behavior.  Preserved as historical context when `destination` becomes `unassigned`.
    ssl_certificate_id - int64 - Current SSL certificate ID.
    domain - string - Customer-owned domain name.
    """
    return _legacy_resource.update(id, params, options)


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


def new(*args, **kwargs) -> CustomDomain:
    return CustomDomain(*args, **kwargs)
