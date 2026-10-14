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


class FormFieldSet:
    """A form field set record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Form field set id
        title: string - Title to be displayed
        require_complete_metadata_capture: boolean - Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
        form_layout: array(int64) - Layout of the form
        form_fields: array(object) - Associated form field definitions; authenticated form field set responses include historical definitions, while form_layout identifies current fields
        skip_name: boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing name
        skip_email: boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing email
        skip_company: boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing company
        in_use: boolean - Form Field Set is in use by an active Inbox / Bundle / Inbox Registration / Bundle Registration
        user_id: int64 - User ID. Provide a value of `0` to operate the current session's user.
        workspace_id: int64 - Workspace ID
    """

    default_attributes = {
        "id": None,  # int64 - Form field set id
        "title": None,  # string - Title to be displayed
        "require_complete_metadata_capture": None,  # boolean - Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
        "form_layout": None,  # array(int64) - Layout of the form
        "form_fields": None,  # array(object) - Associated form field definitions; authenticated form field set responses include historical definitions, while form_layout identifies current fields
        "skip_name": None,  # boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing name
        "skip_email": None,  # boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing email
        "skip_company": None,  # boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing company
        "in_use": None,  # boolean - Form Field Set is in use by an active Inbox / Bundle / Inbox Registration / Bundle Registration
        "user_id": None,  # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        "workspace_id": None,  # int64 - Workspace ID
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    title: str | None
    require_complete_metadata_capture: bool | None
    form_layout: builtins.list[int] | None
    form_fields: builtins.list[dict[str, Any]] | None
    skip_name: bool | None
    skip_email: bool | None
    skip_company: bool | None
    in_use: bool | None
    user_id: int | None
    workspace_id: int | None

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
        ) in FormFieldSet.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FormFieldSet.default_attributes
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
          title - string - Title to be displayed
          require_complete_metadata_capture - boolean - Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
          workspace_id - int64 - Workspace ID
          skip_email - boolean - Skip validating form email
          skip_name - boolean - Skip validating form name
          skip_company - boolean - Skip validating company
          form_fields - array(object)
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
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        if "require_complete_metadata_capture" in params and isinstance(
            params["require_complete_metadata_capture"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: require_complete_metadata_capture must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "skip_email" in params and isinstance(
            params["skip_email"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_email must be an bool"
            )
        if "skip_name" in params and isinstance(
            params["skip_name"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_name must be an bool"
            )
        if "skip_company" in params and isinstance(
            params["skip_company"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_company must be an bool"
            )
        if "form_fields" in params and not isinstance(
            params["form_fields"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: form_fields must be an list"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/form_field_sets/" + path_value(params["id"]), params
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
            "DELETE", "/form_field_sets/" + path_value(params["id"]), params
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
            new_obj = FormFieldSetResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class FormFieldSetResource:
    """FormFieldSet operations that use one client's configuration.

    Get one from a client, such as ``client.form_field_set``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[FormFieldSet]:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
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
        operation = Operation.start(self._scope, options)
        return ListObj(
            FormFieldSet, "GET", "/form_field_sets", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[FormFieldSet]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FormFieldSet:
        """Parameters:
        id (required) - int64 - Form Field Set ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FormFieldSet:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/form_field_sets/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, FormFieldSet)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FormFieldSet:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FormFieldSet:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        title - string - Title to be displayed
        require_complete_metadata_capture - boolean - Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
        workspace_id - int64 - Workspace ID
        skip_email - boolean - Skip validating form email
        skip_name - boolean - Skip validating form name
        skip_company - boolean - Skip validating company
        form_fields - array(object)
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        if "require_complete_metadata_capture" in params and not isinstance(
            params["require_complete_metadata_capture"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: require_complete_metadata_capture must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "skip_email" in params and not isinstance(
            params["skip_email"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_email must be an bool"
            )
        if "skip_name" in params and not isinstance(params["skip_name"], bool):
            raise InvalidParameterError(
                "Bad parameter: skip_name must be an bool"
            )
        if "skip_company" in params and not isinstance(
            params["skip_company"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_company must be an bool"
            )
        if "form_fields" in params and not isinstance(
            params["form_fields"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: form_fields must be an list"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/form_field_sets", params)
        return operation.decode_model(response, FormFieldSet)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FormFieldSet:
        """Parameters:
        title - string - Title to be displayed
        require_complete_metadata_capture - boolean - Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
        workspace_id - int64 - Workspace ID
        skip_email - boolean - Skip validating form email
        skip_name - boolean - Skip validating form name
        skip_company - boolean - Skip validating company
        form_fields - array(object)
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FormFieldSet:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        if "require_complete_metadata_capture" in params and not isinstance(
            params["require_complete_metadata_capture"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: require_complete_metadata_capture must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "skip_email" in params and not isinstance(
            params["skip_email"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_email must be an bool"
            )
        if "skip_name" in params and not isinstance(params["skip_name"], bool):
            raise InvalidParameterError(
                "Bad parameter: skip_name must be an bool"
            )
        if "skip_company" in params and not isinstance(
            params["skip_company"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_company must be an bool"
            )
        if "form_fields" in params and not isinstance(
            params["form_fields"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: form_fields must be an list"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/form_field_sets/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, FormFieldSet)

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
            "DELETE", "/form_field_sets/" + path_value(params["id"]), params
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
    ) -> FormFieldSet:
        """A new FormFieldSet with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = FormFieldSet(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = FormFieldSetResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[FormFieldSet]:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[FormFieldSet]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FormFieldSet:
    """Parameters:
    id (required) - int64 - Form Field Set ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FormFieldSet:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FormFieldSet:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    title - string - Title to be displayed
    require_complete_metadata_capture - boolean - Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
    workspace_id - int64 - Workspace ID
    skip_email - boolean - Skip validating form email
    skip_name - boolean - Skip validating form name
    skip_company - boolean - Skip validating company
    form_fields - array(object)
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FormFieldSet:
    """Parameters:
    title - string - Title to be displayed
    require_complete_metadata_capture - boolean - Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
    workspace_id - int64 - Workspace ID
    skip_email - boolean - Skip validating form email
    skip_name - boolean - Skip validating form name
    skip_company - boolean - Skip validating company
    form_fields - array(object)
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


def new(*args, **kwargs) -> FormFieldSet:
    return FormFieldSet(*args, **kwargs)
