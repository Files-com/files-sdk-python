import unittest
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

import files_sdk
import requests


@patch.object(requests.Session, "send")
class TestPathParameterEncoding(unittest.TestCase):
    def setUp(self):
        super().setUp()
        files_sdk.set_api_key("testkey")

    def test_file_delete_encodes_returned_path_before_request(self, mock_send):
        response = requests.Response()
        response.status_code = 204
        mock_send.return_value = response

        files_sdk.file.delete("root/data?recursive=true")

        request = mock_send.call_args[0][0]
        url = urlsplit(request.url)
        self.assertTrue(
            url.path.endswith("/files/root%2Fdata%3Frecursive%3Dtrue")
        )
        self.assertNotIn("recursive", parse_qs(url.query))


if __name__ == "__main__":
    unittest.main()
