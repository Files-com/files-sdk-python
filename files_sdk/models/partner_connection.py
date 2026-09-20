import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PartnerConnection:
    default_attributes = {
        "id": None,  # int64 - Relationship ID used with DELETE /partner_sites/:id to disconnect.
        "role": None,  # string - This Partner's role in this connection. A host shares local files with the connected site; a guest accesses files shared by the connected site.
        "site_id": None,  # int64 - ID of the connected site.
        "site_name": None,  # string - Name of the connected site.
        "mount_path": None,  # string - File API path to the connected Host's mount on this site when role is guest. Null when role is host. File access remains subject to the caller's permissions and the Host Partner's grants.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

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


def new(*args, **kwargs):
    return PartnerConnection(*args, **kwargs)
