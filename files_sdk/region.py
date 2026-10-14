"""Regional relocation.

A site can require connections through one host, such as its custom domain
or a regional subdomain. Files.com then answers requests that reach another
host with HTTP 403, error type "not-authenticated/lockout-region-mismatch"
and the host to use, a bare host name or an https:// origin, in data.host
or in the X-Files-Host header. data.host is used whenever the answer has
one; the header only when its data names no host, and never with another
status or error type. Files.com's earlier plain-text answer, an HTTP 403
whose body starts exactly "You have connected to a URL", names the host in
the header alone; no other answer that is not JSON names one.

The SDK sends the operation to that host once, with the same request, when
all of these hold:

- The answer came straight from the API origin the client was configured
  with (or had already moved the operation to), over HTTPS with certificate
  verification. An answer reached through a redirect, from storage, or over
  plain HTTP or unverified TLS carries no such authority.
- The host is a DNS host name, optionally as an https:// origin with no
  path, and not the origin the request went to. It uses the default port and
  is not a local development name such as localhost or an IP address.
- The client's region_policy is "automatic" and its region_handler, if it
  has one, allows it.
- The request has a retry left: the move counts against the same
  max_network_retries as retries after failures.

The new host lasts for the rest of that operation, including the pages of a
list and the models it returns, and never changes the client.
"""

import dataclasses
import ipaddress
import re
from urllib.parse import urlsplit, urlunsplit

import idna

from files_sdk.error import InvalidParameterError

MISMATCH = "not-authenticated/lockout-region-mismatch"
HOST_HEADER = "X-Files-Host"
# How Files.com's plain-text mismatch answer starts, exactly.
PLAIN_MISMATCH = b"You have connected to a URL"

# Names that only resolve on a developer's machine or network. They need an
# explicit region_development_origins pair.
_LOCAL_SUFFIXES = (
    "localhost",
    "test",
    "local",
    "internal",
    "invalid",
    "example",
    "home.arpa",
)
_UNSAFE = re.compile(r"[\x00-\x20\x7f\\]")


@dataclasses.dataclass(frozen=True)
class RegionRelocation:
    """What a region_handler decides about.

    original_origin is the origin that answered, and target_origin the one
    its answer names, both as ``https://host`` or ``https://host:port``.
    automatic says whether the SDK would move the operation without a
    handler. The handler returns True to allow that, False or None to
    refuse it (the operation then raises the LockoutRegionMismatchError),
    or an origin to send the operation to instead, which it approves
    explicitly, even with a nondefault port. It is never given
    credentials.
    """

    original_origin: str
    target_origin: str
    automatic: bool
    reason: str = "lockout-region-mismatch"


class Origin(tuple[str, str, int]):
    """(scheme, host, port), with the host lowercased and ASCII."""

    def __new__(cls, scheme, host, port):
        return super().__new__(cls, (scheme, host, port))

    @property
    def scheme(self):
        return self[0]

    @property
    def host(self):
        return self[1]

    @property
    def port(self):
        return self[2]

    def __str__(self):
        default = 443 if self.scheme == "https" else 80
        host = "[{}]".format(self.host) if ":" in self.host else self.host
        if self.port == default:
            return "{}://{}".format(self.scheme, host)
        return "{}://{}:{}".format(self.scheme, host, self.port)

    @property
    def is_local(self):
        try:
            ipaddress.ip_address(self.host)
            return True
        except ValueError:
            pass
        host = self.host.rstrip(".")
        return "." not in host or any(
            host == suffix or host.endswith("." + suffix)
            for suffix in _LOCAL_SUFFIXES
        )


def origin_of(url) -> Origin:
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    port = parts.port or (443 if scheme == "https" else 80)
    return Origin(scheme, _ascii_host(parts.hostname or ""), port)


def _ascii_host(host):
    if not host or host.isascii():
        return host.lower()
    return idna.encode(host, uts46=True).decode("ascii")


def parse_origin(text, schemes=("https",)) -> Origin | None:
    """text as an origin with one of schemes, or None. An origin is a
    scheme, host and optional port, with no path beyond "/", user name,
    query or fragment."""
    if not isinstance(text, str) or not text or _UNSAFE.search(text):
        return None
    scheme, separator, rest = text.partition("://")
    if not separator or scheme.lower() not in schemes:
        return None
    return _host_and_port(scheme.lower(), rest)


def parse_target(host) -> tuple[Origin, bool] | None:
    """A named host as (origin, whether it named a port), or None if it is
    not a bare host name or an https:// origin."""
    if not isinstance(host, str) or not host or _UNSAFE.search(host):
        return None
    if "://" in host:
        origin = parse_origin(host)
        rest = host.partition("://")[2]
    else:
        origin = _host_and_port("https", host)
        rest = host
    if origin is None:
        return None
    return origin, ":" in rest.rstrip("/").rpartition("]")[2]


def _host_and_port(scheme, rest):
    if rest.endswith("/"):
        rest = rest[:-1]
    if not rest or any(character in rest for character in "/?#@"):
        return None
    try:
        parts = urlsplit("{}://{}".format(scheme, rest))
        port = parts.port
        host = _ascii_host(parts.hostname or "")
    except (ValueError, idna.IDNAError):
        return None
    if not host:
        return None
    return Origin(scheme, host, port or (443 if scheme == "https" else 80))


def development_origins(pairs) -> frozenset[tuple["Origin", "Origin"]]:
    """region_development_origins as a set of (source, destination) Origin
    pairs, each allowing an exact, possibly insecure, relocation."""
    checked: set[tuple[Origin, Origin]] = set()
    for pair in pairs or ():
        try:
            source, destination = pair
        except (TypeError, ValueError):
            raise InvalidParameterError(
                "region_development_origins must hold (source, destination) "
                "origin pairs"
            ) from None
        source_origin = parse_origin(source, ("http", "https"))
        destination_origin = parse_origin(destination, ("http", "https"))
        if source_origin is None or destination_origin is None:
            raise InvalidParameterError(
                "region_development_origins entries must be origins such as "
                "http://localhost:3000, without a path, user name or password"
            )
        checked.add((source_origin, destination_origin))
    return frozenset(checked)


def is_plain_mismatch(response):
    """Whether response, whose body is not JSON, is Files.com's plain-text
    region mismatch answer: HTTP 403 with text that starts exactly with
    PLAIN_MISMATCH, naming the host in its X-Files-Host header."""
    return (
        response.status_code == 403
        and response.content.startswith(PLAIN_MISMATCH)
        and bool(response.headers.get(HOST_HEADER))
    )


def _named_host(response):
    """What a region mismatch answer names as the host to use, or None. The
    structured answer names it in data.host, or, when its data names no
    host, in its X-Files-Host header; data that is not a JSON object names
    none. The plain-text answer (response.data None) names it only in the
    header."""
    body = response.data
    if body is None and is_plain_mismatch(response):
        return response.headers[HOST_HEADER]
    if (
        response.status_code != 403
        or not isinstance(body, dict)
        or body.get("type") != MISMATCH
    ):
        return None
    data = body.get("data")
    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None
    host = data.get("host")
    if host is None:
        host = response.headers.get(HOST_HEADER)
    return host


def is_mismatch(response):
    """Whether response, with its JSON body as data (None if it is not
    JSON), is Files.com's region mismatch answer, naming the host to use in
    its data or X-Files-Host header."""
    return _named_host(response) is not None


def relocation(context, response, *, trusted_issuer):
    """The base URL to send the rest of the operation to after response, or
    None to raise its error instead.

    trusted_issuer says whether response came straight from context's API
    origin over verified TLS. The region_handler, if any, may raise; its
    exception stops the operation.
    """
    host = _named_host(response)
    if host is None:
        return None
    if context.region_policy != "automatic":
        return None
    issuer = origin_of(context.base_url)
    parsed = parse_target(host)
    if parsed is None:
        return None
    target, named_port = parsed
    if target[1:] == issuer[1:]:
        return None

    development = next(
        (
            destination
            for source, destination in context.region_development_origins
            if source == issuer
            and destination.host == target.host
            and (not named_port or destination.port == target.port)
        ),
        None,
    )
    trusted = issuer.scheme == "https" and trusted_issuer
    automatic = trusted and target.port == 443 and not target.is_local
    destination = development or (target if automatic else None)

    handler = context.region_handler
    if handler is not None and (trusted or development is not None):
        decision = handler(
            RegionRelocation(str(issuer), str(target), destination is not None)
        )
        if isinstance(decision, str):
            approved = parse_origin(decision)
            if approved is None or not trusted:
                raise InvalidParameterError(
                    "region_handler returned text that is not an https origin "
                    "such as https://example.com"
                )
            destination = approved
        elif decision is not True:
            destination = None
    if destination is None:
        return None
    base = urlsplit(context.base_url)
    return urlunsplit(
        (
            destination.scheme,
            str(destination).partition("://")[2],
            base.path,
            "",
            "",
        )
    )
