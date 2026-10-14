import unittest
import warnings

import files_sdk
import requests
from files_sdk.api import Operation
from files_sdk.api_client import ApiClient
from files_sdk.error import (
    APIConnectionError,
    APIError,
    InvalidParameterError,
    LockoutRegionMismatchError,
)
from tests.loopback_api import start_loopback_api
from tests.network_fixtures import ConnectProxy, TestAuthority
from urllib3.exceptions import InsecureRequestWarning

MISMATCH = "not-authenticated/lockout-region-mismatch"
# Files.com's earlier answer, not JSON, which names the host in a header alone.
PLAIN = b"You have connected to a URL that has different security settings than those required for your site."
NAMED = {"Content-Type": "text/plain", "X-Files-Host": "eu.example.com"}


def mismatch(host=None, error_type=MISMATCH):
    body = {
        "type": error_type,
        "http-code": 403,
        "title": "Lockout Region Mismatch",
        "error": "Use another host.",
    }
    if host is not None:
        body["data"] = {"host": host}
    return body


class TestRegionalRelocation(unittest.TestCase):
    """The site's configured API host, answering over verified TLS, can
    send one operation to the host the site requires. The test hosts are
    reached through a CONNECT proxy, never DNS."""

    def setUp(self):
        self.authority = TestAuthority.create(self)
        self.issuer = start_loopback_api(self, tls=self.authority)
        self.region = start_loopback_api(self, tls=self.authority)
        self.proxy = ConnectProxy(
            self,
            routes={
                "app.example.com:443": self.issuer.port,
                "eu.example.com:443": self.region.port,
                "eu.example.com:8443": self.region.port,
                "custom.example.net:443": self.region.port,
            },
        )

    def client(self, **settings):
        client = files_sdk.Client(
            api_key="sitekey",
            base_url="https://app.example.com",
            verify=self.authority.ca,
            proxies={"https": self.proxy.url},
            **settings,
        )
        self.addCleanup(client.close)
        return client

    def test_a_verified_mismatch_moves_one_operation_and_the_objects_it_returns(
        self,
    ):
        client = self.client()
        self.issuer.reply_json(
            mismatch("eu.example.com"),
            status=403,
            headers={"X-Files-Host": "eu.example.com"},
        )
        self.region.reply_json({"id": 1, "name": "Pat"})
        self.region.reply_json({"id": 1, "name": "Robin"})
        self.issuer.reply_json({"id": 2})

        user = client.user.find(1)
        user.update({"name": "Robin"})
        client.user.find(2)

        first, later = self.issuer.requests
        found, updated = self.region.requests
        self.assertEqual(["/users/1", "/users/2"], [first.path, later.path])
        self.assertEqual(
            [("GET", "/users/1"), ("PATCH", "/users/1")],
            [(r.method, r.path) for r in (found, updated)],
        )
        for request in (found, updated):
            self.assertEqual("sitekey", request.headers["X-FilesAPI-Key"])
        self.assertEqual("Robin", user.name)

    def test_the_host_can_be_named_by_the_header_alone_but_data_host_comes_first(
        self,
    ):
        for body, header, target in (
            (mismatch(None), "eu.example.com", "eu.example.com:443"),
            (
                {**mismatch(None), "data": {"host": None}},
                "https://eu.example.com",
                "eu.example.com:443",
            ),
            (
                mismatch("custom.example.net"),
                "eu.example.com",
                "custom.example.net:443",
            ),
        ):
            with self.subTest(body=body.get("data"), header=header):
                self.issuer.reply_json(
                    body, status=403, headers={"X-Files-Host": header}
                )
                self.region.reply_json([])

                self.client().user.list()

                self.assertEqual(target, self.proxy.targets[-1])
                self.assertEqual(
                    ["/users"],
                    [request.path for request in self.region.requests],
                )
                self.region.requests.clear()

    def test_full_https_origins_and_custom_domains_are_followed(self):
        client = self.client()
        for host, target in (
            ("https://custom.example.net/", "custom.example.net:443"),
            ("https://EU.example.com", "eu.example.com:443"),
        ):
            with self.subTest(host=host):
                self.issuer.reply_json(mismatch(host), status=403)
                self.region.reply_json([])

                client.user.list()

                self.assertEqual(target, self.proxy.targets[-1])
                self.assertEqual(1, len(self.region.requests))
                self.region.requests.clear()

    def test_answers_without_that_authority_raise_the_mismatch_error(self):
        client = self.client()
        for body in (
            mismatch(None),
            mismatch({"nested": "eu.example.com"}),
            mismatch(""),
            mismatch("https://user@eu.example.com"),
            mismatch("https://eu.example.com/other/path"),
            mismatch("https://eu.example.com?next=1"),
            mismatch("http://eu.example.com"),
            mismatch("eu.example.com:8443"),
            mismatch("127.0.0.1"),
            mismatch("files.localhost"),
            mismatch("eu.example.com\\@evil.example"),
            mismatch("app.example.com"),
            mismatch("https://["),
        ):
            with self.subTest(host=body.get("data")):
                self.issuer.reply_json(body, status=403)

                with self.assertRaises(LockoutRegionMismatchError) as caught:
                    client.user.list()

                self.assertEqual(body.get("data"), caught.exception.data)
        named = {"X-Files-Host": "eu.example.com"}
        for status, body, headers in (
            # A host in data.host is used even when it cannot be followed.
            (403, mismatch("http://eu.example.com"), named),
            (403, {**mismatch(None), "data": "eu.example.com"}, named),
            (403, mismatch(None), {"X-Files-Host": "eu.example.com:8443"}),
            # Only Files.com's 403 answer relocates.
            (401, mismatch(None), named),
        ):
            with self.subTest(
                status=status, data=body.get("data"), headers=headers
            ):
                self.issuer.reply_json(body, status=status, headers=headers)

                with self.assertRaises(LockoutRegionMismatchError):
                    client.user.list()
        self.issuer.reply_json(
            mismatch("eu.example.com", "not-authenticated/lockout-region"),
            status=403,
        )
        with self.assertRaises(APIError):
            client.user.list()
        self.issuer.reply_json(
            mismatch(None, "not-authenticated/invalid-api-key"),
            status=403,
            headers=named,
        )
        with self.assertRaises(APIError) as caught:
            client.user.list()
        self.assertNotIsInstance(caught.exception, LockoutRegionMismatchError)
        self.assertEqual([], self.region.requests)

    def test_the_plain_text_mismatch_names_the_host_in_its_header_alone(self):
        self.issuer.reply(403, PLAIN, NAMED)
        self.region.reply_json([])

        self.client().user.list()

        self.assertEqual("eu.example.com:443", self.proxy.targets[-1])
        self.assertEqual(
            ["/users"], [request.path for request in self.issuer.requests]
        )
        self.assertEqual(
            [("/users", "sitekey")],
            [
                (request.path, request.headers["X-FilesAPI-Key"])
                for request in self.region.requests
            ],
        )
        # No other answer that is not JSON names a host.
        for status, body, headers in (
            (403, PLAIN.replace(b"You", b"you", 1), NAMED),
            (403, b"Forbidden", NAMED),
            (403, PLAIN, {"Content-Type": "text/plain"}),
            (403, PLAIN, {**NAMED, "X-Files-Host": ""}),
            (401, PLAIN, NAMED),
        ):
            with self.subTest(status=status, body=body[:16], headers=headers):
                self.issuer.reply(status, body, headers)

                with self.assertRaises(APIConnectionError):
                    self.client().user.list()
                self.assertEqual(1, len(self.region.requests))

    def test_the_plain_text_mismatch_moves_an_operation_only_as_the_structured_one_does(
        self,
    ):
        # Refused, it is the mismatch error, with what the answer said.
        self.issuer.reply(403, PLAIN, NAMED)
        with self.assertRaises(LockoutRegionMismatchError) as caught:
            self.client(region_policy="disabled").user.list()
        error = caught.exception
        self.assertEqual(
            (403, None, None),
            (error.http_status, error.error_type, error.data),
        )
        self.assertEqual(
            (PLAIN.decode(), "eu.example.com"),
            (error.http_body, error.headers["X-Files-Host"]),
        )
        self.assertEqual("HTTP 403 " + PLAIN.decode(), str(error))
        # The move is one of the request's retries.
        self.issuer.reply(403, PLAIN, NAMED)
        with self.assertRaises(LockoutRegionMismatchError) as caught:
            self.client(max_network_retries=0).user.list()
        self.assertIn(
            "max_network_retries", "\n".join(caught.exception.__notes__)
        )
        # Never a second move.
        self.issuer.reply(403, PLAIN, NAMED)
        self.region.reply(
            403, PLAIN, {**NAMED, "X-Files-Host": "custom.example.net"}
        )
        with self.assertRaises(LockoutRegionMismatchError):
            self.client().user.list()
        self.assertEqual("eu.example.com:443", self.proxy.targets[-1])
        # Never from an answer reached through a redirect.
        self.issuer.reply(
            302,
            headers={
                "Location": "https://custom.example.net/api/rest/v1/users"
            },
        )
        self.region.reply(403, PLAIN, NAMED)
        with self.assertRaises(LockoutRegionMismatchError):
            self.client().user.list()
        self.assertEqual("custom.example.net:443", self.proxy.targets[-1])
        self.assertEqual(2, len(self.region.requests))

    def test_a_second_mismatch_raises_instead_of_moving_again(self):
        client = self.client()
        self.issuer.reply_json(mismatch("eu.example.com"), status=403)
        self.region.reply_json(mismatch("custom.example.net"), status=403)

        with self.assertRaises(LockoutRegionMismatchError):
            client.user.list()

        self.assertEqual(
            (1, 1), (len(self.issuer.requests), len(self.region.requests))
        )

    def test_moving_to_the_site_s_host_uses_the_request_s_retry_budget(self):
        busy = {"type": "processing-failure/unknown", "error": "Busy."}
        for retries, issuer_answers, region_answers, error_class in (
            # No retries: one attempt, and the named host is not tried.
            (
                0,
                [(403, mismatch("eu.example.com"))],
                [],
                LockoutRegionMismatchError,
            ),
            # A failure used the only retry before the mismatch arrived.
            (
                1,
                [(503, busy), (403, mismatch("eu.example.com"))],
                [],
                LockoutRegionMismatchError,
            ),
            # The move uses the last retry, so a failure there is final.
            (
                2,
                [(503, busy), (403, mismatch("eu.example.com"))],
                [(503, busy)],
                APIError,
            ),
        ):
            with self.subTest(retries=retries):
                for status, body in issuer_answers:
                    self.issuer.reply_json(body, status=status)
                for status, body in region_answers:
                    self.region.reply_json(body, status=status)
                self.region.reply_json(
                    []
                )  # What a further retry there would get.
                client = self.client(
                    max_network_retries=retries, initial_network_retry_delay=0
                )

                with self.assertRaises(error_class) as caught:
                    client.user.list()

                self.assertEqual(
                    len(issuer_answers), len(self.issuer.requests)
                )
                self.assertEqual(
                    len(region_answers), len(self.region.requests)
                )
                for request in self.region.requests:
                    self.assertEqual(
                        "sitekey", request.headers["X-FilesAPI-Key"]
                    )
                if error_class is LockoutRegionMismatchError:
                    self.assertIn(
                        "max_network_retries",
                        "\n".join(caught.exception.__notes__),
                    )
                self.issuer.requests.clear()
                self.region.requests.clear()
                self.region.responses.clear()

    def test_callers_can_disable_relocation_or_decide_it(self):
        events = []
        cases = (
            ({"region_policy": "disabled"}, None, False),
            ({}, {"region_policy": "disabled"}, False),
            (
                {
                    "region_handler": lambda event: events.append(event)
                    and False
                },
                None,
                False,
            ),
            ({"region_handler": lambda event: True}, None, True),
        )
        for settings, options, moves in cases:
            with self.subTest(settings=settings, options=options):
                self.issuer.reply_json(mismatch("eu.example.com"), status=403)
                self.region.reply_json([])
                client = self.client(**settings)
                if moves:
                    client.user.list({}, options)
                else:
                    with self.assertRaises(
                        LockoutRegionMismatchError
                    ) as caught:
                        client.user.list({}, options)
                    self.assertEqual(
                        {"host": "eu.example.com"}, caught.exception.data
                    )
                self.assertEqual(1 if moves else 0, len(self.region.requests))
                self.region.requests.clear()
                self.region.responses.clear()
        [event] = events
        self.assertEqual(
            ("https://app.example.com", "https://eu.example.com", True),
            (event.original_origin, event.target_origin, event.automatic),
        )
        self.assertNotIn("sitekey", repr(event))

    def test_a_handler_can_approve_a_port_and_its_errors_stop_the_operation(
        self,
    ):
        self.issuer.reply_json(mismatch("eu.example.com:8443"), status=403)
        self.region.reply_json([])
        self.client(
            region_handler=lambda event: event.target_origin
        ).user.list()
        self.assertEqual("eu.example.com:8443", self.proxy.targets[-1])

        def refuse(event):
            raise RuntimeError("not today")

        self.issuer.reply_json(mismatch("eu.example.com"), status=403)
        with self.assertRaises(RuntimeError):
            self.client(region_handler=refuse).user.list()
        self.assertEqual(1, len(self.region.requests))

    def test_an_unverified_issuer_moves_only_for_an_exact_development_pair(
        self,
    ):
        issuer = start_loopback_api(self)
        region = start_loopback_api(self)
        pair = [(issuer.url, region.url)]
        target = region.url.split("://")[1]
        for settings, moves in (
            ({}, False),
            ({"region_development_origins": pair}, True),
        ):
            with self.subTest(settings=settings):
                issuer.reply_json(mismatch(target), status=403)
                region.reply_json([])
                client = files_sdk.Client(
                    api_key="devkey", base_url=issuer.url, **settings
                )
                self.addCleanup(client.close)
                if moves:
                    client.user.list()
                else:
                    with self.assertRaises(LockoutRegionMismatchError):
                        client.user.list()
                self.assertEqual(1 if moves else 0, len(region.requests))
        # Requests turns verification off for any false verify value, so
        # none of them makes an issuer trusted: False, or an empty string in
        # a session of the caller's own. A client refuses the empty string.
        with self.assertRaises(InvalidParameterError):
            files_sdk.Client(api_key="sitekey", verify="")
        empty = requests.Session()
        self.addCleanup(empty.close)
        empty.verify = ""
        empty.proxies = {"https": self.proxy.url}
        for unverified in (
            files_sdk.Client(
                api_key="sitekey",
                base_url="https://app.example.com",
                verify=False,
                proxies={"https": self.proxy.url},
            ),
            files_sdk.Client(
                api_key="sitekey",
                base_url="https://app.example.com",
                http_session=empty,
            ),
        ):
            self.addCleanup(unverified.close)
            for answer in (
                lambda: self.issuer.reply_json(
                    mismatch("eu.example.com"), status=403
                ),
                lambda: self.issuer.reply(403, PLAIN, NAMED),
            ):
                answer()
                with (
                    warnings.catch_warnings(),
                    self.assertRaises(LockoutRegionMismatchError),
                ):
                    warnings.simplefilter("ignore", InsecureRequestWarning)
                    unverified.user.list()
        self.assertEqual([], self.region.requests)

    def test_storage_answers_never_relocate(self):
        storage = start_loopback_api(self, tls=self.authority)
        storage.reply_json(mismatch("eu.example.com"), status=403)
        storage.reply(403, PLAIN, NAMED)
        client = files_sdk.Client(
            api_key="sitekey",
            base_url="https://app.example.com",
            verify=self.authority.ca,
        )
        self.addCleanup(client.close)
        api_client = ApiClient(Operation.start(client))

        with self.assertRaises(LockoutRegionMismatchError):
            api_client.send_remote_request(
                "PUT", storage.url + "/part", body=b"part"
            )
        with self.assertRaises(APIError) as caught:
            api_client.send_remote_request(
                "PUT", storage.url + "/part", body=b"part"
            )
        self.assertEqual(
            "HTTP 403 Transfer request failed", str(caught.exception)
        )

        self.assertEqual([], self.region.requests)
        self.assertEqual(2, len(storage.requests))


if __name__ == "__main__":
    unittest.main()
