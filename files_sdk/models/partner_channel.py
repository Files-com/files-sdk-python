import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PartnerChannel:
    default_attributes = {
        "id": None,  # int64 - The unique ID of the Partner Channel.
        "workspace_id": None,  # int64 - ID of the Workspace associated with this Partner Channel.
        "partner_id": None,  # int64 - ID of the Partner this Channel belongs to.
        "path": None,  # string - Channel path relative to the Partner root folder. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "to_partner_folder_name": None,  # string - Optional Channel-level to-Partner folder name override.
        "from_partner_folder_name": None,  # string - Optional Channel-level from-Partner folder name override.
        "from_partner_route_path": None,  # string - Optional route path for files uploaded by the Partner.
        "to_partner_route_path": None,  # string - Optional route path for files delivered to the Partner.
        "effective_to_partner_folder_name": None,  # string - Resolved to-Partner folder name after Channel override and default.
        "effective_from_partner_folder_name": None,  # string - Resolved from-Partner folder name after Channel override and default.
        "channel_path": None,  # string - Resolved Channel folder path.
        "to_partner_folder_path": None,  # string - Resolved to-Partner folder path.
        "from_partner_folder_path": None,  # string - Resolved from-Partner folder path.
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
        ) in PartnerChannel.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PartnerChannel.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Parameters:
    #   from_partner_folder_name - string - Optional Channel-level from-Partner folder name override.
    #   from_partner_route_path - string - Optional route path for files uploaded by the Partner.
    #   to_partner_folder_name - string - Optional Channel-level to-Partner folder name override.
    #   to_partner_route_path - string - Optional route path for files delivered to the Partner.
    #   path - string - Channel path relative to the Partner root folder.
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
        if "from_partner_folder_name" in params and not isinstance(
            params["from_partner_folder_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_folder_name must be an str"
            )
        if "from_partner_route_path" in params and not isinstance(
            params["from_partner_route_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: from_partner_route_path must be an str"
            )
        if "to_partner_folder_name" in params and not isinstance(
            params["to_partner_folder_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_folder_name must be an str"
            )
        if "to_partner_route_path" in params and not isinstance(
            params["to_partner_route_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: to_partner_route_path must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        response, _options = Api.send_request(
            "PATCH",
            "/partner_channels/{id}".format(
                id=quote(str(params["id"]), safe="")
            ),
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
            "/partner_channels/{id}".format(
                id=quote(str(params["id"]), safe="")
            ),
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
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `path` or `partner_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `partner_id` and `workspace_id`. Valid field combinations are `[ workspace_id, partner_id ]`.
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
    return ListObj(PartnerChannel, "GET", "/partner_channels", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Partner Channel ID.
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
        "/partner_channels/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return PartnerChannel(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   from_partner_folder_name - string - Optional Channel-level from-Partner folder name override.
#   from_partner_route_path - string - Optional route path for files uploaded by the Partner.
#   to_partner_folder_name - string - Optional Channel-level to-Partner folder name override.
#   to_partner_route_path - string - Optional route path for files delivered to the Partner.
#   partner_id (required) - int64 - ID of the Partner this Channel belongs to.
#   path (required) - string - Channel path relative to the Partner root folder.
#   workspace_id - int64 - ID of the Workspace associated with this Partner Channel.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "from_partner_folder_name" in params and not isinstance(
        params["from_partner_folder_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: from_partner_folder_name must be an str"
        )
    if "from_partner_route_path" in params and not isinstance(
        params["from_partner_route_path"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: from_partner_route_path must be an str"
        )
    if "to_partner_folder_name" in params and not isinstance(
        params["to_partner_folder_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: to_partner_folder_name must be an str"
        )
    if "to_partner_route_path" in params and not isinstance(
        params["to_partner_route_path"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: to_partner_route_path must be an str"
        )
    if "partner_id" in params and not isinstance(params["partner_id"], int):
        raise InvalidParameterError("Bad parameter: partner_id must be an int")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: workspace_id must be an int"
        )
    if "partner_id" not in params:
        raise MissingParameterError("Parameter missing: partner_id")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request(
        "POST", "/partner_channels", params, options
    )
    return PartnerChannel(response.data, options)


# Parameters:
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `path` or `partner_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `partner_id` and `workspace_id`. Valid field combinations are `[ workspace_id, partner_id ]`.
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    response, options = Api.send_request(
        "POST", "/partner_channels/create_export", params, options
    )
    return Export(response.data, options)


# Parameters:
#   from_partner_folder_name - string - Optional Channel-level from-Partner folder name override.
#   from_partner_route_path - string - Optional route path for files uploaded by the Partner.
#   to_partner_folder_name - string - Optional Channel-level to-Partner folder name override.
#   to_partner_route_path - string - Optional route path for files delivered to the Partner.
#   path - string - Channel path relative to the Partner root folder.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "from_partner_folder_name" in params and not isinstance(
        params["from_partner_folder_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: from_partner_folder_name must be an str"
        )
    if "from_partner_route_path" in params and not isinstance(
        params["from_partner_route_path"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: from_partner_route_path must be an str"
        )
    if "to_partner_folder_name" in params and not isinstance(
        params["to_partner_folder_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: to_partner_folder_name must be an str"
        )
    if "to_partner_route_path" in params and not isinstance(
        params["to_partner_route_path"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: to_partner_route_path must be an str"
        )
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/partner_channels/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return PartnerChannel(response.data, options)


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
        "/partner_channels/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return PartnerChannel(*args, **kwargs)
