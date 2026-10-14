import json
import traceback
import unittest
from unittest.mock import patch

import files_sdk
import requests
from files_sdk.error import APIConnectionError, APIError, NotFoundError

HTML_PAGE = b"<html><head><title>502 Bad Gateway</title></head><body>files.com</body></html>"
# URLs as an API error might quote them, and how public error text shows them.
URLS_WITH_CREDENTIALS = (
    (
        "https://transfer.example.invalid/file?X-Amz-Credential=private-credential&X-Amz-Signature=private-signature",
        "https://transfer.example.invalid/file?[redacted]",
    ),
    (
        "https://user:private-password@mirror.example.invalid/path?sig=private-query#private-fragment",
        "https://[redacted]@mirror.example.invalid/path?[redacted]",
    ),
    (
        "https://user:private-password@mirror.example.invalid/retry",
        "https://[redacted]@mirror.example.invalid/retry",
    ),
    (
        "'https://a.example/x','https://user:private-password@b.example/y?token=private-query'.",
        "'https://a.example/x','https://[redacted]@b.example/y?[redacted]",
    ),
    (
        "https://bucket.example/O'Brien/key.txt?token=private-query",
        "https://bucket.example/O'Brien/key.txt?[redacted]",
    ),
    (
        "https://a.example/x?next=https://c.example/z&X-Amz-Signature=private-query",
        "https://a.example/x?[redacted]",
    ),
)


def http_response(status, body, content_type="application/json"):
    response = requests.Response()
    response.status_code = status
    response.headers["Content-Type"] = content_type
    response.headers["X-Request-Id"] = "request-7"
    response._content = body
    return response


@patch.object(requests.Session, "send")
class TestApiErrors(unittest.TestCase):
    def setUp(self):
        super().setUp()
        files_sdk.set_api_key("testkey")
        for name in ("initial_network_retry_delay", "max_network_retry_delay"):
            patcher = patch.object(files_sdk, name, 0)
            patcher.start()
            self.addCleanup(patcher.stop)

    def raise_for(self, mock_send, response, expected_error):
        mock_send.return_value = response
        with self.assertRaises(expected_error) as context:
            files_sdk.workspace.find(1)
        return context.exception

    def test_not_found(self, mock_send):
        r = requests.Response()
        r.status_code = 404
        r.headers = {
            "content-type": "application/json; charset=utf8",
        }
        r.json = lambda: {
            "type": "not-found",
            "http-code": 404,
            "error": "Not Found.  This may be related to your permissions.",
            "title": "Not Found",
        }
        mock_send.return_value = r

        with self.assertRaises(files_sdk.error.NotFoundError) as context:
            for f in files_sdk.folder.list_for("/missing").auto_paging_iter():
                pass

        self.assertEqual(context.exception.code, 404)
        self.assertEqual(
            str(context.exception),
            "HTTP 404 Not Found.  This may be related to your permissions.",
        )
        self.assertIn("content-type", context.exception.headers)
        self.assertEqual(
            context.exception.headers["content-type"],
            "application/json; charset=utf8",
        )
        self.assertEqual(context.exception.title, "Not Found")
        self.assertEqual(context.exception.error_type, "not-found")
        self.assertEqual(context.exception.http_code, 404)

    def test_bad_gateway(self, mock_send):
        mock_send.return_value = http_response(503, HTML_PAGE, "text/html")

        with self.assertRaises(files_sdk.error.APIConnectionError) as context:
            for f in files_sdk.folder.list_for("/").auto_paging_iter():
                pass

        self.assertEqual(503, context.exception.http_status)
        self.assertTrue(str(context.exception).startswith("HTTP 503 "))
        self.assertNotIn("Bad Gateway", str(context.exception))
        self.assertEqual(
            "text/html", context.exception.headers["Content-Type"]
        )

    def test_hostname_mismatch(self, mock_send):
        error_msg = "You have connected to a URL that has different security settings than those required for your site."
        r = requests.Response()
        r.status_code = 403
        r.headers = {
            "content-type": "application/json; charset=utf8",
            "x-files-host": "test.example.com",
        }
        r.json = lambda: {
            "type": "not-authenticated/lockout-region-mismatch",
            "http-code": 403,
            "title": "Lockout Region Mismatch",
            "error": error_msg,
            "data": {
                "host": "test.example.com",
            },
        }
        mock_send.return_value = r

        with self.assertRaises(
            files_sdk.error.LockoutRegionMismatchError
        ) as context:
            for f in files_sdk.folder.list_for("/").auto_paging_iter():
                pass

        self.assertEqual(context.exception.code, 403)
        self.assertIn(error_msg, str(context.exception))
        self.assertIn("x-files-host", context.exception.headers)
        self.assertEqual(
            context.exception.headers["x-files-host"], "test.example.com"
        )
        self.assertEqual(context.exception.data["host"], "test.example.com")
        self.assertEqual(context.exception.title, "Lockout Region Mismatch")
        self.assertEqual(
            context.exception.error_type,
            "not-authenticated/lockout-region-mismatch",
        )
        self.assertEqual(context.exception.http_code, 403)

    def test_region_mismatch(self, mock_send):
        error_msg = "Your account must login using a different server, https://test.host."
        r = requests.Response()
        r.status_code = 401
        r.headers = {
            "content-type": "application/json; charset=utf8",
        }
        r.json = lambda: {
            "type": "not-authenticated/lockout-region-mismatch",
            "http-code": 401,
            "title": "Lockout Region Mismatch",
            "error": error_msg,
            "data": {
                "host": "test.example.com",
            },
        }
        mock_send.return_value = r

        with self.assertRaises(
            files_sdk.error.LockoutRegionMismatchError
        ) as context:
            for f in files_sdk.folder.list_for("/").auto_paging_iter():
                pass

        self.assertEqual(context.exception.code, 401)
        self.assertEqual(str(context.exception), f"HTTP 401 {error_msg}")
        self.assertIn("content-type", context.exception.headers)
        self.assertEqual(
            context.exception.headers["content-type"],
            "application/json; charset=utf8",
        )
        self.assertEqual(context.exception.data["host"], "test.example.com")
        self.assertEqual(context.exception.title, "Lockout Region Mismatch")
        self.assertEqual(
            context.exception.error_type,
            "not-authenticated/lockout-region-mismatch",
        )
        self.assertEqual(context.exception.http_code, 401)

    def test_known_error_types_raise_their_class_at_any_status(
        self, mock_send
    ):
        body = {
            "type": "not-found",
            "error": "Workspace not found.",
            "title": "Not Found",
        }
        for status in (400, 404, 500, 503):
            with self.subTest(status=status):
                error = self.raise_for(
                    mock_send,
                    http_response(status, json.dumps(body).encode()),
                    NotFoundError,
                )

                self.assertEqual(status, error.http_status)
                self.assertEqual(status, error.code)
                self.assertEqual(body, error.json_body)
                self.assertEqual("request-7", error.headers["X-Request-Id"])
                self.assertEqual(
                    f"HTTP {status} Workspace not found.", str(error)
                )

    def test_error_objects_without_a_known_string_type_raise_api_error(
        self, mock_send
    ):
        for label, error_type in (
            ("unknown", "brand-new/kind-of-failure"),
            ("empty", ""),
            ("null", None),
            ("integer", 7),
            ("object", {"name": "not-found"}),
            ("list", ["not-found"]),
        ):
            for status in (422, 500):
                with self.subTest(type=label, status=status):
                    body = {
                        "type": error_type,
                        "error": "sentinel",
                        "title": "Sentinel",
                    }
                    error = self.raise_for(
                        mock_send,
                        http_response(status, json.dumps(body).encode()),
                        APIError,
                    )

                    self.assertIs(APIError, type(error))
                    self.assertEqual(f"HTTP {status} sentinel", str(error))
                    self.assertEqual(status, error.http_status)
                    self.assertEqual(error_type, error.error_type)
                    self.assertEqual("Sentinel", error.title)
                    self.assertEqual(
                        "request-7", error.headers["X-Request-Id"]
                    )

        with self.subTest(type="missing"):
            error = self.raise_for(
                mock_send,
                http_response(404, b'{"error": "sentinel"}'),
                APIError,
            )
            self.assertIs(APIError, type(error))
            self.assertEqual("HTTP 404 sentinel", str(error))
            self.assertIsNone(error.error_type)

    def test_responses_that_are_not_error_objects_raise_api_connection_error(
        self, mock_send
    ):
        for label, body, content_type in (
            ("null", b"null", "application/json"),
            (
                "array",
                b'[{"type": "not-found", "error": "sentinel"}]',
                "application/json",
            ),
            ("number", b"42", "application/json"),
            ("string", b'"sentinel error"', "application/json"),
            ("malformed", b'{"error": "sentinel"', "application/json"),
            ("html", HTML_PAGE, "text/html"),
        ):
            for status in (403, 404, 502, 503):
                with self.subTest(body=label, status=status):
                    error = self.raise_for(
                        mock_send,
                        http_response(status, body, content_type),
                        APIConnectionError,
                    )

                    self.assertNotIsInstance(error, APIError)
                    self.assertEqual(status, error.http_status)
                    self.assertEqual(
                        content_type, error.headers["Content-Type"]
                    )
                    self.assertNotIn("sentinel", str(error))
                    self.assertNotIn("Bad Gateway", str(error))

    def test_a_successful_status_with_an_unreadable_body_raises_api_connection_error(
        self, mock_send
    ):
        error = self.raise_for(
            mock_send,
            http_response(200, HTML_PAGE, "text/html"),
            APIConnectionError,
        )

        self.assertEqual(200, error.http_status)
        self.assertNotIn("Bad Gateway", str(error))

    def test_error_text_and_logs_never_include_url_credentials(
        self, mock_send
    ):
        rejected = "Upload rejected: " + " ".join(
            raw for raw, _ in URLS_WITH_CREDENTIALS
        )
        for label, body, expected_error in (
            ("error", {"error": rejected}, APIError),
            ("errors", {"errors": [{"message": rejected}]}, APIError),
            ("title", {"title": rejected}, APIError),
            ("typed", {"type": "not-found", "error": rejected}, NotFoundError),
        ):
            with self.subTest(body=label):
                with self.assertLogs("files_sdk", level="INFO") as logs:
                    error = self.raise_for(
                        mock_send,
                        http_response(422, json.dumps(body).encode()),
                        expected_error,
                    )

                public_text = [
                    str(error),
                    repr(error),
                    "".join(
                        traceback.format_exception(
                            type(error), error, error.__traceback__
                        )
                    ),
                    *logs.output,
                ]
                for text in public_text:
                    self.assertNotIn("private-", text)
                self.assertEqual(
                    "HTTP 422 Upload rejected: "
                    + " ".join(public for _, public in URLS_WITH_CREDENTIALS),
                    str(error),
                )
                self.assertEqual(body, error.json_body)


if __name__ == "__main__":
    unittest.main()
