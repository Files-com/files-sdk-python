import unittest
from unittest.mock import patch

import files_sdk
from files_sdk.error import InvalidSessionError, MissingParameterError
from files_sdk.models import Session
from tests.loopback_api import serve_loopback_api


class TestSessionLifecycle(unittest.TestCase):
    def setUp(self):
        self.api = serve_loopback_api(self)

    def test_destroying_a_session_logs_out_that_session_with_one_delete(self):
        self.api.reply_json({"id": "loginsession"})
        session = files_sdk.session.create(
            {"username": "user", "password": "pass"}
        )
        self.api.reply(204)
        competing = {
            "api_key": "callkey",
            "session_id": "callsession",
            "session": Session({"id": "othersession"}),
            "language": "fr",
        }
        options = dict(competing)

        with patch.object(files_sdk, "session_id", "globalsession"):
            self.assertIsNone(session.destroy({}, options))

        login, logout = self.api.requests
        self.assertEqual(("DELETE", "/sessions"), (logout.method, logout.path))
        self.assertEqual("loginsession", logout.headers["X-FilesAPI-Auth"])
        self.assertNotIn("X-FilesAPI-Key", logout.headers)
        self.assertEqual("fr", logout.headers["Accept-Language"])
        self.assertEqual(competing, options)

    def test_a_rejected_logout_raises_an_sdk_error_without_the_session_id(
        self,
    ):
        session = Session({"id": "rejectedsession"})
        self.api.reply_json(
            {
                "type": "not-authenticated/invalid-session",
                "error": "Invalid session.",
            },
            status=401,
        )

        with self.assertLogs("files_sdk", level="INFO") as logs:
            with self.assertRaises(InvalidSessionError) as caught:
                session.destroy()

        self.assertEqual(1, len(self.api.requests))
        self.assertEqual(401, caught.exception.http_status)
        self.assertNotIn("rejectedsession", str(caught.exception))
        self.assertNotIn("rejectedsession", "\n".join(logs.output))

    def test_a_session_that_was_never_created_cannot_be_destroyed(self):
        with self.assertRaises(MissingParameterError):
            Session({"username": "user"}).destroy()

        self.assertEqual([], self.api.requests)

    def test_module_level_logout_uses_the_session_id_option(self):
        for logout in (files_sdk.session.delete, files_sdk.session.destroy):
            with self.subTest(logout=logout.__name__):
                self.api.requests.clear()
                self.api.reply(204)

                self.assertIsNone(logout({}, {"session_id": "optionsession"}))

                [request] = self.api.requests
                self.assertEqual("DELETE", request.method)
                self.assertEqual(
                    "optionsession", request.headers["X-FilesAPI-Auth"]
                )


if __name__ == "__main__":
    unittest.main()
