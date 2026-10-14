import base64
import errno
import io
import logging
import os
import stat
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import files_sdk
from files_sdk.error import (
    APIConnectionError,
    APIError,
    InvalidParameterError,
    OperationCancelledError,
)
from files_sdk.models import Behavior, Style, User
from tests.loopback_api import serve_loopback_api, start_loopback_api

PICTURE = b"\x89PNG\r\n\x1a\n" + bytes(range(256)) * 4
# A form upload keeps this name; the API's form parser would decode the "%".
FORM_NAME = "avatar.png"
JSON_NAME = "avatar 100%.png"


class ForwardOnly(io.RawIOBase):
    """A stream that cannot seek, such as a pipe, returning at most chunk
    bytes a read."""

    def __init__(self, data, chunk=7):
        self._data = memoryview(data)
        self._chunk = chunk
        self.bytes_read = 0

    def readable(self):
        return True

    def readinto(self, buffer):
        count = min(len(buffer), self._chunk, len(self._data))
        buffer[:count] = self._data[:count]
        self._data = self._data[count:]
        self.bytes_read += count
        return count


class CancelsOnRead(ForwardOnly):
    """A forward-only stream that cancels token when it is read for the
    cancel_on-th time, and counts its reads."""

    def __init__(self, data, token, cancel_on):
        super().__init__(data, chunk=4096)
        self.token = token
        self.cancel_on = cancel_on
        self.reads = 0

    def readinto(self, buffer):
        self.reads += 1
        if self.reads == self.cancel_on:
            self.token.cancel()
        return super().readinto(buffer)


class NoDataReady(io.RawIOBase):
    def readable(self):
        return True

    def readinto(self, buffer):
        return None


class EndsEarly(io.BytesIO):
    """A seekable stream whose reads stop before its end."""

    def __init__(self, data, ends_after):
        super().__init__(data)
        self._ends_after = ends_after

    def read(self, size=-1):
        remaining = max(0, self._ends_after - self.tell())
        return super().read(remaining if size < 0 else min(size, remaining))


class InterruptsWhileSent(io.BytesIO):
    def read(self, size=-1):
        if self.tell() > 0:
            raise KeyboardInterrupt
        return super().read(min(size, 10))


class ReturnsText:
    def read(self, size=-1):
        return "text"


class SpoolThatFailsToClose(io.BytesIO):
    """A temporary spool whose storage fails as it is deleted."""

    def __exit__(self, *exc_info):
        super().__exit__(*exc_info)
        raise OSError("disk failure while deleting a spool")


def sent_file(request, name):
    """(representation, filename, content type, bytes) of the attachment a
    request sent in parameter name."""
    if request.headers["Content-Type"].startswith("multipart/form-data;"):
        part = request.form_file(name)
        return "form", part.filename, part.content_type, part.data
    file_object = request.json[name]
    return (
        "json",
        file_object["filename"],
        file_object["type"],
        base64.b64decode(file_object["encoded_content"], validate=True),
    )


def json_without(request, name):
    """A JSON request's parameters other than name."""
    return {key: value for key, value in request.json.items() if key != name}


def regular_file_descriptors():
    """(device, inode) of every regular file this process has open, where
    the platform lists open descriptors."""
    if not os.path.isdir("/dev/fd"):
        return None
    files = set()
    for name in os.listdir("/dev/fd"):
        try:
            info = os.fstat(int(name))
        except OSError:
            continue
        if stat.S_ISREG(info.st_mode):
            files.add((info.st_dev, info.st_ino))
    return files


class AttachmentTestCase(unittest.TestCase):
    def setUp(self):
        self.api = serve_loopback_api(self, max_network_retries=2)
        # Keep the API errors these tests expect off stderr.
        quiet = logging.NullHandler()
        logging.getLogger("files_sdk").addHandler(quiet)
        self.addCleanup(logging.getLogger("files_sdk").removeHandler, quiet)
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)

    def local_file(self, name, data):
        path = self.scratch / name
        path.write_bytes(data)
        return path

    def open_local(self, name, data):
        stream = self.local_file(name, data).open("rb")
        self.addCleanup(stream.close)
        return stream

    def assert_released(self, path):
        """The SDK holds no handle on the file: no descriptor refers to it,
        and it can be renamed and deleted, which Windows refuses while a
        handle is open."""
        info = path.stat()
        descriptors = regular_file_descriptors()
        if descriptors is not None:
            self.assertNotIn((info.st_dev, info.st_ino), descriptors)
        moved = path.with_name(path.name + ".moved")
        os.replace(path, moved)
        os.remove(moved)


class TestAttachmentWire(AttachmentTestCase):
    def test_update_sends_the_file_and_the_other_parameters_as_form_data(self):
        stream = io.BytesIO(b"already read" + PICTURE)
        stream.seek(len(b"already read"))
        self.api.reply_json({"id": 5, "name": "Pat"})

        with self.assertLogs("files_sdk", level=logging.DEBUG) as logs:
            user = files_sdk.user.update(
                5,
                {
                    "avatar_file": files_sdk.Attachment(
                        stream, filename="avatar.png", content_type="image/png"
                    ),
                    "name": "Pat",
                    "ftp_permission": False,
                    "notification_daily_send_time": 0,
                    "notes": "",
                    "change_password": "private-password",
                },
                {"api_key": "callkey", "workspace_id": 0},
            )

        [request] = self.api.requests
        self.assertEqual(("PATCH", "/users/5"), (request.method, request.path))
        self.assertTrue(request.complete)
        self.assertEqual("callkey", request.headers["X-FilesAPI-Key"])
        self.assertEqual("0", request.headers["X-Files-Workspace-Id"])
        avatar = request.form_file("avatar_file")
        self.assertEqual(
            ("avatar.png", "image/png", PICTURE),
            (avatar.filename, avatar.content_type, avatar.data),
        )
        self.assertEqual(
            [
                ("name", "Pat"),
                ("ftp_permission", "false"),
                ("notification_daily_send_time", "0"),
                ("notes", ""),
                ("change_password", "private-password"),
                ("id", "5"),
            ],
            request.form_values(),
        )
        self.assertIsInstance(user, User)
        self.assertEqual((5, "Pat"), (user.id, user.name))
        self.assertEqual(
            {"api_key": "callkey", "workspace_id": 0}, user.options
        )
        # The caller's stream is left open, at the end of what was sent.
        self.assertFalse(stream.closed)
        self.assertEqual(len(b"already read" + PICTURE), stream.tell())
        # DEBUG shows the request's fields without their values.
        log = "\n".join(logs.output)
        self.assertIn("avatar_file=(avatar.png, image/png", log)
        self.assertNotIn("private-password", log)

    def test_each_file_parameter_is_sent_by_its_operation(self):
        operations = [
            (
                "POST",
                "/users",
                "avatar_file",
                lambda file: files_sdk.user.create(
                    {"username": "pat", "avatar_file": file}
                ),
            ),
            (
                "PATCH",
                "/users/5",
                "avatar_file",
                lambda file: files_sdk.user.update(5, {"avatar_file": file}),
            ),
            (
                "PATCH",
                "/users/5",
                "avatar_file",
                lambda file: User({"id": 5}).update({"avatar_file": file}),
            ),
            (
                "POST",
                "/behaviors",
                "attachment_file",
                lambda file: files_sdk.behavior.create(
                    {
                        "path": "shared",
                        "behavior": "watermark",
                        "attachment_file": file,
                    }
                ),
            ),
            (
                "PATCH",
                "/behaviors/6",
                "attachment_file",
                lambda file: files_sdk.behavior.update(
                    6, {"attachment_file": file}
                ),
            ),
            (
                "POST",
                "/bundles",
                "watermark_attachment_file",
                lambda file: files_sdk.bundle.create(
                    {"paths": ["a.txt"], "watermark_attachment_file": file}
                ),
            ),
            (
                "PATCH",
                "/bundles/7",
                "watermark_attachment_file",
                lambda file: files_sdk.bundle.update(
                    7, {"watermark_attachment_file": file}
                ),
            ),
            (
                "PATCH",
                "/styles/branding",
                "file",
                lambda file: files_sdk.style.update(
                    "branding", {"file": file}
                ),
            ),
            (
                "PATCH",
                "/styles/branding",
                "file",
                lambda file: Style({"path": "branding"}).update(
                    {"file": file}
                ),
            ),
        ] + [
            (
                "PATCH",
                "/site",
                field,
                lambda file, field=field: files_sdk.site.update({field: file}),
            )
            for field in (
                "icon16_file",
                "icon32_file",
                "icon48_file",
                "icon128_file",
                "logo_file",
                "bundle_watermark_attachment_file",
                "login_page_background_image_file",
            )
        ]
        for method, path, field, call in operations:
            with self.subTest(route=f"{method} {path}", field=field):
                self.api.requests.clear()
                self.api.reply_json({"id": 1})

                call(PICTURE)

                [request] = self.api.requests
                self.assertEqual(
                    (method, path), (request.method, request.path)
                )
                part = request.form_file(field)
                self.assertEqual(
                    (field, "application/octet-stream", PICTURE),
                    (part.filename, part.content_type, part.data),
                )

    def test_a_site_update_can_send_every_image_at_once(self):
        images = {
            field: bytes([number]) * (number + 1)
            for number, field in enumerate(
                (
                    "icon16_file",
                    "icon32_file",
                    "icon48_file",
                    "icon128_file",
                    "logo_file",
                    "bundle_watermark_attachment_file",
                    "login_page_background_image_file",
                )
            )
        }
        self.api.reply_json({"name": "Site"})

        files_sdk.site.update({**images, "welcome_email_enabled": True})

        [request] = self.api.requests
        self.assertEqual(
            images,
            {part.name: part.data for part in request.form if part.filename},
        )
        self.assertEqual(
            [("welcome_email_enabled", "true")], request.form_values()
        )

    def test_names_default_to_a_base_name_or_the_parameter_name(self):
        stream = self.open_local("from-disk.png", PICTURE)
        for label, file, filename, data in (
            ("empty bytes", b"", "avatar_file", b""),
            ("bytearray", bytearray(b"abc"), "avatar_file", b"abc"),
            ("stream of a local file", stream, "from-disk.png", PICTURE),
            (
                "local path",
                files_sdk.Attachment.from_path(
                    self.local_file("path.png", b"p")
                ),
                "path.png",
                b"p",
            ),
            (
                "explicit name",
                files_sdk.Attachment(b"x", filename="chosen.png"),
                "chosen.png",
                b"x",
            ),
        ):
            with self.subTest(label):
                self.api.requests.clear()
                self.api.reply_json({"id": 5})

                files_sdk.user.update(5, {"avatar_file": file})

                part = self.api.requests[0].form_file("avatar_file")
                self.assertEqual(
                    (filename, "application/octet-stream", data),
                    (part.filename, part.content_type, part.data),
                )

    def test_metadata_that_could_add_part_headers_is_refused(self):
        for metadata in (
            {"content_type": "image/png\r\nX-Injected: yes"},
            {"content_type": "not a media type"},
            {"filename": "avatar.png\r\nContent-Type: text/html"},
            {"filename": ""},
        ):
            with self.subTest(**metadata):
                with self.assertRaises(ValueError):
                    files_sdk.Attachment(PICTURE, **metadata)

    def test_objects_and_lists_are_sent_with_bracketed_names(self):
        self.api.reply_json({"id": 7})

        files_sdk.bundle.update(
            7,
            {
                "watermark_attachment_file": PICTURE,
                "paths": ["a.txt", "b/c.txt"],
                "watermark_value": {"gravity": "Center", "transparency": "25"},
                "max_uses": 0,
            },
        )

        self.assertEqual(
            [
                ("paths[]", "a.txt"),
                ("paths[]", "b/c.txt"),
                ("watermark_value[gravity]", "Center"),
                ("watermark_value[transparency]", "25"),
                ("max_uses", "0"),
                ("id", "7"),
            ],
            self.api.requests[0].form_values(),
        )

    def test_values_form_fields_would_change_are_sent_exactly_as_json(self):
        for label, call, field in (
            (
                "None",
                lambda file: Behavior({"id": 6}).update(
                    {"attachment_file": file, "recursive": None}
                ),
                "attachment_file",
            ),
            (
                "empty list",
                lambda file: files_sdk.bundle.update(
                    7, {"watermark_attachment_file": file, "paths": []}
                ),
                "watermark_attachment_file",
            ),
            (
                "empty object",
                lambda file: files_sdk.behavior.update(
                    6, {"attachment_file": file, "value": {}}
                ),
                "attachment_file",
            ),
            (
                "typed values inside an object",
                lambda file: files_sdk.behavior.create(
                    {
                        "path": "shared/previews",
                        "behavior": "watermark",
                        "attachment_file": file,
                        "value": {
                            "transparency": 25,
                            "ratio": 0.5,
                            "limit": Decimal("12.50"),
                            "none": None,
                        },
                    }
                ),
                "attachment_file",
            ),
            (
                "booleans inside an object",
                lambda file: files_sdk.site.update(
                    {
                        "logo_file": file,
                        "left_navigation_visibility": {
                            "sharing": {"admin": True, "all": False}
                        },
                    }
                ),
                "logo_file",
            ),
            (
                "list of objects",
                lambda file: files_sdk.behavior.update(
                    6,
                    {
                        "attachment_file": file,
                        "value": {"rules": [{"x": "1"}, {"y": 2}]},
                    },
                ),
                "attachment_file",
            ),
            (
                "key with brackets",
                lambda file: files_sdk.behavior.update(
                    6, {"attachment_file": file, "value": {"a[b]": "c"}}
                ),
                "attachment_file",
            ),
        ):
            with self.subTest(label):
                self.api.requests.clear()
                stream = io.BytesIO(b"skipped" + PICTURE)
                stream.seek(len(b"skipped"))
                self.api.reply_json({"id": 6})
                self.api.reply_json({"id": 6})

                call(None)
                call(stream)

                without_file, with_file = self.api.requests
                self.assertTrue(with_file.complete)
                self.assertEqual(
                    ("json", field, "application/octet-stream", PICTURE),
                    sent_file(with_file, field),
                )
                # The other parameters are exactly what JSON sends without
                # the file.
                self.assertEqual(
                    json_without(without_file, field),
                    json_without(with_file, field),
                )

    def test_existing_file_objects_and_other_values_are_sent_as_given(self):
        file_object = {
            "encoded_content": base64.b64encode(PICTURE).decode(),
            "filename": "avatar.png",
            "type": "image/png",
        }
        for value in (file_object, "", {"unexpected": "shape"}):
            with self.subTest(value=value):
                self.api.requests.clear()
                self.api.reply_json({"id": 5})

                files_sdk.user.update(
                    5, {"avatar_file": value, "notes": "kept"}
                )

                [request] = self.api.requests
                self.assertEqual(
                    "application/json", request.headers["Content-Type"]
                )
                self.assertEqual(
                    {"avatar_file": value, "notes": "kept", "id": 5},
                    request.json,
                )

    def test_existing_file_objects_join_new_attachments_in_one_request(self):
        logo = {
            "encoded_content": base64.b64encode(b"logo").decode(),
            "filename": "logo.png",
            "type": "image/png",
        }
        for representation, companions in (
            ("form", {"welcome_email_enabled": True}),
            ("json", {"additional_text_file_types": []}),
        ):
            with self.subTest(representation):
                self.api.requests.clear()
                self.api.reply_json({"name": "Site"})

                files_sdk.site.update(
                    {"logo_file": logo, "icon16_file": PICTURE, **companions}
                )

                [request] = self.api.requests
                self.assertEqual(
                    (
                        representation,
                        "icon16_file",
                        "application/octet-stream",
                        PICTURE,
                    ),
                    sent_file(request, "icon16_file"),
                )
                if representation == "form":
                    # Rack reads these fields back as the same object.
                    self.assertEqual(
                        [
                            (
                                "logo_file[encoded_content]",
                                logo["encoded_content"],
                            ),
                            ("logo_file[filename]", "logo.png"),
                            ("logo_file[type]", "image/png"),
                            ("welcome_email_enabled", "true"),
                        ],
                        request.form_values(),
                    )
                else:
                    self.assertEqual(
                        {"logo_file": logo, **companions},
                        json_without(request, "icon16_file"),
                    )

    def test_file_names_the_form_parser_would_change_are_sent_as_json(self):
        for filename, representation in (
            ("plain name.png", "form"),
            ("émoji-😀.png", "form"),
            ("a%22b.png", "json"),
            ("a%0Ab.png", "json"),
            ("100% done.png", "json"),
            ('a\\"b.png', "json"),
            ("dir\\path.png", "json"),
            ("dir/path.png", "json"),
            ('a"b.png', "json"),
        ):
            with self.subTest(filename=filename):
                self.api.requests.clear()
                self.api.reply_json({"id": 5})

                files_sdk.user.update(
                    5,
                    {
                        "avatar_file": files_sdk.Attachment(
                            PICTURE,
                            filename=filename,
                            content_type="image/png",
                        )
                    },
                )

                self.assertEqual(
                    (representation, filename, "image/png", PICTURE),
                    sent_file(self.api.requests[0], "avatar_file"),
                )

    def test_values_that_can_never_be_sent_raise_before_a_request(self):
        text_file = self.local_file("notes.txt", b"text").open("r")
        self.addCleanup(text_file.close)
        for label, value in (
            ("a Path", self.local_file("avatar.png", PICTURE)),
            ("a text stream", text_file),
        ):
            with self.subTest(label):
                with self.assertRaises(InvalidParameterError):
                    files_sdk.user.update(5, {"avatar_file": value})
        with self.assertRaises(InvalidParameterError):
            files_sdk.behavior.update(
                6, {"attachment_file": PICTURE, "value": {"at": object()}}
            )
        self.assertEqual([], self.api.requests)

    def test_requests_without_file_content_are_sent_as_json(self):
        self.api.reply_json({"id": 5})

        files_sdk.user.update(5, {"avatar_file": None, "name": "Pat"})

        [request] = self.api.requests
        self.assertEqual("application/json", request.headers["Content-Type"])
        self.assertEqual(
            {"avatar_file": None, "name": "Pat", "id": 5}, request.json
        )


class TestAttachmentReplay(AttachmentTestCase):
    def sources(self):
        """Each kind of attachment source, named so it is sent as form data
        and so it is sent as JSON, with the bytes it should send."""
        sources = []
        for filename in (FORM_NAME, JSON_NAME):
            suffix_stream = io.BytesIO(b"skipped" + PICTURE)
            suffix_stream.seek(len(b"skipped"))
            suffix_file = self.open_local("suffix.png", b"skipped" + PICTURE)
            suffix_file.seek(len(b"skipped"))
            path = self.local_file("path.png", PICTURE)
            for label, content in (
                ("bytes", PICTURE),
                ("stream from its position", suffix_stream),
                ("file from its position", suffix_file),
                ("stream that cannot seek", ForwardOnly(PICTURE)),
            ):
                sources.append(
                    (
                        f"{label} named {filename!r}",
                        lambda content=content, filename=filename: (
                            files_sdk.Attachment(content, filename=filename)
                        ),
                    )
                )
            sources.append(
                (
                    f"local path named {filename!r}",
                    lambda path=path, filename=filename: (
                        files_sdk.Attachment.from_path(path, filename=filename)
                    ),
                )
            )
        return sources

    def assert_attempts_sent_the_same_body(self, expected_attempts):
        self.assertEqual(expected_attempts, len(self.api.requests))
        final = self.api.requests[-1]
        self.assertTrue(final.complete)
        representation, filename, _type, data = sent_file(final, "avatar_file")
        self.assertEqual(
            "form" if filename == FORM_NAME else "json", representation
        )
        self.assertEqual(PICTURE, data)
        if representation == "form":
            self.assertEqual(
                [("name", "Pat"), ("id", "5")], final.form_values()
            )
        else:
            self.assertEqual(
                {"name": "Pat", "id": 5}, json_without(final, "avatar_file")
            )
        return final

    def test_an_update_answered_with_a_server_error_is_not_sent_again(self):
        # Files.com may have carried it out before answering, whatever the
        # answer says.
        for label, source in self.sources():
            with self.subTest(label):
                self.api.requests.clear()
                self.api.reply_json(
                    {"error": "Busy", "type": "service-unavailable"},
                    status=503,
                )
                self.api.reply_json({"id": 5})

                with self.assertRaises(APIError) as caught:
                    files_sdk.user.update(
                        5, {"avatar_file": source(), "name": "Pat"}
                    )

                self.assertTrue(caught.exception.remote_outcome_unknown)
                self.assert_attempts_sent_the_same_body(1)
                self.api.responses.clear()

    def test_an_update_whose_connection_dropped_mid_body_is_not_sent_again(
        self,
    ):
        # Files.com may have received it all, so it is not repeated.
        for label, source in self.sources():
            with self.subTest(label):
                self.api.requests.clear()
                self.api.disconnect(after_body_bytes=21)
                self.api.reply_json({"id": 5})

                with self.assertRaises(APIConnectionError) as caught:
                    files_sdk.user.update(
                        5, {"avatar_file": source(), "name": "Pat"}
                    )

                self.assertTrue(caught.exception.remote_outcome_unknown)
                self.assertEqual(1, len(self.api.requests))
                self.api.responses.clear()

    def test_temporary_redirects_resend_the_body_and_see_other_does_not(self):
        for status in (307, 308):
            for label, source in self.sources():
                with self.subTest(status=status, source=label):
                    self.api.requests.clear()
                    self.api.reply(
                        status, headers={"Location": "/api/rest/v1/users/5"}
                    )
                    self.api.reply_json({"id": 5})

                    files_sdk.user.update(
                        5, {"avatar_file": source(), "name": "Pat"}
                    )

                    first, second = self.api.requests
                    self.assertEqual("PATCH", second.method)
                    self.assertEqual(
                        "globalkey", second.headers["X-FilesAPI-Key"]
                    )
                    self.assertEqual(first.body, second.body)
                    self.assert_attempts_sent_the_same_body(2)

        self.api.requests.clear()
        self.api.reply(303, headers={"Location": "/api/rest/v1/users/5"})
        self.api.reply_json({"id": 5})

        files_sdk.user.create({"username": "pat", "avatar_file": PICTURE})

        post, get = self.api.requests
        self.assertEqual(
            ("POST", "GET", b""), (post.method, get.method, get.body)
        )
        self.assertNotIn("Content-Type", get.headers)

    def test_a_redirect_to_another_origin_is_not_followed_with_the_attachment(
        self,
    ):
        # A 307 would carry the request, attachment and all, to the other
        # origin: neither the credentials nor the body go there.
        other = start_loopback_api(self)
        self.api.reply(
            307, headers={"Location": other.url + "/api/rest/v1/users/5"}
        )
        other.reply_json({"id": 5})

        with self.assertRaises(APIConnectionError) as caught:
            files_sdk.user.update(
                5,
                {"avatar_file": PICTURE},
                {"api_key": "callkey", "workspace_id": 3},
            )

        self.assertIn("not followed", str(caught.exception))
        self.assertEqual([], other.requests)
        [sent] = self.api.requests
        self.assertEqual(PICTURE, sent_file(sent, "avatar_file")[3])

    def test_json_requests_are_not_sent_again_after_an_error_either(self):
        self.api.reply_json({"error": "Busy"}, status=503)
        self.api.reply_json({"id": 5})

        with self.assertRaises(APIError) as caught:
            files_sdk.user.update(5, {"name": "Pat"})

        self.assertTrue(caught.exception.remote_outcome_unknown)
        [request] = self.api.requests
        self.assertEqual({"name": "Pat", "id": 5}, request.json)
        self.api.responses.clear()


class TestAttachmentOwnership(AttachmentTestCase):
    def test_the_sdk_closes_files_it_opens_and_leaves_the_callers_open(self):
        replies = {
            "success": lambda: self.api.reply_json({"id": 5}),
            "after retries": lambda: [
                self.api.reply_json({"error": "Busy"}, status=503)
                for _ in range(3)
            ],
            "API error": lambda: [
                self.api.reply_json(
                    {"type": "not-found", "error": "No user"}, status=404
                )
                for _ in range(3)
            ],
        }
        for representation, companions in (
            ("form", {}),
            (
                "json",
                {"left_navigation_visibility": {"sharing": {"admin": True}}},
            ),
        ):
            for label, reply in replies.items():
                with self.subTest(representation=representation, reply=label):
                    owned = self.local_file("owned.png", PICTURE)
                    borrowed = self.open_local("borrowed.png", PICTURE)
                    before = regular_file_descriptors()
                    reply()

                    try:
                        files_sdk.site.update(
                            {
                                "logo_file": files_sdk.Attachment.from_path(
                                    owned
                                ),
                                "icon16_file": borrowed,
                                # Large enough that its spool moves to disk.
                                "icon32_file": ForwardOnly(
                                    PICTURE * 1100, chunk=65536
                                ),
                                **companions,
                            }
                        )
                    except files_sdk.error.Error:
                        pass

                    self.assertEqual(
                        representation,
                        sent_file(self.api.requests[-1], "logo_file")[0],
                    )
                    self.assertFalse(borrowed.closed)
                    self.assert_released(owned)
                    if before is not None:
                        # The spool of the stream that cannot seek is gone.
                        self.assertEqual(before, regular_file_descriptors())

    def test_an_interrupted_request_still_closes_what_the_sdk_opened(self):
        for companions in ({}, {"additional_text_file_types": []}):
            with self.subTest(companions=companions):
                self.api.requests.clear()
                owned = self.local_file("owned.png", PICTURE)
                borrowed = InterruptsWhileSent(PICTURE)

                with self.assertRaises(KeyboardInterrupt):
                    files_sdk.site.update(
                        {
                            "logo_file": files_sdk.Attachment.from_path(owned),
                            "icon16_file": borrowed,
                            **companions,
                        }
                    )

                [request] = self.api.wait_for_requests(1)
                self.assertFalse(request.complete)
                self.assertFalse(borrowed.closed)
                self.assert_released(owned)

    def test_a_failed_preparation_keeps_its_error_when_cleanup_fails(self):
        with patch.object(
            tempfile,
            "SpooledTemporaryFile",
            lambda **options: SpoolThatFailsToClose(),
        ):
            with self.assertRaises(InvalidParameterError) as caught:
                files_sdk.site.update(
                    {
                        "logo_file": ForwardOnly(PICTURE),
                        "icon16_file": NoDataReady(),
                    }
                )
            self.assertIn("returned None", str(caught.exception))
            self.assertIn(
                "disk failure while deleting a spool",
                "\n".join(caught.exception.__notes__),
            )
            self.assertEqual([], self.api.requests)

            # With no other failure, the cleanup failure is the error.
            self.api.reply_json({"id": 5})
            with self.assertRaises(OSError):
                files_sdk.user.update(5, {"avatar_file": ForwardOnly(PICTURE)})
            [request] = self.api.requests
            self.assertTrue(request.complete)

    def test_streams_that_cannot_be_sent_completely_fail_without_a_retry(self):
        for label, file, message in (
            ("no data ready", NoDataReady(), "returned None"),
            ("text", ReturnsText(), "instead of bytes"),
            (
                "larger than its spool limit",
                files_sdk.Attachment(ForwardOnly(PICTURE), spool_limit=100),
                "more than the 100 bytes",
            ),
        ):
            with self.subTest(label):
                with self.assertRaises(InvalidParameterError) as caught:
                    files_sdk.user.update(5, {"avatar_file": file})
                self.assertIn(message, str(caught.exception))
        self.assertEqual([], self.api.requests)

        ends_early = EndsEarly(PICTURE, ends_after=100)
        with self.assertRaises(InvalidParameterError) as caught:
            files_sdk.user.update(5, {"avatar_file": ends_early})
        self.assertIn(
            f"ended after 100 of its {len(PICTURE)} bytes",
            str(caught.exception),
        )
        [request] = self.api.wait_for_requests(1)
        self.assertFalse(request.complete)
        self.assertFalse(ends_early.closed)

    def test_a_failing_source_s_own_error_text_stays_out_of_the_message(self):
        signed = (
            "https://source.example.test/object?token=private_source_token"
        )
        failure = OSError(errno.EIO, "cannot read " + signed)

        class FailingSource(io.RawIOBase):
            def readable(self):
                return True

            def readinto(self, buffer):
                raise failure

        source = FailingSource()
        with self.assertLogs("files_sdk", level=logging.DEBUG) as logs:
            with self.assertRaises(InvalidParameterError) as caught:
                files_sdk.user.update(5, {"avatar_file": source})

        message = str(caught.exception)
        self.assertNotIn("private_source_token", message)
        self.assertEqual(
            "Could not read the stream for avatar_file (OSError, errno 5 EIO).",
            message,
        )
        self.assertIs(failure, caught.exception.__cause__)
        self.assertIn("private_source_token", "\n".join(logs.output))
        self.assertFalse(source.closed)
        self.assertEqual([], self.api.requests)

    def test_a_cancelled_operation_reads_no_more_of_a_stream_it_buffers(self):
        for cancel_on, reads in ((0, 0), (1, 1)):
            with self.subTest(cancel_on=cancel_on):
                token = files_sdk.CancellationToken()
                if cancel_on == 0:
                    token.cancel()
                source = CancelsOnRead(PICTURE * 20, token, cancel_on)

                with self.assertRaises(OperationCancelledError):
                    files_sdk.user.update(
                        5, {"avatar_file": source}, {"cancel_token": token}
                    )

                self.assertEqual(reads, source.reads)
                self.assertFalse(source.closed)
        self.assertEqual([], self.api.requests)

    def test_a_stream_that_cannot_seek_is_buffered_up_to_its_limit(self):
        stream = ForwardOnly(PICTURE * 50, chunk=4096)

        with self.assertRaises(InvalidParameterError):
            files_sdk.user.update(
                5,
                {
                    "avatar_file": files_sdk.Attachment(
                        stream, spool_limit=10_000
                    )
                },
            )

        self.assertEqual([], self.api.requests)
        # It read one byte past the limit, and no more.
        self.assertEqual(10_001, stream.bytes_read)

    def test_short_reads_still_send_the_whole_stream(self):
        self.api.reply_json({"id": 5})

        files_sdk.user.update(
            5, {"avatar_file": ForwardOnly(PICTURE, chunk=1)}
        )

        self.assertEqual(
            PICTURE, self.api.requests[0].form_file("avatar_file").data
        )

    def test_a_local_file_that_changes_between_attempts_is_not_sent_again(
        self,
    ):
        path = self.local_file("changing.png", PICTURE)

        def change_the_file_keeping_its_size():
            path.write_bytes(bytes(reversed(PICTURE)))
            later = path.stat().st_mtime_ns + 1_000_000_000
            os.utime(path, ns=(later, later))

        # A temporary redirect sends the body again.
        self.api.reply(
            307,
            headers={"Location": "/api/rest/v1/users/5"},
            when_received=change_the_file_keeping_its_size,
        )

        with self.assertRaises(InvalidParameterError) as caught:
            files_sdk.user.update(
                5, {"avatar_file": files_sdk.Attachment.from_path(path)}
            )

        self.assertIn("changed while it was being sent", str(caught.exception))
        [request] = self.api.requests
        self.assertEqual(PICTURE, request.form_file("avatar_file").data)
        self.assert_released(path)


if __name__ == "__main__":
    unittest.main()
