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


class SftpHostKey:
    """A sftp host key record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        active: boolean - If true, use this SFTP Host Key.
        custom_domain_id: int64 - Custom Domain ID. If set, this key is used only for that Custom Domain.
        id: int64 - SFTP Host Key ID
        name: string - The friendly name of this SFTP Host Key.
        key_type: string - SSH key type
        fingerprint_md5: string - MD5 Fingerprint of the public key
        fingerprint_sha256: string - SHA256 Fingerprint of the public key
        private_key: string - The private key data.
    """

    default_attributes = {
        "active": None,  # boolean - If true, use this SFTP Host Key.
        "custom_domain_id": None,  # int64 - Custom Domain ID. If set, this key is used only for that Custom Domain.
        "id": None,  # int64 - SFTP Host Key ID
        "name": None,  # string - The friendly name of this SFTP Host Key.
        "key_type": None,  # string - SSH key type
        "fingerprint_md5": None,  # string - MD5 Fingerprint of the public key
        "fingerprint_sha256": None,  # string - SHA256 Fingerprint of the public key
        "private_key": None,  # string - The private key data.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    active: bool | None
    custom_domain_id: int | None
    id: int | None
    name: str | None
    key_type: str | None
    fingerprint_md5: str | None
    fingerprint_sha256: str | None
    private_key: str | None

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
        for attribute, default_value in SftpHostKey.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SftpHostKey.default_attributes
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
          active - boolean - If true, use this SFTP Host Key.
          custom_domain_id - int64 - Custom Domain ID. If set, this key is used only for that Custom Domain.
          name - string - The friendly name of this SFTP Host Key.
          private_key - string - The private key data.
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
        if "active" in params and isinstance(
            params["active"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: active must be an bool"
            )
        if "custom_domain_id" in params and (
            not isinstance(params["custom_domain_id"], int)
            or isinstance(params["custom_domain_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: custom_domain_id must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/sftp_host_keys/" + path_value(params["id"]), params
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
            "DELETE", "/sftp_host_keys/" + path_value(params["id"]), params
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
            new_obj = SftpHostKeyResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class SftpHostKeyResource:
    """SftpHostKey operations that use one client's configuration.

    Get one from a client, such as ``client.sftp_host_key``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SftpHostKey]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            SftpHostKey, "GET", "/sftp_host_keys", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SftpHostKey]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SftpHostKey:
        """Parameters:
        id (required) - int64 - Sftp Host Key ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> SftpHostKey:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/sftp_host_keys/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, SftpHostKey)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SftpHostKey:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SftpHostKey:
        """Parameters:
        active - boolean - If true, use this SFTP Host Key.
        custom_domain_id - int64 - Custom Domain ID. If set, this key is used only for that Custom Domain.
        name - string - The friendly name of this SFTP Host Key.
        private_key - string - The private key data.
        """
        params = copy_params(params)
        if "active" in params and not isinstance(params["active"], bool):
            raise InvalidParameterError(
                "Bad parameter: active must be an bool"
            )
        if "custom_domain_id" in params and (
            not isinstance(params["custom_domain_id"], int)
            or isinstance(params["custom_domain_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: custom_domain_id must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/sftp_host_keys", params)
        return operation.decode_model(response, SftpHostKey)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SftpHostKey:
        """Parameters:
        active - boolean - If true, use this SFTP Host Key.
        custom_domain_id - int64 - Custom Domain ID. If set, this key is used only for that Custom Domain.
        name - string - The friendly name of this SFTP Host Key.
        private_key - string - The private key data.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> SftpHostKey:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "active" in params and not isinstance(params["active"], bool):
            raise InvalidParameterError(
                "Bad parameter: active must be an bool"
            )
        if "custom_domain_id" in params and (
            not isinstance(params["custom_domain_id"], int)
            or isinstance(params["custom_domain_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: custom_domain_id must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/sftp_host_keys/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, SftpHostKey)

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
            "DELETE", "/sftp_host_keys/" + path_value(params["id"]), params
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
    ) -> SftpHostKey:
        """A new SftpHostKey with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = SftpHostKey(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SftpHostKeyResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SftpHostKey]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SftpHostKey]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SftpHostKey:
    """Parameters:
    id (required) - int64 - Sftp Host Key ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SftpHostKey:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SftpHostKey:
    """Parameters:
    active - boolean - If true, use this SFTP Host Key.
    custom_domain_id - int64 - Custom Domain ID. If set, this key is used only for that Custom Domain.
    name - string - The friendly name of this SFTP Host Key.
    private_key - string - The private key data.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SftpHostKey:
    """Parameters:
    active - boolean - If true, use this SFTP Host Key.
    custom_domain_id - int64 - Custom Domain ID. If set, this key is used only for that Custom Domain.
    name - string - The friendly name of this SFTP Host Key.
    private_key - string - The private key data.
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


def new(*args, **kwargs) -> SftpHostKey:
    return SftpHostKey(*args, **kwargs)
