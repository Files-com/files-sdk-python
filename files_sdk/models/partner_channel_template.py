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


class PartnerChannelTemplate:
    """A partner channel template record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - The unique ID of the Partner Channel Template.
        workspace_id: int64 - ID of the Workspace associated with this Partner Channel Template.
        direction: string - Channel directions. `two_way` enables both directions, `to_partner` enables outgoing downloads, and `from_partner` enables incoming uploads.
        use_channel_root: boolean - Use the Channel folder directly for a one-way exchange. Defaults to false. Cannot be changed after creation. Folder name overrides must be blank when enabled, and the Template must remain one-way.
        name: string - The name of the Partner Channel Template.
        path: string - Channel path relative to the Partner root folder. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        to_partner_folder_name: string - Optional Channel-level to-Partner folder name override.
        from_partner_folder_name: string - Optional Channel-level from-Partner folder name override.
        from_partner_route_path_pattern: string - Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
        to_partner_route_path_pattern: string - Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
        to_partner_managed_folder_paths: array(string) - Managed folder paths inside the to-Partner folder.
        from_partner_managed_folder_paths: array(string) - Managed folder paths inside the from-Partner folder.
        effective_to_partner_folder_name: string - Resolved to-Partner subfolder name. Null when the direction is disabled or uses the Channel folder directly.
        effective_from_partner_folder_name: string - Resolved from-Partner subfolder name. Null when the direction is disabled or uses the Channel folder directly.
    """

    default_attributes = {
        "id": None,  # int64 - The unique ID of the Partner Channel Template.
        "workspace_id": None,  # int64 - ID of the Workspace associated with this Partner Channel Template.
        "direction": None,  # string - Channel directions. `two_way` enables both directions, `to_partner` enables outgoing downloads, and `from_partner` enables incoming uploads.
        "use_channel_root": None,  # boolean - Use the Channel folder directly for a one-way exchange. Defaults to false. Cannot be changed after creation. Folder name overrides must be blank when enabled, and the Template must remain one-way.
        "name": None,  # string - The name of the Partner Channel Template.
        "path": None,  # string - Channel path relative to the Partner root folder. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "to_partner_folder_name": None,  # string - Optional Channel-level to-Partner folder name override.
        "from_partner_folder_name": None,  # string - Optional Channel-level from-Partner folder name override.
        "from_partner_route_path_pattern": None,  # string - Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
        "to_partner_route_path_pattern": None,  # string - Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
        "to_partner_managed_folder_paths": None,  # array(string) - Managed folder paths inside the to-Partner folder.
        "from_partner_managed_folder_paths": None,  # array(string) - Managed folder paths inside the from-Partner folder.
        "effective_to_partner_folder_name": None,  # string - Resolved to-Partner subfolder name. Null when the direction is disabled or uses the Channel folder directly.
        "effective_from_partner_folder_name": None,  # string - Resolved from-Partner subfolder name. Null when the direction is disabled or uses the Channel folder directly.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    direction: str | None
    use_channel_root: bool | None
    name: str | None
    path: str | None
    to_partner_folder_name: str | None
    from_partner_folder_name: str | None
    from_partner_route_path_pattern: str | None
    to_partner_route_path_pattern: str | None
    to_partner_managed_folder_paths: builtins.list[str] | None
    from_partner_managed_folder_paths: builtins.list[str] | None
    effective_to_partner_folder_name: str | None
    effective_from_partner_folder_name: str | None

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
        ) in PartnerChannelTemplate.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PartnerChannelTemplate.default_attributes
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
          direction - string - Channel directions. `two_way` enables both directions, `to_partner` enables outgoing downloads, and `from_partner` enables incoming uploads.
          use_channel_root - boolean - Use the Channel folder directly for a one-way exchange. Defaults to false. Cannot be changed after creation. Folder name overrides must be blank when enabled, and the Template must remain one-way.
          from_partner_folder_name - string - Optional Channel-level from-Partner folder name override.
          from_partner_managed_folder_paths - array(string) - Managed folder paths inside the from-Partner folder.
          from_partner_route_path_pattern - string - Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
          to_partner_folder_name - string - Optional Channel-level to-Partner folder name override.
          to_partner_managed_folder_paths - array(string) - Managed folder paths inside the to-Partner folder.
          to_partner_route_path_pattern - string - Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
          name - string - The name of the Partner Channel Template.
          path - string - Channel path relative to the Partner root folder.
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
        if "direction" in params and not isinstance(params["direction"], str):
            raise InvalidParameterError(
                "Bad parameter: direction must be an str"
            )
        if "use_channel_root" in params and isinstance(
            params["use_channel_root"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: use_channel_root must be an bool"
            )
        if "from_partner_folder_name" in params and not isinstance(
            params["from_partner_folder_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_folder_name must be an str"
            )
        if "from_partner_managed_folder_paths" in params and not isinstance(
            params["from_partner_managed_folder_paths"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_managed_folder_paths must be an list"
            )
        if "from_partner_route_path_pattern" in params and not isinstance(
            params["from_partner_route_path_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_route_path_pattern must be an str"
            )
        if "to_partner_folder_name" in params and not isinstance(
            params["to_partner_folder_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_folder_name must be an str"
            )
        if "to_partner_managed_folder_paths" in params and not isinstance(
            params["to_partner_managed_folder_paths"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_managed_folder_paths must be an list"
            )
        if "to_partner_route_path_pattern" in params and not isinstance(
            params["to_partner_route_path_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_route_path_pattern must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH",
            "/partner_channel_templates/" + path_value(params["id"]),
            params,
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
            "DELETE",
            "/partner_channel_templates/" + path_value(params["id"]),
            params,
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
            new_obj = PartnerChannelTemplateResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class PartnerChannelTemplateResource:
    """PartnerChannelTemplate operations that use one client's configuration.

    Get one from a client, such as ``client.partner_channel_template``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[PartnerChannelTemplate]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
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
            PartnerChannelTemplate,
            "GET",
            "/partner_channel_templates",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[PartnerChannelTemplate]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PartnerChannelTemplate:
        """Parameters:
        id (required) - int64 - Partner Channel Template ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> PartnerChannelTemplate:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/partner_channel_templates/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, PartnerChannelTemplate)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PartnerChannelTemplate:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PartnerChannelTemplate:
        """Parameters:
        direction - string - Channel directions. `two_way` enables both directions, `to_partner` enables outgoing downloads, and `from_partner` enables incoming uploads.
        use_channel_root - boolean - Use the Channel folder directly for a one-way exchange. Defaults to false. Cannot be changed after creation. Folder name overrides must be blank when enabled, and the Template must remain one-way.
        from_partner_folder_name - string - Optional Channel-level from-Partner folder name override.
        from_partner_managed_folder_paths - array(string) - Managed folder paths inside the from-Partner folder.
        from_partner_route_path_pattern - string - Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
        to_partner_folder_name - string - Optional Channel-level to-Partner folder name override.
        to_partner_managed_folder_paths - array(string) - Managed folder paths inside the to-Partner folder.
        to_partner_route_path_pattern - string - Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
        name (required) - string - The name of the Partner Channel Template.
        path (required) - string - Channel path relative to the Partner root folder.
        workspace_id - int64 - ID of the Workspace associated with this Partner Channel Template.
        """
        params = copy_params(params)
        if "direction" in params and not isinstance(params["direction"], str):
            raise InvalidParameterError(
                "Bad parameter: direction must be an str"
            )
        if "use_channel_root" in params and not isinstance(
            params["use_channel_root"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: use_channel_root must be an bool"
            )
        if "from_partner_folder_name" in params and not isinstance(
            params["from_partner_folder_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_folder_name must be an str"
            )
        if "from_partner_managed_folder_paths" in params and not isinstance(
            params["from_partner_managed_folder_paths"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_managed_folder_paths must be an list"
            )
        if "from_partner_route_path_pattern" in params and not isinstance(
            params["from_partner_route_path_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_route_path_pattern must be an str"
            )
        if "to_partner_folder_name" in params and not isinstance(
            params["to_partner_folder_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_folder_name must be an str"
            )
        if "to_partner_managed_folder_paths" in params and not isinstance(
            params["to_partner_managed_folder_paths"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_managed_folder_paths must be an list"
            )
        if "to_partner_route_path_pattern" in params and not isinstance(
            params["to_partner_route_path_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_route_path_pattern must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/partner_channel_templates", params
        )
        return operation.decode_model(response, PartnerChannelTemplate)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PartnerChannelTemplate:
        """Parameters:
        direction - string - Channel directions. `two_way` enables both directions, `to_partner` enables outgoing downloads, and `from_partner` enables incoming uploads.
        use_channel_root - boolean - Use the Channel folder directly for a one-way exchange. Defaults to false. Cannot be changed after creation. Folder name overrides must be blank when enabled, and the Template must remain one-way.
        from_partner_folder_name - string - Optional Channel-level from-Partner folder name override.
        from_partner_managed_folder_paths - array(string) - Managed folder paths inside the from-Partner folder.
        from_partner_route_path_pattern - string - Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
        to_partner_folder_name - string - Optional Channel-level to-Partner folder name override.
        to_partner_managed_folder_paths - array(string) - Managed folder paths inside the to-Partner folder.
        to_partner_route_path_pattern - string - Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
        name - string - The name of the Partner Channel Template.
        path - string - Channel path relative to the Partner root folder.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> PartnerChannelTemplate:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "direction" in params and not isinstance(params["direction"], str):
            raise InvalidParameterError(
                "Bad parameter: direction must be an str"
            )
        if "use_channel_root" in params and not isinstance(
            params["use_channel_root"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: use_channel_root must be an bool"
            )
        if "from_partner_folder_name" in params and not isinstance(
            params["from_partner_folder_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_folder_name must be an str"
            )
        if "from_partner_managed_folder_paths" in params and not isinstance(
            params["from_partner_managed_folder_paths"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_managed_folder_paths must be an list"
            )
        if "from_partner_route_path_pattern" in params and not isinstance(
            params["from_partner_route_path_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_route_path_pattern must be an str"
            )
        if "to_partner_folder_name" in params and not isinstance(
            params["to_partner_folder_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_folder_name must be an str"
            )
        if "to_partner_managed_folder_paths" in params and not isinstance(
            params["to_partner_managed_folder_paths"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_managed_folder_paths must be an list"
            )
        if "to_partner_route_path_pattern" in params and not isinstance(
            params["to_partner_route_path_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_route_path_pattern must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH",
            "/partner_channel_templates/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, PartnerChannelTemplate)

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
            "/partner_channel_templates/" + path_value(params["id"]),
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
    ) -> PartnerChannelTemplate:
        """A new PartnerChannelTemplate with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = PartnerChannelTemplate(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = PartnerChannelTemplateResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[PartnerChannelTemplate]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[PartnerChannelTemplate]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PartnerChannelTemplate:
    """Parameters:
    id (required) - int64 - Partner Channel Template ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PartnerChannelTemplate:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PartnerChannelTemplate:
    """Parameters:
    direction - string - Channel directions. `two_way` enables both directions, `to_partner` enables outgoing downloads, and `from_partner` enables incoming uploads.
    use_channel_root - boolean - Use the Channel folder directly for a one-way exchange. Defaults to false. Cannot be changed after creation. Folder name overrides must be blank when enabled, and the Template must remain one-way.
    from_partner_folder_name - string - Optional Channel-level from-Partner folder name override.
    from_partner_managed_folder_paths - array(string) - Managed folder paths inside the from-Partner folder.
    from_partner_route_path_pattern - string - Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
    to_partner_folder_name - string - Optional Channel-level to-Partner folder name override.
    to_partner_managed_folder_paths - array(string) - Managed folder paths inside the to-Partner folder.
    to_partner_route_path_pattern - string - Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
    name (required) - string - The name of the Partner Channel Template.
    path (required) - string - Channel path relative to the Partner root folder.
    workspace_id - int64 - ID of the Workspace associated with this Partner Channel Template.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PartnerChannelTemplate:
    """Parameters:
    direction - string - Channel directions. `two_way` enables both directions, `to_partner` enables outgoing downloads, and `from_partner` enables incoming uploads.
    use_channel_root - boolean - Use the Channel folder directly for a one-way exchange. Defaults to false. Cannot be changed after creation. Folder name overrides must be blank when enabled, and the Template must remain one-way.
    from_partner_folder_name - string - Optional Channel-level from-Partner folder name override.
    from_partner_managed_folder_paths - array(string) - Managed folder paths inside the from-Partner folder.
    from_partner_route_path_pattern - string - Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
    to_partner_folder_name - string - Optional Channel-level to-Partner folder name override.
    to_partner_managed_folder_paths - array(string) - Managed folder paths inside the to-Partner folder.
    to_partner_route_path_pattern - string - Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
    name - string - The name of the Partner Channel Template.
    path - string - Channel path relative to the Partner root folder.
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


def new(*args, **kwargs) -> PartnerChannelTemplate:
    return PartnerChannelTemplate(*args, **kwargs)
