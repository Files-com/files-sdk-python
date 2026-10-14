import itertools
import unittest
from decimal import Decimal

import files_sdk
from files_sdk.error import APIConnectionError, NotFoundError
from tests.loopback_api import serve_loopback_api

CONTEXT = {"api_key": "listkey", "workspace_id": 31}


class TestListPagination(unittest.TestCase):
    def setUp(self):
        self.api = serve_loopback_api(self)

    def reply_page(self, names, cursor=None):
        headers = {} if cursor is None else {"X-Files-Cursor": cursor}
        self.api.reply_json(
            [{"path": "reports/" + name, "type": "file"} for name in names],
            headers=headers,
        )

    def list_reports(self, params=None, options=None):
        return files_sdk.folder.list_for(
            "reports", params or {"per_page": 1}, options or dict(CONTEXT)
        )

    def sent_cursors(self):
        return [request.query.get("cursor") for request in self.api.requests]

    def test_every_page_is_visited_even_when_some_are_empty(self):
        def auto_paging(pager):
            return [item.path for item in pager.auto_paging_iter()]

        def documented_manual_loop(pager):
            paths = []
            while True:
                for item in pager:
                    paths.append(item.path)
                if not pager.has_next_page:
                    break
                pager.load_next_page()
            return paths

        for walk in (auto_paging, documented_manual_loop):
            with self.subTest(walk=walk.__name__):
                self.api.requests.clear()
                self.reply_page(["a"], cursor="c1")
                self.reply_page([], cursor="c2")
                self.reply_page([], cursor="c3")
                self.reply_page(["d"])

                paths = walk(self.list_reports())

                self.assertEqual(["reports/a", "reports/d"], paths)
                self.assertEqual([None, "c1", "c2", "c3"], self.sent_cursors())
                for request in self.api.requests:
                    self.assertEqual("/folders/reports", request.path)
                    self.assertEqual("1", request.query["per_page"])
                    self.assertEqual(
                        "listkey", request.headers["X-FilesAPI-Key"]
                    )
                    self.assertEqual(
                        "31", request.headers["X-Files-Workspace-Id"]
                    )

    def test_the_next_cursor_header_leads_to_the_next_page(self):
        # A cursor is opaque: it goes back exactly as it came, even with
        # characters a query string gives meaning to.
        cursor = "opaque/next+token=%25&route?"
        for name, headers in (
            ("next", {"X-Files-Cursor-Next": cursor}),
            (
                "next over legacy",
                {"X-Files-Cursor-Next": cursor, "X-Files-Cursor": "stale"},
            ),
            ("legacy only", {"X-Files-Cursor": cursor}),
        ):
            with self.subTest(name):
                self.api.requests.clear()
                self.api.reply_json([{"id": 73}, {"id": 74}], headers=headers)
                self.api.reply_json([{"id": 75}])

                users = files_sdk.user.list({"per_page": 2}, dict(CONTEXT))

                self.assertEqual(
                    [73, 74, 75],
                    [user.id for user in users.auto_paging_iter()],
                )
                self.assertEqual([None, cursor], self.sent_cursors())
                self.assertEqual(
                    ["/users", "/users"],
                    [request.path for request in self.api.requests],
                )
                self.assertFalse(users.has_next_page)

    def test_records_from_later_pages_keep_the_list_context(self):
        self.reply_page(["a"], cursor="c1")
        self.reply_page(["b"])
        pager = self.list_reports()

        pager.load_next_page()

        [record] = pager
        self.assertEqual("reports/b", record.path)
        self.assertEqual(CONTEXT, record.options)

    def test_the_callers_params_and_options_are_not_shared_with_the_list(self):
        params = {"per_page": 1}
        options = dict(CONTEXT)
        self.reply_page(["a"], cursor="c1")
        pager = self.list_reports(params, options)
        params["per_page"] = 50
        options["api_key"] = "changedkey"
        self.reply_page(["b"])

        pager.load_next_page()

        self.assertNotIn("cursor", params)
        self.assertEqual("1", self.api.requests[1].query["per_page"])
        self.assertEqual(
            "listkey", self.api.requests[1].headers["X-FilesAPI-Key"]
        )

    def test_a_blank_cursor_ends_the_list(self):
        self.reply_page(["a"], cursor="")

        pager = self.list_reports()

        self.assertFalse(pager.has_next_page)
        self.assertEqual(
            ["reports/a"], [item.path for item in pager.auto_paging_iter()]
        )
        self.assertEqual(1, len(self.api.requests))

    def test_advancing_past_the_last_page_sends_nothing_and_keeps_the_page(
        self,
    ):
        self.reply_page(["a", "b"])
        pager = self.list_reports()

        for _ in range(2):
            self.assertIs(pager, pager.load_next_page())

        self.assertEqual(
            ["reports/a", "reports/b"], [item.path for item in pager]
        )
        self.assertEqual(2, len(pager))
        self.assertEqual(1, len(self.api.requests))

    def test_a_repeated_cursor_raises_instead_of_refetching_pages(self):
        for name, cursors in (
            ("self loop", ["A", "A"]),
            ("cycle", ["A", "B", "A"]),
        ):
            with self.subTest(name):
                self.api.requests.clear()
                for index, cursor in enumerate(cursors):
                    self.reply_page([str(index)], cursor=cursor)
                seen = []

                with self.assertRaises(APIConnectionError) as caught:
                    for item in self.list_reports().auto_paging_iter():
                        seen.append(item.path)

                self.assertIsInstance(caught.exception, files_sdk.error.Error)
                self.assertEqual(len(cursors), len(self.api.requests))
                self.assertEqual(
                    [
                        "reports/{}".format(index)
                        for index in range(len(cursors))
                    ],
                    seen,
                )

    def test_stopping_early_fetches_no_further_pages(self):
        self.reply_page(["a", "b"], cursor="c1")
        self.assertEqual(
            ["reports/a", "reports/b"],
            [
                item.path
                for item in itertools.islice(
                    self.list_reports().auto_paging_iter(), 2
                )
            ],
        )

        self.reply_page(["a", "b"], cursor="c1")
        for _ in self.list_reports().auto_paging_iter():
            break

        self.assertEqual(2, len(self.api.requests))

    def test_a_failed_page_leaves_the_current_page_in_place(self):
        self.reply_page(["a"], cursor="c1")
        pager = self.list_reports()
        failures = (
            (NotFoundError, 404, {"type": "not-found", "error": "Gone."}),
            (APIConnectionError, 200, {"records": ["not", "a", "list"]}),
            (APIConnectionError, 200, [None]),
            (APIConnectionError, 200, [{"path": "reports/b"}, "reports/c"]),
        )

        for error, status, body in failures:
            self.api.reply_json(
                body, status=status, headers={"X-Files-Cursor": "c2"}
            )
            with self.assertRaises(error):
                pager.load_next_page()

        self.assertEqual(["reports/a"], [item.path for item in pager])
        self.assertEqual("c1", pager.cursor)
        self.reply_page(["b"])
        self.assertEqual(
            ["reports/b"], [item.path for item in pager.load_next_page()]
        )
        self.assertEqual(
            [None] + ["c1"] * (len(failures) + 1), self.sent_cursors()
        )

    def test_records_are_read_like_any_other_response(self):
        self.api.reply_json([{}, {"id": 2, "min_free_cpu": "12.50"}])
        records = list(files_sdk.remote_mount_backend.list())
        self.assertEqual([None, 2], [record.id for record in records])
        self.assertEqual(Decimal("12.50"), records[1].min_free_cpu)

        self.api.reply_json(
            [{"id": 3, "min_free_cpu": "not a number"}], status=200
        )
        with self.assertRaises(APIConnectionError) as caught:
            files_sdk.remote_mount_backend.list()
        self.assertEqual(200, caught.exception.http_status)


if __name__ == "__main__":
    unittest.main()
