import unittest
from unittest import mock

import files_sdk
from files_sdk.error import InvalidParameterError
from files_sdk.models import file as file_model


class TestFileDownloadDefaultPath(unittest.TestCase):
    def test_download_without_local_path_uses_the_remote_file_name(self):
        with mock.patch.object(file_model.os, "name", "posix"), mock.patch.object(file_model.File, "download_file") as mock_download_file:
            files_sdk.file.download_file("folder/report:2026.txt")

        mock_download_file.assert_called_once_with("report:2026.txt")

    def test_windows_download_without_local_path_rejects_drive_and_stream_names(self):
        for remote_path in ("folder/C:victim.txt", "C:victim.txt", "folder/victim.txt::$DATA"):
            with self.subTest(remote_path=remote_path):
                with mock.patch.object(file_model.os, "name", "nt"), mock.patch.object(file_model.File, "download_file") as mock_download_file:
                    with self.assertRaises(InvalidParameterError):
                        files_sdk.file.download_file(remote_path)

                mock_download_file.assert_not_called()


if __name__ == '__main__':
    unittest.main()
