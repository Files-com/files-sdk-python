import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class IntegrationCentricProfile:
    default_attributes = {
        "id": None,  # int64 - Integration Centric Profile ID
        "name": None,  # string - Profile name
        "workspace_id": None,  # int64 - Workspace ID
        "use_for_all_users": None,  # boolean - Whether this profile applies to all users in the Workspace by default
        "expected_remote_servers": None,  # array(object) - Remote Server integrations the user is expected to add and connect. Each entry requires `server_type` and may include a display `name`.
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
        ) in IntegrationCentricProfile.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in IntegrationCentricProfile.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Parameters:
    #   name - string - Profile name
    #   workspace_id - int64 - Workspace ID
    #   expected_remote_servers - array(object) - Remote Server integrations the user is expected to add and connect. Each entry requires `server_type` and may include a display `name`.
    #   use_for_all_users - boolean - Whether this profile applies to all users in the Workspace by default
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
        if "workspace_id" in params and not isinstance(
            params["workspace_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "expected_remote_servers" in params and not isinstance(
            params["expected_remote_servers"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: expected_remote_servers must be an list"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/integration_centric_profiles/{id}".format(
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
            "/integration_centric_profiles/{id}".format(
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
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
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
    return ListObj(
        IntegrationCentricProfile,
        "GET",
        "/integration_centric_profiles",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Integration Centric Profile ID.
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
        "/integration_centric_profiles/{id}".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )
    return IntegrationCentricProfile(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name (required) - string - Profile name
#   expected_remote_servers (required) - array(object) - Remote Server integrations the user is expected to add and connect. Each entry requires `server_type` and may include a display `name`.
#   workspace_id - int64 - Workspace ID
#   use_for_all_users - boolean - Whether this profile applies to all users in the Workspace by default
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "expected_remote_servers" in params and not isinstance(
        params["expected_remote_servers"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: expected_remote_servers must be an list"
        )
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: workspace_id must be an int"
        )
    if "use_for_all_users" in params and not isinstance(
        params["use_for_all_users"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: use_for_all_users must be an bool"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    if "expected_remote_servers" not in params:
        raise MissingParameterError(
            "Parameter missing: expected_remote_servers"
        )
    response, options = Api.send_request(
        "POST", "/integration_centric_profiles", params, options
    )
    return IntegrationCentricProfile(response.data, options)


# Parameters:
#   name - string - Profile name
#   workspace_id - int64 - Workspace ID
#   expected_remote_servers - array(object) - Remote Server integrations the user is expected to add and connect. Each entry requires `server_type` and may include a display `name`.
#   use_for_all_users - boolean - Whether this profile applies to all users in the Workspace by default
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
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: workspace_id must be an int"
        )
    if "expected_remote_servers" in params and not isinstance(
        params["expected_remote_servers"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: expected_remote_servers must be an list"
        )
    if "use_for_all_users" in params and not isinstance(
        params["use_for_all_users"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: use_for_all_users must be an bool"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/integration_centric_profiles/{id}".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )
    return IntegrationCentricProfile(response.data, options)


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
        "/integration_centric_profiles/{id}".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return IntegrationCentricProfile(*args, **kwargs)
