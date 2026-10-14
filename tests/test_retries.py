import io
import logging
import re
import tempfile
import threading
import time
import traceback
import unittest
from pathlib import Path
from unittest import mock

import files_sdk
import requests
from files_sdk.api_client import ApiClient
from files_sdk.error import (
    APIConnectionError,
    APIError,
    DeadlineExceededError,
    OperationCancelledError,
)
from tests.loopback_api import start_loopback_api
from tests.network_fixtures import WAIT, ScriptedServer, TestAuthority
from tests.upload_fixtures import SITE_DISABLED
from urllib3.exceptions import MaxRetryError, NewConnectionError

JSON_ERROR = {"type": "processing-failure/unknown", "error": "Try again."}


def traceback_text(error):
    return "".join(traceback.format_exception(error))


CHECK_BEFORE_REPEATING = "Check whether it took effect before repeating it."


def retry_waits(logs):
    """The waits of the retries the SDK logged, in seconds."""
    return [
        float(re.search(r"wait=([0-9.]+)", record.getMessage()).group(1))
        for record in logs.records
        if "Retrying request" in record.getMessage()
    ]


class TestApiRetries(unittest.TestCase):
    def setUp(self):
        self.api = start_loopback_api(self)

    def client(self, **settings):
        settings.setdefault("initial_network_retry_delay", 0)
        client = files_sdk.Client(
            api_key="key", base_url=self.api.url, **settings
        )
        self.addCleanup(client.close)
        return client

    def test_zero_retries_sends_once_and_the_default_sends_four_times(self):
        for retries, attempts in ((0, 1), (None, 4), (1, 2)):
            with self.subTest(retries=retries):
                self.api.requests.clear()
                for _ in range(attempts):
                    self.api.reply_json(JSON_ERROR, status=503)
                settings = (
                    {} if retries is None else {"max_network_retries": retries}
                )

                with self.assertRaises(APIError) as caught:
                    self.client(**settings).user.list()

                self.assertEqual(
                    attempts, len(self.api.wait_for_requests(attempts))
                )
                # A request that only asks changed nothing, so nothing warns.
                self.assertFalse(caught.exception.remote_outcome_unknown)
                self.assertNotIn(
                    CHECK_BEFORE_REPEATING, traceback_text(caught.exception)
                )

    def test_only_rate_limits_and_server_errors_other_than_501_are_retried(
        self,
    ):
        client = self.client(max_network_retries=1)
        for status, attempts in (
            (429, 2),
            (500, 2),
            (502, 2),
            (504, 2),
            (501, 1),
            (400, 1),
            (403, 1),
            (404, 1),
        ):
            with self.subTest(status=status):
                self.api.requests.clear()
                for _ in range(attempts):
                    self.api.reply_json(JSON_ERROR, status=status)
                self.api.reply_json(
                    []
                )  # What a retry of a non-retried status would get.

                with self.assertRaises(APIError):
                    client.user.list()

                self.assertEqual(attempts, len(self.api.requests))
                self.api.responses.clear()

    def test_a_change_answered_with_an_error_is_not_sent_again(self):
        # No status, type or body shows Files.com did not carry out a change
        # before answering: the create is sent once, and the error says its
        # outcome is unknown, whatever retries are left.
        for retries in (None, 0):
            client = (
                self.client()
                if retries is None
                else self.client(max_network_retries=retries)
            )
            for status in (429, 503, 500, 502, 504, 422, 404):
                for body in (JSON_ERROR, {}):
                    with self.subTest(
                        retries=retries, status=status, body=body
                    ):
                        self.api.requests.clear()
                        self.api.reply_json(body, status=status)
                        self.api.reply_json({"id": 1})

                        with self.assertRaises(APIError) as caught:
                            client.user.create({"username": "pat"})

                        self.assertTrue(
                            caught.exception.remote_outcome_unknown
                        )
                        self.assertEqual(1, len(self.api.requests))
                        self.api.responses.clear()

    def test_an_error_answering_a_change_says_to_check_before_repeating_it(
        self,
    ):
        # Files.com's own message may say to try again; the traceback keeps
        # it and says what the SDK knows, including when a borrowed session
        # could have sent the change again by itself.
        retrying = requests.Session()
        self.addCleanup(retrying.close)
        retrying.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
        for label, settings in (
            ("owned", {}),
            ("retrying adapter", {"http_session": retrying}),
        ):
            with self.subTest(session=label):
                self.api.reply_json(JSON_ERROR, status=503)

                with self.assertRaises(APIError) as caught:
                    self.client(**settings).user.create({"username": "pat"})

                text = traceback_text(caught.exception)
                self.assertIn(
                    "files_sdk.error.APIError: HTTP 503 Try again.", text
                )
                self.assertIn("may still have happened", text)
                self.assertIn(CHECK_BEFORE_REPEATING, text)
                self.assertEqual(
                    label == "retrying adapter",
                    "adapter retries requests itself" in text,
                )
                self.assertEqual(
                    (503, "Try again."),
                    (caught.exception.http_status, caught.exception.error),
                )
                self.assertNotIn("no response arrived", text)

    def test_an_answer_while_the_site_is_disabled_shows_the_change_was_not_carried_out(
        self,
    ):
        # Files.com sends it before carrying out anything; it is not a reason
        # to send the change again.
        self.api.reply_json(SITE_DISABLED, status=422)
        self.api.reply_json({"id": 1})

        with self.assertRaises(APIError) as caught:
            self.client().user.create({"username": "pat"})

        self.assertFalse(caught.exception.remote_outcome_unknown)
        self.assertNotIn(
            CHECK_BEFORE_REPEATING, traceback_text(caught.exception)
        )
        self.assertEqual(1, len(self.api.requests))
        # Not in any other form: another status or http-code, or another type.
        for body, status in (
            ({**SITE_DISABLED, "http-code": "422"}, 422),
            (SITE_DISABLED, 503),
            (
                {
                    **SITE_DISABLED,
                    "type": "service-unavailable/uploads-unavailable",
                },
                422,
            ),
        ):
            with self.subTest(body=body, status=status):
                self.api.responses.clear()
                self.api.reply_json(body, status=status)
                with self.assertRaises(APIError) as caught:
                    self.client().user.create({"username": "pat"})
                self.assertTrue(caught.exception.remote_outcome_unknown)
                self.assertIn(
                    CHECK_BEFORE_REPEATING, traceback_text(caught.exception)
                )

    def test_a_refusal_that_is_not_a_files_com_error_does_not_send_a_change_again(
        self,
    ):
        # A proxy's page proves nothing about the create behind it, which
        # may have been carried out; a request that only asks is retried.
        page = (
            b"<html>Service unavailable</html>",
            {"Content-Type": "text/html"},
        )
        for status, unknown in ((503, True), (429, True)):
            with self.subTest(status=status):
                self.api.requests.clear()
                self.api.reply(status, *page)
                self.api.reply_json({"id": 1})

                with self.assertRaises(APIConnectionError) as caught:
                    self.client().user.create({"username": "pat"})

                self.assertEqual(
                    (unknown, 1),
                    (
                        caught.exception.remote_outcome_unknown,
                        len(self.api.requests),
                    ),
                )
                self.api.responses.clear()
        self.api.requests.clear()
        self.api.reply(503, *page)
        self.api.reply_json([])
        self.client().user.list()
        self.assertEqual(2, len(self.api.requests))

    def test_api_retries_wait_100_200_and_400_milliseconds(self):
        client = files_sdk.Client(api_key="key", base_url=self.api.url)
        self.addCleanup(client.close)
        for _ in range(3):
            self.api.reply_json(JSON_ERROR, status=503)
        self.api.reply_json([])

        with self.assertLogs("files_sdk", level=logging.INFO) as logs:
            client.user.list()

        self.assertEqual([0.1, 0.2, 0.4], retry_waits(logs))

    def test_a_request_that_only_asks_is_sent_again_after_its_answer_was_lost(
        self,
    ):
        self.api.disconnect(
            after_body_bytes=10**6
        )  # Read it all, then hang up.
        self.api.reply_json({"id": 1})

        user = self.client(max_network_retries=1).user.find(1)

        first, second = self.api.wait_for_requests(2)
        self.assertEqual((first.path, first.body), (second.path, second.body))
        self.assertEqual(1, user.id)

    def test_a_change_whose_answer_was_lost_is_not_sent_again(self):
        # Files.com may have carried it out: the caller hears that, rather
        # than a second create, update or delete.
        changes = (
            ("create", lambda client: client.user.create({"username": "pat"})),
            ("update", lambda client: client.user.update(1, {"name": "Pat"})),
            ("delete", lambda client: client.user.delete(1)),
        )
        sessions = (("owned", None), ("borrowed", requests.Session()))
        for (change, call), (label, session) in (
            (c, s) for c in changes for s in sessions
        ):
            with self.subTest(change=change, session=label):
                self.api.requests.clear()
                self.api.disconnect(after_body_bytes=10**6)
                self.api.reply_json({"id": 1})
                client = (
                    self.client(http_session=session)
                    if session
                    else self.client()
                )

                with self.assertRaises(APIConnectionError) as caught:
                    call(client)

                self.assertTrue(caught.exception.remote_outcome_unknown)
                self.assertEqual("response", caught.exception.phase)
                self.assertEqual(1, len(self.api.requests))
                self.api.responses.clear()

    def test_a_change_that_was_never_sent_is_sent_again_with_the_same_body(
        self,
    ):
        class RefusesTheFirstConnection(requests.adapters.HTTPAdapter):
            refused = 0

            def send(self, request, *args, **kwargs):
                if not self.refused:
                    self.refused += 1
                    reason = NewConnectionError(None, "Connection refused")
                    raise requests.exceptions.ConnectionError(
                        MaxRetryError(None, request.url, reason)
                    )
                return super().send(request, *args, **kwargs)

        session = requests.Session()
        self.addCleanup(session.close)
        adapter = RefusesTheFirstConnection()
        session.mount("http://", adapter)
        self.api.reply_json({"id": 1, "username": "pat"})

        user = self.client(http_session=session).user.create(
            {"username": "pat"}
        )

        [request] = self.api.requests
        self.assertEqual(
            (1, {"username": "pat"}, "pat"),
            (adapter.refused, request.json, user.username),
        )

    def test_a_lost_answer_warns_that_a_retrying_adapter_may_have_sent_it_again(
        self,
    ):
        session = requests.Session()
        self.addCleanup(session.close)
        # Its default Retry does not repeat a POST, but it could be set to.
        session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
        self.api.disconnect(after_body_bytes=10**6)

        with self.assertRaises(APIConnectionError) as caught:
            self.client(http_session=session).user.create({"username": "pat"})

        self.assertTrue(caught.exception.remote_outcome_unknown)
        self.assertIn("adapter retries requests itself", str(caught.exception))
        self.assertEqual(1, len(self.api.requests))

    def test_a_certificate_failure_is_not_retried(self):
        authority = TestAuthority.create(self)
        server = ScriptedServer(
            self, lambda peer: peer.read_request(), tls=authority
        )
        client = files_sdk.Client(
            api_key="key",
            base_url=server.url("", host="localhost"),
            initial_network_retry_delay=0,
        )
        self.addCleanup(client.close)

        with self.assertRaises(APIConnectionError):
            client.user.list()

        self.assertEqual(1, len(server.connections))

    def test_a_cancelled_retry_wait_sends_nothing_more(self):
        self.api.reply_json(JSON_ERROR, status=503)
        client = self.client(initial_network_retry_delay=30)
        token = files_sdk.CancellationToken()
        threading.Timer(0.3, token.cancel).start()
        started = time.monotonic()

        with self.assertRaises(OperationCancelledError) as caught:
            client.user.list({}, {"cancel_token": token})

        self.assertLess(time.monotonic() - started, WAIT)
        self.assertEqual("retry wait", caught.exception.phase)
        self.assertEqual(1, len(self.api.requests))

    def test_one_deadline_covers_every_page_of_a_list(self):
        self.api.reply_json([{"id": 1}], headers={"X-Files-Cursor": "next"})
        page = self.client().user.list(
            {}, {"deadline": time.monotonic() + 0.5}
        )
        time.sleep(0.6)

        with self.assertRaises(DeadlineExceededError):
            page.load_next_page()

        self.assertEqual(1, len(self.api.requests))
        self.assertEqual([1], [item.id for item in page])


class TestTransferRetries(unittest.TestCase):
    def setUp(self):
        self.storage = start_loopback_api(self)
        # The module facade's transfers: a plain-HTTP API, like the storage.
        patcher = mock.patch.object(
            files_sdk, "base_url", "http://localhost:4042"
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def send_part(self):
        return ApiClient().send_remote_request(
            "PUT",
            self.storage.url + "/part?X-Amz-Signature=secret",
            body=b"part",
        )

    def test_storage_waits_follow_retry_after_and_otherwise_100_milliseconds(
        self,
    ):
        self.storage.reply(503, headers={"Retry-After": "0.3"})
        self.storage.reply(429)
        self.storage.reply(
            503, headers={"Retry-After": "Fri, 31 Dec 1999 23:59:59 GMT"}
        )
        self.storage.reply(500)
        self.storage.reply(502)
        self.storage.reply(200)

        with self.assertLogs("files_sdk", level=logging.INFO) as logs:
            with self.assertRaises(APIError):
                self.send_part()
        with self.assertLogs("files_sdk", level=logging.INFO) as later:
            self.send_part()

        self.assertEqual([0.3, 0.0, 0.0], retry_waits(logs))
        self.assertEqual([0.1], retry_waits(later))

    def test_storage_retry_after_waits_are_bounded(self):
        # A storage service's Retry-After is waited for, but never longer
        # than MAX_RETRY_AFTER at a time: a wait of days, or a value too
        # long for a number, is shortened to the ceiling rather than
        # blocking the operation or failing it with an overflow.
        self.storage.reply(503, headers={"Retry-After": "86400000"})
        self.storage.reply(503, headers={"Retry-After": "1" * 400})
        self.storage.reply(200)

        with mock.patch("files_sdk.api_client.MAX_RETRY_AFTER", 0.2):
            with self.assertLogs("files_sdk", level=logging.INFO) as logs:
                response = self.send_part()

        self.assertEqual(200, response.status_code)
        self.assertEqual([0.2, 0.2], retry_waits(logs))
        self.assertEqual(3, len(self.storage.requests))

    def test_a_download_is_retried_only_until_it_writes(self):
        self.storage.disconnect(after_body_bytes=0)
        self.storage.reply(200, b"content")
        output = io.BytesIO()

        ApiClient().stream_download(self.storage.url + "/object", output)

        self.assertEqual(b"content", output.getvalue())
        self.assertEqual(2, len(self.storage.wait_for_requests(2)))


class TestUploadCompletion(unittest.TestCase):
    """The request that completes an upload is sent at most once after it
    may have been received."""

    def setUp(self):
        self.api = start_loopback_api(self)
        self.client = files_sdk.Client(
            api_key="key", base_url=self.api.url, initial_network_retry_delay=0
        )
        self.addCleanup(self.client.close)
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.local = Path(directory.name) / "file.txt"
        self.local.write_bytes(b"hello")

    def begin(self, **reply):
        self.api.reply_json(
            [
                {
                    "ref": "ref1",
                    "part_number": 1,
                    "partsize": 1024,
                    "http_method": "PUT",
                    "upload_uri": self.api.url + "/storage/part1",
                }
            ]
        )
        self.api.reply(200, headers={"ETag": '"etag1"'}, **reply)

    def borrowing(self, session):
        """A client like self.client that sends through session."""
        self.addCleanup(session.close)
        client = files_sdk.Client(
            api_key="key",
            base_url=self.api.url,
            http_session=session,
            initial_network_retry_delay=0,
        )
        self.addCleanup(client.close)
        return client

    def completions(self):
        return [request.url_path for request in self.api.requests].count(
            "/api/rest/v1/files/file.txt"
        )

    def test_a_lost_completion_answer_is_reported_without_sending_it_again(
        self,
    ):
        # The SDK's own session, and a plain one of the caller's, which the
        # SDK cannot watch send: either way the request may have arrived.
        for label, client in (
            ("owned", self.client),
            ("borrowed", self.borrowing(requests.Session())),
        ):
            with self.subTest(session=label):
                self.api.requests.clear()
                self.begin()
                self.api.disconnect(
                    after_body_bytes=10**6
                )  # Read it all, then hang up.
                self.api.reply_json({"path": "file.txt"})

                with self.assertRaises(APIConnectionError) as caught:
                    client.file.upload_file(self.local, "file.txt")

                self.assertTrue(caught.exception.remote_outcome_unknown)
                self.api.wait_for_requests(3)
                self.assertEqual(1, self.completions())
                self.api.responses.clear()

    def test_a_completion_that_could_not_connect_is_sent_again(self):
        class RefusesTheFirstCompletion(requests.adapters.HTTPAdapter):
            refused = 0

            def send(self, request, *args, **kwargs):
                if (
                    request.url.endswith("/files/file.txt")
                    and not self.refused
                ):
                    self.refused += 1
                    reason = NewConnectionError(None, "Connection refused")
                    raise requests.exceptions.ConnectionError(
                        MaxRetryError(None, request.url, reason)
                    )
                return super().send(request, *args, **kwargs)

        session = requests.Session()
        adapter = RefusesTheFirstCompletion()
        session.mount("http://", adapter)
        client = self.borrowing(session)
        self.begin()
        self.api.reply_json({"path": "file.txt"})

        client.file.upload_file(self.local, "file.txt")

        self.assertEqual((1, 1), (adapter.refused, self.completions()))

    def test_a_lost_answer_to_a_request_for_part_urls_is_sent_again(self):
        # An upload Files.com began but the SDK never heard of is harmless.
        self.api.disconnect(after_body_bytes=10**6)
        self.begin()
        self.api.reply_json({"path": "file.txt"})

        self.client.file.upload_file(self.local, "file.txt")

        paths = [request.url_path for request in self.api.requests]
        self.assertEqual(
            2, paths.count("/api/rest/v1/file_actions/begin_upload/file.txt")
        )
        self.assertEqual(1, self.completions())

    def test_an_error_answering_the_completion_is_not_sent_again(self):
        for body in (JSON_ERROR, {}):
            with self.subTest(body=body):
                self.api.requests.clear()
                self.begin()
                self.api.reply_json(body, status=503)
                self.api.reply_json({"path": "file.txt"})

                with self.assertRaises(APIError) as caught:
                    self.client.file.upload_file(self.local, "file.txt")

                self.assertTrue(caught.exception.remote_outcome_unknown)
                self.assertEqual(1, self.completions())
                self.api.responses.clear()

    def test_an_unreliable_server_error_from_the_completion_is_not_sent_again(
        self,
    ):
        self.begin()
        self.api.reply(
            503,
            b"<html>Service unavailable</html>",
            {"Content-Type": "text/html"},
        )
        self.api.reply_json({"path": "file.txt"})

        with self.assertRaises(APIConnectionError) as caught:
            self.client.file.upload_file(self.local, "file.txt")

        self.assertTrue(caught.exception.remote_outcome_unknown)
        self.assertEqual(1, self.completions())

    def test_cancelling_before_completion_sends_no_completion(self):
        token = files_sdk.CancellationToken()
        self.begin(when_received=token.cancel)

        with self.assertRaises(OperationCancelledError):
            self.client.file.upload_file(
                self.local, "file.txt", {"cancel_token": token}
            )

        paths = [request.url_path for request in self.api.requests]
        self.assertNotIn("/api/rest/v1/files/file.txt", paths)


if __name__ == "__main__":
    unittest.main()
