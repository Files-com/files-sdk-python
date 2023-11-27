import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Snapshot:
    default_attributes = {
        "id": None,  # int64 - The snapshot's unique ID.
        "expires_at": None,  # date-time - When the snapshot expires.
        "finalized_at": None,  # date-time - When the snapshot was finalized.
        "name": None,  # string - A name for the snapshot.
        "user_id": None,  # int64 - The user that created this snapshot, if applicable.
        "bundle_id": None,  # int64 - The bundle using this snapshot, if applicable.
        "paths": None,  # array(string) - An array of paths to add to the snapshot.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Snapshot.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Snapshot.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   expires_at - string - When the snapshot expires.
    #   name - string - A name for the snapshot.
    #   paths - array(string) - An array of paths to add to the snapshot.
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
        if "expires_at" in params and not isinstance(
            params["expires_at"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: expires_at must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "paths" in params and not isinstance(
            params["paths"], builtins.list
        ):
            raise InvalidParameterError("Bad parameter: paths must be an list")
        response, _options = Api.send_request(
            "PATCH",
            "/snapshots/{id}".format(id=params["id"]),
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
            "/snapshots/{id}".format(id=params["id"]),
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
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(Snapshot, "GET", "/snapshots", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Snapshot ID.
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
        "GET", "/snapshots/{id}".format(id=params["id"]), params, options
    )
    return Snapshot(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   expires_at - string - When the snapshot expires.
#   name - string - A name for the snapshot.
#   paths - array(string) - An array of paths to add to the snapshot.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "paths" in params and not isinstance(params["paths"], builtins.list):
        raise InvalidParameterError("Bad parameter: paths must be an list")
    response, options = Api.send_request("POST", "/snapshots", params, options)
    return Snapshot(response.data, options)


# Parameters:
#   expires_at - string - When the snapshot expires.
#   name - string - A name for the snapshot.
#   paths - array(string) - An array of paths to add to the snapshot.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "paths" in params and not isinstance(params["paths"], builtins.list):
        raise InvalidParameterError("Bad parameter: paths must be an list")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/snapshots/{id}".format(id=params["id"]), params, options
    )
    return Snapshot(response.data, options)


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
        "DELETE", "/snapshots/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Snapshot(*args, **kwargs)
