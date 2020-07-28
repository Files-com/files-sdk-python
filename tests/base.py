import unittest
import os
import logging
import files_sdk

class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Suppress logging to stdout/stderr, we will see errors at the end
        logging.getLogger("files_sdk").addHandler(logging.NullHandler())
        logging.getLogger("files_sdk").propagate = False
    def setUp(self):
        files_sdk.set_api_key("placeholderKey")
        files_sdk.base_url = "http://localhost:40410"
        files_sdk.base_path = ''

if __name__ == '__main__':
    unittest.main()