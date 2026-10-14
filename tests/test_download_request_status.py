"""Storage's status of a download request, as a download without a download
identity reads it: to confirm a file whose response declared no size, and to
explain storage's error answer. The status URL is the one the Go SDK's
DownloadRequestStatus reads: the download URL joined with the
X-Files-Download-Request-Id storage names its answer with. Status documents
follow the status protocol's producer as its source builds them
(download_fixtures.historical_status, and MISSING_REQUEST for a request it
does not know); the values in them, and the documents of other forms, are
made up."""

import io
import logging
import random
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import urlsplit

import files_sdk
from files_sdk.error import (
    APIConnectionError,
    APIError,
    DeadlineExceededError,
    OperationCancelledError,
)
from tests.download_fixtures import (
    DownloadService,
    historical_status,
    sdk_entries,
)

JSON = "application/json"
RANGE = 1000

# Headers that carry Files.com credentials or context: none may reach
# storage, the status request included.
FILES_HEADERS = (
    "x-filesapi-key",
    "x-filesapi-auth",
    "x-files-reauthentication",
    "x-files-workspace-id",
)


def content(size, seed=1):
    return random.Random(seed).randbytes(size)


def completed(size, **members):
    return (
        200,
        historical_status(
            "completed", size, completed_at="2026-01-01T00:00:01Z", **members
        ),
        JSON,
    )


def failed(state, bytes_transferred, error, **members):
    return (
        200,
        historical_status(state, bytes_transferred, error=error, **members),
        JSON,
    )


# A request storage has not recorded the outcome of yet.
STARTED = (200, historical_status("started", None), JSON)


class StatusTestCase(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)
        for name in ("DEFAULT_RANGE_SIZE", "READ_RANGE_SIZE"):
            patch = mock.patch("files_sdk.download." + name, RANGE)
            patch.start()
            self.addCleanup(patch.stop)

    def client(self, service, **settings):
        return self.client_with(service, api_key="key", **settings)

    def client_with(self, service, **settings):
        client = files_sdk.Client(
            base_url=service.url,
            **{"initial_network_retry_delay": 0, **settings},
        )
        self.addCleanup(client.close)
        return client

    def existing(self, data=b"old content", name="out.bin"):
        path = self.scratch / name
        path.write_bytes(data)
        return path

    def stages(self):
        return sdk_entries(self.scratch)

    def service(self, data, request_id="request-1", unsized="full"):
        """A file storage serves whole, without a download identity, naming
        each successful answer with request_id; unsized answers have no
        Content-Length."""
        service = DownloadService(self, data)
        service.identity = "absent"
        service.request_id = request_id
        service.whole_unsized = unsized
        return service

    def assertNothingPublished(self, path):
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])

    def assertUnconfirmed(self, service, why, sizes=(3000, 0)):
        """Every way of downloading a file of each size in sizes, whose
        unsized response service answers, fails as unconfirmed for why, with
        nothing published."""
        for size in sizes:
            data = content(size)
            service.content = data
            service.reported_size = size
            with self.subTest(size=size, how="download_file"):
                path = self.existing()
                with self.assertRaisesRegex(
                    APIConnectionError, "could not be confirmed.*" + why
                ) as caught:
                    self.client(
                        service, max_network_retries=0
                    ).file.download_file("a.bin", path)
                self.assertIn("Nothing was written.", str(caught.exception))
                self.assertNothingPublished(path)
            with self.subTest(size=size, how="download_stream"):
                output = io.BytesIO()
                with self.assertRaisesRegex(
                    APIConnectionError, "could not be confirmed.*" + why
                ):
                    self.client(
                        service, max_network_retries=0
                    ).file.download_stream("a.bin", output)
            with self.subTest(size=size, how="open"):
                with self.client(service, max_network_retries=0).file.open(
                    "a.bin", "rb"
                ) as remote:
                    with self.assertRaisesRegex(
                        APIConnectionError, "could not be confirmed.*" + why
                    ):
                        remote.read()
        return caught.exception


class TestConfirmingAnUnsizedDownload(StatusTestCase):
    def test_storage_s_status_confirms_a_file_whose_response_declared_no_size(
        self,
    ):
        data = content(5000)
        reauthentication = {
            "headers": {"X-Files-Reauthentication": "password:secret"}
        }
        for credentials in (
            dict(api_key="key", workspace_id=7, **reauthentication),
            dict(session_id="session", **reauthentication),
        ):
            with self.subTest(credentials=sorted(credentials)):
                service = self.service(data)
                service.statuses["request-1"] = completed(len(data))
                client = self.client_with(service, **credentials)
                with self.assertLogs("files_sdk", logging.INFO) as logs:
                    client.file.download_file("a.bin", self.scratch / "a.bin")

                self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
                [status] = service.status_requests()
                [download] = service.storage_requests()
                # The download URL joined with the request's ID, with its query
                # (and the signature in it) as it was.
                self.assertEqual(status["path"], "/storage/file/request-1")
                self.assertEqual(status["query"], download["query"])
                self.assertIn("X-Amz-Signature=secret", status["query"])
                sent = {name.lower() for name in status["headers"]}
                self.assertEqual(sent & set(FILES_HEADERS), set())
                self.assertIn(
                    "Files.com Python SDK", status["headers"]["User-Agent"]
                )
                # Neither the signed URL nor the request's ID is logged.
                self.assertNotIn("secret", "\n".join(logs.output))
                self.assertNotIn("request-1", "\n".join(logs.output))

    def test_a_file_of_no_bytes_is_confirmed_by_a_completed_count_of_none(
        self,
    ):
        service = self.service(b"")
        service.statuses["request-1"] = completed(0)
        self.client(service).file.download_file(
            "empty.bin", self.scratch / "empty.bin"
        )
        self.assertEqual((self.scratch / "empty.bin").read_bytes(), b"")
        output = io.BytesIO()
        self.client(service).file.download_stream("empty.bin", output)
        with self.client(service).file.open("empty.bin", "rb") as remote:
            self.assertEqual(remote.read(), b"")
        self.assertEqual(len(service.status_requests()), 3)

    def test_a_short_file_storage_reports_sending_whole_is_not_published(self):
        data = content(5000)
        service = self.service(data, unsized="short")
        service.statuses["request-1"] = completed(len(data))
        path = self.existing()
        with self.assertRaisesRegex(
            APIConnectionError,
            "ended after 2500 bytes, but file storage's status of the download request reports "
            "5000 bytes transferred",
        ):
            self.client(service).file.download_file("a.bin", path)
        self.assertNothingPublished(path)

        output = io.BytesIO()
        with self.assertRaisesRegex(
            APIConnectionError, "The stream has already received them"
        ):
            self.client(service).file.download_stream("a.bin", output)
        self.assertEqual(output.getvalue(), data[:2500])

        with self.client(service).file.open("a.bin", "rb") as remote:
            with self.assertRaisesRegex(
                APIConnectionError, "ended after 2500 bytes"
            ) as caught:
                remote.read()
        self.assertEqual(
            caught.exception.download_request_status.bytes_transferred, 5000
        )

    def test_a_request_storage_reports_failed_fails_with_its_explanation(self):
        # As the producer answers for a request that failed: HTTP 200, the
        # stored error and its type at the top, http_code with an underscore.
        data = content(3000)
        for state in ("failed", "error"):
            with self.subTest(state=state):
                service = self.service(data)
                service.statuses["request-1"] = failed(
                    state,
                    1200,
                    "the remote server closed the connection",
                    type="remote_server_error",
                    http_code=502,
                )
                path = self.existing()
                with self.assertRaises(APIError) as caught:
                    self.client(service).file.download_file("a.bin", path)
                error = caught.exception
                self.assertIs(type(error), APIError)
                self.assertIn(
                    "did not complete: the remote server closed the connection (status {}, 1200 bytes "
                    "transferred). Nothing was written.".format(state),
                    str(error),
                )
                self.assertEqual(error.http_status, 502)
                self.assertEqual(error.download_request_status.status, state)
                self.assertEqual(
                    error.download_request_status.type, "remote_server_error"
                )
                self.assertNothingPublished(path)

    def test_the_go_sdk_s_spelling_of_http_code_is_read_only_without_the_producer_s(
        self,
    ):
        data = content(3000)
        for label, members, code in (
            ("http-code alone", {"http-code": 503}, 503),
            ("both", {"http_code": 500, "http-code": 503}, 500),
            ("http_code alone", {"http_code": 500}, 500),
            ("neither", {}, None),
        ):
            with self.subTest(label):
                document = historical_status("failed", 0, error="stopped")
                del document["http_code"]
                document.update(members)
                service = self.service(data)
                service.statuses["request-1"] = (200, document, JSON)
                with self.assertRaises(APIError) as caught:
                    self.client(service).file.download_file(
                        "a.bin", self.existing()
                    )
                self.assertEqual(caught.exception.http_status, code)
                self.assertEqual(
                    caught.exception.download_request_status.http_code, code
                )

    def test_a_status_that_cannot_be_read_leaves_the_file_unconfirmed_and_unpublished(
        self,
    ):
        for label, status, why in (
            # The producer's 404 for a request it does not know, or no longer does.
            (
                "an unknown request",
                None,
                r"could not be read \(HTTP 404, download_request_not_found\)",
            ),
            (
                "an error answer of another kind",
                (403, b"denied", "text/plain"),
                r"could not be read \(HTTP 403\)",
            ),
            (
                "a count that is not a number",
                (
                    200,
                    {
                        "data": {
                            "status": "completed",
                            "bytes_transferred": "3000",
                        }
                    },
                    JSON,
                ),
                r"its bytes_transferred is not a whole number",
            ),
            (
                "not JSON",
                (200, b"<html>ok</html>", "text/html"),
                r"it is not a JSON document",
            ),
            (
                "a JSON string",
                (200, "completed", JSON),
                r"it is a JSON str, not an object",
            ),
            (
                "a document too large",
                (
                    200,
                    {"data": {"status": "completed"}, "pad": "x" * 70000},
                    JSON,
                ),
                r"it is larger than 65536 bytes",
            ),
        ):
            with self.subTest(label):
                service = self.service(b"")
                if status is not None:
                    service.statuses["request-1"] = status
                error = self.assertUnconfirmed(service, why)
                self.assertIsNotNone(error.__cause__)
                self.assertIsNone(error.download_request_status)

    def test_an_absent_request_never_confirms_a_download_of_no_bytes(self):
        # The producer's 404 carries no status and no count: it confirms
        # nothing, not even that no bytes were to arrive.
        service = self.service(b"")
        error = self.assertUnconfirmed(
            service, "download_request_not_found", sizes=(0,)
        )
        self.assertIsInstance(error.__cause__, APIError)
        self.assertEqual(error.__cause__.http_status, 404)
        self.assertEqual(len(service.status_requests()), 3)

    def test_a_status_that_does_not_report_a_completed_count_confirms_nothing(
        self,
    ):
        for label, document, why in (
            (
                "completed, without a count",
                historical_status("completed", None),
                "reports no count of the bytes",
            ),
            (
                "no state",
                {"data": {"bytes_transferred": 3000}},
                "does not report that the request completed",
            ),
            (
                "a state of another protocol",
                historical_status("finished", 3000),
                "does not report that the request completed",
            ),
            # A count while started is no contract: it confirms nothing.
            (
                "still started, with a count",
                historical_status("started", 3000),
                "still reports the request started",
            ),
        ):
            with self.subTest(label):
                service = self.service(b"")
                service.statuses["request-1"] = (200, document, JSON)
                error = self.assertUnconfirmed(service, why)
                self.assertIsNotNone(error.download_request_status)

    def test_a_short_file_whose_request_is_still_started_is_not_published(
        self,
    ):
        # The response ends early but well framed, and storage has not
        # recorded the request's outcome: nothing shows the file is whole.
        data = content(5000)
        service = self.service(data, unsized="short")
        service.statuses["request-1"] = STARTED
        path = self.existing()
        with self.assertRaisesRegex(
            APIConnectionError,
            "could not be confirmed.*still reports the request started",
        ) as caught:
            self.client(service, max_network_retries=2).file.download_file(
                "a.bin", path
            )
        self.assertIn("Nothing was written.", str(caught.exception))
        self.assertEqual(
            caught.exception.download_request_status.status, "started"
        )
        self.assertNothingPublished(path)
        # Read once, then again for each retry.
        self.assertEqual(len(service.status_requests()), 3)

        output = io.BytesIO()
        with self.assertRaisesRegex(
            APIConnectionError,
            "still reports the request started.*The stream has already received them",
        ):
            self.client(service).file.download_stream("a.bin", output)
        self.assertEqual(output.getvalue(), data[:2500])

        with self.client(service).file.open("a.bin", "rb") as remote:
            with self.assertRaisesRegex(
                APIConnectionError, "still reports the request started"
            ):
                remote.read()

    def test_a_status_still_started_is_read_again_until_storage_reports_an_outcome(
        self,
    ):
        full, short = content(3000), content(5000)
        for label, data, unsized, answers, outcome in (
            (
                "completed with the bytes received",
                full,
                "full",
                [STARTED, STARTED, completed(3000)],
                None,
            ),
            (
                "completed with bytes that did not all arrive",
                short,
                "short",
                [STARTED, completed(5000)],
                (APIConnectionError, "ended after 2500 bytes"),
            ),
            (
                "failed",
                full,
                "full",
                [
                    STARTED,
                    failed(
                        "failed",
                        1200,
                        "the remote server closed the connection",
                    ),
                ],
                (APIError, "did not complete"),
            ),
        ):
            with self.subTest(label):
                service = self.service(data, unsized=unsized)
                service.statuses["request-1"] = answers
                path = self.existing()
                if outcome is None:
                    self.client(service).file.download_file("a.bin", path)
                    self.assertEqual(path.read_bytes(), data)
                    self.assertEqual(self.stages(), [])
                else:
                    with self.assertRaisesRegex(*outcome):
                        self.client(service).file.download_file("a.bin", path)
                    self.assertNothingPublished(path)
                self.assertEqual(
                    len(service.status_requests()), 3 if outcome is None else 2
                )

    def test_cancelling_or_running_out_of_time_while_waiting_for_a_started_request_stops_the_download(
        self,
    ):
        data = content(3000)
        for label, error_class in (
            ("cancelled", OperationCancelledError),
            ("out of time", DeadlineExceededError),
        ):
            with self.subTest(label):
                service = self.service(data)
                service.statuses["request-1"] = STARTED
                if label == "cancelled":
                    token = files_sdk.CancellationToken()
                    options: dict = {"cancel_token": token}

                    def cancel_soon(_headers, token=token):
                        # Once the status has answered started, while the
                        # download waits to read it again.
                        timer = threading.Timer(0.2, token.cancel)
                        self.addCleanup(timer.cancel)
                        timer.start()

                    service.on_status = cancel_soon
                else:
                    options = {"request_timeout": 1}
                path = self.existing()
                # A wait far longer than either stop takes.
                client = self.client(
                    service,
                    initial_network_retry_delay=30,
                    max_network_retry_delay=30,
                )
                started = time.monotonic()
                with (
                    self.assertLogs("files_sdk", logging.INFO) as logs,
                    self.assertRaises(error_class),
                ):
                    client.file.download_file("a.bin", path, options)
                self.assertLess(time.monotonic() - started, 10)
                # It stopped in the wait, after one read.
                self.assertIn(
                    "Waiting for the download request status",
                    "\n".join(logs.output),
                )
                self.assertEqual(len(service.status_requests()), 1)
                self.assertNothingPublished(path)

    def test_the_request_s_times_are_not_read(self):
        # How the producer encodes them is not known.
        data = content(3000)
        for started_at in (
            "2026-01-01T00:00:00Z",
            1767225600,
            None,
            {"seconds": 1},
        ):
            with self.subTest(started_at=started_at):
                service = self.service(data)
                service.statuses["request-1"] = completed(
                    len(data), started_at=started_at
                )
                self.client(service).file.download_file(
                    "a.bin", self.scratch / "a.bin"
                )
                self.assertEqual((self.scratch / "a.bin").read_bytes(), data)

    def test_an_encoded_response_is_confirmed_with_the_bytes_it_decodes_to(
        self,
    ):
        data = content(4000)
        service = self.service(data, unsized=None)
        service.gzip = "whole"
        service.statuses["request-1"] = completed(len(data))
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        self.assertEqual(len(service.status_requests()), 1)

    def test_the_status_request_follows_a_redirect_without_files_credentials(
        self,
    ):
        data = content(3000)
        service = self.service(data)
        elsewhere = DownloadService(self, b"")
        elsewhere.statuses["request-1"] = completed(len(data))
        service.statuses["request-1"] = (
            "redirect",
            elsewhere.url + "/storage/file/request-1",
        )
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        [followed] = elsewhere.status_requests()
        self.assertEqual(
            {name.lower() for name in followed["headers"]}
            & set(FILES_HEADERS),
            set(),
        )

    def test_cancelling_while_the_status_is_read_cancels_the_download(self):
        data = content(3000)
        service = self.service(data)
        token = files_sdk.CancellationToken()
        release = threading.Event()
        self.addCleanup(release.set)

        def hold(_headers):
            token.cancel()
            release.wait(10)

        service.on_status = hold
        service.statuses["request-1"] = completed(len(data))
        path = self.existing()
        started = time.monotonic()
        with self.assertRaises(OperationCancelledError):
            self.client(service).file.download_file(
                "a.bin", path, {"cancel_token": token}
            )
        self.assertLess(time.monotonic() - started, 5)
        self.assertNothingPublished(path)


class TestDownloadsTheStatusDoesNotConcern(StatusTestCase):
    def test_a_sized_response_is_not_checked_against_a_status(self):
        data = content(3000)
        service = self.service(data, unsized=None)
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        self.assertEqual(service.status_requests(), [])

    def test_an_unsized_response_that_names_no_request_cannot_be_confirmed_and_is_kept(
        self,
    ):
        # Nothing names a request whose status could say otherwise.
        data = content(3000)
        service = self.service(data, request_id=None)
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        self.assertEqual(service.status_requests(), [])

    def test_a_request_id_that_would_change_the_url_is_not_joined_to_it(self):
        data = content(3000)
        for request_id in (
            "../file",
            "a/b",
            "a?b=c",
            "%2e%2e",
            ".hidden",
            "a b",
        ):
            with self.subTest(request_id=request_id):
                service = self.service(data, request_id=request_id)
                self.client(service).file.download_file(
                    "a.bin", self.scratch / "a.bin"
                )
                self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
                self.assertEqual(service.status_requests(), [])

    def test_an_identified_download_never_reads_a_status(self):
        # Its ranges are checked against the size its identity gives, even
        # where storage names its error answers too.
        data = content(5000)
        service = DownloadService(self, data)
        service.request_id = "request-1"
        service.request_id_on_errors = True
        service.statuses["request-1"] = completed(1)
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        service.fail(0, status=404, times=5)
        path = self.existing()
        with self.assertRaises(APIError):
            self.client(service).file.download_file("a.bin", path)
        self.assertEqual(service.status_requests(), [])


class TestExplainingStorage_sError(StatusTestCase):
    def refused(self, request_id="request-1"):
        # The producer of the status protocol names no error answer; these
        # tests' storage does, as the Go SDK allows for.
        service = self.service(
            content(3000), request_id=request_id, unsized=None
        )
        service.request_id_on_errors = True
        service.first_answer = (404, b"<Error><Code>NoSuchKey</Code></Error>")
        return service

    def test_storage_s_error_carries_the_request_s_explanation(self):
        explanation = failed(
            "error",
            0,
            "permission denied on the remote server",
            type="remote_server_error",
            http_code=403,
        )
        for how in ("download_file", "download_stream", "open"):
            with self.subTest(how=how):
                service = self.refused()
                service.statuses["request-1"] = explanation
                client = self.client(service, max_network_retries=0)
                with self.assertRaises(APIError) as caught:
                    if how == "download_file":
                        client.file.download_file("a.bin", self.existing())
                    elif how == "download_stream":
                        client.file.download_stream("a.bin", io.BytesIO())
                    else:
                        with client.file.open("a.bin", "rb") as remote:
                            remote.read()
                error = caught.exception
                # Still storage's answer: the same error, naming the file,
                # with the explanation added.
                self.assertIs(type(error), APIError)
                self.assertEqual(error.http_status, 404)
                self.assertEqual(
                    str(error),
                    "HTTP 404 Transfer request failed for the download of a.bin",
                )
                self.assertEqual(
                    error.download_request_status.error,
                    "permission denied on the remote server",
                )
                self.assertEqual(error.download_request_status.http_code, 403)
                self.assertEqual(
                    error.__notes__,
                    [
                        "File storage's status of this download request: "
                        "permission denied on the remote server (status error, 0 bytes transferred)"
                    ],
                )
                self.assertEqual(len(service.status_requests()), 1)

    def test_the_producer_s_error_answers_read_no_status(self):
        # They name no request, so there is none to explain them.
        service = self.refused()
        service.request_id_on_errors = False
        service.statuses["request-1"] = failed("error", 0, "denied")
        with self.assertRaises(APIError) as caught:
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", self.existing()
            )
        self.assertEqual(caught.exception.http_status, 404)
        self.assertIsNone(caught.exception.download_request_status)
        self.assertEqual(service.status_requests(), [])

    def test_a_status_that_cannot_be_read_or_explains_nothing_leaves_the_error_as_it_was(
        self,
    ):
        for label, status in (
            # Its 404 has an error of its own, which explains nothing of the download's.
            ("an unknown request", None),
            ("no error", failed("failed", 0, None)),
            ("not JSON", (200, b"<html/>", "text/html")),
            ("unreadable", (200, b"{", JSON)),
        ):
            with self.subTest(label):
                service = self.refused()
                if status is not None:
                    service.statuses["request-1"] = status
                with self.assertRaises(APIError) as caught:
                    self.client(
                        service, max_network_retries=0
                    ).file.download_file("a.bin", self.existing())
                self.assertEqual(caught.exception.http_status, 404)
                self.assertIsNone(caught.exception.download_request_status)
                self.assertFalse(getattr(caught.exception, "__notes__", None))
                self.assertEqual(len(service.status_requests()), 1)

    def test_an_explanation_quoting_a_signed_url_is_redacted(self):
        service = self.refused()
        service.statuses["request-1"] = failed(
            "error",
            0,
            "could not read https://user:pw@mount.example/x?signature=abc",
        )
        with self.assertRaises(APIError) as caught:
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", self.existing()
            )
        [note] = caught.exception.__notes__
        self.assertIn("https://[redacted]@mount.example/x?[redacted]", note)
        self.assertNotIn("pw", note)

    def test_cancelling_while_explaining_keeps_storage_s_error(self):
        service = self.refused()
        token = files_sdk.CancellationToken()
        release = threading.Event()
        self.addCleanup(release.set)

        def hold(_headers):
            token.cancel()
            release.wait(10)

        service.on_status = hold
        service.statuses["request-1"] = failed("error", 0, "late")
        path = self.existing()
        with self.assertRaises(APIError) as caught:
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", path, {"cancel_token": token}
            )
        self.assertEqual(caught.exception.http_status, 404)
        self.assertIsNone(caught.exception.download_request_status)
        self.assertNothingPublished(path)

    def test_errors_without_a_request_id_or_for_an_expired_url_read_no_status(
        self,
    ):
        service = self.refused(request_id=None)
        with self.assertRaises(APIError):
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", self.existing()
            )
        self.assertEqual(service.status_requests(), [])

        service = self.service(content(3000), unsized=None)
        service.request_id_on_errors = True
        service.refuse_all = (
            True  # Every URL refused as expired: renewed, never explained.
        )
        service.statuses["request-1"] = failed("error", 0, "expired")
        with self.assertRaises(APIError) as caught:
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", self.existing()
            )
        self.assertEqual(caught.exception.http_status, 403)
        self.assertEqual(service.status_requests(), [])
        self.assertGreater(len(service.uris), 1)

    def test_the_status_url_is_the_download_url_joined_with_the_id(self):
        # The producer's IDs are 25 letters and digits.
        for request_id in ("Zx9aB3kLmN0pQr5StUv7WxY2z", "3f2a-9c_1~z"):
            with self.subTest(request_id=request_id):
                service = self.refused(request_id=request_id)
                service.statuses[request_id] = failed(
                    "error", 0, "denied", request_id=request_id
                )
                with self.assertRaises(APIError) as caught:
                    self.client(
                        service, max_network_retries=0
                    ).file.download_file("a.bin", self.existing())
                self.assertEqual(
                    caught.exception.download_request_status.error, "denied"
                )
                [status] = service.status_requests()
                [download] = service.storage_requests()
                self.assertEqual(
                    (status["path"], status["query"]),
                    ("/storage/file/" + request_id, download["query"]),
                )
                self.assertEqual(
                    urlsplit(service.uris[0]).path, "/storage/file"
                )
