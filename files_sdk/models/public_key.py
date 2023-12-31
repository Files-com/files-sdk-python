import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PublicKey:
    default_attributes = {
        "id": None,  # int64 - Public key ID
        "title": None,  # string - Public key title
        "created_at": None,  # date-time - Public key created at date/time
        "fingerprint": None,  # string - Public key fingerprint (MD5)
        "fingerprint_sha256": None,  # string - Public key fingerprint (SHA256)
        "username": None,  # string - Username of the user this public key is associated with
        "user_id": None,  # int64 - User ID this public key is associated with
        "public_key": None,  # string - Actual contents of SSH key.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in PublicKey.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in PublicKey.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   title (required) - string - Internal reference for key.
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "title" not in params:
            raise MissingParameterError("Parameter missing: title")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        response, _options = Api.send_request(
            "PATCH",
            "/public_keys/{id}".format(id=params["id"]),
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
            "/public_keys/{id}".format(id=params["id"]),
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
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(PublicKey, "GET", "/public_keys", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Public Key ID.
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
        "GET", "/public_keys/{id}".format(id=params["id"]), params, options
    )
    return PublicKey(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   title (required) - string - Internal reference for key.
#   public_key (required) - string - Actual contents of SSH key.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "title" in params and not isinstance(params["title"], str):
        raise InvalidParameterError("Bad parameter: title must be an str")
    if "public_key" in params and not isinstance(params["public_key"], str):
        raise InvalidParameterError("Bad parameter: public_key must be an str")
    if "title" not in params:
        raise MissingParameterError("Parameter missing: title")
    if "public_key" not in params:
        raise MissingParameterError("Parameter missing: public_key")
    response, options = Api.send_request(
        "POST", "/public_keys", params, options
    )
    return PublicKey(response.data, options)


# Parameters:
#   title (required) - string - Internal reference for key.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "title" in params and not isinstance(params["title"], str):
        raise InvalidParameterError("Bad parameter: title must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "title" not in params:
        raise MissingParameterError("Parameter missing: title")
    response, options = Api.send_request(
        "PATCH", "/public_keys/{id}".format(id=params["id"]), params, options
    )
    return PublicKey(response.data, options)


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
        "DELETE", "/public_keys/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return PublicKey(*args, **kwargs)
