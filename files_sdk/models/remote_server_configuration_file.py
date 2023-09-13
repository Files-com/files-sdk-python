import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class RemoteServerConfigurationFile:
    default_attributes = {
        "id": None,  # int64 - Agent ID
        "permission_set": None,  # string -
        "api_token": None,  # string - Files Agent API Token
        "root": None,  # string - Agent local root path
        "port": None,  # int64 - Incoming port for files agent connections
        "hostname": None,  # string
        "public_key": None,  # string - public key
        "private_key": None,  # string - private key
        "status": None,  # string - either running or shutdown
        "config_version": None,  # string - agent config version
        "server_host_key": None,  # string
        "subdomain": None,  # string
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
        ) in RemoteServerConfigurationFile.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in RemoteServerConfigurationFile.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return RemoteServerConfigurationFile(*args, **kwargs)
