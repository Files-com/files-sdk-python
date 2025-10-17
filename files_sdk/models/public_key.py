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
        "status": None,  # string - Only returned when generating keys. Can be invalid, not_generated, generating, complete
        "last_login_at": None,  # date-time - Key's most recent login time via SFTP
        "generated_private_key": None,  # string - Only returned when generating keys. Private key generated for the user.
        "generated_public_key": None,  # string - Only returned when generating keys. Public key generated for the user.
        "username": None,  # string - Username of the user this public key is associated with
        "user_id": None,  # int64 - User ID this public key is associated with
        "public_key": None,  # string - Actual contents of SSH key.
        "generate_keypair": None,  # boolean - If true, generate a new SSH key pair. Can not be used with `public_key`
        "generate_private_key_password": None,  # string - Password for the private key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        "generate_algorithm": None,  # string - Type of key to generate.  One of rsa, dsa, ecdsa, ed25519. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        "generate_length": None,  # int64 - Length of key to generate. If algorithm is ecdsa, this is the signature size. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
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
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `title`, `created_at` or `user_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
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
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
        raise InvalidParameterError("Bad parameter: filter_gt must be an dict")
    if "filter_gteq" in params and not isinstance(params["filter_gteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_gteq must be an dict"
        )
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_lteq must be an dict"
        )
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
#   public_key - string - Actual contents of SSH key.
#   generate_keypair - boolean - If true, generate a new SSH key pair. Can not be used with `public_key`
#   generate_private_key_password - string - Password for the private key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
#   generate_algorithm - string - Type of key to generate.  One of rsa, dsa, ecdsa, ed25519. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
#   generate_length - int64 - Length of key to generate. If algorithm is ecdsa, this is the signature size. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
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
    if "generate_keypair" in params and not isinstance(
        params["generate_keypair"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: generate_keypair must be an bool"
        )
    if "generate_private_key_password" in params and not isinstance(
        params["generate_private_key_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: generate_private_key_password must be an str"
        )
    if "generate_algorithm" in params and not isinstance(
        params["generate_algorithm"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: generate_algorithm must be an str"
        )
    if "generate_length" in params and not isinstance(
        params["generate_length"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: generate_length must be an int"
        )
    if "title" not in params:
        raise MissingParameterError("Parameter missing: title")
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
