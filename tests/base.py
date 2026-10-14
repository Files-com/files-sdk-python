import types
import typing
import unittest
import logging
import files_sdk
from tests.schema_examples import PLACEHOLDERS

BASE_URL = "http://localhost:4042"


def conforms(value, annotation):
    """Whether value is of the type annotation declares, as the SDK's
    annotations use them."""
    if annotation is typing.Any:
        return True
    if annotation is type(None):
        return value is None
    origin = typing.get_origin(annotation)
    if origin in (typing.Union, types.UnionType):
        return any(conforms(value, arg) for arg in typing.get_args(annotation))
    if origin is list:
        (item,) = typing.get_args(annotation)
        return isinstance(value, list) and all(
            conforms(v, item) for v in value
        )
    if origin is dict:
        key, item = typing.get_args(annotation)
        return isinstance(value, dict) and all(
            conforms(k, key) and conforms(v, item) for k, v in value.items()
        )
    if origin is not None:
        return isinstance(value, origin)
    if annotation is int:
        return isinstance(value, int) and not isinstance(value, bool)
    if annotation is float:
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, annotation)


class TestBase(unittest.TestCase):
    def assert_returns(self, function, result):
        """Raise unless result is of the type function declares it returns."""
        annotation = typing.get_type_hints(function).get("return", typing.Any)
        self.assertTrue(
            conforms(result, annotation),
            "{} returned {!r}, not {}".format(
                function.__qualname__, result, annotation
            ),
        )

    def assert_typed(self, result):
        """Raise unless each record in result (a record, a list of them or
        a page of a ListObj, which is loaded) holds values of the types its
        class declares for its attributes, other than those the mock server
        answers with a schema placeholder (see tests.schema_examples)."""
        from files_sdk.list_obj import ListObj

        if isinstance(result, ListObj):
            records = list(result.load_next_page())
        elif isinstance(result, list):
            records = result
        else:
            records = [result]
        for record in records:
            if not hasattr(type(record), "default_attributes"):
                continue
            placeholders = PLACEHOLDERS.get(type(record).__name__, set())
            for name, annotation in typing.get_type_hints(
                type(record)
            ).items():
                if name.startswith("_") or name in placeholders:
                    continue
                value = getattr(record, name, None)
                self.assertTrue(
                    conforms(value, annotation),
                    "{}.{} is {!r}, not {}".format(
                        type(record).__name__, name, value, annotation
                    ),
                )

    @classmethod
    def setUpClass(cls):
        # Suppress logging to stdout/stderr, we will see errors at the end
        logging.getLogger("files_sdk").addHandler(logging.NullHandler())
        logging.getLogger("files_sdk").propagate = False

    def setUp(self):
        files_sdk.set_api_key("placeholderKey")
        files_sdk.base_url = BASE_URL


if __name__ == "__main__":
    unittest.main()
