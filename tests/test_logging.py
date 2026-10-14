import io
import logging
import subprocess
import sys
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

import files_sdk
from files_sdk.api_client import ApiClient
from files_sdk.error import NotFoundError
from tests.loopback_api import start_loopback_api

SECRETS = ("canarykey42", "X-Amz-Signature", "private-signature")


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.api = start_loopback_api(self)
        self.client = files_sdk.Client(
            api_key="canarykey42", base_url=self.api.url
        )
        self.addCleanup(self.client.close)
        # The module facade's transfers: a plain-HTTP API, like the stand-in.
        patcher = patch.object(files_sdk, "base_url", self.api.url)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_an_application_that_has_not_configured_logging_sees_nothing(self):
        # A fresh interpreter, so the test runner's logging setup cannot hide
        # output: an API error (logged at ERROR) prints nothing.
        self.api.reply_json(
            {"type": "not-found", "error": "Not Found"}, status=404
        )
        code = (
            "import files_sdk\n"
            "client = files_sdk.Client(api_key='canarykey42', base_url={!r})\n"
            "try:\n"
            "    client.user.find(1)\n"
            "except files_sdk.error.NotFoundError:\n"
            "    print('raised')\n"
        ).format(self.api.url)
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=60,
        )

        self.assertEqual(("raised\n", ""), (result.stdout, result.stderr))
        self.assertEqual(1, len(self.api.requests))

    def test_logs_below_debug_are_safe_and_debug_has_the_details(self):
        self.api.reply_json({"id": 1, "name": "Pat"})
        self.api.reply_json(
            {"type": "not-found", "error": "Not Found"}, status=404
        )
        storage = (
            self.api.url + "/storage/part?X-Amz-Signature=private-signature"
        )
        self.api.reply(200)

        with self.assertLogs("files_sdk", level=logging.DEBUG) as logs:
            self.client.user.find(1)
            with self.assertRaises(NotFoundError) as caught:
                self.client.user.find(2)
            ApiClient().send_remote_request("PUT", storage, body=b"part body")

        ordinary = "\n".join(
            r.getMessage() for r in logs.records if r.levelno > logging.DEBUG
        )
        detailed = "\n".join(
            r.getMessage() for r in logs.records if r.levelno == logging.DEBUG
        )
        for secret in SECRETS:
            self.assertNotIn(secret, ordinary)
            self.assertNotIn(secret, str(caught.exception))
        self.assertIn("method=GET", ordinary)
        self.assertIn("status=404", ordinary)
        self.assertIn("private-signature", detailed)
        self.assertIn('"name": "Pat"', detailed)
        self.assertIn("part body", detailed)

    def test_debug_logs_the_headers_of_api_requests_and_responses(self):
        self.api.reply_json(
            {"id": 1, "name": "Pat"},
            headers={"X-Response-Marker": "response-marker-77"},
        )

        with self.assertLogs("files_sdk", level=logging.DEBUG) as logs:
            user = self.client.user.find(
                1, None, {"headers": {"X-Request-Marker": "request-marker-77"}}
            )

        self.assertEqual(1, user.id)
        self.assertEqual(
            "request-marker-77",
            self.api.requests[0].headers["X-Request-Marker"],
        )
        ordinary = "\n".join(
            r.getMessage() for r in logs.records if r.levelno > logging.DEBUG
        )
        detailed = "\n".join(
            r.getMessage() for r in logs.records if r.levelno == logging.DEBUG
        )
        for text in (
            "X-Request-Marker",
            "request-marker-77",
            "X-Response-Marker",
            "response-marker-77",
        ):
            self.assertIn(text, detailed)
            self.assertNotIn(text, ordinary)

    def test_debug_logs_a_download_as_it_streams(self):
        body = bytes(range(256)) * 64  # Two 8 KiB chunks.
        self.api.reply(200, body)
        output = io.BytesIO()

        with self.assertLogs("files_sdk", level=logging.DEBUG) as logs:
            ApiClient().stream_download(
                self.api.url + "/storage/object", output
            )

        chunks = [
            r.getMessage()
            for r in logs.records
            if "Download body" in r.getMessage()
        ]
        self.assertEqual(2, len(chunks))
        self.assertIn("offset=8192", chunks[1])
        self.assertEqual(body, output.getvalue())

    def test_console_log_level_still_prints_to_standard_error(self):
        self.api.reply_json([])
        stderr = io.StringIO()
        with (
            patch.object(files_sdk, "console_log_level", "info"),
            redirect_stderr(stderr),
        ):
            self.client.user.list()

        self.assertIn("INFO message=Request", stderr.getvalue())
        self.assertNotIn("canarykey42", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
