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
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class DirectConnectionInfo:
    """A direct connection info record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        version: int64 - Direct connection information schema version.
        server_name: string - TLS server name (SNI and Host header) for the Agent's direct transfer listener.
        addresses: array(string) - Validated ip:port candidates that may be dialed over TCP+TLS for this transfer.
        direct_uri: string - Signed HTTPS URI for direct Agent transfer traffic.
        ca_pem: string - PEM-encoded CA certificate used to verify the Agent's direct transfer TLS certificate.
    """

    default_attributes = {
        "version": None,  # int64 - Direct connection information schema version.
        "server_name": None,  # string - TLS server name (SNI and Host header) for the Agent's direct transfer listener.
        "addresses": None,  # array(string) - Validated ip:port candidates that may be dialed over TCP+TLS for this transfer.
        "direct_uri": None,  # string - Signed HTTPS URI for direct Agent transfer traffic.
        "ca_pem": None,  # string - PEM-encoded CA certificate used to verify the Agent's direct transfer TLS certificate.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    version: int | None
    server_name: str | None
    addresses: builtins.list[str] | None
    direct_uri: str | None
    ca_pem: str | None

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
        for (
            attribute,
            default_value,
        ) in DirectConnectionInfo.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in DirectConnectionInfo.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> DirectConnectionInfo:
    return DirectConnectionInfo(*args, **kwargs)
