"""The HTTP transport: the Requests session a client sends through, and the
connection hooks that let an operation stop a request in flight.

A client either owns its session, which the SDK creates, or borrows one the
caller passed as http_session. An owned session sends through
CancellableAdapter. Each request runs in an Exchange, which records the
sockets of the connections the request leases from the adapter's pools, so
cancelling the operation can shut them down however far the request has got:
connecting through a proxy or TLS, sending the body, or waiting for or
reading the response. A borrowed session keeps its own adapters, so an
operation using it stops only between the steps it can see.

The hooks rely on urllib3's connection pools calling _get_conn and _put_conn
to lease and return a connection, and a connection calling _new_conn to open
its socket, as every urllib3 release the SDK supports does.
"""

import contextvars
import http.cookiejar
import socket
import ssl
import threading
import weakref
from contextlib import contextmanager
from typing import Any
from urllib.parse import urlsplit

import idna
import requests
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from requests.sessions import merge_hooks
from urllib3.connection import HTTPConnection, HTTPSConnection
from urllib3.connectionpool import HTTPConnectionPool, HTTPSConnectionPool
from urllib3.exceptions import NewConnectionError
from urllib3.util.retry import Retry

from files_sdk.error import APIConnectionError, InvalidRequestError
from files_sdk.lifetime import CancellationToken

# The headers that carry a Files.com credential or workspace. They go only
# to the API origin they were meant for.
FILES_AUTH_HEADERS = (
    "X-FilesAPI-Key",
    "X-FilesAPI-Auth",
    "X-Files-Workspace-Id",
)

# What an API request keeps when a redirect sends it to another origin.
# Everything else, such as Files.com credentials, the caller's extra
# headers and whatever the session added, stays behind.
_CROSS_ORIGIN_HEADERS = frozenset(
    {
        "user-agent",
        "accept",
        "accept-encoding",
        "connection",
        "content-type",
        "content-length",
        "transfer-encoding",
        "proxy-authorization",
    }
)


def url_origin(url):
    """The (scheme, host, port) that decides whether two URLs are the same
    origin."""
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    port = parts.port
    if port is None:
        port = 443 if scheme == "https" else 80
    return scheme, _ascii_host(parts.hostname or ""), port


def _ascii_host(host):
    """host as Requests sends it: lowercase, and IDNA-encoded if it is not
    ASCII."""
    if host.isascii():
        return host.lower()
    try:
        return idna.encode(host, uts46=True).decode("ascii")
    except idna.IDNAError:
        return host.lower()


# Errors that prove a request's bytes cannot have left: Requests refused
# the URL or a header, or the connection (or the proxy's) never opened.
_UNSENT_ERRORS = (
    requests.exceptions.ConnectTimeout,
    requests.exceptions.InvalidURL,
    requests.exceptions.InvalidSchema,
    requests.exceptions.MissingSchema,
    requests.exceptions.URLRequired,
    requests.exceptions.InvalidHeader,
)


def provably_unsent(error):
    """Whether error shows that nothing of its request was sent. Anything
    else that fails after a request was dispatched may have reached the
    server."""
    if isinstance(error, _UNSENT_ERRORS):
        return True
    # A connection error wraps urllib3's reason, which may wrap another:
    # a proxy error around the failed connection, or a certificate that
    # failed verification during the TLS handshake.
    cause = error
    for _ in range(4):
        cause = (
            getattr(cause, "reason", None)
            or getattr(cause, "original_error", None)
            or (cause.args[0] if getattr(cause, "args", None) else None)
        )
        if isinstance(
            cause, (NewConnectionError, ssl.SSLCertVerificationError)
        ):
            return True
        if cause is None or isinstance(cause, str):
            return False
    return False


def check_url(url):
    """Raise requests' InvalidURL unless url is an http or https URL
    without a user name or password."""
    parts = urlsplit(url)
    try:
        parts.port
    except ValueError:
        raise requests.exceptions.InvalidURL(
            "The URL has an invalid port"
        ) from None
    if parts.scheme.lower() not in ("http", "https") or not parts.hostname:
        raise requests.exceptions.InvalidURL(
            "Only http and https URLs with a host can be requested"
        )
    if "@" in parts.netloc:
        raise requests.exceptions.InvalidURL(
            "URLs with a user name or password cannot be requested"
        )


# The exchange whose request an owned adapter is sending on this thread.
_sending: contextvars.ContextVar["Exchange | None"] = contextvars.ContextVar(
    "files_sdk_sending", default=None
)


class Exchange:
    """The connections one request uses, so it can be stopped.

    A connection belongs to the exchange from when its pool leases it until
    the pool gets it back. For each socket such a connection opens or
    already has, the exchange keeps a duplicate handle. abort() shuts those
    sockets down, which makes a blocked send or receive on them fail at
    once, and marks the exchange so that its connections are closed rather
    than reused. Once a connection is returned, nothing this exchange does
    can reach it, so a late abort cannot touch another request's connection.
    """

    def __init__(self, source_address=None):
        self.source_address = source_address
        self._lock = threading.Lock()
        self._handles: dict[Any, socket.socket | None] = {}
        self._aborted = False
        self._interrupted = False
        self._ended = False
        self._completed = False
        self._leased = False
        self._connected = False
        # Set by Transport.send: whether a request was handed to the session
        # to send; whether the last one verified the server's certificate;
        # whether a redirect took the request to another origin; and whether
        # its socket timeouts were shortened to end at the operation's
        # deadline.
        self.dispatched = False
        self.verified = False
        self.left_origin = False
        self.deadline_bound = False

    @property
    def interrupted(self):
        """Whether abort() shut down a socket the request was using. Its
        outcome is then unknown: even a response that seemed to end
        normally may have been cut short."""
        return self._interrupted

    @property
    def connected(self):
        """Whether any socket was opened or reused."""
        return self._connected

    def may_have_sent(self, error):
        """Whether the request may have reached the server before error.
        A request never dispatched was not sent, and one whose connections
        the owned pools leased but never opened a socket for cannot have
        been. Otherwise only an error that proves it was not sent says so:
        a caller's session, or a SOCKS proxy's pools, give no other
        evidence."""
        if not self.dispatched or provably_unsent(error):
            return False
        return self._connected or not self._leased

    def finish(self):
        """Mark the response complete. Returns False if the operation had
        already been stopped, so its response must not be used."""
        with self._lock:
            if self._aborted:
                return False
            self._completed = True
            return True

    def bind(self, connection):
        """Take a connection its pool has just leased."""
        with self._lock:
            if self._ended:
                return
            self._leased = True
            connection._files_exchange = self
            self._handles.setdefault(connection, None)
            if connection.sock is not None:
                self._attach(connection, connection.sock)

    def attach(self, connection, sock):
        """Record the socket a bound connection has just opened."""
        with self._lock:
            if not self._ended and connection in self._handles:
                self._attach(connection, sock)

    def _attach(self, connection, sock):
        old = self._handles.get(connection)
        if old is not None:
            old.close()
        handle = socket.fromfd(sock.fileno(), sock.family, sock.type)
        self._handles[connection] = handle
        self._connected = True
        if self._aborted:
            self._interrupted = True
            _shut_down(handle)

    def release(self, connection):
        """Give back a connection its pool is taking back. An aborted
        exchange closes it, so the pool never reuses its socket."""
        with self._lock:
            handle = self._handles.pop(connection, None)
            if getattr(connection, "_files_exchange", None) is self:
                connection._files_exchange = None
            aborted = self._aborted
        if handle is not None:
            handle.close()
        if aborted:
            connection.close()

    def abort(self):
        """Stop the request: shut down every socket it is using now, and
        any it opens later."""
        with self._lock:
            if self._aborted or self._ended or self._completed:
                return
            self._aborted = True
            handles = [h for h in self._handles.values() if h is not None]
            # Mark the request first: the shutdown wakes its thread, which
            # must then see why its connection failed.
            self._interrupted = bool(handles)
            for handle in handles:
                _shut_down(handle)

    def end(self):
        """Forget every connection, once the request has settled."""
        with self._lock:
            self._ended = True
            handles = self._handles
            self._handles = {}
            for connection in handles:
                if getattr(connection, "_files_exchange", None) is self:
                    connection._files_exchange = None
        for handle in handles.values():
            if handle is not None:
                handle.close()


def _shut_down(handle):
    try:
        handle.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass  # The peer or the connection closed it already.


class _CancellableHTTPConnection(HTTPConnection):
    _files_exchange: Exchange | None = None

    def _new_conn(self):
        sock = super()._new_conn()
        exchange = self._files_exchange
        if exchange is not None:
            exchange.attach(self, sock)
        return sock


class _CancellableHTTPSConnection(_CancellableHTTPConnection, HTTPSConnection):
    pass


class _CancellableHTTPConnectionPool(HTTPConnectionPool):
    # urllib3 declares ConnectionCls with a protocol its own connection
    # classes do not satisfy for type checkers.
    ConnectionCls = (
        _CancellableHTTPConnection  # pyright: ignore[reportAssignmentType]
    )

    def _get_conn(self, timeout=None):
        connection = super()._get_conn(timeout)
        exchange = _sending.get()
        if exchange is not None:
            exchange.bind(connection)
        return connection

    def _put_conn(self, conn):
        exchange = getattr(conn, "_files_exchange", None)
        if exchange is not None:
            exchange.release(conn)
        super()._put_conn(conn)


class _CancellableHTTPSConnectionPool(
    _CancellableHTTPConnectionPool, HTTPSConnectionPool
):
    ConnectionCls = _CancellableHTTPSConnection


_CANCELLABLE_POOLS = {
    "http": _CancellableHTTPConnectionPool,
    "https": _CancellableHTTPSConnectionPool,
}


# Connections each owned pool keeps for reuse: upload.MAX_UPLOAD_CONCURRENCY.
# Reuse only: pools do not block (pool_block is False), so this admits no
# request and limits none; it lets connections opened for a large upload
# target be kept rather than closed after each request.
_POOL_SIZE = 1024


class CancellableAdapter(HTTPAdapter):
    """The adapter an owned session sends through.

    Its pools lease connections to the Exchange passed to send(), which
    Session.send forwards. It binds each request's connections to the
    exchange's source address, if it has one, and leaves retries to the
    SDK. SOCKS proxies use urllib3's own pools, so a request through one
    cannot be stopped while it waits on the network.
    """

    def __init__(self):
        # Keep as many connections to each host for reuse as one upload can
        # use at once.
        super().__init__(max_retries=0, pool_maxsize=_POOL_SIZE)
        # Every pool the adapter has handed a request, while anything refers
        # to it. The adapter owns them all, though each of its managers
        # keeps only the most recent few and drops the others unclosed.
        self._pools: weakref.WeakSet[HTTPConnectionPool] = weakref.WeakSet()
        self._pools_lock = threading.Lock()

    def init_poolmanager(
        self, connections, maxsize, block=False, **pool_kwargs
    ):
        super().init_poolmanager(connections, maxsize, block, **pool_kwargs)
        self.poolmanager.pool_classes_by_scheme = dict(_CANCELLABLE_POOLS)

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        manager = super().proxy_manager_for(proxy, **proxy_kwargs)
        if not proxy.lower().startswith("socks"):
            manager.pool_classes_by_scheme = dict(_CANCELLABLE_POOLS)
        return manager

    def build_connection_pool_key_attributes(self, request, verify, cert=None):
        host_params, pool_kwargs = (
            super().build_connection_pool_key_attributes(request, verify, cert)
        )
        exchange = _sending.get()
        if exchange is not None and exchange.source_address is not None:
            pool_kwargs["source_address"] = exchange.source_address
        return host_params, pool_kwargs

    def get_connection_with_tls_context(
        self, request, verify, proxies=None, cert=None
    ):
        # Every request gets its pool here: direct, through a proxy or
        # through a SOCKS proxy.
        pool = super().get_connection_with_tls_context(
            request, verify, proxies, cert
        )
        with self._pools_lock:
            self._pools.add(pool)
        return pool

    def send(
        self,
        request,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,
        proxies=None,
        exchange=None,
    ):
        sending = _sending.set(exchange)
        try:
            return super().send(
                request, stream, timeout, verify, cert, proxies
            )
        finally:
            _sending.reset(sending)

    def close(self):
        # urllib3 drops pools rather than closing them, both here and when
        # newer origins push them out of a manager, so their idle
        # connections stay open until the pools are garbage collected,
        # which a kept error's traceback can put off indefinitely. Close
        # every pool the adapter handed out that is still alive. The
        # transport closes its session only once its requests have settled,
        # so no request is using one.
        with self._pools_lock:
            pools = list(self._pools)
        super().close()
        for pool in pools:
            pool.close()


class _OwnedSession(requests.Session):
    """The session of an owned transport. Transport.send decides which
    credentials each redirect keeps, so this never looks one up in a .netrc
    file, as Requests would. It keeps no cookie a server sets, so nothing
    from one request's principal rides along with the next; Files.com
    authenticates each request by its headers. Cookies a caller adds to
    session.cookies are still sent."""

    def __init__(self):
        super().__init__()
        self.cookies.set_policy(_NoServerCookies())

    def rebuild_auth(self, prepared_request, response):
        pass


class _NoServerCookies(http.cookiejar.DefaultCookiePolicy):
    def set_ok(self, cookie, request):
        return False


class _NoNetrc(AuthBase):
    """Request authentication that adds nothing. Giving it to a request
    stops Requests from reading credentials from a .netrc file."""

    def __call__(self, r):
        return r


_NO_NETRC = _NoNetrc()


class Transport:
    """The Requests session a client, or the module facade, sends every
    request through, and whether the SDK owns it.

    closing is cancelled when the transport closes, which stops every
    operation that uses it.
    """

    def __init__(
        self,
        http_session: requests.Session | None = None,
        *,
        verify: bool | str = True,
        cert: str | tuple[str, str] | None = None,
        proxies: Any = None,
        trust_env: bool = True,
    ):
        self.owned = http_session is None
        if http_session is None:
            http_session = _OwnedSession()
            http_session.verify = verify
            http_session.cert = cert
            http_session.proxies = dict(proxies or {})
            http_session.trust_env = trust_env
            adapter = CancellableAdapter()
            http_session.mount("https://", adapter)
            http_session.mount("http://", adapter)
        self.session = http_session
        self.closing = CancellationToken()
        self._condition = threading.Condition()
        self._active: dict[Exchange, int] = {}
        self._closed = False

    @property
    def closed(self):
        return self.closing.cancelled

    def close(self):
        """Stop every operation using this transport. An owned transport
        also waits for their requests to settle and then closes its
        session. A borrowed session stays open."""
        with self._condition:
            if threading.get_ident() in self._active.values():
                raise RuntimeError(
                    "A client cannot be closed from inside one of its own "
                    "requests, such as from a download's destination "
                    "stream. Close it after the request returns."
                )
            first_close = not self._closed
            self._closed = True
        self.closing.cancel()
        if not self.owned:
            return
        with self._condition:
            self._condition.wait_for(lambda: not self._active)
        if first_close:
            self.session.close()

    @contextmanager
    def exchange(self, lifetime, source_address=None):
        """Run one request, with its redirects, in an Exchange that stops it
        when lifetime ends."""
        exchange = Exchange(source_address)
        with self._condition:
            lifetime.check("request")
            self._active[exchange] = threading.get_ident()
        stop_watching = lifetime.watch(exchange.abort)
        try:
            yield exchange
        finally:
            stop_watching()
            exchange.end()
            with self._condition:
                del self._active[exchange]
                self._condition.notify_all()

    def resends(self, url):
        """Whether the session's own adapter for url is set to retry
        requests, as a borrowed session's can be, so it could send a request
        again without the SDK knowing."""
        if self.owned:
            return False
        adapter = self.session.get_adapter(url)
        retries = getattr(adapter, "max_retries", None)
        if isinstance(adapter, CancellableAdapter) or not isinstance(
            retries, Retry
        ):
            return False
        return retries.total not in (0, False)

    def send(
        self,
        exchange,
        request,
        *,
        lifetime,
        open_timeout,
        read_timeout,
        max_redirects,
        api_origin=None,
    ):
        """Send request and follow its redirects. Returns the last response,
        with its body unread.

        An API request (api_origin set) is prepared by the session, so its
        headers, cookies, authentication and hooks apply. Once a redirect
        leaves api_origin, even if a later one returns, the request keeps
        only generic headers. A transfer request to a signed URL gets only
        the session's hooks, and a redirect to another origin drops what
        Requests adds for it. Neither sends credentials from a .netrc file.
        A redirect that would carry the request's body to another origin
        (a 307 or 308 of a request with one, such as an upload part or an
        API request with parameters) is not followed: the body goes only
        where the request was sent, which may have carried it out, so the
        error raised has remote_outcome_unknown set.
        """
        session = self.session
        check_url(request.url)
        if api_origin is None:
            # Only the session's hooks, which instrument requests without
            # adding credentials.
            request.hooks = merge_hooks(request.hooks, session.hooks)
            prepared = request.prepare()
            origin = url_origin(prepared.url)
        else:
            if session.auth is None and request.auth is None:
                request.auth = _NO_NETRC
            prepared = session.prepare_request(request)
            origin = api_origin
            # The session's authentication may change the prepared request,
            # as Requests allows, but not send the SDK's credentials to
            # another origin.
            check_url(prepared.url)
            if url_origin(prepared.url) != origin:
                raise InvalidRequestError(
                    "The http_session's authentication changed the request's "
                    "destination from {} to another origin. The SDK sends "
                    "Files.com credentials only to the client's base_url.".format(
                        "{}://{}:{}".format(*origin)
                    )
                )
        authorization = prepared.headers.get("Authorization")
        # A request only its own origin may answer, such as a download bound
        # to one version of a file: a redirect elsewhere is not followed.
        same_origin = getattr(request, "files_same_origin", False)
        left_origin = False

        response = self._send_hop(
            exchange, prepared, lifetime, open_timeout, read_timeout, "request"
        )
        if getattr(request, "files_no_redirect", False):
            # A request only its own resource may answer, such as a range of
            # a download that storage's own answer binds to a version: a
            # redirect is its answer, not followed.
            return response
        redirects = 0
        while response.is_redirect and response.next is not None:
            # Requests has read and closed the redirect and prepared the
            # next request from it, as it does to follow one itself.
            prepared = response.next
            redirects += 1
            if redirects > max_redirects:
                raise requests.exceptions.TooManyRedirects(
                    "Exceeded {} redirects.".format(max_redirects)
                )
            check_url(prepared.url)
            if same_origin and url_origin(prepared.url) != origin:
                # Raised before anything is sent there.
                raise APIConnectionError(
                    "File storage redirected the download to {}, another "
                    "origin than its URL's, where the version the download "
                    "requires cannot be enforced, so the redirect was not "
                    "followed.".format(
                        "{}://{}:{}".format(*url_origin(prepared.url))
                    )
                )
            left_origin = left_origin or url_origin(prepared.url) != origin
            exchange.left_origin = left_origin
            if left_origin and prepared.body is not None:
                # Requests keeps the body only for a 307 or 308. Raised
                # before anything is sent there, but after the request's own
                # origin had it and answered, so it may have taken effect.
                raise APIConnectionError(
                    "{} redirected a request that carries a body to {}, another "
                    "origin than its URL's, so the redirect was not followed: "
                    "the body is sent only where the request was.{}".format(
                        (
                            "Files.com"
                            if api_origin is not None
                            else "File storage"
                        ),
                        "{}://{}:{}".format(*url_origin(prepared.url)),
                        (
                            " What it asked for may still have happened there "
                            "(remote_outcome_unknown is True). Check whether it "
                            "took effect before repeating it."
                            if api_origin is not None
                            else ""
                        ),
                    ),
                    phase="response",
                    remote_outcome_unknown=True,
                )
            headers = prepared.headers
            if left_origin:
                for name in list(headers):
                    if api_origin is not None:
                        if name.lower() not in _CROSS_ORIGIN_HEADERS:
                            del headers[name]
                    elif name in FILES_AUTH_HEADERS or name.lower() in (
                        "authorization",
                        "cookie",
                    ):
                        del headers[name]
            else:
                # Keep the authorization the request started with, not
                # one Requests found in a .netrc file for the redirect.
                headers.pop("Authorization", None)
                if authorization is not None:
                    headers["Authorization"] = authorization
            response = self._send_hop(
                exchange,
                prepared,
                lifetime,
                open_timeout,
                read_timeout,
                "redirect",
            )
        return response

    def _send_hop(
        self, exchange, prepared, lifetime, open_timeout, read_timeout, phase
    ):
        session = self.session
        check_url(prepared.url)
        lifetime.check(phase)
        settings = session.merge_environment_settings(
            prepared.url, {}, True, None, None
        )
        timeout = (lifetime.bound(open_timeout), lifetime.bound(read_timeout))
        exchange.deadline_bound = timeout != (open_timeout, read_timeout)
        # As Requests decides: any false value, such as "" or None, turns
        # certificate verification off.
        exchange.verified = url_origin(prepared.url)[0] == "https" and bool(
            settings["verify"]
        )
        options: dict[str, Any] = {
            "allow_redirects": False,
            "timeout": timeout,
            **settings,
        }
        if isinstance(session.get_adapter(prepared.url), CancellableAdapter):
            options["exchange"] = exchange
        exchange.dispatched = True
        return session.send(prepared, **options)
