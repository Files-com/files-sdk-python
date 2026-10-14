import typing
import unittest
from decimal import Decimal, InvalidOperation
from typing import Any

import files_sdk
from files_sdk.error import APIConnectionError, NotFoundError
from files_sdk.models import (
    AutomationRun,
    RemoteMountBackend,
    Style,
    Workspace,
)
from tests.base import conforms
from tests.loopback_api import serve_loopback_api


class TestModelPersistence(unittest.TestCase):
    def setUp(self):
        self.api = serve_loopback_api(self)

    def test_saving_an_existing_record_patches_once_and_adopts_the_server_copy(
        self,
    ):
        workspace = Workspace(
            {"id": 12, "name": "Draft"}, {"api_key": "objectkey"}
        )
        self.api.reply_json({"id": 12, "name": "Server Name"})

        self.assertIsNone(workspace.save())

        [request] = self.api.requests
        self.assertEqual(
            ("PATCH", "/workspaces/12"), (request.method, request.path)
        )
        self.assertEqual({"id": 12, "name": "Draft"}, request.json)
        self.assertEqual("objectkey", request.headers["X-FilesAPI-Key"])
        self.assertEqual(
            {"id": 12, "name": "Server Name"}, workspace.get_attributes()
        )
        self.assertEqual({"api_key": "objectkey"}, workspace.options)

    def test_update_refreshes_the_object_in_place_and_returns_none(self):
        workspace = Workspace({"id": 12, "name": "Old"})
        self.api.reply_json({"id": 12, "name": "Canonical"})

        self.assertIsNone(workspace.update({"name": "Requested"}))

        self.assertEqual(
            {"id": 12, "name": "Canonical"}, workspace.get_attributes()
        )
        [request] = self.api.requests
        self.assertEqual({"id": 12, "name": "Requested"}, request.json)

    def test_operations_leave_the_callers_params_unchanged(self):
        # Version 1.x added the id it sent to the caller's dictionary.
        for name, call in (
            ("module", lambda params: files_sdk.workspace.update(12, params)),
            ("member", lambda params: Workspace({"id": 12}).update(params)),
        ):
            with self.subTest(name):
                self.api.requests.clear()
                self.api.reply_json({"id": 12, "name": "Canonical"})
                params = {"name": "Requested"}
                call(params)
                [request] = self.api.requests
                self.assertEqual({"id": 12, "name": "Requested"}, request.json)
                self.assertEqual({"name": "Requested"}, params)

    def test_saving_a_new_record_creates_it_with_one_post(self):
        workspace = Workspace({"name": "Fresh"}, {"api_key": "objectkey"})
        self.api.reply_json({"id": 99, "name": "Fresh"})

        self.assertIsNone(workspace.save())

        [request] = self.api.requests
        self.assertEqual(
            ("POST", "/workspaces"), (request.method, request.path)
        )
        self.assertEqual({"name": "Fresh"}, request.json)
        self.assertEqual(99, workspace.id)

    def test_a_new_record_keeps_its_draft_when_the_created_record_is_unreadable(
        self,
    ):
        workspace = Workspace({"name": "Draft"}, {"api_key": "objectkey"})
        self.api.reply_json(None)

        with self.assertRaises(APIConnectionError):
            workspace.save()

        [request] = self.api.requests
        self.assertEqual(
            ("POST", "/workspaces"), (request.method, request.path)
        )
        self.assertEqual({"name": "Draft"}, workspace.get_attributes())
        self.assertEqual({"api_key": "objectkey"}, workspace.options)

    def test_module_calls_build_records_only_from_json_objects(self):
        for label, call in (
            ("find", lambda: files_sdk.workspace.find(12)),
            ("create", lambda: files_sdk.workspace.create({"name": "New"})),
            (
                "update",
                lambda: files_sdk.workspace.update(12, {"name": "New"}),
            ),
            (
                "list without cursor",
                lambda: files_sdk.file.zip_list_contents("archive.zip"),
            ),
        ):
            with self.subTest(call=label):
                many = label == "list without cursor"
                self.api.reply_json([None] if many else None)
                with self.assertRaises(APIConnectionError):
                    call()

                self.api.reply_json([{}] if many else {})
                result = call()

                records = result if many else [result]
                self.assertEqual(
                    [{}], [record.get_attributes() for record in records]
                )

    def test_saving_an_update_only_record_patches_it_by_path(self):
        style = Style(
            {"path": "branding", "logo_click_href": "https://old.example"}
        )
        self.api.reply_json(
            {
                "id": 3,
                "path": "branding",
                "logo_click_href": "https://new.example",
            }
        )

        self.assertIsNone(style.save())

        [request] = self.api.requests
        self.assertEqual(
            ("PATCH", "/styles/branding"), (request.method, request.path)
        )
        self.assertEqual("https://new.example", style.logo_click_href)
        self.assertEqual(3, style.id)

    def test_refreshed_values_are_normalized_like_a_fetched_record(self):
        backend = RemoteMountBackend(
            {"id": 7, "enabled": True, "fall": 3, "min_free_cpu": "5.5"}
        )
        self.api.reply_json(
            {
                "id": 7,
                "enabled": False,
                "fall": 0,
                "min_free_cpu": "12.50",
                "min_free_mem": None,
                "remote_path": "",
                "health_check_results": [],
            }
        )

        backend.save()

        [request] = self.api.requests
        self.assertEqual(
            {"id": 7, "enabled": True, "fall": 3, "min_free_cpu": "5.5"},
            request.json,
        )
        self.assertEqual(Decimal("12.50"), backend.min_free_cpu)
        self.assertIsInstance(backend.min_free_cpu, Decimal)
        self.assertEqual(
            {
                "id": 7,
                "enabled": False,
                "fall": 0,
                "min_free_cpu": "12.50",
                "remote_path": "",
                "health_check_results": [],
            },
            backend.get_attributes(),
        )

    def test_failed_save_leaves_the_object_and_its_options_unchanged(self):
        workspace = Workspace(
            {"id": 12, "name": "Before"}, {"api_key": "objectkey"}
        )
        self.api.reply_json(
            {"type": "not-found", "error": "Workspace not found."}, status=404
        )

        with self.assertRaises(NotFoundError):
            workspace.save()

        self.assertEqual(1, len(self.api.requests))
        self.assertEqual(
            {"id": 12, "name": "Before"}, workspace.get_attributes()
        )
        self.assertEqual({"api_key": "objectkey"}, workspace.options)

    def test_an_unreadable_server_copy_raises_api_connection_error_and_changes_nothing(
        self,
    ):
        for label, body in (
            ("null", None),
            ("array", [{"id": 7}]),
            ("string", "updated"),
            (
                "malformed decimal",
                {"id": 7, "enabled": False, "min_free_cpu": "not a number"},
            ),
        ):
            for persist in ("update", "save"):
                with self.subTest(body=label, method=persist):
                    self.api.requests.clear()
                    backend = RemoteMountBackend(
                        {"id": 7, "enabled": True, "min_free_cpu": "5.5"},
                        {"api_key": "objectkey"},
                    )
                    self.api.reply_json(
                        body, headers={"X-Request-Id": "request-9"}
                    )

                    with self.assertRaises(APIConnectionError) as caught:
                        getattr(backend, persist)()

                    self.assertEqual(1, len(self.api.requests))
                    self.assertEqual(200, caught.exception.http_status)
                    self.assertEqual(
                        "request-9", caught.exception.headers["X-Request-Id"]
                    )
                    self.assertEqual(
                        {"id": 7, "enabled": True, "min_free_cpu": "5.5"},
                        backend.get_attributes(),
                    )
                    self.assertEqual({"api_key": "objectkey"}, backend.options)

    def test_invalid_values_from_the_caller_still_raise_where_they_are_given(
        self,
    ):
        with self.assertRaises(InvalidOperation):
            RemoteMountBackend({"id": 7, "min_free_cpu": "not a number"})

    def test_actions_that_answer_with_another_record_leave_the_object_alone(
        self,
    ):
        run = AutomationRun({"id": 8, "status": "failure"})
        rerun = {"id": 9, "status": "queued"}
        self.api.reply_json(rerun)

        self.assertEqual(rerun, run.rerun({"node_id": "node-1"}))

        self.assertEqual({"id": 8, "status": "failure"}, run.get_attributes())

    def test_found_records_keep_their_own_context_when_saved(self):
        self.api.reply_json({"id": 12, "name": "Found"})
        workspace = files_sdk.workspace.find(
            12, {}, {"api_key": "findkey", "workspace_id": 44}
        )
        self.api.reply_json({"id": 12, "name": "Renamed"})

        workspace.name = "Renamed"
        workspace.save()

        find, save = self.api.requests
        for request in (find, save):
            self.assertEqual("findkey", request.headers["X-FilesAPI-Key"])
            self.assertEqual("44", request.headers["X-Files-Workspace-Id"])
        self.assertEqual("PATCH", save.method)


class TestRecordTypes(unittest.TestCase):
    """Records decoded from realistic answers have the types their classes
    declare, including objects and lists whose schema examples are
    placeholders ("example", ["example"]), and AutoEntity data keeps
    whatever JSON value the API renders it as."""

    def setUp(self):
        self.api = serve_loopback_api(self)

    def assert_declared(self, record, expected):
        hints = typing.get_type_hints(type(record))
        for name, annotation in hints.items():
            if not name.startswith("_"):
                self.assertTrue(
                    conforms(getattr(record, name, None), annotation), name
                )
        for name, annotation in expected.items():
            self.assertEqual(annotation, hints[name], name)

    def test_objects_and_lists_with_placeholder_examples_keep_their_declared_types(
        self,
    ):
        definition = {
            "schema_version": 1,
            "nodes": [{"id": "trigger", "type": "trigger_manual"}],
            "edges": [],
        }
        self.api.reply_json({"id": 1, "definition": definition})
        automation = files_sdk.automation.find(1)
        self.assertEqual(definition, automation.definition)
        self.assert_declared(automation, {"definition": dict[str, Any] | None})

        self.api.reply_json(
            {"id": 2, "requested_upload_slots": [{"name": "Photo ID"}]}
        )
        bundle = files_sdk.bundle.find(2)
        self.assertEqual("Photo ID", bundle.requested_upload_slots[0]["name"])
        self.assert_declared(
            bundle, {"requested_upload_slots": list[dict[str, Any]] | None}
        )

        # ImageEntity renders a logo as its name and URI.
        self.api.reply_json(
            {
                "path": "brand",
                "logo": {
                    "name": "My logo",
                    "uri": "https://example.com/logo.png",
                },
            }
        )
        style = files_sdk.style.find("brand")
        self.assert_declared(style, {"logo": dict[str, Any] | None})

        self.api.reply_json(
            [
                {
                    "id": 3,
                    "actor": {"type": "user", "id": 7},
                    "payload": {"path": "a.txt"},
                    "human_fields": [{"label": "Path", "value": "a.txt"}],
                    "resources": [{"type": "file", "path": "a.txt"}],
                }
            ]
        )
        [record] = files_sdk.event_record.list().load_next_page()
        self.assert_declared(
            record,
            {
                "actor": dict[str, Any] | None,
                "payload": dict[str, Any] | None,
                "human_fields": list[dict[str, Any]] | None,
                "resources": list[dict[str, Any]] | None,
            },
        )

    def test_auto_entity_data_keeps_any_json_value(self):
        # AutoEntity renders data as a string, number, boolean, list or
        # object, whichever it is, so it is declared Any.
        for data in ("text", 7, True, ["a", 1], {"key": "value"}):
            with self.subTest(data=data):
                self.api.reply_json(
                    {"code": 200, "data": data, "success": True}
                )
                test = files_sdk.webhook_test.create(
                    {"url": "https://example.com/hook"}
                )
                self.assertEqual(data, test.data)
                self.assert_declared(test, {"data": Any})


if __name__ == "__main__":
    unittest.main()
