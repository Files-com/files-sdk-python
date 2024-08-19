import unittest

import files_sdk
from requests_toolbelt.adapters import source


import files_sdk.api as Api

class TestConnectionAdapters(unittest.TestCase):
    def setUp(self):
        super().setUp()
        files_sdk.set_api_key("testkey")

    def test_bind_to_source_ip(self):
        files_sdk.set_source_ip("127.0.0.1")
        session_adapter = Api.ApiClient().session.adapters[files_sdk.base_url]
        self.assertIsInstance(session_adapter, source.SourceAddressAdapter)
        self.assertEqual(session_adapter.source_address, ("127.0.0.1", 0))

    def test_does_not_autobind_to_source_ip(self):
        files_sdk.set_source_ip(None)
        api_client = Api.ApiClient()

        self.assertIsNone(files_sdk.get_source_ip())
        session_adapter = api_client.session.adapters.get(files_sdk.base_url, None)
        self.assertIsNone(session_adapter)
