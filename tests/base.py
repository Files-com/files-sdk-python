import unittest
import os
import files_com

class TestBase(unittest.TestCase):
    def setUp(self):
        files_com.api_key = "placeholderKey"
        files_com.base_url = "http://localhost:40410"
        files_com.base_path = ''

if __name__ == '__main__':
    unittest.main()