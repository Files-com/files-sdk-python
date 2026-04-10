import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class MetadataCategory:
    default_attributes = {
        "id": None,  # int64 - Metadata Category ID
        "name": None,  # string - Name of the metadata category.
        "definitions": None,  # hash(string,array(string)) - Map of key names to arrays of allowed values. An empty array means free-form text.
        "default_columns": None,  # array(string) - Metadata keys that should appear as columns in the UI by default.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in MetadataCategory.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in MetadataCategory.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Parameters:
    #   name - string - Name of the metadata category.
    #   default_columns - array(string) - Metadata keys that should appear as columns in the UI by default.
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
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "default_columns" in params and not isinstance(
            params["default_columns"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: default_columns must be an list"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/metadata_categories/{id}".format(id=params["id"]),
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
        Api.send_request(
            "DELETE",
            "/metadata_categories/{id}".format(id=params["id"]),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            new_obj = self.update(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            return True
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
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
    return ListObj(
        MetadataCategory, "GET", "/metadata_categories", params, options
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Metadata Category ID.
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
        "GET",
        "/metadata_categories/{id}".format(id=params["id"]),
        params,
        options,
    )
    return MetadataCategory(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name (required) - string - Name of the metadata category.
#   default_columns - array(string) - Metadata keys that should appear as columns in the UI by default.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "default_columns" in params and not isinstance(
        params["default_columns"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: default_columns must be an list"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    response, options = Api.send_request(
        "POST", "/metadata_categories", params, options
    )
    return MetadataCategory(response.data, options)


# Parameters:
#   name - string - Name of the metadata category.
#   default_columns - array(string) - Metadata keys that should appear as columns in the UI by default.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "default_columns" in params and not isinstance(
        params["default_columns"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: default_columns must be an list"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/metadata_categories/{id}".format(id=params["id"]),
        params,
        options,
    )
    return MetadataCategory(response.data, options)


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
    Api.send_request(
        "DELETE",
        "/metadata_categories/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return MetadataCategory(*args, **kwargs)
