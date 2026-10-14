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


class PartnerConnection:
    """A partner connection record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Relationship ID used with DELETE /partner_sites/:id to disconnect.
        role: string - This Partner's role in this connection. A host shares local files with the connected site; a guest accesses files shared by the connected site.
        site_id: int64 - ID of the connected site.
        site_name: string - Name of the connected site.
        mount_path: string - File API path to the connected Host's mount on this site when role is guest. Null when role is host. File access remains subject to the caller's permissions and the Host Partner's grants.
    """

    default_attributes = {
        "id": None,  # int64 - Relationship ID used with DELETE /partner_sites/:id to disconnect.
        "role": None,  # string - This Partner's role in this connection. A host shares local files with the connected site; a guest accesses files shared by the connected site.
        "site_id": None,  # int64 - ID of the connected site.
        "site_name": None,  # string - Name of the connected site.
        "mount_path": None,  # string - File API path to the connected Host's mount on this site when role is guest. Null when role is host. File access remains subject to the caller's permissions and the Host Partner's grants.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    role: str | None
    site_id: int | None
    site_name: str | None
    mount_path: str | None

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
        ) in PartnerConnection.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PartnerConnection.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> PartnerConnection:
    return PartnerConnection(*args, **kwargs)
