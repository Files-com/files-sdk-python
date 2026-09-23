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
        with open(
            "shared/normalization_for_comparison_test_data.json"
        ) as json_file:
            for entry in json.load(json_file):
                self.assertEqual(
                    files_sdk.path_util.normalize_for_comparison(entry[0]),
                    entry[-1],
                )
                self.assertEqual(
                    files_sdk.path_util.normalize_for_comparison(entry[-1]),
                    entry[-1],
                )

    def test_server_comparison_examples(self):
        with open(
            "shared/comparison_examples.json", encoding="utf-8"
        ) as json_file:
            for original, expected in json.load(json_file):
                self.assertEqual(
                    files_sdk.path_util.normalize_for_comparison(original),
                    expected,
                )

    def test_normalize_preserves_path_identity(self):
        self.assertEqual(
            files_sdk.path_util.normalize(
                "/../../remote\\path//./to/file.txt"
            ),
            "remote/path/to/file.txt",
        )
        self.assertEqual(
            files_sdk.path_util.normalize("remote/../path/to/file.txt"),
            "remote/path/to/file.txt",
        )


if __name__ == "__main__":
    unittest.main()
