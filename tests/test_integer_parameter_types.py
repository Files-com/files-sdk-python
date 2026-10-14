"""Integer parameters refuse booleans before any request starts.

bool is a subclass of int, so a plain isinstance(value, int) check lets True
and False through. These cases call the generated User model and patch only
Operation.start, which each operation calls once its parameter checks pass:
a refused value never reaches it, and an accepted one stops there on a local
exception instead of making a request.
"""

import unittest
from unittest import mock

from files_sdk.error import InvalidParameterError
from files_sdk.models.user import User, UserResource


class ReachedService(Exception):
    """Raised by the patched Operation.start: the parameters were accepted."""


class IntegerParameterTypesTest(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch(
            "files_sdk.models.user.Operation.start", side_effect=ReachedService
        )
        self.start = patcher.start()
        self.addCleanup(patcher.stop)

    def test_integer_parameters_refuse_booleans(self):
        calls = [
            (
                "UserResource.find id",
                lambda value: UserResource(None).find(value),
            ),
            (
                "User.update group_id",
                lambda value: User({"id": 1}).update({"group_id": value}),
            ),
        ]
        for name, call in calls:
            for value in (True, False):
                with self.subTest(name, value=value):
                    self.start.reset_mock()
                    with self.assertRaises(InvalidParameterError):
                        call(value)
                    self.start.assert_not_called()

    def test_valid_values_reach_the_service(self):
        calls = [
            ("UserResource.find id 0", lambda: UserResource(None).find(0)),
            (
                "UserResource.list include_parent_site_users False",
                lambda: UserResource(None).list(
                    {"include_parent_site_users": False}
                ),
            ),
            (
                "User.update disabled False",
                lambda: User({"id": 1}).update({"disabled": False}),
            ),
        ]
        for name, call in calls:
            with self.subTest(name):
                self.start.reset_mock()
                with self.assertRaises(ReachedService):
                    call()
                self.start.assert_called_once()


if __name__ == "__main__":
    unittest.main()
