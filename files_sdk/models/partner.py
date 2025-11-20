import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Partner:
    default_attributes = {
        "allow_bypassing_2fa_policies": None,  # boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
        "allow_credential_changes": None,  # boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
        "allow_providing_gpg_keys": None,  # boolean - Allow Partner Admins to provide GPG keys.
        "allow_user_creation": None,  # boolean - Allow Partner Admins to create users.
        "id": None,  # int64 - The unique ID of the Partner.
        "name": None,  # string - The name of the Partner.
        "notes": None,  # string - Notes about this Partner.
        "partner_admin_ids": None,  # array(int64) - Array of User IDs that are Partner Admins for this Partner.
        "root_folder": None,  # string - The root folder path for this Partner.
        "tags": None,  # string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
        "user_ids": None,  # array(int64) - Array of User IDs that belong to this Partner.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Partner.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Partner.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   allow_bypassing_2fa_policies - boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
    #   allow_credential_changes - boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
    #   allow_providing_gpg_keys - boolean - Allow Partner Admins to provide GPG keys.
    #   allow_user_creation - boolean - Allow Partner Admins to create users.
    #   notes - string - Notes about this Partner.
    #   root_folder - string - The root folder path for this Partner.
    #   tags - string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
    #   name - string - The name of the Partner.
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
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "root_folder" in params and not isinstance(
            params["root_folder"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: root_folder must be an str"
            )
        if "tags" in params and not isinstance(params["tags"], str):
            raise InvalidParameterError("Bad parameter: tags must be an str")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        response, _options = Api.send_request(
            "PATCH",
            "/partners/{id}".format(id=params["id"]),
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
            "/partners/{id}".format(id=params["id"]),
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
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`.
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
    return ListObj(Partner, "GET", "/partners", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Partner ID.
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
        "GET", "/partners/{id}".format(id=params["id"]), params, options
    )
    return Partner(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   allow_bypassing_2fa_policies - boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
#   allow_credential_changes - boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
#   allow_providing_gpg_keys - boolean - Allow Partner Admins to provide GPG keys.
#   allow_user_creation - boolean - Allow Partner Admins to create users.
#   notes - string - Notes about this Partner.
#   root_folder - string - The root folder path for this Partner.
#   tags - string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
#   name (required) - string - The name of the Partner.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "allow_bypassing_2fa_policies" in params and not isinstance(
        params["allow_bypassing_2fa_policies"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: allow_bypassing_2fa_policies must be an bool"
        )
    if "allow_credential_changes" in params and not isinstance(
        params["allow_credential_changes"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: allow_credential_changes must be an bool"
        )
    if "allow_providing_gpg_keys" in params and not isinstance(
        params["allow_providing_gpg_keys"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: allow_providing_gpg_keys must be an bool"
        )
    if "allow_user_creation" in params and not isinstance(
        params["allow_user_creation"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: allow_user_creation must be an bool"
        )
    if "notes" in params and not isinstance(params["notes"], str):
        raise InvalidParameterError("Bad parameter: notes must be an str")
    if "root_folder" in params and not isinstance(params["root_folder"], str):
        raise InvalidParameterError(
            "Bad parameter: root_folder must be an str"
        )
    if "tags" in params and not isinstance(params["tags"], str):
        raise InvalidParameterError("Bad parameter: tags must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    response, options = Api.send_request("POST", "/partners", params, options)
    return Partner(response.data, options)


# Parameters:
#   allow_bypassing_2fa_policies - boolean - Allow Partner Admins to change Two-Factor Authentication requirements for Partner Users.
#   allow_credential_changes - boolean - Allow Partner Admins to change or reset credentials for users belonging to this Partner.
#   allow_providing_gpg_keys - boolean - Allow Partner Admins to provide GPG keys.
#   allow_user_creation - boolean - Allow Partner Admins to create users.
#   notes - string - Notes about this Partner.
#   root_folder - string - The root folder path for this Partner.
#   tags - string - Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
#   name - string - The name of the Partner.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "allow_bypassing_2fa_policies" in params and not isinstance(
        params["allow_bypassing_2fa_policies"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: allow_bypassing_2fa_policies must be an bool"
        )
    if "allow_credential_changes" in params and not isinstance(
        params["allow_credential_changes"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: allow_credential_changes must be an bool"
        )
    if "allow_providing_gpg_keys" in params and not isinstance(
        params["allow_providing_gpg_keys"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: allow_providing_gpg_keys must be an bool"
        )
    if "allow_user_creation" in params and not isinstance(
        params["allow_user_creation"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: allow_user_creation must be an bool"
        )
    if "notes" in params and not isinstance(params["notes"], str):
        raise InvalidParameterError("Bad parameter: notes must be an str")
    if "root_folder" in params and not isinstance(params["root_folder"], str):
        raise InvalidParameterError(
            "Bad parameter: root_folder must be an str"
        )
    if "tags" in params and not isinstance(params["tags"], str):
        raise InvalidParameterError("Bad parameter: tags must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/partners/{id}".format(id=params["id"]), params, options
    )
    return Partner(response.data, options)


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
        "DELETE", "/partners/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Partner(*args, **kwargs)
