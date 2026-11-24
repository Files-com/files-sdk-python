import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.models.automation import Automation
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


class AutomationVersion:
    """A automation version record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Automation revision ID.
        automation_id: int64 - ID of the Automation that owns this revision.
        workspace_id: int64 - Workspace that owns the Automation. Zero is the Default Workspace.
        version: int64 - Revision number within the Automation.
        created_at: date-time - Time the revision was saved.
        user_id: int64 - ID of the user who saved the revision, when available.
        username: string - Username recorded when the revision was saved, when available.
        api_key_id: int64 - ID of the API key used to save the revision, when available.
        definition: object - Saved Automation v2 graph definition. Included when retrieving a single revision.
    """

    default_attributes = {
        "id": None,  # int64 - Automation revision ID.
        "automation_id": None,  # int64 - ID of the Automation that owns this revision.
        "workspace_id": None,  # int64 - Workspace that owns the Automation. Zero is the Default Workspace.
        "version": None,  # int64 - Revision number within the Automation.
        "created_at": None,  # date-time - Time the revision was saved.
        "user_id": None,  # int64 - ID of the user who saved the revision, when available.
        "username": None,  # string - Username recorded when the revision was saved, when available.
        "api_key_id": None,  # int64 - ID of the API key used to save the revision, when available.
        "definition": None,  # object - Saved Automation v2 graph definition. Included when retrieving a single revision.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    automation_id: int | None
    workspace_id: int | None
    version: int | None
    created_at: str | None
    user_id: int | None
    username: str | None
    api_key_id: int | None
    definition: dict[str, Any] | None

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
        ) in AutomationVersion.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AutomationVersion.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def restore(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Restore an Automation v2 definition as a new current version"""
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
        response = operation.request(
            "POST",
            "/automation_versions/" + path_value(params["id"]) + "/restore",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data


class AutomationVersionResource:
    """AutomationVersion operations that use one client's configuration.

    Get one from a client, such as ``client.automation_version``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[AutomationVersion]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
        automation_id (required) - int64 - ID of the Automation that owns this revision.
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
        if "automation_id" in params and (
            not isinstance(params["automation_id"], int)
            or isinstance(params["automation_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: automation_id must be an int"
            )
        if "automation_id" not in params:
            raise MissingParameterError("Parameter missing: automation_id")
        operation = Operation.start(self._scope, options)
        return ListObj(
            AutomationVersion, "GET", "/automation_versions", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[AutomationVersion]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationVersion:
        """Parameters:
        id (required) - int64 - Automation Version ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> AutomationVersion:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/automation_versions/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, AutomationVersion)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationVersion:
        """The same as find()."""
        return self.find(id, params, options)

    def restore(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Automation:
        """Restore an Automation v2 definition as a new current version"""
        return self.__restore({"id": id}, params, options)

    def __restore(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Automation:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/automation_versions/" + path_value(params["id"]) + "/restore",
            params,
        )
        return operation.decode_model(response, Automation)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationVersion:
        """A new AutomationVersion with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = AutomationVersion(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = AutomationVersionResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[AutomationVersion]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
    automation_id (required) - int64 - ID of the Automation that owns this revision.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[AutomationVersion]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationVersion:
    """Parameters:
    id (required) - int64 - Automation Version ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationVersion:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def restore(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Automation:
    """Restore an Automation v2 definition as a new current version"""
    return _legacy_resource.restore(id, params, options)


def new(*args, **kwargs) -> AutomationVersion:
    return AutomationVersion(*args, **kwargs)
