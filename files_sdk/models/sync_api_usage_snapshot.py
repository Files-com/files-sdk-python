import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SyncApiUsageSnapshot:
    default_attributes = {
        "ifname": None,  # string - Interface Name
        "api_reads": None,  # int64 - API Reads
        "api_writes": None,  # int64 - API Writes
        "list_cache_hits": None,  # int64 - List Cache Hits
        "list_cache_misses": None,  # int64 - List Cache Misses
        "stat_cache_hits": None,  # int64 - Stat Cache Hits
        "stat_cache_misses": None,  # int64 - Stat Cache Misses
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
        ) in SyncApiUsageSnapshot.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SyncApiUsageSnapshot.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return SyncApiUsageSnapshot(*args, **kwargs)
