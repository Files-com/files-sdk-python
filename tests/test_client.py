import unittest

import files_sdk
from files_sdk.error import AuthenticationError, InvalidParameterError
from files_sdk.models import Session
from tests.loopback_api import serve_loopback_api, start_loopback_api


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
