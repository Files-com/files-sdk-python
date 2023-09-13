import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class App:
    default_attributes = {
        "name": None,  # string - Name of the App
        "extended_description": None,  # string - Long form description of the App
        "short_description": None,  # string - Short description of the App
        "documentation_links": None,  # object - Collection of named links to documentation
        "icon_url": None,  # string - App icon
        "logo_url": None,  # string - Full size logo for the App
        "screenshot_list_urls": None,  # array - Screenshots of the App
        "logo_thumbnail_url": None,  # string - Logo thumbnail for the App
        "sso_strategy_type": None,  # string - Associated SSO Strategy type, if any
        "remote_server_type": None,  # string - Associated Remote Server type, if any
        "folder_behavior_type": None,  # string - Associated Folder Behavior type, if any
        "external_homepage_url": None,  # string - Link to external homepage
        "marketing_youtube_url": None,  # string - Marketing video page
        "tutorial_youtube_url": None,  # string - Tutorial video page
        "app_type": None,  # string - The type of the App
        "featured": None,  # boolean - Is featured on the App listing?
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in App.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in App.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[name]=desc`). Valid fields are `name` and `app_type`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]` and `[ app_type, name ]`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    return ListObj(App, "GET", "/apps", params, options)


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return App(*args, **kwargs)
