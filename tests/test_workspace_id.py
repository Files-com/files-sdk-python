import unittest
from unittest.mock import patch

import files_sdk
import requests
from files_sdk.api import Api
from files_sdk.api_client import ApiClient


class TestWorkspaceId(unittest.TestCase):
    def setUp(self):
        super().setUp()
        files_sdk.set_api_key("testkey")
        files_sdk.set_workspace_id(None)

    def test_request_headers_include_configured_workspace_id(self):
        files_sdk.set_workspace_id(123)
        client = ApiClient()
        response = requests.Response()
        response.status_code = 204

        with patch.object(
            client, "execute_request_with_auto_retry", return_value=response
        ) as mock_execute:
            client.send_request(
                "GET", "/folders", api_key="testkey", params={}
            )

        request = mock_execute.call_args[0][0]
        self.assertEqual(request.headers["X-Files-Workspace-Id"], "123")

    def test_per_call_workspace_id_overrides_configured_workspace_id(self):
        files_sdk.set_workspace_id(123)
        client = ApiClient()
        response = requests.Response()
        response.status_code = 204

        with patch.object(
            client, "execute_request_with_auto_retry", return_value=response
        ) as mock_execute:
            client.send_request(
                "GET",
                "/folders",
                api_key="testkey",
                workspace_id=456,
                params={},
            )

        request = mock_execute.call_args[0][0]
        self.assertEqual(request.headers["X-Files-Workspace-Id"], "456")

    def test_request_headers_omit_workspace_id_when_unset(self):
        client = ApiClient()
        response = requests.Response()
        response.status_code = 204

        with patch.object(
            client, "execute_request_with_auto_retry", return_value=response
        ) as mock_execute:
            client.send_request(
                "GET", "/folders", api_key="testkey", params={}
            )

        request = mock_execute.call_args[0][0]
        self.assertNotIn("X-Files-Workspace-Id", request.headers)

    def test_per_call_options_pass_workspace_id_to_api_client(self):
        with patch.object(Api, "client") as mock_client:
            response = requests.Response()
            mock_client.return_value.send_request.return_value = response

            actual_response, options = Api.send_request(
                "GET", "/folders", {}, {"workspace_id": 456}
            )

        self.assertEqual(actual_response, response)
        self.assertEqual(options["workspace_id"], 456)
        mock_client.return_value.send_request.assert_called_once_with(
            "GET",
            "/folders",
            api_key=None,
            session_id=None,
            language=None,
            workspace_id=456,
            params={},
        )


if __name__ == "__main__":
    unittest.main()
