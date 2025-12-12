import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class GpgKey:
    default_attributes = {
        "id": None,  # int64 - GPG key ID.
        "expires_at": None,  # date-time - GPG key expiration date.
        "name": None,  # string - GPG key name.
        "partner_id": None,  # int64 - Partner ID who owns this GPG Key, if applicable.
        "partner_name": None,  # string - Name of the Partner who owns this GPG Key, if applicable.
        "user_id": None,  # int64 - User ID who owns this GPG Key, if applicable.
        "public_key_md5": None,  # string - MD5 hash of the GPG public key
        "private_key_md5": None,  # string - MD5 hash of the GPG private key.
        "generated_public_key": None,  # string - GPG public key
        "generated_private_key": None,  # string - GPG private key.
        "private_key_password_md5": None,  # string - GPG private key password. Only required for password protected keys.
        "public_key": None,  # string - The GPG public key
        "private_key": None,  # string - The GPG private key
        "private_key_password": None,  # string - The GPG private key password
        "generate_expires_at": None,  # string - Expiration date of the key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        "generate_keypair": None,  # boolean - If true, generate a new GPG key pair. Can not be used with `public_key`/`private_key`
        "generate_full_name": None,  # string - Full name of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        "generate_email": None,  # string - Email address of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in GpgKey.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in GpgKey.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   partner_id - int64 - Partner ID who owns this GPG Key, if applicable.
    #   public_key - string - The GPG public key
    #   private_key - string - The GPG private key
    #   private_key_password - string - The GPG private key password
    #   name - string - GPG key name.
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
        if "partner_id" in params and not isinstance(
            params["partner_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_id must be an int"
            )
        if "public_key" in params and not isinstance(
            params["public_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_key must be an str"
            )
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        if "private_key_password" in params and not isinstance(
            params["private_key_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key_password must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        response, _options = Api.send_request(
            "PATCH",
            "/gpg_keys/{id}".format(id=params["id"]),
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
            "/gpg_keys/{id}".format(id=params["id"]),
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
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name` and `expires_at`.
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
    return ListObj(GpgKey, "GET", "/gpg_keys", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Gpg Key ID.
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
        "GET", "/gpg_keys/{id}".format(id=params["id"]), params, options
    )
    return GpgKey(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   partner_id - int64 - Partner ID who owns this GPG Key, if applicable.
#   public_key - string - The GPG public key
#   private_key - string - The GPG private key
#   private_key_password - string - The GPG private key password
#   name (required) - string - GPG key name.
#   generate_expires_at - string - Expiration date of the key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
#   generate_keypair - boolean - If true, generate a new GPG key pair. Can not be used with `public_key`/`private_key`
#   generate_full_name - string - Full name of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
#   generate_email - string - Email address of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "partner_id" in params and not isinstance(params["partner_id"], int):
        raise InvalidParameterError("Bad parameter: partner_id must be an int")
    if "public_key" in params and not isinstance(params["public_key"], str):
        raise InvalidParameterError("Bad parameter: public_key must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError(
            "Bad parameter: private_key must be an str"
        )
    if "private_key_password" in params and not isinstance(
        params["private_key_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: private_key_password must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "generate_expires_at" in params and not isinstance(
        params["generate_expires_at"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: generate_expires_at must be an str"
        )
    if "generate_keypair" in params and not isinstance(
        params["generate_keypair"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: generate_keypair must be an bool"
        )
    if "generate_full_name" in params and not isinstance(
        params["generate_full_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: generate_full_name must be an str"
        )
    if "generate_email" in params and not isinstance(
        params["generate_email"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: generate_email must be an str"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    response, options = Api.send_request("POST", "/gpg_keys", params, options)
    return GpgKey(response.data, options)


# Parameters:
#   partner_id - int64 - Partner ID who owns this GPG Key, if applicable.
#   public_key - string - The GPG public key
#   private_key - string - The GPG private key
#   private_key_password - string - The GPG private key password
#   name - string - GPG key name.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "partner_id" in params and not isinstance(params["partner_id"], int):
        raise InvalidParameterError("Bad parameter: partner_id must be an int")
    if "public_key" in params and not isinstance(params["public_key"], str):
        raise InvalidParameterError("Bad parameter: public_key must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError(
            "Bad parameter: private_key must be an str"
        )
    if "private_key_password" in params and not isinstance(
        params["private_key_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: private_key_password must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/gpg_keys/{id}".format(id=params["id"]), params, options
    )
    return GpgKey(response.data, options)


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
        "DELETE", "/gpg_keys/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return GpgKey(*args, **kwargs)
