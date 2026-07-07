import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import AgentProxyIdentity
from files_sdk import agent_proxy_identity

class AgentProxyIdentityTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/agent_proxy_identities/lookup"), "Mock path does not exist")
    def test_lookup(self):
        params = {
            "ips" : ["foo1"],
        }
        agent_proxy_identity.lookup(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/agent_proxy_identities/report"), "Mock path does not exist")
    def test_report(self):
        params = {
            "private_ip" : "foo",
            "peer_id" : "foo",
        }
        agent_proxy_identity.report(params)

if __name__ == '__main__':
    unittest.main()