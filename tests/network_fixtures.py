"""Loopback servers that misbehave on purpose.

They stall, trickle or stop reading, speak TLS with a throwaway certificate
authority, or act as a CONNECT proxy, so tests can stop the SDK's requests
while they wait on the network and see what reached the other side.
"""

import os
import shutil
import socket
import ssl
import subprocess
import tempfile
import threading
import time
import unittest

WAIT = 10  # Seconds a fixture waits for something that should be prompt.

# Every test certificate names these hosts. Tests reach the example names
# through CONNECT proxies, never DNS.
TLS_HOSTS = (
    "localhost",
    "app.example.com",
    "eu.example.com",
    "custom.example.net",
)


class Peer:
    """One accepted connection, as a server script sees it."""

    def __init__(self, sock, record):
        self.sock = sock
        self.record = record
        self._buffer = b""

    def read_head(self):
        """Read a request or response head up to its blank line. Returns
        (first line, headers with lower-case names)."""
        while b"\r\n\r\n" not in self._buffer:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("closed before the head ended")
            self._buffer += chunk
        head, self._buffer = self._buffer.split(b"\r\n\r\n", 1)
        first, *lines = head.decode("latin-1").split("\r\n")
        headers = {}
        for line in lines:
            name, _, value = line.partition(":")
            headers[name.strip().lower()] = value.strip()
        self.record.request_line = first
        self.record.headers = headers
        return first, headers

    def read_body(self, length):
        while len(self._buffer) < length:
            chunk = self.sock.recv(65536)
            if not chunk:
                break
            self._buffer += chunk
        body, self._buffer = self._buffer[:length], self._buffer[length:]
        return body

    def read_request(self):
        """Read one whole request: (request line, headers, body)."""
        first, headers = self.read_head()
        body = self.read_body(int(headers.get("content-length") or 0))
        self.record.body = body
        return first, headers, body

    def send(self, data):
        self.sock.sendall(data)

    def respond(self, status=200, body=b"", headers=None):
        lines = ["HTTP/1.1 {} Status".format(status)]
        for name, value in {
            "Content-Length": str(len(body)),
            **(headers or {}),
        }.items():
            lines.append("{}: {}".format(name, value))
        self.send("\r\n".join(lines).encode() + b"\r\n\r\n" + body)

    def wait_for_close(self, timeout=WAIT):
        """Read and discard until the client closes the connection. Returns
        whether it did within timeout."""
        self.sock.settimeout(timeout)
        try:
            while self.sock.recv(65536):
                pass
        except socket.timeout:
            return False
        except OSError:
            pass  # A reset also means the client let go.
        self.record.closed_at = time.monotonic()
        self.record.closed.set()
        return True


class ConnectionRecord:
    def __init__(self):
        self.accepted_at = time.monotonic()
        self.request_line = None
        self.headers = None
        self.body = None
        self.received = threading.Event()
        self.closed = threading.Event()
        self.closed_at = None


class ScriptedServer:
    """A loopback server that runs script(peer) for each connection it
    accepts, in its own thread. With tls, each connection is a TLS
    connection presenting the fixture certificate. stop() closes every
    connection and waits for its thread; a connection accepted as the
    server stops is closed without being served."""

    def __init__(self, test_case, script, tls=None):
        self.script = script
        self.tls = tls
        self.connections: list[ConnectionRecord] = []
        self._listener = socket.create_server(("127.0.0.1", 0))
        self.port = self._listener.getsockname()[1]
        self._threads = []
        self._sockets = []
        # Held while a connection is taken on, its thread started, and while
        # stop() begins: stop() sees each connection with its thread running,
        # and none is taken on after it.
        self._lock = threading.Lock()
        self._stopped = False
        accept = threading.Thread(target=self._accept, daemon=True)
        accept.start()
        test_case.addCleanup(self.stop)

    def url(self, path="/", host="127.0.0.1"):
        scheme = "https" if self.tls else "http"
        return "{}://{}:{}{}".format(scheme, host, self.port, path)

    def wait_for_connections(self, count, timeout=WAIT):
        deadline = time.monotonic() + timeout
        while len(self.connections) < count and time.monotonic() < deadline:
            time.sleep(0.005)
        return self.connections

    def _accept(self):
        while True:
            try:
                sock, _address = self._listener.accept()
            except OSError:
                return
            with self._lock:
                if self._stopped:
                    sock.close()
                    return
                record = ConnectionRecord()
                self.connections.append(record)
                self._sockets.append(sock)
                thread = threading.Thread(
                    target=self._serve, args=(sock, record), daemon=True
                )
                thread.start()
                self._threads.append(thread)

    def _serve(self, sock, record):
        try:
            if self.tls is not None:
                sock = self.tls.server_context().wrap_socket(
                    sock, server_side=True
                )
            self.script(Peer(sock, record))
        except (OSError, ConnectionError, ssl.SSLError):
            pass
        finally:
            record.closed.set()
            try:
                sock.close()
            except OSError:
                pass

    def stop(self):
        with self._lock:
            self._stopped = True
        self._listener.close()
        for sock in self._sockets:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        for thread in self._threads:
            thread.join(WAIT)


class ConnectProxy:
    """A CONNECT proxy to the loopback interface, which records the targets
    it is asked for. routes maps a "host:port" target to a loopback port;
    target_port takes any other target. With stall, it accepts CONNECT
    requests but never answers them."""

    def __init__(self, test_case, target_port=None, stall=False, routes=None):
        self.target_port = target_port
        self.routes = dict(routes or {})
        self.stall = stall
        self.targets = []
        self.server = ScriptedServer(test_case, self._tunnel)
        self.url = "http://127.0.0.1:{}".format(self.server.port)

    def _tunnel(self, peer):
        first, _headers = peer.read_head()
        target = first.split()[1]
        self.targets.append(target)
        peer.record.received.set()
        port = self.routes.get(target, self.target_port)
        if self.stall or port is None:
            peer.wait_for_close()
            return
        with socket.create_connection(("127.0.0.1", port)) as upstream:
            peer.send(b"HTTP/1.1 200 Connection established\r\n\r\n")
            leftover = peer._buffer
            if leftover:
                upstream.sendall(leftover)
            pump = threading.Thread(
                target=_pump, args=(upstream, peer.sock), daemon=True
            )
            pump.start()
            _pump(peer.sock, upstream)
            pump.join(WAIT)
        peer.record.closed_at = time.monotonic()


def _pump(source, destination):
    try:
        while True:
            chunk = source.recv(65536)
            if not chunk:
                break
            destination.sendall(chunk)
    except OSError:
        pass
    for sock in (source, destination):
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass


class TestAuthority:
    """A throwaway certificate authority and a server certificate for
    TLS_HOSTS, made with the openssl command on PATH in a temporary
    directory. The commands name the key encoding and digest rather than
    rely on each tool's defaults (checked with OpenSSL 3.6.3 and the
    LibreSSL 3.3.6 that macOS ships), and create() fails, naming the
    openssl used, if this Python's ssl module cannot use the result."""

    def __init__(self, directory):
        self.directory = directory
        self.ca = os.path.join(directory, "ca.pem")
        self.cert = os.path.join(directory, "server.pem")
        self.key = os.path.join(directory, "server-key.pem")

    def server_context(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(self.cert, self.key)
        return context

    @classmethod
    def create(cls, test_case):
        openssl = shutil.which("openssl")
        if openssl is None:
            raise unittest.SkipTest("TLS tests need the openssl command")
        directory = tempfile.mkdtemp()
        test_case.addCleanup(shutil.rmtree, directory, True)
        authority = cls(directory)
        names = ", ".join(
            ["IP:127.0.0.1"] + ["DNS:" + host for host in TLS_HOSTS]
        )
        _write(directory, "ca.cnf", _CA_CONFIG)
        _write(directory, "server.cnf", _SERVER_EXTENSIONS + names + "\n")

        def run(*args):
            try:
                subprocess.run(
                    [openssl, *args],
                    cwd=directory,
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as error:
                raise RuntimeError(
                    f"{openssl} could not make the test certificates: "
                    + error.stderr.decode(errors="replace").strip()
                ) from None

        # A named curve and SHA-256: OpenSSL 3 refuses explicit curve
        # parameters and, at its default security level, SHA-1 signatures.
        key = (
            "-newkey",
            "ec",
            "-pkeyopt",
            "ec_paramgen_curve:prime256v1",
            "-pkeyopt",
            "ec_param_enc:named_curve",
            "-nodes",
            "-sha256",
        )
        run(
            "req",
            "-x509",
            *key,
            "-keyout",
            "ca-key.pem",
            "-out",
            "ca.pem",
            "-days",
            "2",
            "-config",
            "ca.cnf",
        )
        run(
            "req",
            *key,
            "-keyout",
            "server-key.pem",
            "-out",
            "server.csr",
            "-subj",
            "/CN=localhost",
        )
        run(
            "x509",
            "-req",
            "-in",
            "server.csr",
            "-CA",
            "ca.pem",
            "-CAkey",
            "ca-key.pem",
            "-CAcreateserial",
            "-out",
            "server.pem",
            "-sha256",
            "-days",
            "2",
            "-extfile",
            "server.cnf",
        )
        authority._check(openssl)
        return authority

    def _check(self, openssl):
        """Fail now, naming the openssl that made them, unless this Python's
        ssl module completes a handshake with these certificates; otherwise
        the TLS tests would fail later as unexplained connection errors."""
        client_in, client_out, server_in, server_out = (
            ssl.MemoryBIO() for _ in range(4)
        )
        try:
            client = ssl.create_default_context(cafile=self.ca).wrap_bio(
                client_in, client_out, server_hostname="localhost"
            )
            server = self.server_context().wrap_bio(
                server_in, server_out, server_side=True
            )
            # Each end reads what the other wrote.
            ends = (
                (client, client_out, server_in),
                (server, server_out, client_in),
            )
            pending = {client, server}
            for _ in range(10):
                for end, written, peer_reads in ends:
                    if end in pending:
                        try:
                            end.do_handshake()
                            pending.discard(end)
                        except ssl.SSLWantReadError:
                            pass
                    peer_reads.write(written.read())
                if not pending:
                    return
            raise ssl.SSLError("the handshake did not finish")
        except ssl.SSLError as error:
            raise RuntimeError(
                f"The test certificates {openssl} made do not work with "
                f"{ssl.OPENSSL_VERSION}: {error}. Put an openssl that makes "
                "named-curve SHA-256 certificates first on PATH."
            ) from None


def _write(directory, name, text):
    with open(os.path.join(directory, name), "w", encoding="utf-8") as file:
        file.write(text)


_CA_CONFIG = """[req]
distinguished_name = dn
x509_extensions = ca
prompt = no
[dn]
CN = files_sdk test CA
[ca]
basicConstraints = critical, CA:TRUE
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash
"""

_SERVER_EXTENSIONS = """basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid
subjectAltName = """
