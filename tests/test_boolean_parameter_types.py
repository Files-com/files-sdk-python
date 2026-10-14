"""A record's own operations refuse a container for a Boolean parameter
before any request is sent.

A list or dictionary is not a Boolean, but user.update() used to send one as
given. Only containers are refused: True, False, None and leaving the
parameter out are sent as before. These cases call the generated User model
through a client, and only requests.Session.send, where a request would
leave for Files.com, is replaced: it records the request and answers with
the updated record.
"""

import json
import unittest
from unittest.mock import patch

import files_sdk
import requests
from files_sdk.error import InvalidParameterError


def record_response(record):
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = json.dumps(record).encode()
    return response


@patch.object(requests.Session, "send")
class TestBooleanParameterTypes(unittest.TestCase):
    def setUp(self):
        super().setUp()
        client = files_sdk.Client(api_key="booleankey")
        self.addCleanup(client.close)
        self.user = client.user.new(
            {"id": 77, "disabled": False, "username": "member77"}
        )

    def test_a_record_operation_refuses_a_container_for_a_boolean(
        self, mock_send
    ):
        for value in (["invalid-container"], {"disabled": True}):
            with self.subTest(value=value):
                mock_send.reset_mock()
                with self.assertRaises(InvalidParameterError) as caught:
                    self.user.update({"disabled": value})
                self.assertIn("disabled", str(caught.exception))
                mock_send.assert_not_called()

        for params in (
            {"disabled": False},
            {"disabled": True},
            {"disabled": None},
            {},
        ):
            with self.subTest(params=params):
                mock_send.reset_mock()
                mock_send.return_value = record_response(
                    {"id": 77, "username": "member77", **params}
                )

                self.user.update(params)

                mock_send.assert_called_once()
                request = mock_send.call_args[0][0]
                self.assertEqual("PATCH", request.method)
                self.assertTrue(request.url.endswith("/users/77"))
                self.assertEqual(
                    {"id": 77, **params}, json.loads(request.body)
                )


if __name__ == "__main__":
    unittest.main()
