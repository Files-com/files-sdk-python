import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Behavior:
    default_attributes = {
        "id": None,  # int64 - Folder behavior ID
        "path": None,  # string - Folder path.  Note that Behavior paths cannot be updated once initially set.  You will need to remove and re-create the behavior on the new path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "attachment_url": None,  # string - URL for attached file
        "behavior": None,  # string - Behavior type.
        "name": None,  # string - Name for this behavior.
        "description": None,  # string - Description for this behavior.
        "value": None,  # object - Settings for this behavior.  See the section above for an example value to provide here.  Formatting is different for each Behavior type.  May be sent as nested JSON or a single JSON-encoded string.  If using XML encoding for the API call, this data must be sent as a JSON-encoded string.
        "attachment_file": None,  # file - Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
        "attachment_delete": None,  # boolean - If true, will delete the file stored in attachment
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Behavior.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Behavior.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   value - string - The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior. See The Behavior Types section for example values for each type of behavior.
    #   attachment_file - file - Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
    #   name - string - Name for this behavior.
    #   description - string - Description for this behavior.
    #   behavior - string - Behavior type.
    #   path - string - Folder behaviors path.
    #   attachment_delete - boolean - If true, will delete the file stored in attachment
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "value" in params and not isinstance(params["value"], str):
            raise InvalidParameterError("Bad parameter: value must be an str")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "behavior" in params and not isinstance(params["behavior"], str):
            raise InvalidParameterError(
                "Bad parameter: behavior must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        response, _options = Api.send_request(
            "PATCH",
            "/behaviors/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request(
            "DELETE",
            "/behaviors/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[behavior]=desc`). Valid fields are `behavior`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `behavior`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `behavior`.
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
    return ListObj(Behavior, "GET", "/behaviors", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Behavior ID.
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET", "/behaviors/{id}".format(id=params["id"]), params, options
    )
    return Behavior(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[behavior]=desc`). Valid fields are `behavior`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `behavior`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `behavior`.
#   path (required) - string - Path to operate on.
#   recursive - string - Show behaviors above this path?
#   behavior - string - DEPRECATED: If set only shows folder behaviors matching this behavior type. Use `filter[behavior]` instead.
def list_for(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
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
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "recursive" in params and not isinstance(params["recursive"], str):
        raise InvalidParameterError("Bad parameter: recursive must be an str")
    if "behavior" in params and not isinstance(params["behavior"], str):
        raise InvalidParameterError("Bad parameter: behavior must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(
        Behavior,
        "GET",
        "/behaviors/folders/{path}".format(path=params["path"]),
        params,
        options,
    )


# Parameters:
#   value - string - The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior. See The Behavior Types section for example values for each type of behavior.
#   attachment_file - file - Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
#   name - string - Name for this behavior.
#   description - string - Description for this behavior.
#   path (required) - string - Folder behaviors path.
#   behavior (required) - string - Behavior type.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "value" in params and not isinstance(params["value"], str):
        raise InvalidParameterError("Bad parameter: value must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "behavior" in params and not isinstance(params["behavior"], str):
        raise InvalidParameterError("Bad parameter: behavior must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "behavior" not in params:
        raise MissingParameterError("Parameter missing: behavior")
    response, options = Api.send_request("POST", "/behaviors", params, options)
    return Behavior(response.data, options)


# Parameters:
#   url (required) - string - URL for testing the webhook.
#   method - string - HTTP method(GET or POST).
#   encoding - string - HTTP encoding method.  Can be JSON, XML, or RAW (form data).
#   headers - object - Additional request headers.
#   body - object - Additional body parameters.
#   action - string - action for test body
def webhook_test(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "url" in params and not isinstance(params["url"], str):
        raise InvalidParameterError("Bad parameter: url must be an str")
    if "method" in params and not isinstance(params["method"], str):
        raise InvalidParameterError("Bad parameter: method must be an str")
    if "encoding" in params and not isinstance(params["encoding"], str):
        raise InvalidParameterError("Bad parameter: encoding must be an str")
    if "headers" in params and not isinstance(params["headers"], dict):
        raise InvalidParameterError("Bad parameter: headers must be an dict")
    if "body" in params and not isinstance(params["body"], dict):
        raise InvalidParameterError("Bad parameter: body must be an dict")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "url" not in params:
        raise MissingParameterError("Parameter missing: url")
    response, _options = Api.send_request(
        "POST", "/behaviors/webhook/test", params, options
    )
    return response.data


# Parameters:
#   value - string - The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior. See The Behavior Types section for example values for each type of behavior.
#   attachment_file - file - Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
#   name - string - Name for this behavior.
#   description - string - Description for this behavior.
#   behavior - string - Behavior type.
#   path - string - Folder behaviors path.
#   attachment_delete - boolean - If true, will delete the file stored in attachment
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], (str, int, dict)):
        raise InvalidParameterError(
            "Bad parameter: id must be one of str, int, dict"
        )
    if "value" in params and not isinstance(params["value"], str):
        raise InvalidParameterError("Bad parameter: value must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "behavior" in params and not isinstance(params["behavior"], str):
        raise InvalidParameterError("Bad parameter: behavior must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "attachment_delete" in params and not isinstance(
        params["attachment_delete"], (str, int, dict)
    ):
        raise InvalidParameterError(
            "Bad parameter: attachment_delete must be one of str, int, dict"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/behaviors/{id}".format(id=params["id"]), params, options
    )
    return Behavior(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request(
        "DELETE", "/behaviors/{id}".format(id=params["id"]), params, options
    )
    return response.data


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Behavior(*args, **kwargs)
