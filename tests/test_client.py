import contextlib
import io
import platform
import re
import sys
import unittest
from unittest import mock

import files_sdk
import requests
from files_sdk.api_client import ApiClient
from files_sdk.error import AuthenticationError, InvalidParameterError
from files_sdk.models import Session
from tests.loopback_api import serve_loopback_api, start_loopback_api

# The User-Agent the SDK sends by default: its name and version, then one
# comment with the coarse operating system and, when it can say it, the
# Python version of the process.
SDK_USER_AGENT = re.compile(
    r"Files\.com Python SDK v(?P<version>\S+) \(files-sdk-meta/1; "
    r"os=(?P<os>[a-z][a-z0-9-]{0,15}); "
    r"runtime=python(?:/(?P<runtime>[0-9][A-Za-z0-9._+-]{0,47}))?\)"
)
COARSE_OPERATING_SYSTEMS = {
    "windows",
    "macos",
    "linux",
    "android",
    "ios",
    "freebsd",
    "other",
    "unknown",
}


class TestUserAgent(unittest.TestCase):
    """The User-Agent of the SDK's requests: its own, with a comment about
    the process, wherever the SDK chooses it, and exactly the one given
    wherever a caller chooses it."""

    def setUp(self):
        self.module_api = serve_loopback_api(self)
        self.api = start_loopback_api(self)

    def test_api_and_storage_requests_carry_the_sdk_and_its_process(self):
        client = files_sdk.Client(
            api_key="clientkey",
            base_url=self.api.url,
            headers={"User-Agent": "client-agent/1"},
        )
        self.addCleanup(client.close)
        self.api.reply_json([])
        self.api.reply_json([])
        self.api.reply_json(
            {
                "path": "doc.txt",
                "download_uri": self.api.url + "/storage/doc.txt",
            }
        )
        self.api.reply(200, b"content")
        self.module_api.reply_json([])
        downloaded = io.BytesIO()

        client.user.list()
        client.user.list({}, {"headers": {"User-Agent": "call-agent/1"}})
        client.file.find("doc.txt").download_content(downloaded)
        files_sdk.user.list()

        self.assertEqual(b"content", downloaded.getvalue())
        self.assertEqual("/storage/doc.txt", self.api.requests[3].url_path)
        agents = [
            request.headers["User-Agent"]
            for request in self.api.requests + self.module_api.requests
        ]
        # A client's or a call's headers never replace it on an API request.
        self.assertEqual([agents[0]] * 5, agents)
        agent = agents[0]
        match = SDK_USER_AGENT.fullmatch(agent)
        self.assertIsNotNone(match, agent)
        assert match is not None
        self.assertEqual(files_sdk.version, match["version"])
        self.assertIn(match["os"], COARSE_OPERATING_SYSTEMS)
        self.assertEqual(platform.python_version(), match["runtime"])
        self.assertTrue(agent.isascii())
        self.assertLessEqual(
            len(agent[agent.index(" (files-sdk-meta/1;") :]), 128
        )
        self.assertLessEqual(len(agent), 190)

    def test_a_transfer_sends_the_user_agent_it_is_given_exactly(self):
        given = [
            # One that looks like the SDK's own, and one too long to be.
            "Files.com Python SDK v{} (files-sdk-meta/1; os=other; runtime=python/0.1)".format(
                files_sdk.version
            ),
            "Files.com Python SDK v{} ({})".format(
                files_sdk.version, "x" * 300
            ),
            "Agent/2.0 (compatible; café) (+https://example.com/bot)",
        ]
        for agent in given:
            self.module_api.reply(200)
            ApiClient().send_remote_request(
                "PUT",
                self.module_api.url + "/storage/part",
                headers={"User-Agent": agent},
                body=b"part",
            )

        self.assertEqual(
            given,
            [
                request.headers["User-Agent"]
                for request in self.module_api.requests
            ],
        )

    def test_a_request_headers_override_replaces_the_whole_user_agent(self):
        # As the Files.com MCP server does: call the SDK's own and replace
        # the User-Agent it returns.
        class McpApiClient(ApiClient):
            def request_headers(
                self, api_key, session_id, language, workspace_id
            ):
                headers = super().request_headers(
                    api_key, session_id, language, workspace_id
                )
                headers["User-Agent"] = "Files.com Python MCP SDK v9.9.9"
                return headers

        self.module_api.reply_json([])
        McpApiClient().send_request("GET", "/users")

        [request] = self.module_api.requests
        self.assertEqual(("GET", "/users"), (request.method, request.path))
        self.assertEqual(
            "Files.com Python MCP SDK v9.9.9", request.headers["User-Agent"]
        )
        self.assertEqual("globalkey", request.headers["X-FilesAPI-Key"])

    def test_a_borrowed_session_keeps_its_own_user_agent_and_settings(self):
        session = requests.Session()
        self.addCleanup(session.close)
        session.headers["User-Agent"] = "caller-agent/1"
        session.auth = ("user", "private-password")

        def hook(response, **_):
            pass

        session.hooks["response"].append(hook)

        def settings():
            return (
                dict(session.headers),
                session.auth,
                list(session.hooks["response"]),
                dict(session.adapters),
            )

        before = settings()
        client = files_sdk.Client(
            api_key="clientkey", base_url=self.api.url, http_session=session
        )
        self.api.reply_json(
            {
                "path": "doc.txt",
                "download_uri": self.api.url + "/storage/doc.txt",
            }
        )
        self.api.reply(200, b"content")
        self.api.reply(200, b"own")

        client.file.find("doc.txt").download_content(io.BytesIO())
        client.close()
        session.get(self.api.url + "/own")

        lookup, transfer, own = self.api.requests
        self.assertIsNotNone(
            SDK_USER_AGENT.fullmatch(lookup.headers["User-Agent"]),
            lookup.headers["User-Agent"],
        )
        self.assertEqual(
            lookup.headers["User-Agent"], transfer.headers["User-Agent"]
        )
        for header in ("Authorization", "X-FilesAPI-Key"):
            self.assertNotIn(header, transfer.headers)
        self.assertEqual("caller-agent/1", own.headers["User-Agent"])
        self.assertEqual(before, settings())

    def user_agent_of_process(
        self, platform_id, python_version, android=False
    ):
        """The User-Agent of a module request made while sys.platform is
        platform_id and platform.python_version() returns python_version,
        or raises it if it is an exception. The process has the marker
        Android builds of Python have, sys.getandroidapilevel, exactly when
        android is true, whether or not it had one of its own; it has its
        own back, as it was, afterwards."""

        def process_python_version():
            if isinstance(python_version, Exception):
                raise python_version
            return python_version

        with contextlib.ExitStack() as process:
            process.enter_context(
                mock.patch.object(sys, "platform", platform_id)
            )
            process.enter_context(
                mock.patch.object(
                    platform, "python_version", process_python_version
                )
            )
            if android:
                process.enter_context(
                    mock.patch.object(
                        sys, "getandroidapilevel", lambda: 34, create=True
                    )
                )
            elif hasattr(sys, "getandroidapilevel"):
                marker = sys.getandroidapilevel
                del sys.getandroidapilevel
                process.callback(setattr, sys, "getandroidapilevel", marker)
            self.module_api.reply_json([])
            files_sdk.user.list()
        return self.module_api.requests.pop().headers["User-Agent"]

    def test_the_process_is_named_coarsely_and_an_unusable_python_version_left_out(
        self,
    ):
        identity = "Files.com Python SDK v{}".format(files_sdk.version)
        for platform_id, android, os_name in (
            ("win32", False, "windows"),
            ("darwin", False, "macos"),
            ("linux", False, "linux"),
            ("linux", True, "android"),
            ("android", False, "android"),
            ("ios", False, "ios"),
            ("freebsd14", False, "freebsd"),
            ("cygwin", False, "other"),
            ("", False, "unknown"),
        ):
            with self.subTest(platform=platform_id, android=android):
                self.assertEqual(
                    identity
                    + " (files-sdk-meta/1; os={}; runtime=python/3.14.7)".format(
                        os_name
                    ),
                    self.user_agent_of_process(platform_id, "3.14.7", android),
                )
        longest = "3." + "1" * 46  # 48 bytes, the longest version carried
        for version, runtime in (
            ("3.15.0a1+", "python/3.15.0a1+"),
            (longest, "python/" + longest),
            (longest + "1", "python"),
            ("", "python"),
            ("v3.14.7", "python"),
            ("3.14.7 (custom)", "python"),
            ("3.14.7é", "python"),
            (ValueError("failed to parse CPython sys.version"), "python"),
        ):
            with self.subTest(version=version):
                self.assertEqual(
                    identity
                    + " (files-sdk-meta/1; os=linux; runtime={})".format(
                        runtime
                    ),
                    self.user_agent_of_process("linux", version),
                )


class TestClientContext(unittest.TestCase):
    """Each client, and every object it returns, keeps its own origin,
    principal and settings; the module-level settings never reach it."""

    def setUp(self):
        self.module_api = serve_loopback_api(self)
        self.api_a = start_loopback_api(self)
        self.api_b = start_loopback_api(self)
        self.a = files_sdk.Client(
            api_key="keyA", workspace_id=0, base_url=self.api_a.url
        )
        self.b = files_sdk.Client(
            session_id="sessionB", workspace_id=7, base_url=self.api_b.url
        )
        self.addCleanup(self.a.close)
        self.addCleanup(self.b.close)

    def test_retained_objects_keep_their_client_after_module_settings_change(
        self,
    ):
        self.api_a.reply_json({"id": 1, "name": "Pat"})
        user = self.a.user.find(1)
        filters = {"filter": {"username": "pat"}}
        self.api_b.reply_json([{"id": 2}], headers={"X-Files-Cursor": "page2"})
        page = self.b.user.list(filters)

        files_sdk.set_api_key("changedkey")
        files_sdk.set_workspace_id(99)
        self.addCleanup(files_sdk.set_workspace_id, None)
        files_sdk.base_url = (
            "http://127.0.0.1:9"  # The patch in setUp restores it.
        )
        filters["filter"]["username"] = "changed"

        self.api_a.reply_json({"id": 1, "name": "Robin"})
        self.assertIsNone(user.save())
        self.api_b.reply_json([{"id": 3}])
        self.assertEqual([3], [item.id for item in page.load_next_page()])

        [find, save] = self.api_a.requests
        self.assertEqual(("PATCH", "/users/1"), (save.method, save.path))
        for request in (find, save):
            self.assertEqual("keyA", request.headers["X-FilesAPI-Key"])
            self.assertEqual("0", request.headers["X-Files-Workspace-Id"])
        [first, second] = self.api_b.requests
        self.assertEqual(
            {"filter[username]": "pat", "cursor": "page2"}, second.query
        )
        for request in (first, second):
            self.assertEqual("sessionB", request.headers["X-FilesAPI-Auth"])
            self.assertNotIn("X-FilesAPI-Key", request.headers)
            self.assertEqual("7", request.headers["X-Files-Workspace-Id"])
        self.assertEqual("Robin", user.name)
        self.assertEqual([], self.module_api.requests)

    def test_the_module_facade_uses_its_settings_as_of_each_call(self):
        self.module_api.reply_json({"id": 1})
        legacy_user = files_sdk.user.find(1)
        files_sdk.set_api_key("laterkey")
        self.module_api.reply_json({"id": 1})
        self.module_api.reply_json({"id": 2})

        legacy_user.save()
        files_sdk.user.find(2)

        keys = [
            request.headers["X-FilesAPI-Key"]
            for request in self.module_api.requests
        ]
        self.assertEqual(["globalkey", "globalkey", "laterkey"], keys)

    def test_a_client_never_reads_the_module_credentials(self):
        files_sdk.set_session(Session({"id": "globalsession"}))
        self.addCleanup(setattr, files_sdk, "session_id", None)
        client = files_sdk.Client(base_url=self.api_a.url)
        self.addCleanup(client.close)

        with self.assertRaises(AuthenticationError):
            client.user.find(1)

        self.assertEqual([], self.api_a.requests)

    def test_clear_removes_an_inherited_workspace_and_zero_is_a_workspace(
        self,
    ):
        self.api_a.reply_json([])
        self.a.user.list({}, {"workspace_id": files_sdk.CLEAR})
        self.api_b.reply_json([])
        self.b.user.list({}, {"workspace_id": 0})

        self.assertNotIn(
            "X-Files-Workspace-Id", self.api_a.requests[0].headers
        )
        self.assertEqual(
            "0", self.api_b.requests[0].headers["X-Files-Workspace-Id"]
        )

    def test_new_objects_and_their_saves_use_the_client(self):
        self.api_a.reply_json({"id": 9, "username": "pat"})
        user = self.a.user.new({"username": "pat"})

        self.assertIsNone(user.save())

        [create] = self.api_a.requests
        self.assertEqual(
            ("POST", "/users", "keyA"),
            (create.method, create.path, create.headers["X-FilesAPI-Key"]),
        )
        self.assertEqual(9, user.id)

    def test_logout_uses_the_session_and_client_that_created_it(self):
        self.api_a.reply_json({"id": "loginsession"})
        session = self.a.session.create(
            {"username": "pat", "password": "secret"}
        )
        self.api_a.reply(204)

        session.destroy(
            {},
            {
                "api_key": "otherkey",
                "session_id": "othersession",
                "language": "fr",
            },
        )

        login, logout = self.api_a.requests
        self.assertEqual(("DELETE", "/sessions"), (logout.method, logout.path))
        self.assertEqual("loginsession", logout.headers["X-FilesAPI-Auth"])
        self.assertNotIn("X-FilesAPI-Key", logout.headers)
        self.assertEqual("fr", logout.headers["Accept-Language"])
        self.assertEqual([], self.api_b.requests)


class TestPrincipal(unittest.TestCase):
    """Which credential a request carries when several are configured."""

    def setUp(self):
        self.module_api = serve_loopback_api(self)
        self.api = start_loopback_api(self)

    def credentials(self, client, options=None, path_call=None):
        self.api.reply_json([])
        (path_call or client.user.list)({}, options)
        request = self.api.requests.pop()
        return request.headers.get("X-FilesAPI-Key"), request.headers.get(
            "X-FilesAPI-Auth"
        )

    def client(self, **settings):
        client = files_sdk.Client(base_url=self.api.url, **settings)
        self.addCleanup(client.close)
        return client

    def test_a_key_wins_at_the_same_level_and_an_override_wins_over_inheritance(
        self,
    ):
        both = self.client(api_key="clientkey", session_id="clientsession")
        self.assertEqual(("clientkey", None), self.credentials(both))
        self.assertEqual(
            (None, "callsession"),
            self.credentials(both, {"session_id": "callsession"}),
        )
        self.assertEqual(
            (None, "sessionobj"),
            self.credentials(both, {"session": Session({"id": "sessionobj"})}),
        )
        self.assertEqual(
            (None, "clientsession"),
            self.credentials(both, {"api_key": files_sdk.CLEAR}),
        )
        self.assertEqual(
            ("callkey", None),
            self.credentials(
                both, {"api_key": "callkey", "session_id": "callsession"}
            ),
        )
        session_client = self.client(session_id="clientsession")
        self.assertEqual(
            ("callkey", None),
            self.credentials(session_client, {"api_key": "callkey"}),
        )

    def test_clearing_every_credential_sends_an_anonymous_login(self):
        client = self.client(api_key="clientkey", session_id="clientsession")
        none = {"api_key": files_sdk.CLEAR, "session_id": files_sdk.CLEAR}
        self.api.reply_json({"id": "newsession"})

        client.session.create({"username": "pat", "password": "secret"}, none)
        with self.assertRaises(AuthenticationError):
            client.user.list({}, none)

        [login] = self.api.requests
        self.assertNotIn("X-FilesAPI-Key", login.headers)
        self.assertNotIn("X-FilesAPI-Auth", login.headers)

    def test_module_settings_follow_the_same_rules_and_an_empty_key_inherits(
        self,
    ):
        files_sdk.set_session(Session({"id": "globalsession"}))
        self.addCleanup(setattr, files_sdk, "session_id", None)

        def module_credentials(options):
            self.module_api.reply_json([])
            files_sdk.user.list({}, options)
            request = self.module_api.requests.pop()
            return request.headers.get("X-FilesAPI-Key"), request.headers.get(
                "X-FilesAPI-Auth"
            )

        self.assertEqual(("globalkey", None), module_credentials(None))
        # The Files.com MCP server passes an empty key when it has none.
        self.assertEqual(
            ("globalkey", None), module_credentials({"api_key": ""})
        )
        self.assertEqual(
            (None, "globalsession"),
            module_credentials({"api_key": files_sdk.CLEAR}),
        )
        self.assertEqual(
            (None, "callsession"),
            module_credentials({"session_id": "callsession"}),
        )

    def test_a_session_option_must_have_logged_in(self):
        with self.assertRaises(InvalidParameterError):
            self.client(session=Session({"username": "pat"}))
        with self.assertRaises(InvalidParameterError):
            files_sdk.user.list({}, {"session": Session({"username": "pat"})})
        self.assertEqual([], self.module_api.requests)


class TestOptions(unittest.TestCase):
    def setUp(self):
        self.module_api = serve_loopback_api(self)
        self.api = start_loopback_api(self)
        self.client = files_sdk.Client(
            api_key="clientkey", base_url=self.api.url
        )
        self.addCleanup(self.client.close)

    def test_unknown_options_and_bad_values_are_refused_before_sending(self):
        for options in (
            {"api_kee": "typo"},
            {"read_timeout": 0},
            {"open_timeout": files_sdk.CLEAR},
            {"max_network_retries": -1},
            {"max_network_retries": True},
            {"headers": {"X-FilesAPI-Key": "smuggled"}},
            {"region_policy": "sometimes"},
            {"cancel_token": object()},
        ):
            with self.subTest(options=options):
                with self.assertRaises(InvalidParameterError):
                    self.client.user.list({}, options)
        self.assertEqual([], self.api.requests)

    def test_the_client_option_routes_a_module_call_and_a_different_one_is_refused(
        self,
    ):
        self.api.reply_json([])
        files_sdk.user.list({}, {"client": self.client})
        other = files_sdk.Client(api_key="otherkey", base_url=self.api.url)
        self.addCleanup(other.close)

        with self.assertRaises(InvalidParameterError):
            self.client.user.list({}, {"client": other})

        [request] = self.api.requests
        self.assertEqual("clientkey", request.headers["X-FilesAPI-Key"])
        self.assertEqual([], self.module_api.requests)

    def test_headers_and_timeouts_apply_per_call_without_changing_the_client(
        self,
    ):
        client = files_sdk.Client(
            api_key="clientkey",
            base_url=self.api.url,
            headers={"X-Trace": "client"},
        )
        self.addCleanup(client.close)
        self.api.reply_json([])
        self.api.reply_json([])

        client.user.list({}, {"headers": {"X-Trace": "call", "X-Extra": "1"}})
        client.user.list()

        call, later = self.api.requests
        self.assertEqual(
            ("call", "1"), (call.headers["X-Trace"], call.headers["X-Extra"])
        )
        self.assertEqual(
            ("client", None),
            (later.headers["X-Trace"], later.headers.get("X-Extra")),
        )


if __name__ == "__main__":
    unittest.main()
