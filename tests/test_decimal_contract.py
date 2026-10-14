import importlib
import inspect
import json
import pkgutil
import unittest
from decimal import Decimal, InvalidOperation
from urllib.parse import parse_qsl

import files_sdk
import files_sdk.models as models_pkg
from files_sdk.error import Error, InvalidParameterError, ModelSaveErrorError
from files_sdk.models import RemoteMountBackend
from tests.loopback_api import serve_loopback_api

EXACT = "0.123456789012345678901234567890"
# Very small and very large decimals, some of which Decimal writes with an
# exponent.
SMALL_AND_LARGE = (
    "0.0000001",
    "-0.000000000000000000001",
    "15E2",
    "1E+1001",
    "12.50",
    "0.000",
)
REQUIRED = {
    "canary_file_path": "health.txt",
    "remote_server_mount_id": 1,
    "remote_server_id": 2,
}


def assert_exact(test, value, sent):
    """sent is a string holding exactly the decimal value: its sign, digits
    and exponent, so its numeric value and its scale."""
    test.assertIsInstance(sent, str)
    test.assertEqual(Decimal(value).as_tuple(), Decimal(sent).as_tuple())


def iter_model_classes():
    for module_info in pkgutil.iter_modules(models_pkg.__path__):
        module_name = module_info.name
        if module_name.startswith("_"):
            continue
        module = importlib.import_module(
            f"{models_pkg.__name__}.{module_name}"
        )
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

        self.assertIsNotNone(
            target, "No model classes expose __decimal_fields"
        )
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


class TestDecimalRequests(unittest.TestCase):
    """RemoteMountBackend's min_free_cpu and min_free_mem take a float, as
    they always have, or an exact Decimal or its text, whether the API schema
    documents them as doubles or as decimals."""

    def setUp(self):
        self.api = serve_loopback_api(self)

    def operations(self, values):
        return (
            (
                "create",
                ("POST", "/remote_mount_backends"),
                lambda: files_sdk.remote_mount_backend.create(
                    {**REQUIRED, **values}
                ),
            ),
            (
                "update",
                ("PATCH", "/remote_mount_backends/7"),
                lambda: files_sdk.remote_mount_backend.update(7, values),
            ),
        )

    def sent(self, values):
        """The raw bodies each operation sends for values."""
        bodies = []
        for name, route, call in self.operations(values):
            with self.subTest(operation=name):
                self.api.requests.clear()
                self.api.reply_json({"id": 7})
                call()
                [request] = self.api.requests
                self.assertEqual(route, (request.method, request.path))
                bodies.append(request.body)
        return bodies

    def test_floats_are_sent_as_the_json_numbers_they_were(self):
        for body in self.sent({"min_free_cpu": 1.25, "min_free_mem": 1e-07}):
            self.assertIn(b'"min_free_cpu": 1.25', body)
            self.assertIn(b'"min_free_mem": 1e-07', body)

    def test_decimals_and_decimal_text_are_sent_exactly(self):
        for label, value in (("Decimal", Decimal(EXACT)), ("text", EXACT)):
            with self.subTest(label):
                for body in self.sent(
                    {"min_free_cpu": value, "min_free_mem": value}
                ):
                    self.assertIn(f'"min_free_cpu": "{EXACT}"'.encode(), body)
                    self.assertIn(f'"min_free_mem": "{EXACT}"'.encode(), body)

    def test_small_and_large_decimals_are_sent_as_exact_strings(self):
        for value in SMALL_AND_LARGE:
            with self.subTest(value=value):
                for body in self.sent({"min_free_cpu": Decimal(value)}):
                    assert_exact(self, value, json.loads(body)["min_free_cpu"])

    def test_a_records_attributes_hold_its_exact_decimal_strings(self):
        backend = RemoteMountBackend(
            {"id": 7, "min_free_cpu": "1E-7", "min_free_mem": Decimal("15E2")}
        )
        attributes = backend.get_attributes()
        assert_exact(self, "1E-7", attributes["min_free_cpu"])
        assert_exact(self, "15E2", attributes["min_free_mem"])
        # The model's module has a list() operation of its own; reading
        # attributes asks nothing of the API.
        self.assertEqual([], self.api.requests)

    def test_ordinary_arrays_keep_their_elements(self):
        # Only decimal arrays are limited to exact decimals.
        self.api.reply_json({"id": 1})
        files_sdk.ai_task.create(
            {"name": "n", "prompt": "p", "recurring_days": [1, 2]}
        )
        [request] = self.api.requests
        self.assertIn(b'"recurring_days": [1, 2]', request.body)

    def test_zero_is_sent_and_an_omitted_field_is_not(self):
        for body in self.sent({"min_free_cpu": Decimal("0")}):
            self.assertIn(b'"min_free_cpu": "0"', body)
            self.assertNotIn(b"min_free_mem", body)

    def test_other_values_are_refused_before_a_request_as_before(self):
        for value in ([1.25], {"value": 1.25}, None, False, 1):
            for name, _route, call in self.operations({"min_free_cpu": value}):
                with self.subTest(value=value, operation=name):
                    with self.assertRaises(InvalidParameterError):
                        call()
        # A float JSON cannot encode never reaches the API.
        for name, _route, call in self.operations(
            {"min_free_cpu": float("nan")}
        ):
            with self.subTest(value="nan", operation=name):
                with self.assertRaises(Error):
                    call()
        self.assertEqual([], self.api.requests)

    def test_a_record_updated_through_its_object_takes_what_it_always_took(
        self,
    ):
        backend = RemoteMountBackend({"id": 7, "min_free_cpu": "5.5"})
        for value in (2, None, False, Decimal(EXACT)):
            with self.subTest(value=value):
                self.api.requests.clear()
                self.api.reply_json({"id": 7, "min_free_cpu": "5.5"})
                backend.update({"min_free_cpu": value})
                [request] = self.api.requests
                self.assertEqual(
                    str(value) if isinstance(value, Decimal) else value,
                    request.json["min_free_cpu"],
                )

    def test_saving_new_and_existing_records_sends_exact_decimals(self):
        backend = RemoteMountBackend(
            {
                **REQUIRED,
                "min_free_cpu": EXACT,
                "min_free_mem": Decimal("12.50"),
            },
            {"api_key": "objectkey"},
        )
        self.api.reply_json(
            {
                **REQUIRED,
                "id": 9,
                "min_free_cpu": EXACT,
                "min_free_mem": "12.5",
            }
        )
        backend.save()

        self.api.reply_json(
            {"id": 9, "min_free_cpu": "40", "min_free_mem": "12.5"}
        )
        backend.min_free_cpu = Decimal("40.0")
        backend.save()

        create, update = self.api.requests
        self.assertEqual(("POST", "PATCH"), (create.method, update.method))
        self.assertEqual(
            (EXACT, "12.50"),
            (create.json["min_free_cpu"], create.json["min_free_mem"]),
        )
        self.assertEqual("40.0", update.json["min_free_cpu"])
        for request in (create, update):
            self.assertEqual("objectkey", request.headers["X-FilesAPI-Key"])
        self.assertEqual(
            (9, Decimal("40"), Decimal("12.5")),
            (backend.id, backend.min_free_cpu, backend.min_free_mem),
        )
        self.assertEqual({"api_key": "objectkey"}, backend.options)

    def test_decimal_text_the_api_rejects_leaves_the_record_unchanged(self):
        backend = RemoteMountBackend(
            {**REQUIRED, "id": 7, "min_free_cpu": "5.5"}
        )
        self.api.reply_json(
            {
                "type": "processing-failure/model-save-error",
                "error": "Min free cpu is invalid",
            },
            status=422,
        )

        with self.assertRaises(ModelSaveErrorError):
            backend.update({"min_free_cpu": "5.5.5"})

        [request] = self.api.requests
        self.assertEqual("5.5.5", request.json["min_free_cpu"])
        self.assertEqual(Decimal("5.5"), backend.min_free_cpu)


class TestQueryArrays(unittest.TestCase):
    """A list in a query is sent as name[] repeated, the form the API reads
    as an array, whether the caller names it name or already name[]."""

    def setUp(self):
        self.api = serve_loopback_api(self)

    def test_bare_and_bracketed_names_are_sent_as_one_array(self):
        for name in ("amounts", "amounts[]"):
            with self.subTest(name=name):
                self.api.requests.clear()
                self.api.reply_json({})
                files_sdk.api.Api.send_request(
                    "GET", "/foos", {name: ["1.25", "2.50"], "page": 2}
                )
                [request] = self.api.requests
                self.assertEqual(
                    "amounts%5B%5D=1.25&amounts%5B%5D=2.50&page=2",
                    request.query_string,
                )


# Foo and Bar are declared only by the generator's decimal-compat fixture
# (spec/fixtures/swagger_decimal_compat_new.json): decimal and decimal-array
# fields, query and body parameters, a plain number (ratio) and a string with
# a decimal format that is not a decimal (decimal_string).
foo = getattr(files_sdk, "foo", None)
HIGH = "12345678901234567890.123456789012345678901234567890"


@unittest.skipIf(foo is None, "the schema declares no decimal arrays")
class TestDecimalArrays(unittest.TestCase):
    def setUp(self):
        self.api = serve_loopback_api(self)

    def record(self, **values):
        self.api.reply_json({"amount": "1", **values})

    def test_query_arrays_send_every_element_exactly(self):
        self.record()
        foo.list(
            {
                "amount": Decimal(HIGH),
                "amounts": [Decimal(HIGH), Decimal("1E-7"), Decimal("0")],
                "decimal_string": "1.10",
                "ratio": 0.5,
            }
        )
        [request] = self.api.requests
        self.assertEqual(("GET", "/foos"), (request.method, request.path))
        sent = parse_qsl(request.query_string)
        self.assertEqual(
            ["amount", "amounts[]", "amounts[]", "amounts[]"]
            + ["decimal_string", "ratio"],
            [name for name, _ in sent],
        )
        for value, (_, text) in zip((HIGH, HIGH, "1E-7", "0"), sent):
            assert_exact(self, value, text)
        self.assertEqual(
            [("decimal_string", "1.10"), ("ratio", "0.5")], sent[4:]
        )

    def test_an_empty_query_array_is_not_sent(self):
        # A query string cannot hold an empty array.
        self.record()
        foo.list({"amounts": []})
        [request] = self.api.requests
        self.assertEqual("", request.query_string)

    def test_body_arrays_send_every_element_as_its_exact_string(self):
        for values in ([HIGH, "-0.000000000000000000001", "12.50"], []):
            with self.subTest(values=values):
                self.api.requests.clear()
                self.record()
                foo.create(
                    {
                        "amount": Decimal("0.10"),
                        "amounts": [Decimal(value) for value in values],
                        "ratio": 1.25,
                        "decimal_string": "0.10",
                    }
                )
                [request] = self.api.requests
                self.assertEqual(
                    ("POST", "/foos"), (request.method, request.path)
                )
                sent = request.json
                self.assertEqual(
                    {"amount", "amounts", "ratio", "decimal_string"}, set(sent)
                )
                assert_exact(self, "0.10", sent["amount"])
                self.assertEqual(len(values), len(sent["amounts"]))
                for value, text in zip(values, sent["amounts"]):
                    assert_exact(self, value, text)
                # The plain number and the plain string are sent as they were.
                self.assertEqual(
                    (1.25, "0.10"), (sent["ratio"], sent["decimal_string"])
                )

    def test_responses_give_exact_decimals_and_leave_other_fields_alone(self):
        nested = {"amount": "0.5", "amounts": ["1.10", "2"], "ratio": 0.5}
        self.record(
            amount=HIGH,
            amounts=[HIGH, "0.0000001", "1E-7", "-0", "12.50"],
            ratio=0.5,
            decimal_string="1.10",
            bar=nested,
        )
        created = foo.create({"amounts": [Decimal("1")]})
        self.assertEqual(Decimal(HIGH), created.amount)
        self.assertEqual(
            [Decimal] * 5, [type(value) for value in created.amounts]
        )
        self.assertEqual(
            [
                Decimal(text).as_tuple()
                for text in (HIGH, "0.0000001", "1E-7", "-0", "12.50")
            ],
            [value.as_tuple() for value in created.amounts],
        )
        self.assertEqual(
            (0.5, "1.10"), (created.ratio, created.decimal_string)
        )
        # A nested record stays the JSON object the API sent.
        self.assertEqual(nested, created.bar)

        self.record(amounts=[])
        self.assertEqual([], foo.list().amounts)
        self.record()
        self.assertIsNone(foo.list().amounts)

    def test_saving_a_new_foo_sends_its_decimals_and_adopts_the_answer(self):
        draft = foo.new(
            {
                "amount": "1E-7",
                "amounts": ["1E-7", Decimal(HIGH)],
                "ratio": 2.5,
            }
        )
        self.record(amount="0.0000001", amounts=["0.0000001", HIGH])
        self.assertIsNone(draft.save())
        [request] = self.api.requests
        self.assertEqual(("POST", "/foos"), (request.method, request.path))
        sent = request.json
        self.assertEqual({"amount", "amounts", "ratio"}, set(sent))
        assert_exact(self, "1E-7", sent["amount"])
        self.assertEqual(2, len(sent["amounts"]))
        for value, text in zip(("1E-7", HIGH), sent["amounts"]):
            assert_exact(self, value, text)
        self.assertEqual(2.5, sent["ratio"])
        # The record takes the created record the API answered with.
        self.assertEqual(
            [Decimal("0.0000001").as_tuple(), Decimal(HIGH).as_tuple()],
            [value.as_tuple() for value in draft.amounts],
        )

    def test_a_models_attributes_are_exact_strings_and_ask_nothing(self):
        for cls in (files_sdk.Foo, files_sdk.Bar):
            with self.subTest(model=cls.__name__):
                record = cls({"amount": "2.50", "amounts": ["1E-7", "3.000"]})
                self.assertEqual(
                    [Decimal("1E-7").as_tuple(), Decimal("3.000").as_tuple()],
                    [value.as_tuple() for value in record.amounts],
                )
                attributes = record.get_attributes()
                self.assertEqual({"amount", "amounts"}, set(attributes))
                assert_exact(self, "2.50", attributes["amount"])
                for value, text in zip(
                    ("1E-7", "3.000"), attributes["amounts"]
                ):
                    assert_exact(self, value, text)
                self.assertEqual(2, len(attributes["amounts"]))
        # foo's module has a list() operation of its own.
        self.assertEqual([], self.api.requests)

    def test_decimal_text_is_sent_as_given(self):
        self.record()
        foo.create({"amount": "2.50", "amounts": ["1.10", Decimal("2")]})
        [request] = self.api.requests
        self.assertEqual(
            {"amount": "2.50", "amounts": ["1.10", "2"]}, request.json
        )

    def test_elements_that_are_not_exact_decimals_are_refused(self):
        # A float was already rounded, and a number, boolean or null is not a
        # decimal's text, so none is sent, as a string or otherwise.
        client = files_sdk.Client(
            api_key="clientkey", base_url=self.api.url, max_network_retries=0
        )
        self.addCleanup(client.close)
        for element in (1.25, 1, True, None):
            for name, call in (
                ("create", lambda: foo.create({"amounts": [element]})),
                (
                    "client create",
                    lambda: client.foo.create({"amounts": [element]}),
                ),
                (
                    "list",
                    lambda: foo.list({"amounts": [Decimal("1"), element]}),
                ),
            ):
                with self.subTest(element=element, call=name):
                    with self.assertRaises(InvalidParameterError):
                        call()
        self.assertEqual([], self.api.requests)

    def test_a_model_converts_what_it_is_given_before_it_is_saved(self):
        # A model stores each element as Decimal(str(element)), as it does a
        # decimal field: a number becomes the Decimal of its text (a float's
        # shortest repr, not its binary value), so save() sends text; that is
        # conversion, not the operation's refusal. A boolean or null element
        # is not a decimal, and the model refuses it when it is set.
        draft = foo.new({"amounts": [1.25, 2]})
        self.assertEqual(
            [Decimal("1.25").as_tuple(), Decimal("2").as_tuple()],
            [value.as_tuple() for value in draft.amounts],
        )
        self.record(amounts=["1.25", "2"])
        draft.save()
        [request] = self.api.requests
        self.assertEqual(["1.25", "2"], request.json["amounts"])
        for element in (True, None):
            with self.subTest(element=element):
                with self.assertRaises(InvalidOperation):
                    foo.new({"amounts": [element]})

    def test_floats_and_single_values_are_refused_before_a_request(self):
        for call in (
            lambda: foo.list({"amount": 1.5}),
            lambda: foo.list({"amounts": Decimal("1.5")}),
            lambda: foo.create({"amount": 1.5}),
            lambda: foo.create({"amounts": "1.5"}),
        ):
            with self.assertRaises(InvalidParameterError):
                call()
        self.assertEqual([], self.api.requests)


if __name__ == "__main__":
    unittest.main()
