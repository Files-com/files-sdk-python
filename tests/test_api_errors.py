import json
import unittest
from unittest.mock import patch

import files_sdk
import requests

@patch.object(requests.Session, "send")
class TestApiErrors(unittest.TestCase):
    def setUp(self):
        super().setUp()
        files_sdk.set_api_key("testkey")

    def test_not_found(self, mock_send):
        r = requests.Response()
        r.status_code = 404
        r.headers = {
            "content-type": "application/json; charset=utf8",
        }
        r.json = lambda: {
            "type": "not-found/folder-not-found",
            "http-code": 404,
            "error": "Folder missing not found.",
        }
        mock_send.return_value = r

        with self.assertRaises(files_sdk.error.NotFoundError) as context:
            for f in files_sdk.folder.list_for("/missing").auto_paging_iter():
                pass
        
        self.assertEqual(context.exception.code, 404)
        self.assertEqual(str(context.exception), "HTTP 404 Folder missing not found.")
        self.assertIn("content-type", context.exception.headers)
        self.assertEqual(context.exception.headers["content-type"], "application/json; charset=utf8")

    def test_bad_gateway(self, mock_send):
        r = unittest.mock.MagicMock(spec=requests.Response)
        r.status_code = 503
        r.headers = {}
        r.json.side_effect = json.decoder.JSONDecodeError("", "", 0)
        r.content = "Bad Gateway"
        mock_send.return_value = r

        with self.assertRaises(files_sdk.error.APIConnectionError) as context:
            for f in files_sdk.folder.list_for("/").auto_paging_iter():
                pass

        self.assertEqual("HTTP 503 Bad Gateway", str(context.exception))

    def test_hostname_mismatch(self, mock_send):
        body = "You have connected to a URL that has different security settings than those required for your site."
        r = unittest.mock.MagicMock(spec=requests.Response)
        r.status_code = 403
        r.headers = {
            "x-files-host": "test.example.com",
        }
        r.content = body
        mock_send.return_value = r

        with self.assertRaises(files_sdk.error.AuthenticationError) as context:
            for f in files_sdk.folder.list_for("/").auto_paging_iter():
                pass

        self.assertIn(body, str(context.exception))
        self.assertIn("x-files-host", context.exception.headers)
        self.assertEqual(context.exception.headers["x-files-host"], "test.example.com")

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
        }
        mock_send.return_value = r

        with self.assertRaises(files_sdk.error.LockoutRegionMismatchError) as context:
            for f in files_sdk.folder.list_for("/").auto_paging_iter():
                pass
        
        self.assertEqual(context.exception.code, 401)
        self.assertEqual(str(context.exception), f"HTTP 401 {error_msg}")
        self.assertIn("content-type", context.exception.headers)
        self.assertEqual(context.exception.headers["content-type"], "application/json; charset=utf8")
        self.assertEqual(context.exception.json_body["title"], "Lockout Region Mismatch")

if __name__ == '__main__':
    unittest.main()