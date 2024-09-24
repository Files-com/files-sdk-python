import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class RemoteServerConfigurationFile:
    default_attributes = {
        "id": None,  # int64 - The remote server ID of the agent
        "permission_set": None,  # string - The permission set for the agent ['read_write', 'read_only', 'write_only']
        "private_key": None,  # string - The private key for the agent
        "subdomain": None,  # string - Files.com subdomain site name
        "root": None,  # string - The root directory for the agent
        "follow_links": None,  # boolean - Follow symlinks when traversing directories
        "prefer_protocol": None,  # string - Preferred network protocol ['udp', 'tcp'] (default udp)
        "dns": None,  # string - DNS lookup method ['auto','doh','system'] (default auto)
        "proxy_all_outbound": None,  # boolean - Proxy all outbound traffic through files.com proxy server
        "endpoint_override": None,  # string - Custom site endpoint URL
        "log_file": None,  # string - Log file name and location
        "log_level": None,  # string - Log level for the agent logs ['debug', 'info', 'warn', 'error', 'fatal'] (default info)
        "log_rotate_num": None,  # int64 - Log route for agent logs. (default 5)
        "log_rotate_size": None,  # int64 - Log route size in MB for agent logs. (default 20)
        "override_max_concurrent_jobs": None,  # int64 - Maximum number of concurrent jobs (default 500)
        "graceful_shutdown_timeout": None,  # int64 - Graceful shutdown timeout in seconds (default 15)
        "transfer_rate_limit": None,  # string - File transfer (upload/download) rate limit
        #  `<limit>-<period>`, with the given periods:
        # * 'S': second
        # * 'M': minute
        # * 'H': hour
        # * 'D': day
        # Examples:
        # * 5 requests/second: '5-S'
        # * 10 requests/minute: '10-M'
        # * 1000 requests/hour: '1000-H'
        # * 2000 requests/day: '2000-D'
        "api_token": None,  # string - Files Agent API Token
        "port": None,  # int64 - Incoming port for files agent connections
        "hostname": None,  # string
        "public_key": None,  # string - public key
        "status": None,  # string - either running or shutdown
        "server_host_key": None,  # string
        "config_version": None,  # string - agent config version
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
