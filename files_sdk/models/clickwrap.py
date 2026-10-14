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


class Clickwrap:
    """A clickwrap record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Clickwrap ID
        name: string - Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
        body: string - Body text of Clickwrap (supports Markdown formatting).
        use_with_users: string - Use this Clickwrap for Users? Values: `none`, `require` (new user signup via email invitation only), `require_all_users_once` (show to all users at their next web login; once accepted, not shown again), `require_all_users_always` (show to all users on every web login).
        use_with_bundles: string - Use this Clickwrap for Bundles?
        use_with_inboxes: string - Use this Clickwrap for Inboxes?
    """

    default_attributes = {
        "id": None,  # int64 - Clickwrap ID
        "name": None,  # string - Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
        "body": None,  # string - Body text of Clickwrap (supports Markdown formatting).
        "use_with_users": None,  # string - Use this Clickwrap for Users?  Values: `none`, `require` (new user signup via email invitation only), `require_all_users_once` (show to all users at their next web login; once accepted, not shown again), `require_all_users_always` (show to all users on every web login).
        "use_with_bundles": None,  # string - Use this Clickwrap for Bundles?
        "use_with_inboxes": None,  # string - Use this Clickwrap for Inboxes?
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    body: str | None
    use_with_users: str | None
    use_with_bundles: str | None
    use_with_inboxes: str | None

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
        for attribute, default_value in Clickwrap.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Clickwrap.default_attributes
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
          name - string - Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
          body - string - Body text of Clickwrap (supports Markdown formatting).
          use_with_bundles - string - Use this Clickwrap for Bundles?
          use_with_inboxes - string - Use this Clickwrap for Inboxes?
          use_with_users - string - Use this Clickwrap for Users?  Values: `none`, `require` (new user signup via email invitation only), `require_all_users_once` (show to all users at their next web login; once accepted, not shown again), `require_all_users_always` (show to all users on every web login).
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
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "body" in params and not isinstance(params["body"], str):
            raise InvalidParameterError("Bad parameter: body must be an str")
        if "use_with_bundles" in params and not isinstance(
            params["use_with_bundles"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_bundles must be an str"
            )
        if "use_with_inboxes" in params and not isinstance(
            params["use_with_inboxes"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_inboxes must be an str"
            )
        if "use_with_users" in params and not isinstance(
            params["use_with_users"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_users must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/clickwraps/" + path_value(params["id"]), params
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
            "DELETE", "/clickwraps/" + path_value(params["id"]), params
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
            new_obj = ClickwrapResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class ClickwrapResource:
    """Clickwrap operations that use one client's configuration.

    Get one from a client, such as ``client.clickwrap``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Clickwrap]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
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
        operation = Operation.start(self._scope, options)
        return ListObj(Clickwrap, "GET", "/clickwraps", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Clickwrap]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Clickwrap:
        """Parameters:
        id (required) - int64 - Clickwrap ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Clickwrap:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/clickwraps/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Clickwrap)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Clickwrap:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Clickwrap:
        """Parameters:
        name - string - Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
        body - string - Body text of Clickwrap (supports Markdown formatting).
        use_with_bundles - string - Use this Clickwrap for Bundles?
        use_with_inboxes - string - Use this Clickwrap for Inboxes?
        use_with_users - string - Use this Clickwrap for Users?  Values: `none`, `require` (new user signup via email invitation only), `require_all_users_once` (show to all users at their next web login; once accepted, not shown again), `require_all_users_always` (show to all users on every web login).
        """
        params = copy_params(params)
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "body" in params and not isinstance(params["body"], str):
            raise InvalidParameterError("Bad parameter: body must be an str")
        if "use_with_bundles" in params and not isinstance(
            params["use_with_bundles"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_bundles must be an str"
            )
        if "use_with_inboxes" in params and not isinstance(
            params["use_with_inboxes"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_inboxes must be an str"
            )
        if "use_with_users" in params and not isinstance(
            params["use_with_users"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_users must be an str"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/clickwraps", params)
        return operation.decode_model(response, Clickwrap)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Clickwrap:
        """Parameters:
        name - string - Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
        body - string - Body text of Clickwrap (supports Markdown formatting).
        use_with_bundles - string - Use this Clickwrap for Bundles?
        use_with_inboxes - string - Use this Clickwrap for Inboxes?
        use_with_users - string - Use this Clickwrap for Users?  Values: `none`, `require` (new user signup via email invitation only), `require_all_users_once` (show to all users at their next web login; once accepted, not shown again), `require_all_users_always` (show to all users on every web login).
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Clickwrap:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "body" in params and not isinstance(params["body"], str):
            raise InvalidParameterError("Bad parameter: body must be an str")
        if "use_with_bundles" in params and not isinstance(
            params["use_with_bundles"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_bundles must be an str"
            )
        if "use_with_inboxes" in params and not isinstance(
            params["use_with_inboxes"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_inboxes must be an str"
            )
        if "use_with_users" in params and not isinstance(
            params["use_with_users"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: use_with_users must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/clickwraps/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Clickwrap)

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
            "DELETE", "/clickwraps/" + path_value(params["id"]), params
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
    ) -> Clickwrap:
        """A new Clickwrap with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Clickwrap(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ClickwrapResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Clickwrap]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Clickwrap]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Clickwrap:
    """Parameters:
    id (required) - int64 - Clickwrap ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Clickwrap:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Clickwrap:
    """Parameters:
    name - string - Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
    body - string - Body text of Clickwrap (supports Markdown formatting).
    use_with_bundles - string - Use this Clickwrap for Bundles?
    use_with_inboxes - string - Use this Clickwrap for Inboxes?
    use_with_users - string - Use this Clickwrap for Users?  Values: `none`, `require` (new user signup via email invitation only), `require_all_users_once` (show to all users at their next web login; once accepted, not shown again), `require_all_users_always` (show to all users on every web login).
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Clickwrap:
    """Parameters:
    name - string - Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
    body - string - Body text of Clickwrap (supports Markdown formatting).
    use_with_bundles - string - Use this Clickwrap for Bundles?
    use_with_inboxes - string - Use this Clickwrap for Inboxes?
    use_with_users - string - Use this Clickwrap for Users?  Values: `none`, `require` (new user signup via email invitation only), `require_all_users_once` (show to all users at their next web login; once accepted, not shown again), `require_all_users_always` (show to all users on every web login).
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


def new(*args, **kwargs) -> Clickwrap:
    return Clickwrap(*args, **kwargs)
