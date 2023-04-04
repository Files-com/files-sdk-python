import unittest
import logging
import json

import files_sdk

class TestPathUtil(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Suppress logging to stdout/stderr, we will see errors at the end
        logging.getLogger("files_sdk").addHandler(logging.NullHandler())
        logging.getLogger("files_sdk").propagate = False

    def test_normalization_for_comparison(self):
        with open("shared/normalization_for_comparison_test_data.json") as json_file:
            for entry in json.load(json_file):
                self.assertEqual(files_sdk.path_util.normalize_for_comparison(entry[0]), entry[-1])

if __name__ == '__main__':
    unittest.main()

  # json_str = File.read("shared/normalization_for_comparison_test_data.json")
  # test_cases = JSON.parse json_str