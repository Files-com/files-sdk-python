import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FrontendMetric
from files_sdk import frontend_metric

class FrontendMetricTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/frontend_metrics"), "Mock path does not exist")
    def test_create(self):
        params = {
            "metric_type" : "foo",
            "subkey" : "foo",
        }
        frontend_metric.create(params)

if __name__ == '__main__':
    unittest.main()