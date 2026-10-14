"""scripts/tasks.py build writes only into a directory of its own: a new
one, an empty one, or one holding only an earlier build's output, which it
replaces. Anything else there is refused and left as it is. The package's
scripts are not installed with it, so this runs only from the source tree."""

import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def contents(directory):
    return {
        entry.relative_to(directory).as_posix(): (
            os.readlink(entry)
            if entry.is_symlink()
            else entry.read_bytes() if entry.is_file() else None
        )
        for entry in directory.rglob("*")
    }


@unittest.skipUnless(
    (SCRIPTS / "tasks.py").exists(),
    "the package's scripts are not beside these tests",
)
class TestBuildOutput(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
            self.tasks = importlib.import_module("tasks")

    def scratch(self):
        return Path(self.enterContext(tempfile.TemporaryDirectory()))

    def earlier_build(self, directory):
        (directory / "files_com-1.0.tar.gz").write_bytes(b"sdist")
        (directory / "files_com-1.0-py3-none-any.whl").write_bytes(b"wheel")
        (directory / "SHA256SUMS.json").write_text("{}")
        (directory / "from-sdist").mkdir()
        (
            directory / "from-sdist" / "files_com-1.0-py3-none-any.whl"
        ).write_bytes(b"rebuilt")

    def test_a_new_or_earlier_build_directory_is_used_and_emptied(self):
        missing = self.scratch() / "dist" / "nested"
        earlier = self.scratch()
        self.earlier_build(earlier)

        self.assertEqual(missing, self.tasks.build_output(missing))
        self.assertEqual({}, contents(missing))
        self.assertEqual(earlier, self.tasks.build_output(earlier))
        self.assertEqual({}, contents(earlier))

    @unittest.skipIf(
        os.name == "nt", "symbolic links need privileges on Windows"
    )
    def test_a_directory_holding_other_files_is_refused_and_left_alone(self):
        outside = self.scratch()
        (outside / "kept.txt").write_text("a symbolic link's target")
        crowded = self.scratch()
        self.earlier_build(crowded)
        (crowded / "notes.txt").write_text("the caller's own file")
        linked = self.scratch()
        self.earlier_build(linked)
        (linked / "files_com-1.0.tar.gz").unlink()
        (linked / "files_com-1.0.tar.gz").symlink_to(outside / "kept.txt")
        nested = self.scratch()
        self.earlier_build(nested)
        (nested / "from-sdist" / "deeper").mkdir()
        before = {
            directory: contents(directory)
            for directory in (crowded, linked, nested, outside)
        }

        for case, outdir in (
            ("a file a build did not write", crowded),
            ("a link named like an artifact", linked),
            ("a folder inside from-sdist", nested),
        ):
            with self.subTest(case):
                with self.assertRaisesRegex(
                    self.tasks.TaskFailed, "holds files a build did not write"
                ):
                    self.tasks.build_output(outdir)
        self.assertEqual(
            before, {directory: contents(directory) for directory in before}
        )


if __name__ == "__main__":
    unittest.main()
