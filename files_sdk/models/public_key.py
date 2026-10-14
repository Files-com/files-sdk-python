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


class PublicKey:
    """A public key record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Public key ID
        workspace_id: int64 - Workspace ID (0 for default workspace).
        title: string - Public key title
        created_at: date-time - Public key created at date/time
        expires_at: date-time - Public key expiration date/time
        expired: boolean - Is this public key expired?
        fingerprint: string - Public key fingerprint (MD5)
        fingerprint_sha256: string - Public key fingerprint (SHA256)
        status: string - Only returned when generating keys. Can be invalid, not_generated, generating, complete
        last_login_at: date-time - Key's most recent login time via SFTP
        generated_private_key: string - Only returned when generating keys. Private key generated for the user.
        generated_public_key: string - Only returned when generating keys. Public key generated for the user.
        username: string - Username of the user this public key is associated with
        user_id: int64 - User ID this public key is associated with
        public_key: string - Actual contents of SSH key.
        generate_keypair: boolean - If true, generate a new SSH key pair. Can not be used with `public_key`
        generate_private_key_password: string - Password for the private key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        generate_algorithm: string - Type of key to generate. One of rsa, dsa, ecdsa, ed25519. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        generate_length: int64 - Length of key to generate. If algorithm is ecdsa, this is the signature size. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    """

    default_attributes = {
        "id": None,  # int64 - Public key ID
        "workspace_id": None,  # int64 - Workspace ID (0 for default workspace).
        "title": None,  # string - Public key title
        "created_at": None,  # date-time - Public key created at date/time
        "expires_at": None,  # date-time - Public key expiration date/time
        "expired": None,  # boolean - Is this public key expired?
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

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    title: str | None
    created_at: str | None
    expires_at: str | None
    expired: bool | None
    fingerprint: str | None
    fingerprint_sha256: str | None
    status: str | None
    last_login_at: str | None
    generated_private_key: str | None
    generated_public_key: str | None
    username: str | None
    user_id: int | None
    public_key: str | None
    generate_keypair: bool | None
    generate_private_key_password: str | None
    generate_algorithm: str | None
    generate_length: int | None

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
        for attribute, default_value in PublicKey.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PublicKey.default_attributes
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
          title (required) - string - Internal reference for key.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "title" not in params:
            raise MissingParameterError("Parameter missing: title")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/public_keys/" + path_value(params["id"]), params
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
            "DELETE", "/public_keys/" + path_value(params["id"]), params
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
            new_obj = PublicKeyResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class PublicKeyResource:
    """PublicKey operations that use one client's configuration.

    Get one from a client, such as ``client.public_key``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[PublicKey]:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `user_id`, `title` or `created_at`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at` and `workspace_id`. Valid field combinations are `[ workspace_id, created_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
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
        return ListObj(PublicKey, "GET", "/public_keys", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[PublicKey]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PublicKey:
        """Parameters:
        id (required) - int64 - Public Key ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> PublicKey:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/public_keys/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, PublicKey)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PublicKey:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PublicKey:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        title (required) - string - Internal reference for key.
        public_key - string - Actual contents of SSH key.
        generate_keypair - boolean - If true, generate a new SSH key pair. Can not be used with `public_key`
        generate_private_key_password - string - Password for the private key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        generate_algorithm - string - Type of key to generate.  One of rsa, dsa, ecdsa, ed25519. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        generate_length - int64 - Length of key to generate. If algorithm is ecdsa, this is the signature size. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        if "public_key" in params and not isinstance(
            params["public_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_key must be an str"
            )
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
        if "generate_length" in params and (
            not isinstance(params["generate_length"], int)
            or isinstance(params["generate_length"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: generate_length must be an int"
            )
        if "title" not in params:
            raise MissingParameterError("Parameter missing: title")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/public_keys", params)
        return operation.decode_model(response, PublicKey)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> PublicKey:
        """Parameters:
        title (required) - string - Internal reference for key.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> PublicKey:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "title" not in params:
            raise MissingParameterError("Parameter missing: title")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/public_keys/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, PublicKey)

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
            "DELETE", "/public_keys/" + path_value(params["id"]), params
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
    ) -> PublicKey:
        """A new PublicKey with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = PublicKey(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = PublicKeyResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[PublicKey]:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `user_id`, `title` or `created_at`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at` and `workspace_id`. Valid field combinations are `[ workspace_id, created_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[PublicKey]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PublicKey:
    """Parameters:
    id (required) - int64 - Public Key ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PublicKey:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PublicKey:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    title (required) - string - Internal reference for key.
    public_key - string - Actual contents of SSH key.
    generate_keypair - boolean - If true, generate a new SSH key pair. Can not be used with `public_key`
    generate_private_key_password - string - Password for the private key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    generate_algorithm - string - Type of key to generate.  One of rsa, dsa, ecdsa, ed25519. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    generate_length - int64 - Length of key to generate. If algorithm is ecdsa, this is the signature size. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> PublicKey:
    """Parameters:
    title (required) - string - Internal reference for key.
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


def new(*args, **kwargs) -> PublicKey:
    return PublicKey(*args, **kwargs)
