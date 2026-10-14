import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.attachment import with_attachments
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


class Behavior:
    """A behavior record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Folder behavior ID
        path: string - Folder path. Note that Behavior paths cannot be updated once initially set. You will need to remove and re-create the behavior on the new path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        attachment_url: string - URL for attached file
        behavior: string - Behavior type.
        name: string - Name for this behavior.
        description: string - Description for this behavior.
        value: object - Settings for this behavior. See the section above for an example value to provide here. Formatting is different for each Behavior type. May be sent as nested JSON or a single JSON-encoded string. If using XML encoding for the API call, this data must be sent as a JSON-encoded string.
        public_hosting_url: string - Public URL for this publicly hosted folder when the `Serve Publicly` behavior has a key configured. When a Custom Domain with `public_hosting` destination is attached to this behavior, the URL uses that domain. Otherwise it uses the site's `subdomain.hosted-by-files.com` host, unless `custom_domain_only` is enabled, in which case no URL is returned.
        disable_parent_folder_behavior: boolean - If true, disables the inherited behavior for this folder and its children. Valid only for behavior types that child folders may override, and requires recursive to be true. Rejected for all other behavior types.
        recursive: boolean - Whether this behavior is recursive for this record. `always` behaviors are always `true`, `never` behaviors are always `false`, and `sometimes` behaviors may be either value.
        inherited: boolean - If true, this behavior is inherited from a higher scope rather than owned by the requested workspace.
        managed: boolean - If true, this behavior is controlled by a parent-site policy and cannot be modified locally.
        root_behavior_site_admin_only: boolean - If true, this behavior may only be modified by a site admin because it is at the site root or disables a root behavior.
        attachment_file: file - Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
        attachment_delete: boolean - If `true`, delete the file stored in `attachment`.
    """

    default_attributes = {
        "id": None,  # int64 - Folder behavior ID
        "path": None,  # string - Folder path.  Note that Behavior paths cannot be updated once initially set.  You will need to remove and re-create the behavior on the new path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "attachment_url": None,  # string - URL for attached file
        "behavior": None,  # string - Behavior type.
        "name": None,  # string - Name for this behavior.
        "description": None,  # string - Description for this behavior.
        "value": None,  # object - Settings for this behavior.  See the section above for an example value to provide here.  Formatting is different for each Behavior type.  May be sent as nested JSON or a single JSON-encoded string.  If using XML encoding for the API call, this data must be sent as a JSON-encoded string.
        "public_hosting_url": None,  # string - Public URL for this publicly hosted folder when the `Serve Publicly` behavior has a key configured. When a Custom Domain with `public_hosting` destination is attached to this behavior, the URL uses that domain. Otherwise it uses the site's `subdomain.hosted-by-files.com` host, unless `custom_domain_only` is enabled, in which case no URL is returned.
        "disable_parent_folder_behavior": None,  # boolean - If true, disables the inherited behavior for this folder and its children. Valid only for behavior types that child folders may override, and requires recursive to be true. Rejected for all other behavior types.
        "recursive": None,  # boolean - Whether this behavior is recursive for this record. `always` behaviors are always `true`, `never` behaviors are always `false`, and `sometimes` behaviors may be either value.
        "inherited": None,  # boolean - If true, this behavior is inherited from a higher scope rather than owned by the requested workspace.
        "managed": None,  # boolean - If true, this behavior is controlled by a parent-site policy and cannot be modified locally.
        "root_behavior_site_admin_only": None,  # boolean - If true, this behavior may only be modified by a site admin because it is at the site root or disables a root behavior.
        "attachment_file": None,  # file - Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
        "attachment_delete": None,  # boolean - If `true`, delete the file stored in `attachment`.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    path: str | None
    attachment_url: str | None
    behavior: str | None
    name: str | None
    description: str | None
    value: dict[str, Any] | None
    public_hosting_url: str | None
    disable_parent_folder_behavior: bool | None
    recursive: bool | None
    inherited: bool | None
    managed: bool | None
    root_behavior_site_admin_only: bool | None
    attachment_file: Any
    attachment_delete: bool | None

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
        for attribute, default_value in Behavior.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Behavior.default_attributes
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
          value - object - This field stores data specific to the type of behavior. See The Behavior Types section for the accepted value for each type of behavior.
          attachment_file - file - Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
          disable_parent_folder_behavior - boolean - If true, disables the inherited behavior for this folder and its children. Valid only for behavior types that child folders may override, and requires recursive to be true. Rejected for all other behavior types.
          recursive - boolean - Whether the behavior should apply to child folders. This is only configurable for behavior types whose recursion mode is `sometimes`; `always` behaviors stay recursive and `never` behaviors stay non-recursive.
          name - string - Name for this behavior.
          description - string - Description for this behavior.
          attachment_delete - boolean - If `true`, delete the file stored in `attachment`.
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
        if "disable_parent_folder_behavior" in params and isinstance(
            params["disable_parent_folder_behavior"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: disable_parent_folder_behavior must be an bool"
            )
        if "recursive" in params and isinstance(
            params["recursive"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        params = with_attachments(params, "attachment_file")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/behaviors/" + path_value(params["id"]), params
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
            "DELETE", "/behaviors/" + path_value(params["id"]), params
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
            new_obj = BehaviorResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class BehaviorResource:
    """Behavior operations that use one client's configuration.

    Get one from a client, such as ``client.behavior``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Behavior]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `behavior`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `clickwrap_id`, `form_field_set_id`, `impacts_ui`, `remote_server_id` or `behavior`. Valid field combinations are `[ impacts_ui, behavior ]` and `[ behavior, remote_server_id ]`.
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
        return ListObj(Behavior, "GET", "/behaviors", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Behavior]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Behavior:
        """Parameters:
        id (required) - int64 - Behavior ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Behavior:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/behaviors/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Behavior)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Behavior:
        """The same as find()."""
        return self.find(id, params, options)

    def list_for(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Behavior]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `behavior`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `impacts_ui` and `behavior`. Valid field combinations are `[ impacts_ui, behavior ]`.
        path (required) - string - Path to operate on.
        ancestor_behaviors - boolean - If `true`, behaviors above this path are shown.
        """
        return self.__list_for({"path": path}, params, options)

    def __list_for(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ListObj[Behavior]:
        params = copy_params(params, path_values)
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
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "ancestor_behaviors" in params and not isinstance(
            params["ancestor_behaviors"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ancestor_behaviors must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        return ListObj(
            Behavior,
            "GET",
            "/behaviors/folders/" + path_value(params["path"]),
            params,
            operation,
        )

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Behavior:
        """Parameters:
        value - object - This field stores data specific to the type of behavior. See The Behavior Types section for the accepted value for each type of behavior.
        attachment_file - file - Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
        disable_parent_folder_behavior - boolean - If true, disables the inherited behavior for this folder and its children. Valid only for behavior types that child folders may override, and requires recursive to be true. Rejected for all other behavior types.
        recursive - boolean - Whether the behavior should apply to child folders. This is only configurable for behavior types whose recursion mode is `sometimes`; `always` behaviors stay recursive and `never` behaviors stay non-recursive.
        name - string - Name for this behavior.
        description - string - Description for this behavior.
        path (required) - string - Path where this behavior should apply.
        behavior (required) - string - Behavior type.
        """
        params = copy_params(params)
        if "value" in params and not isinstance(params["value"], dict):
            raise InvalidParameterError("Bad parameter: value must be an dict")
        if "disable_parent_folder_behavior" in params and not isinstance(
            params["disable_parent_folder_behavior"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: disable_parent_folder_behavior must be an bool"
            )
        if "recursive" in params and not isinstance(params["recursive"], bool):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "behavior" in params and not isinstance(params["behavior"], str):
            raise InvalidParameterError(
                "Bad parameter: behavior must be an str"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "behavior" not in params:
            raise MissingParameterError("Parameter missing: behavior")
        params = with_attachments(params, "attachment_file")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/behaviors", params)
        return operation.decode_model(response, Behavior)

    def webhook_test(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        url (required) - string - URL for testing the webhook.
        method - string - HTTP request method (GET or POST).
        encoding - string - Encoding type for the webhook payload. Can be JSON, XML, or RAW (form data).
        headers - object - Additional request headers to send via HTTP.
        body - object - Additional body parameters to include in the webhook payload.
        action - string - Action for test body.
        """
        params = copy_params(params)
        if "url" in params and not isinstance(params["url"], str):
            raise InvalidParameterError("Bad parameter: url must be an str")
        if "method" in params and not isinstance(params["method"], str):
            raise InvalidParameterError("Bad parameter: method must be an str")
        if "encoding" in params and not isinstance(params["encoding"], str):
            raise InvalidParameterError(
                "Bad parameter: encoding must be an str"
            )
        if "headers" in params and not isinstance(params["headers"], dict):
            raise InvalidParameterError(
                "Bad parameter: headers must be an dict"
            )
        if "body" in params and not isinstance(params["body"], dict):
            raise InvalidParameterError("Bad parameter: body must be an dict")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "url" not in params:
            raise MissingParameterError("Parameter missing: url")
        operation = Operation.start(self._scope, options)
        operation.request("POST", "/behaviors/webhook/test", params)

    def update(
        self,
        id: dict[str, Any] | str | int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Behavior:
        """Parameters:
        value - object - This field stores data specific to the type of behavior. See The Behavior Types section for the accepted value for each type of behavior.
        attachment_file - file - Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
        disable_parent_folder_behavior - boolean - If true, disables the inherited behavior for this folder and its children. Valid only for behavior types that child folders may override, and requires recursive to be true. Rejected for all other behavior types.
        recursive - boolean - Whether the behavior should apply to child folders. This is only configurable for behavior types whose recursion mode is `sometimes`; `always` behaviors stay recursive and `never` behaviors stay non-recursive.
        name - string - Name for this behavior.
        description - string - Description for this behavior.
        attachment_delete - boolean - If `true`, delete the file stored in `attachment`.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Behavior:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], (dict, str, int))
            or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: id must be one of dict, str, int"
            )
        if "value" in params and not isinstance(params["value"], dict):
            raise InvalidParameterError("Bad parameter: value must be an dict")
        if "disable_parent_folder_behavior" in params and not isinstance(
            params["disable_parent_folder_behavior"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: disable_parent_folder_behavior must be an bool"
            )
        if "recursive" in params and not isinstance(params["recursive"], bool):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "attachment_delete" in params and (
            not isinstance(params["attachment_delete"], (dict, str, int))
            or isinstance(params["attachment_delete"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: attachment_delete must be one of dict, str, int"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        params = with_attachments(params, "attachment_file")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/behaviors/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Behavior)

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
            "DELETE", "/behaviors/" + path_value(params["id"]), params
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
    ) -> Behavior:
        """A new Behavior with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Behavior(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = BehaviorResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Behavior]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `behavior`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `clickwrap_id`, `form_field_set_id`, `impacts_ui`, `remote_server_id` or `behavior`. Valid field combinations are `[ impacts_ui, behavior ]` and `[ behavior, remote_server_id ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Behavior]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Behavior:
    """Parameters:
    id (required) - int64 - Behavior ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Behavior:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def list_for(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Behavior]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `behavior`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `impacts_ui` and `behavior`. Valid field combinations are `[ impacts_ui, behavior ]`.
    path (required) - string - Path to operate on.
    ancestor_behaviors - boolean - If `true`, behaviors above this path are shown.
    """
    return _legacy_resource.list_for(path, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Behavior:
    """Parameters:
    value - object - This field stores data specific to the type of behavior. See The Behavior Types section for the accepted value for each type of behavior.
    attachment_file - file - Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
    disable_parent_folder_behavior - boolean - If true, disables the inherited behavior for this folder and its children. Valid only for behavior types that child folders may override, and requires recursive to be true. Rejected for all other behavior types.
    recursive - boolean - Whether the behavior should apply to child folders. This is only configurable for behavior types whose recursion mode is `sometimes`; `always` behaviors stay recursive and `never` behaviors stay non-recursive.
    name - string - Name for this behavior.
    description - string - Description for this behavior.
    path (required) - string - Path where this behavior should apply.
    behavior (required) - string - Behavior type.
    """
    return _legacy_resource.create(params, options)


def webhook_test(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    url (required) - string - URL for testing the webhook.
    method - string - HTTP request method (GET or POST).
    encoding - string - Encoding type for the webhook payload. Can be JSON, XML, or RAW (form data).
    headers - object - Additional request headers to send via HTTP.
    body - object - Additional body parameters to include in the webhook payload.
    action - string - Action for test body.
    """
    _legacy_resource.webhook_test(params, options)


def update(
    id: dict[str, Any] | str | int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Behavior:
    """Parameters:
    value - object - This field stores data specific to the type of behavior. See The Behavior Types section for the accepted value for each type of behavior.
    attachment_file - file - Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
    disable_parent_folder_behavior - boolean - If true, disables the inherited behavior for this folder and its children. Valid only for behavior types that child folders may override, and requires recursive to be true. Rejected for all other behavior types.
    recursive - boolean - Whether the behavior should apply to child folders. This is only configurable for behavior types whose recursion mode is `sometimes`; `always` behaviors stay recursive and `never` behaviors stay non-recursive.
    name - string - Name for this behavior.
    description - string - Description for this behavior.
    attachment_delete - boolean - If `true`, delete the file stored in `attachment`.
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


def new(*args, **kwargs) -> Behavior:
    return Behavior(*args, **kwargs)
