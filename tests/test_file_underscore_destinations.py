import unittest
from unittest import mock

import files_sdk
from files_sdk.models import file as file_model


class TestFileUnderscoreDestinations(unittest.TestCase):
    def test_copy_to_remote_server_builds_destination(self):
        with mock.patch.object(file_model, "copy") as mock_copy:
            files_sdk.copy_to_remote_server("source.txt", 42, "/../../remote\\path//./to/file.txt", {"overwrite": True})

        mock_copy.assert_called_once_with(
            "source.txt",
            {"overwrite": True, "destination": "_/RemoteServers/42/remote/path/to/file.txt"},
            None,
        )

    def test_upload_to_remote_server_uses_local_basename(self):
        with mock.patch.object(file_model, "upload_file") as mock_upload_file:
            files_sdk.upload_to_remote_server("local/path/to/file.txt", 42)

        mock_upload_file.assert_called_once_with(
            "local/path/to/file.txt",
            "_/RemoteServers/42/file.txt",
            None,
            None,
        )


if __name__ == '__main__':
    unittest.main()
