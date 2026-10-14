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
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Style:
    """A style record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Style ID
        path: string - Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        logo: Image - Logo
        logo_click_href: string - URL to open when a public visitor clicks the logo
        thumbnail: Image - Logo thumbnail
        file: file - Logo for custom branding. Required when creating a new style.
    """

    default_attributes = {
        "id": None,  # int64 - Style ID
        "path": None,  # string - Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "logo": None,  # Image - Logo
        "logo_click_href": None,  # string - URL to open when a public visitor clicks the logo
        "thumbnail": None,  # Image - Logo thumbnail
        "file": None,  # file - Logo for custom branding. Required when creating a new style.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    path: str | None
    logo: dict[str, Any] | None
    logo_click_href: str | None
    thumbnail: dict[str, Any] | None
    file: Any

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
        for attribute, default_value in Style.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Style.default_attributes
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
          file - file - Logo for custom branding. Required when creating a new style.
          logo_click_href - string - URL to open when a public visitor clicks the logo.
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "logo_click_href" in params and not isinstance(
            params["logo_click_href"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: logo_click_href must be an str"
            )
        params = with_attachments(params, "file")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/styles/" + path_value(params["path"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/styles/" + path_value(params["path"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server with its attributes, taking in
        place the record the server returns."""
        self.update(self.get_attributes())


class StyleResource:
    """Style operations that use one client's configuration.

    Get one from a client, such as ``client.style``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def find(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Style:
        """Parameters:
        path (required) - string - Style path.
        """
        return self.__find({"path": path}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Style:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/styles/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, Style)

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Style:
        """The same as find()."""
        return self.find(path, params, options)

    def update(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Style:
        """Parameters:
        file - file - Logo for custom branding. Required when creating a new style.
        logo_click_href - string - URL to open when a public visitor clicks the logo.
        """
        return self.__update({"path": path}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Style:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "logo_click_href" in params and not isinstance(
            params["logo_click_href"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: logo_click_href must be an str"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        params = with_attachments(params, "file")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/styles/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, Style)

    def delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"path": path}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/styles/" + path_value(params["path"]), params
        )

    def destroy(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(path, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Style:
        """A new Style with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Style(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = StyleResource(LEGACY)


def find(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Style:
    """Parameters:
    path (required) - string - Style path.
    """
    return _legacy_resource.find(path, params, options)


def get(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Style:
    """The same as find()."""
    return _legacy_resource.find(path, params, options)


def update(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Style:
    """Parameters:
    file - file - Logo for custom branding. Required when creating a new style.
    logo_click_href - string - URL to open when a public visitor clicks the logo.
    """
    return _legacy_resource.update(path, params, options)


def delete(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(path, params, options)


def destroy(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(path, params, options)


def new(*args, **kwargs) -> Style:
    return Style(*args, **kwargs)
