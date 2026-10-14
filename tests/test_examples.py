import ast
import contextlib
import importlib.util
import io
import json
import os
import re
import typing
import unittest
from pathlib import Path
from unittest import mock

import files_sdk
from files_sdk.list_obj import ListObj
from tests.loopback_api import serve_loopback_api, start_loopback_api

EXAMPLE = (
    Path(__file__).resolve().parent.parent / "examples" / "getting_started.py"
)
DOCS = Path(__file__).resolve().parent.parent / "docs"


class TestGettingStarted(unittest.TestCase):
    def test_the_getting_started_example_runs_its_whole_tour(self):
        api = start_loopback_api(self)
        content = b"id,total\n1,10.50\n"
        api.reply_json([{"id": 1, "username": "admin"}])
        api.reply_json({"id": 5, "name": "SDK example"})
        api.reply_json({"id": 5, "name": "SDK example (renamed)"})
        api.reply(204)
        api.reply_json(
            [
                {
                    "ref": "r1",
                    "part_number": 1,
                    "partsize": 5242880,
                    "upload_uri": api.url + "/storage/part1",
                    "http_method": "PUT",
                    "headers": {},
                    "parameters": {},
                    "parallel_parts": False,
                }
            ]
        )
        api.reply(200, headers={"ETag": '"e1"'})
        api.reply_json(
            {
                "path": "sdk-example/report.csv",
                "type": "file",
                "size": len(content),
            }
        )
        for _ in range(
            2
        ):  # download_file(), then open(): a URL each, and the content.
            api.reply_json(
                {
                    "path": "sdk-example/report.csv",
                    "download_uri": api.url + "/storage/report",
                }
            )
            api.reply(200, content)
        api.reply(204)
        api.reply_json(
            {"type": "not-found", "error": "Not Found", "http-code": 404},
            status=404,
        )

        spec = importlib.util.spec_from_file_location(
            "getting_started", EXAMPLE
        )
        example = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(example)
        output = io.StringIO()
        environment = {"FILES_API_KEY": "key", "FILES_BASE_URL": api.url}
        with (
            mock.patch.dict(os.environ, environment),
            contextlib.redirect_stdout(output),
        ):
            example.main()

        printed = output.getvalue()
        for expected in (
            "User 1: admin",
            "Group 5 is named 'SDK example (renamed)'",
            "Uploaded 17 bytes to sdk-example/report.csv",
            "Downloaded 17 bytes from sdk-example/report-",
            "  1,10.50",
            "Expected error:",
        ):
            self.assertIn(expected, printed)
        steps = [
            (
                request.method,
                (
                    request.path.split("/")[1]
                    if request.url_path.startswith("/api/")
                    else request.url_path
                ),
            )
            for request in api.requests
        ]
        self.assertEqual(
            steps,
            [
                ("GET", "users"),
                ("POST", "groups"),
                ("PATCH", "groups"),
                ("DELETE", "groups"),
                ("POST", "file_actions"),
                ("PUT", "/storage/part1"),
                ("POST", "files"),
                ("GET", "files"),
                ("GET", "/storage/report"),
                ("GET", "files"),
                ("GET", "/storage/report"),
                ("DELETE", "files"),
                ("GET", "file_actions"),
            ],
        )


def answered(value):
    """A record a page shows, as the API would send it: without the empty
    text a page shows where the schema gives no example, such as for a
    decimal, which the API sends with a value or not at all."""
    if isinstance(value, dict):
        return {
            key: answered(item) for key, item in value.items() if item != ""
        }
    if isinstance(value, list):
        return [answered(item) for item in value if item != ""]
    return value


class TestResourceExamples(unittest.TestCase):
    """Runs the Python examples of every resource page in docs/ against a
    local API that answers each call with the record its page shows."""

    def setUp(self):
        if not DOCS.is_dir():
            self.skipTest("the generated docs are not beside these tests")
        self.pages = {
            page: page.read_text() for page in sorted(DOCS.glob("*.md"))
        }
        self.records = {}
        for text in self.pages.values():
            name = re.search(r"^# (\w+)$", text, re.M)
            record = re.search(r"^```json\n(.*?)^```$", text, re.M | re.S)
            if name and record:
                self.records[name.group(1)] = answered(
                    json.loads(record.group(1))
                )

    def examples(self):
        """Each example, with values for the names it leaves to the reader,
        such as the ID of the record it works on, of the types its section's
        parameter list gives."""
        for page, text in self.pages.items():
            number = 0
            for section in text.split("\n---\n"):
                types = dict(
                    re.findall(r"^\* `(\w+)` \(([^)]*)\)", section, re.M)
                )
                values = {"path": "folder/a.txt"}
                for name in ("id", "user_id"):
                    values[name] = "a1" if types.get(name) == "string" else 1
                for code in re.findall(
                    r"^```python\n(.*?)^```$", section, re.M | re.S
                ):
                    number += 1
                    yield f"{page.name} example {number}", code, values

    def calls(self, code):
        """The SDK calls an example makes, in order: each one's name and
        the type the API answers it with, for a function or for a method of
        a record an earlier call returned. That is its return type, except
        for a record's update, which returns nothing but answers with the
        record, which the object takes in place."""
        tree = ast.parse(code)
        calls = sorted(
            (node for node in ast.walk(tree) if isinstance(node, ast.Call)),
            key=lambda node: (node.lineno, node.col_offset),
        )
        record_type = None
        for call in calls:
            target = call.func
            if not isinstance(target, ast.Attribute) or not isinstance(
                target.value, (ast.Attribute, ast.Name)
            ):
                continue
            if (
                isinstance(target.value, ast.Attribute)
                and isinstance(target.value.value, ast.Name)
                and target.value.value.id == "files_sdk"
            ):
                function = getattr(
                    getattr(files_sdk, target.value.attr), target.attr
                )
            elif (
                isinstance(target.value, ast.Name)
                and target.value.id != "files_sdk"
                and record_type
            ):
                function = getattr(record_type, target.attr)
            else:
                continue
            returns = typing.get_type_hints(function)["return"]
            if function is getattr(
                record_type, "update", None
            ) and returns is type(None):
                returns = record_type
            yield target.attr, returns
            if typing.get_origin(returns) is ListObj:
                record_type = typing.get_args(returns)[0]
            elif isinstance(returns, type) and returns.__module__.startswith(
                "files_sdk.models"
            ):
                record_type = returns

    def reply(self, api, returns, found=True):
        """Queue the answer to a call whose return type is returns."""
        if typing.get_origin(returns) in (ListObj, list):
            item = getattr(typing.get_args(returns)[0], "__name__", None)
            api.reply_json([self.records.get(item, {})] if found else [])
        elif returns is type(None):
            api.reply(204)
        elif typing.get_origin(returns) is dict:
            api.reply_json({})
        elif isinstance(returns, type) and returns.__module__.startswith(
            "files_sdk.models"
        ):
            api.reply_json(self.records.get(returns.__name__, {}))
        else:
            self.fail(f"no answer for a call returning {returns}")

    def run_example(self, api, code, values, found=True):
        api.requests.clear()
        api.responses.clear()
        sent = 0
        for index, (name, returns) in enumerate(self.calls(code)):
            if name == "new":
                continue
            self.reply(api, returns, found)
            sent += 1
            if not found and index == 0:
                break  # An empty list: the example goes no further.
        exec(
            compile(code, "<example>", "exec"),
            {"files_sdk": files_sdk, **values},
        )
        self.assertEqual(api.responses, [], "an expected call was not made")
        self.assertEqual(len(api.requests), sent)

    def test_each_resource_example_runs_against_the_api(self):
        api = serve_loopback_api(self)
        examples = list(self.examples())
        self.assertGreater(len(examples), 100)
        for label, code, values in examples:
            with self.subTest(label):
                self.run_example(api, code, values)

    def test_an_example_that_lists_records_handles_an_empty_list(self):
        api = serve_loopback_api(self)
        listing = [
            example for example in self.examples() if "next(" in example[1]
        ]
        self.assertGreater(len(listing), 0)
        for label, code, values in listing:
            with self.subTest(label):
                self.run_example(api, code, values, found=False)


class TestKeylessRecordExamples(unittest.TestCase):
    """The record-method examples of models whose records the API sends
    without their ID: run with the ID the caller knows, each sends the
    request below, which is written out here, not read from the docs."""

    EXAMPLES = [
        # model, record method, HTTP method, path, where the parameters go, required values
        (
            "group_user",
            "update",
            "PATCH",
            "/group_users/5",
            "json",
            {"group_id": 1, "user_id": 1},
        ),
        (
            "group_user",
            "delete",
            "DELETE",
            "/group_users/5",
            "query",
            {"group_id": "1", "user_id": "1"},
        ),
        ("partner_site", "delete", "DELETE", "/partner_sites/5", "query", {}),
    ]

    def setUp(self):
        if not DOCS.is_dir():
            self.skipTest("the generated docs are not beside these tests")

    def record_method_examples(self, model, method):
        """The examples on model's page that call method on a record made by
        files_sdk.<model>, rather than on the module: found by their code,
        whatever they call the record or how they give it its ID."""
        found = []
        for code in re.findall(
            r"^```python(?:[ \t][^\n]*)?\n(.*?)^```[ \t]*$",
            (DOCS / f"{model}.md").read_text(),
            re.M | re.S,
        ):
            nodes = list(ast.walk(ast.parse(code)))
            records = {
                target.id
                for node in nodes
                if isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Attribute)
                and ast.unparse(node.value.func.value) == f"files_sdk.{model}"
                for target in node.targets
                if isinstance(target, ast.Name)
            }
            if any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == method
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in records
                for node in nodes
            ):
                found.append(code)
        return found

    def test_each_sets_the_known_id_and_sends_its_request(self):
        api = serve_loopback_api(self)
        for model, record_method, method, path, where, values in self.EXAMPLES:
            with self.subTest(f"{model}.{record_method}"):
                examples = self.record_method_examples(model, record_method)
                self.assertEqual(
                    len(examples),
                    1,
                    "the example is missing or not the only one",
                )
                api.requests.clear()
                if method == "PATCH":
                    api.reply_json({"group_id": 1, "user_id": 1})
                else:
                    api.reply(204)
                exec(
                    compile(examples[0], f"{model}.md", "exec"),
                    {"files_sdk": files_sdk, "id": 5},
                )
                [request] = api.requests
                self.assertEqual(
                    (request.method, request.path), (method, path)
                )
                sent = request.json if where == "json" else request.query
                self.assertEqual(
                    {key: sent.get(key) for key in values}, values
                )


if __name__ == "__main__":
    unittest.main()
