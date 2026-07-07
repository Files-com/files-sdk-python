import builtins  # noqa: F401
from decimal import Decimal
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SyncBandwidthSnapshot:
    __decimal_fields = {
        "sync_bytes_received",
        "sync_bytes_sent",
    }
    __decimal_array_fields = {}
    default_attributes = {
        "id": None,  # int64 - sync bandwidth snapshot ID
        "site_id": None,  # int64 - Site ID
        "sync_bytes_received": None,  # decimal - bytes received
        "sync_bytes_sent": None,  # decimal - bytes sent
        "created_at": None,  # date-time - sync bandwidth snapshot created at date/time
        "remote_server_id": None,  # int64 - ID for the remote server consuming sync bandwidth
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
        ) in SyncBandwidthSnapshot.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if (
                attribute in SyncBandwidthSnapshot.__decimal_fields
                and value is not None
            ):
                value = Decimal(str(value))
            if (
                attribute in SyncBandwidthSnapshot.__decimal_array_fields
                and value is not None
            ):
                value = [Decimal(str(v)) for v in (value or [])]
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SyncBandwidthSnapshot.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in list(attrs.keys()):
            if (
                k in SyncBandwidthSnapshot.__decimal_fields
                and attrs[k] is not None
            ):
                attrs[k] = str(attrs[k])
            if (
                k in SyncBandwidthSnapshot.__decimal_array_fields
                and attrs[k] is not None
            ):
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The SyncBandwidthSnapshot object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   remote_server_id (required) - int64 - ID for the remote server consuming sync bandwidth
#   sync_bytes_sent (required) - int64 - Sync bytes sent
#   sync_bytes_received (required) - int64 - Sync bytes received
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "remote_server_id" in params and not isinstance(
        params["remote_server_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: remote_server_id must be an int"
        )
    if "sync_bytes_sent" in params and not isinstance(
        params["sync_bytes_sent"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: sync_bytes_sent must be an int"
        )
    if "sync_bytes_received" in params and not isinstance(
        params["sync_bytes_received"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: sync_bytes_received must be an int"
        )
    if "remote_server_id" not in params:
        raise MissingParameterError("Parameter missing: remote_server_id")
    if "sync_bytes_sent" not in params:
        raise MissingParameterError("Parameter missing: sync_bytes_sent")
    if "sync_bytes_received" not in params:
        raise MissingParameterError("Parameter missing: sync_bytes_received")
    response, options = Api.send_request(
        "POST", "/sync_bandwidth_snapshots", params, options
    )
    return SyncBandwidthSnapshot(response.data, options)


def create_batch(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request(
        "POST", "/sync_bandwidth_snapshots/create_batch", params, options
    )
    return [
        SyncBandwidthSnapshot(entity_data, options)
        for entity_data in response.data
    ]


def new(*args, **kwargs):
    return SyncBandwidthSnapshot(*args, **kwargs)
