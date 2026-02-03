import importlib
import inspect
import pkgutil
import unittest
from decimal import Decimal

import files_sdk.models as models_pkg


def iter_model_classes():
    for module_info in pkgutil.iter_modules(models_pkg.__path__):
        module_name = module_info.name
        if module_name.startswith("_"):
            continue
        module = importlib.import_module(f"{models_pkg.__name__}.{module_name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__:
                yield obj


def decimal_fields_for(cls):
    return getattr(cls, f"_{cls.__name__}__decimal_fields", set())


def decimal_array_fields_for(cls):
    return getattr(cls, f"_{cls.__name__}__decimal_array_fields", set())


class TestDecimalContract(unittest.TestCase):
    def test_decimal_fields_parse_and_serialize_as_strings(self):
        target = None
        for cls in iter_model_classes():
            fields = decimal_fields_for(cls)
            if fields:
                field = next(iter(fields))
                target = (cls, field)
                break

        self.assertIsNotNone(target, "No model classes expose __decimal_fields")
        cls, field = target

        raw = "1.2300"
        obj = cls({field: raw})

        parsed = getattr(obj, field)
        self.assertIsInstance(parsed, Decimal)
        self.assertEqual(parsed, Decimal(raw))

        attrs = obj.get_attributes()
        self.assertIn(field, attrs)
        self.assertEqual(attrs[field], raw)

    def test_decimal_array_fields_parse_and_serialize_as_strings(self):
        target = None
        for cls in iter_model_classes():
            fields = decimal_array_fields_for(cls)
            if fields:
                field = next(iter(fields))
                target = (cls, field)
                break

        if target is None:
            self.skipTest("No models expose __decimal_array_fields")

        cls, field = target
        raw = ["1.23", "4.56"]

        obj = cls({field: raw})
        parsed = getattr(obj, field)

        self.assertIsInstance(parsed, list)
        self.assertEqual([type(v) for v in parsed], [Decimal, Decimal])
        self.assertEqual([str(v) for v in parsed], raw)

        attrs = obj.get_attributes()
        self.assertEqual(attrs[field], raw)


if __name__ == "__main__":
    unittest.main()
