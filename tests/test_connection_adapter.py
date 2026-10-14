import os
import unittest
from unittest.mock import patch

import files_sdk
import requests
from files_sdk.error import APIConnectionError, InvalidParameterError
from tests.loopback_api import serve_loopback_api, start_loopback_api
from tests.network_fixtures import ConnectProxy, TestAuthority

# An address no interface has (TEST-NET-1), so binding to it fails.
UNASSIGNED = "192.0.2.1"


class TestSourceIp(unittest.TestCase):
    def setUp(self):
        self.api = serve_loopback_api(self)
        files_sdk.set_source_ip(None)
        self.addCleanup(files_sdk.set_source_ip, None)

    def list_folder(self, options=None):
        self.api.reply_json([])
        return files_sdk.folder.list_for("/", {}, options)

    def test_requests_are_sent_from_the_module_source_ip(self):
        files_sdk.set_source_ip("127.0.0.1")
        self.list_folder()

        files_sdk.set_source_ip(UNASSIGNED)
        with self.assertRaises(APIConnectionError):
            self.list_folder()
        self.assertEqual(1, len(self.api.requests))

    def test_a_source_ip_option_binds_only_that_call(self):
        with self.assertRaises(APIConnectionError):
            self.list_folder({"source_ip": UNASSIGNED})
        self.list_folder()

        self.assertEqual(1, len(self.api.requests))

    def test_a_client_with_its_own_session_refuses_a_source_ip(self):
        session = requests.Session()
        self.addCleanup(session.close)
        with self.assertRaises(InvalidParameterError):
            files_sdk.Client(
                api_key="key", http_session=session, source_ip="127.0.0.1"
            )
        client = files_sdk.Client(
            api_key="key", http_session=session, base_url=self.api.url
        )
        with self.assertRaises(InvalidParameterError):
            client.folder.list_for("/", {}, {"source_ip": "127.0.0.1"})
        self.assertEqual([], self.api.requests)


class TestProxyAndCertificateSettings(unittest.TestCase):
    """Clients honor the standard proxy and CA bundle environment variables
    unless trust_env is off, and explicit settings win."""

    def setUp(self):
        self.authority = TestAuthority.create(self)
        self.api = start_loopback_api(self, tls=self.authority)
        self.proxy = ConnectProxy(
            self, routes={"app.example.com:443": self.api.port}
        )

    def list_users(self, **settings):
        client = files_sdk.Client(
            api_key="key", base_url="https://app.example.com", **settings
        )
        self.addCleanup(client.close)
        return client.user.list()

    def test_environment_proxy_and_ca_bundle_are_used_unless_trust_env_is_off(
        self,
    ):
        environment = {
            "HTTPS_PROXY": self.proxy.url,
            "REQUESTS_CA_BUNDLE": self.authority.ca,
            "NO_PROXY": "",
        }
        with patch.dict(os.environ, environment):
            self.api.reply_json([])
            self.list_users()
            with self.assertRaises(APIConnectionError):
                self.list_users(trust_env=False, open_timeout=2)

        self.assertEqual(["app.example.com:443"], self.proxy.targets)
        self.assertEqual(1, len(self.api.requests))

    def test_explicit_proxies_and_verify_apply_without_the_environment(self):
        self.api.reply_json([])
        self.list_users(
            proxies={"https": self.proxy.url}, verify=self.authority.ca
        )
        with self.assertRaises(APIConnectionError):
            self.list_users(proxies={"https": self.proxy.url})

        self.assertEqual(
            ["app.example.com:443", "app.example.com:443"], self.proxy.targets
        )
        self.assertEqual(1, len(self.api.requests))


if __name__ == "__main__":
    unittest.main()
