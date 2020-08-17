import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ExternalEvent
from files_sdk import external_event

class ExternalEventTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        resp = external_event.list()

if __name__ == '__main__':
    unittest.main()