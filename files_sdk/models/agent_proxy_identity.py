import builtins  # noqa: F401
from files_sdk.models.agent_proxy_identity_result import (
    AgentProxyIdentityResult,
)
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AgentProxyIdentity:
    default_attributes = {
        "peer_id": None,  # string - Libp2p peer ID for this identity candidate.
        "endpoints": None,  # array(object) - Protocol-specific endpoints for this peer ID.
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
        ) in AgentProxyIdentity.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AgentProxyIdentity.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


# Parameters:
#   ips (required) - array(string) - One or more public IPv4 addresses to resolve
def lookup(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "ips" in params and not isinstance(params["ips"], builtins.list):
        raise InvalidParameterError("Bad parameter: ips must be an list")
    if "ips" not in params:
        raise MissingParameterError("Parameter missing: ips")
    response, options = Api.send_request(
        "POST", "/agent_proxy_identities/lookup", params, options
    )
    return [
        AgentProxyIdentityResult(entity_data, options)
        for entity_data in response.data
    ]


# Parameters:
#   private_ip (required) - string - Proxy private IPv4 address
#   peer_id (required) - string - Libp2p peer ID currently served by the proxy
def report(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "private_ip" in params and not isinstance(params["private_ip"], str):
        raise InvalidParameterError("Bad parameter: private_ip must be an str")
    if "peer_id" in params and not isinstance(params["peer_id"], str):
        raise InvalidParameterError("Bad parameter: peer_id must be an str")
    if "private_ip" not in params:
        raise MissingParameterError("Parameter missing: private_ip")
    if "peer_id" not in params:
        raise MissingParameterError("Parameter missing: peer_id")
    Api.send_request("POST", "/agent_proxy_identities/report", params, options)


def new(*args, **kwargs):
    return AgentProxyIdentity(*args, **kwargs)
