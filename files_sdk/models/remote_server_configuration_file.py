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


class RemoteServerConfigurationFile:
    """A remote server configuration file record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - The remote server ID of the agent
        permission_set: string - The permission set for the agent ['read_write', 'read_only', 'write_only']
        private_key: string - The private key for the agent
        subdomain: string - Files.com subdomain site name
        root: string - The root directory for the agent
        node_name: string - Optional customer-facing name for this Agent installation
        follow_links: boolean - Follow symlinks when traversing directories
        prefer_protocol: string - Preferred network protocol ['udp', 'tcp'] (default udp)
        dns: string - DNS lookup method ['auto','doh','system'] (default auto)
        proxy_all_outbound: boolean - Proxy all outbound traffic through files.com proxy server
        endpoint_override: string - Custom site endpoint URL
        log_file: string - Log file name and location
        log_level: string - Log level for the agent logs ['debug', 'info', 'warn', 'error', 'fatal'] (default info)
        log_rotate_num: int64 - Log route for agent logs. (default 5)
        log_rotate_size: int64 - Log route size in MB for agent logs. (default 20)
        override_max_concurrent_jobs: int64 - Maximum number of concurrent jobs (default 500)
        graceful_shutdown_timeout: int64 - Graceful shutdown timeout in seconds (default 15)
        transfer_rate_limit: string - File transfer (upload/download) rate limit `<limit>-<period>`, with the given periods: * 'S': second * 'M': minute * 'H': hour * 'D': day Examples: * 5 requests/second: '5-S' * 10 requests/minute: '10-M' * 1000 requests/hour: '1000-H' * 2000 requests/day: '2000-D'
        auto_update_policy: string - Auto update policy ['manual_trigger', 'critical_only', 'always', 'never'] (default always)
    """

    default_attributes = {
        "id": None,  # int64 - The remote server ID of the agent
        "permission_set": None,  # string - The permission set for the agent ['read_write', 'read_only', 'write_only']
        "private_key": None,  # string - The private key for the agent
        "subdomain": None,  # string - Files.com subdomain site name
        "root": None,  # string - The root directory for the agent
        "node_name": None,  # string - Optional customer-facing name for this Agent installation
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
        "auto_update_policy": None,  # string - Auto update policy ['manual_trigger', 'critical_only', 'always', 'never'] (default always)
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    permission_set: str | None
    private_key: str | None
    subdomain: str | None
    root: str | None
    node_name: str | None
    follow_links: bool | None
    prefer_protocol: str | None
    dns: str | None
    proxy_all_outbound: bool | None
    endpoint_override: str | None
    log_file: str | None
    log_level: str | None
    log_rotate_num: int | None
    log_rotate_size: int | None
    override_max_concurrent_jobs: int | None
    graceful_shutdown_timeout: int | None
    transfer_rate_limit: str | None
    auto_update_policy: str | None

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
        ) in RemoteServerConfigurationFile.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in RemoteServerConfigurationFile.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> RemoteServerConfigurationFile:
    return RemoteServerConfigurationFile(*args, **kwargs)
