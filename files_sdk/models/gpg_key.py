import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class GpgKey:
    """A gpg key record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - GPG key ID.
        workspace_id: int64 - Workspace ID (0 for default workspace).
        expires_at: date-time - GPG key expiration date.
        name: string - GPG key name.
        partner_id: int64 - Partner ID who owns this GPG Key, if applicable.
        partner_name: string - Name of the Partner who owns this GPG Key, if applicable.
        user_id: int64 - User ID who owns this GPG Key, if applicable.
        public_key_md5: string - MD5 hash of the GPG public key
        private_key_md5: string - MD5 hash of the GPG private key.
        generated_public_key: string - GPG public key
        generated_private_key: string - GPG private key.
        private_key_password_md5: string - GPG private key password. Only required for password protected keys.
        public_key: string - The GPG public key
        private_key: string - The GPG private key
        private_key_password: string - The GPG private key password
        generate_expires_at: string - Expiration date of the key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        generate_keypair: boolean - If true, generate a new GPG key pair. Can not be used with `public_key`/`private_key`
        generate_full_name: string - Full name of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        generate_email: string - Email address of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    """

    default_attributes = {
        "id": None,  # int64 - GPG key ID.
        "workspace_id": None,  # int64 - Workspace ID (0 for default workspace).
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

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    expires_at: str | None
    name: str | None
    partner_id: int | None
    partner_name: str | None
    user_id: int | None
    public_key_md5: str | None
    private_key_md5: str | None
    generated_public_key: str | None
    generated_private_key: str | None
    private_key_password_md5: str | None
    public_key: str | None
    private_key: str | None
    private_key_password: str | None
    generate_expires_at: str | None
    generate_keypair: bool | None
    generate_full_name: str | None
    generate_email: str | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

    def set_attributes(self, attributes):
        for attribute, default_value in GpgKey.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in GpgKey.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          partner_id - int64 - Partner ID who owns this GPG Key, if applicable.
          public_key - string - The GPG public key
          private_key - string - The GPG private key
          private_key_password - string - The GPG private key password
          name - string - GPG key name.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "partner_id" in params and (
            not isinstance(params["partner_id"], int)
            or isinstance(params["partner_id"], bool)
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
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/gpg_keys/" + path_value(params["id"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/gpg_keys/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = GpgKeyResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class GpgKeyResource:
    """GpgKey operations that use one client's configuration.

    Get one from a client, such as ``client.gpg_key``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[GpgKey]:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name` or `expires_at`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`, `partner_id` or `expires_at`. Valid field combinations are `[ workspace_id, partner_id ]`, `[ workspace_id, expires_at ]`, `[ partner_id, expires_at ]` or `[ workspace_id, partner_id, expires_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `expires_at`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `expires_at`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `expires_at`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `expires_at`.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_gt must be an dict"
            )
        if "filter_gteq" in params and not isinstance(
            params["filter_gteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_gteq must be an dict"
            )
        if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_lt must be an dict"
            )
        if "filter_lteq" in params and not isinstance(
            params["filter_lteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_lteq must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(GpgKey, "GET", "/gpg_keys", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[GpgKey]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> GpgKey:
        """Parameters:
        id (required) - int64 - Gpg Key ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> GpgKey:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/gpg_keys/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, GpgKey)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> GpgKey:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> GpgKey:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        partner_id - int64 - Partner ID who owns this GPG Key, if applicable.
        public_key - string - The GPG public key
        private_key - string - The GPG private key
        private_key_password - string - The GPG private key password
        name (required) - string - GPG key name.
        workspace_id - int64 - Workspace ID (0 for default workspace).
        generate_expires_at - string - Expiration date of the key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        generate_keypair - boolean - If true, generate a new GPG key pair. Can not be used with `public_key`/`private_key`
        generate_full_name - string - Full name of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        generate_email - string - Email address of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "partner_id" in params and (
            not isinstance(params["partner_id"], int)
            or isinstance(params["partner_id"], bool)
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
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
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
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/gpg_keys", params)
        return operation.decode_model(response, GpgKey)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> GpgKey:
        """Parameters:
        partner_id - int64 - Partner ID who owns this GPG Key, if applicable.
        public_key - string - The GPG public key
        private_key - string - The GPG private key
        private_key_password - string - The GPG private key password
        name - string - GPG key name.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> GpgKey:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "partner_id" in params and (
            not isinstance(params["partner_id"], int)
            or isinstance(params["partner_id"], bool)
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
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/gpg_keys/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, GpgKey)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/gpg_keys/" + path_value(params["id"]), params
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> GpgKey:
        """A new GpgKey with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = GpgKey(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = GpgKeyResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[GpgKey]:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name` or `expires_at`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`, `partner_id` or `expires_at`. Valid field combinations are `[ workspace_id, partner_id ]`, `[ workspace_id, expires_at ]`, `[ partner_id, expires_at ]` or `[ workspace_id, partner_id, expires_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `expires_at`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `expires_at`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `expires_at`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `expires_at`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[GpgKey]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> GpgKey:
    """Parameters:
    id (required) - int64 - Gpg Key ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> GpgKey:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> GpgKey:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    partner_id - int64 - Partner ID who owns this GPG Key, if applicable.
    public_key - string - The GPG public key
    private_key - string - The GPG private key
    private_key_password - string - The GPG private key password
    name (required) - string - GPG key name.
    workspace_id - int64 - Workspace ID (0 for default workspace).
    generate_expires_at - string - Expiration date of the key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    generate_keypair - boolean - If true, generate a new GPG key pair. Can not be used with `public_key`/`private_key`
    generate_full_name - string - Full name of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    generate_email - string - Email address of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> GpgKey:
    """Parameters:
    partner_id - int64 - Partner ID who owns this GPG Key, if applicable.
    public_key - string - The GPG public key
    private_key - string - The GPG private key
    private_key_password - string - The GPG private key password
    name - string - GPG key name.
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> GpgKey:
    return GpgKey(*args, **kwargs)
