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


class App:
    """A app record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        app_type: string - The type of the App
        documentation_links: object - Collection of named links to documentation
        extended_description: string - Long description for the in-App landing page
        extended_description_for_marketing_site: string - Long form description of the App
        external_homepage_url: string - Link to external homepage
        featured: boolean - Is featured on the App listing?
        folder_behavior_type: string - Associated Folder Behavior type, if any
        icon_url: string - App icon
        logo_thumbnail_url: string - Logo thumbnail for the App
        logo_url: string - Full size logo for the App
        marketing_intro: string - Marketing introdution of the App
        marketing_youtube_url: string - Marketing video page
        name: string - Name of the App
        package_manager_install_command: string - Package manager install command
        remote_server_type: string - Associated Remote Server type, if any
        screenshot_list_urls: array(string) - Screenshots of the App
        sdk_installation_instructions_link: string - Link to SDK installation instructions
        short_description: string - Short description of the App
        sso_strategy_type: string - Associated SSO Strategy type, if any
        siem_type: string - Associated SIEM type, if any
        tutorial_youtube_url: string - Tutorial video page
    """

    default_attributes = {
        "app_type": None,  # string - The type of the App
        "documentation_links": None,  # object - Collection of named links to documentation
        "extended_description": None,  # string - Long description for the in-App landing page
        "extended_description_for_marketing_site": None,  # string - Long form description of the App
        "external_homepage_url": None,  # string - Link to external homepage
        "featured": None,  # boolean - Is featured on the App listing?
        "folder_behavior_type": None,  # string - Associated Folder Behavior type, if any
        "icon_url": None,  # string - App icon
        "logo_thumbnail_url": None,  # string - Logo thumbnail for the App
        "logo_url": None,  # string - Full size logo for the App
        "marketing_intro": None,  # string - Marketing introdution of the App
        "marketing_youtube_url": None,  # string - Marketing video page
        "name": None,  # string - Name of the App
        "package_manager_install_command": None,  # string - Package manager install command
        "remote_server_type": None,  # string - Associated Remote Server type, if any
        "screenshot_list_urls": None,  # array(string) - Screenshots of the App
        "sdk_installation_instructions_link": None,  # string - Link to SDK installation instructions
        "short_description": None,  # string - Short description of the App
        "sso_strategy_type": None,  # string - Associated SSO Strategy type, if any
        "siem_type": None,  # string - Associated SIEM type, if any
        "tutorial_youtube_url": None,  # string - Tutorial video page
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    app_type: str | None
    documentation_links: dict[str, Any] | None
    extended_description: str | None
    extended_description_for_marketing_site: str | None
    external_homepage_url: str | None
    featured: bool | None
    folder_behavior_type: str | None
    icon_url: str | None
    logo_thumbnail_url: str | None
    logo_url: str | None
    marketing_intro: str | None
    marketing_youtube_url: str | None
    name: str | None
    package_manager_install_command: str | None
    remote_server_type: str | None
    screenshot_list_urls: builtins.list[str] | None
    sdk_installation_instructions_link: str | None
    short_description: str | None
    sso_strategy_type: str | None
    siem_type: str | None
    tutorial_youtube_url: str | None

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
        for attribute, default_value in App.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in App.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class AppResource:
    """App operations that use one client's configuration.

    Get one from a client, such as ``client.app``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[App]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name` and `app_type`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
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
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(App, "GET", "/apps", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[App]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> App:
        """A new App with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = App(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = AppResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[App]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name` and `app_type`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[App]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> App:
    return App(*args, **kwargs)
