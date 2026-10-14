import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.context import checked_options
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
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Session:
    """A session record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: string - Session ID
        language: string - Session language
        read_only: boolean - Is this session read only?
        sftp_insecure_ciphers: boolean - Are insecure SFTP ciphers allowed for this user? (If this is set to true, the site administrator has signaled that it is ok to use less secure SSH ciphers for this user.)
        username: string - Username to sign in as
        password: string - Password for sign in
        otp: string - If this user has a 2FA device, provide its OTP or code here.
        partial_session_id: string - Identifier for a partially-completed login
    """

    default_attributes = {
        "id": None,  # string - Session ID
        "language": None,  # string - Session language
        "read_only": None,  # boolean - Is this session read only?
        "sftp_insecure_ciphers": None,  # boolean - Are insecure SFTP ciphers allowed for this user? (If this is set to true, the site administrator has signaled that it is ok to use less secure SSH ciphers for this user.)
        "username": None,  # string - Username to sign in as
        "password": None,  # string - Password for sign in
        "otp": None,  # string - If this user has a 2FA device, provide its OTP or code here.
        "partial_session_id": None,  # string - Identifier for a partially-completed login
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: str | None
    language: str | None
    read_only: bool | None
    sftp_insecure_ciphers: bool | None
    username: str | None
    password: str | None
    otp: str | None
    partial_session_id: str | None

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
        for attribute, default_value in Session.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Session.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def destroy(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Log out this session. The request always authenticates as this
        session, through the client that made it, whatever credentials
        options name."""
        if not self.id:
            raise MissingParameterError("Current object doesn't have a id")
        options = {
            name: value
            for name, value in checked_options(options).items()
            if name not in ("api_key", "session_id", "session", "client")
        }
        options["session_id"] = self.id
        SessionResource(self._scope()).delete(params, options)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns. One that already has an id cannot be updated, and raises
        NotImplementedError."""
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The Session object doesn't support updates."
            )
        else:
            new_obj = SessionResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class SessionResource:
    """Session operations that use one client's configuration.

    Get one from a client, such as ``client.session``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Session:
        """Parameters:
        username - string - Username to sign in as
        password - string - Password for sign in
        otp - string - If this user has a 2FA device, provide its OTP or code here.
        partial_session_id - string - Identifier for a partially-completed login
        """
        params = copy_params(params)
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError(
                "Bad parameter: username must be an str"
            )
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "otp" in params and not isinstance(params["otp"], str):
            raise InvalidParameterError("Bad parameter: otp must be an str")
        if "partial_session_id" in params and not isinstance(
            params["partial_session_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: partial_session_id must be an str"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/sessions", params)
        return operation.decode_model(response, Session)

    def delete(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        params = copy_params(params)
        operation = Operation.start(self._scope, options)
        operation.request("DELETE", "/sessions", params)

    def destroy(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Session:
        """A new Session with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Session(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SessionResource(LEGACY)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Session:
    """Parameters:
    username - string - Username to sign in as
    password - string - Password for sign in
    otp - string - If this user has a 2FA device, provide its OTP or code here.
    partial_session_id - string - Identifier for a partially-completed login
    """
    return _legacy_resource.create(params, options)


def delete(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(params, options)


def destroy(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(params, options)


def new(*args, **kwargs) -> Session:
    return Session(*args, **kwargs)
