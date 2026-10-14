"""Path parameters fill one segment of the request path, and "." and ".."
are refused before any request starts.

A URL resolves "." and ".." away, so a path of ".." would send the request
to another path than the operation's. These cases call the generated File
and Folder models with an operation whose request() stops the call where
it would send: a refused value never reaches it, and an accepted one stops
there on a local exception instead of making a request.
"""

import unittest
from unittest import mock

from files_sdk.api import Operation
from files_sdk.error import InvalidParameterError
from files_sdk.models.file import File
from files_sdk.models.folder import FolderResource


class ReachedService(Exception):
    """Raised by the operation's request(): the parameters were accepted."""


class PathParameterValuesTest(unittest.TestCase):
    def setUp(self):
        operation = mock.Mock(spec=Operation)
        operation.options = {}
        operation.request.side_effect = ReachedService
        self.start = operation.request
        for module in ("file", "folder"):
            patcher = mock.patch(
                "files_sdk.models.{}.Operation.start".format(module),
                return_value=operation,
            )
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_dot_segments_are_refused(self):
        calls = [
            (
                "FolderResource.list_for path",
                lambda value: FolderResource(None).list_for(value),
            ),
            (
                "File.delete path",
                lambda value: File({"path": value}).delete({}),
            ),
        ]
        for name, call in calls:
            for value in (".", ".."):
                with self.subTest(name, value=value):
                    self.start.reset_mock()
                    with self.assertRaises(InvalidParameterError):
                        call(value)
                    self.start.assert_not_called()

    def test_other_values_reach_the_service_as_one_segment(self):
        # A value holding dot segments between other text is one quoted
        # segment, which a URL does not resolve.
        for value in ("a/../b", "...", "", "reports/q3.csv"):
            with self.subTest(value=value):
                self.start.reset_mock()
                with self.assertRaises(ReachedService):
                    FolderResource(None).list_for(value)
                self.start.assert_called_once()


if __name__ == "__main__":
    unittest.main()
