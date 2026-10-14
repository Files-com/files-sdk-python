import unittest
from unittest import mock

import files_sdk
from files_sdk.error import InvalidParameterError
from files_sdk.models import file as file_model


class TestFileDownloadDefaultPath(unittest.TestCase):
    # A client's download_file and the module's both choose the default local
    # path in FileResource.download_file, before the download itself
    # (files_sdk.download.download_path) begins; that is where these stop it.
    def downloads(self):
        client = files_sdk.Client(api_key="key")
        self.addCleanup(client.close)
        self.addCleanup(files_sdk.close)
        return (
            ("client", client.file.download_file),
            ("module", files_sdk.file.download_file),
        )

    def test_download_without_local_path_uses_the_remote_file_name(self):
        for how, download_file in self.downloads():
            with self.subTest(how=how):
                with (
                    mock.patch.object(file_model.os, "name", "posix"),
                    mock.patch.object(
                        file_model.downloads, "download_path"
                    ) as download_path,
                ):
                    download_file("folder/report:2026.txt")

                download_path.assert_called_once()
                _operation, _file, local_path = download_path.call_args.args
                self.assertEqual(local_path, "report:2026.txt")

    def test_windows_download_without_local_path_rejects_drive_stream_and_device_names(
        self,
    ):
        for how, download_file in self.downloads():
            for remote_path in (
                "folder/C:victim.txt",
                "C:victim.txt",
                "folder/victim.txt::$DATA",
                "folder/NUL",
                "folder/con",
                "COM1",
                "folder/CONIN$",
            ):
                with self.subTest(how=how, remote_path=remote_path):
                    with (
                        mock.patch.object(file_model.os, "name", "nt"),
                        mock.patch.object(
                            file_model.downloads, "download_path"
                        ) as download_path,
                    ):
                        with self.assertRaises(InvalidParameterError):
                            download_file(remote_path)

                    download_path.assert_not_called()


if __name__ == "__main__":
    unittest.main()
