import unittest
import os
import logging
import requests
import re
import files_sdk

BASE_URL = "http://files-mock-server:4041"

class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Suppress logging to stdout/stderr, we will see errors at the end
        logging.getLogger("files_sdk").addHandler(logging.NullHandler())
        logging.getLogger("files_sdk").propagate = False
    
    def setUp(self):
        files_sdk.set_api_key("placeholderKey")
        files_sdk.base_url = BASE_URL
    
    @staticmethod
    def mock_server_path_exists(verb, path):
        populated_path = re.sub(r"\{.*\}", "1", path)
        response = requests.request(verb, url=BASE_URL + "/" + files_sdk.base_path + populated_path)
            
        if response.status_code > 400:
            return False
        return True

if __name__ == '__main__':
    unittest.main()