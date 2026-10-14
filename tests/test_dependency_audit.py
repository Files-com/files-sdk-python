"""scripts/tasks.py audit, with a stand-in for pip-audit: each lock must have
a fresh report that lists every package it pins, at its pinned version, with
nothing skipped and no known vulnerability, and the audit replaces only an
earlier audit's output, never anything else. The package's scripts are not
installed with it, so this runs only from the source tree."""

import contextlib
import hashlib
import importlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"

# What each lock pins, written as scripts/lock.py writes a lock. Only Linux
# needs cffi, but the audit covers it on every platform.
LOCKS = {
    "runtime": {"idna": "3.20", "requests": "2.34.2"},
    "runtime-minimum": {"idna": "3.15", "requests": "2.34.2"},
    "pip": {"pip": "25.2"},
    "build-backend": {"setuptools": "80.9.0"},
    "check": {"black": "25.1.0"},
    "package": {"build": "1.3.0", "cffi": "2.1.1"},
    "audit": {"pip-audit": "2.10.1"},
    "docs": {"sphinx": "8.2.3"},  # a lock added later is audited too
}
MARKERS = {"cffi": ' ; sys_platform == "linux"'}

# Run as python -m pip_audit: writes the report the case gives for its
# --output file, if the case gives one, and exits 1 for the case's
# vulnerable report, as pip-audit does when it finds a vulnerability.
PIP_AUDIT = """\
import os
import shutil
import sys
from pathlib import Path

output = Path(sys.argv[sys.argv.index("--output") + 1])
given = Path(os.environ["GIVEN_REPORTS"]) / output.name
if given.exists():
    shutil.copy(given, output)
sys.exit(1 if output.name == os.environ["GIVEN_VULNERABLE"] else 0)
"""


def report(pins):
    """pip-audit's JSON report of pins, each audited with no known
    vulnerability, as pip_audit/_format/json.py writes it."""
    return {
        "dependencies": [
            {"name": name, "version": version, "vulns": []}
            for name, version in pins.items()
        ],
        "fixes": [],
    }


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contents(directory):
    """What directory holds: each entry's name, with its bytes, or its
    target if it is a symbolic link."""
    return {
        entry.name: (
            os.readlink(entry) if entry.is_symlink() else entry.read_bytes()
        )
        for entry in directory.iterdir()
    }


@unittest.skipUnless(
    (SCRIPTS / "tasks.py").exists(),
    "the package's scripts are not beside these tests",
)
class TestDependencyAudit(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
            self.tasks = importlib.import_module("tasks")

    def scratch(self):
        return Path(self.enterContext(tempfile.TemporaryDirectory()))

    def audit(self, reports, locks=LOCKS, vulnerable="", outdir=None):
        """Run tasks.py's audit of locks into outdir (a new directory unless
        given), with the stand-in pip-audit giving reports (by lock), and
        return outdir and the audit's failure, if it failed."""
        scratch = self.scratch()
        requirements, given, fake = (
            scratch / name for name in ("requirements", "given", "fake")
        )
        outdir = outdir or scratch / "audit"
        for directory in (
            requirements,
            given,
            fake / "pip_audit",
            fake / "pip_audit-2.10.1.dist-info",
        ):
            directory.mkdir(parents=True)
        for stem, pins in locks.items():
            (requirements / f"{stem}.txt").write_text(
                "".join(
                    f"{name}=={version}{MARKERS.get(name, '')} \\\n"
                    f"    --hash=sha256:{'0' * 64}\n"
                    for name, version in pins.items()
                )
            )
        for stem, content in reports.items():
            if content is not None:
                text = (
                    content
                    if isinstance(content, str)
                    else json.dumps(content)
                )
                (given / f"audit-{stem}.json").write_text(text)
        (fake / "pip_audit" / "__init__.py").write_text("")
        (fake / "pip_audit" / "__main__.py").write_text(PIP_AUDIT)
        (fake / "pip_audit-2.10.1.dist-info" / "METADATA").write_text(
            "Metadata-Version: 2.1\nName: pip-audit\nVersion: 2.10.1\n"
        )
        environment = {
            "PYTHONPATH": str(fake),
            "GIVEN_REPORTS": str(given),
            "GIVEN_VULNERABLE": vulnerable,
        }
        with (
            mock.patch.dict(os.environ, environment),
            mock.patch.object(self.tasks, "REQUIREMENTS", requirements),
            mock.patch.object(
                self.tasks, "environment", return_value=Path(sys.executable)
            ),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            try:
                self.tasks.audit(outdir)
            except self.tasks.TaskFailed as failure:
                return outdir, str(failure)
        return outdir, None

    def test_each_lock_needs_a_fresh_complete_report_with_no_known_vulnerability(
        self,
    ):
        clean = {stem: report(pins) for stem, pins in LOCKS.items()}
        # An earlier audit's output, of a lock since removed too, is replaced:
        # only this audit's files are left.
        reused = self.scratch()
        for name in (
            "audit-coverage.json",
            "audit-old.json",
            "old-all-platforms.txt",
        ):
            (reused / name).write_text("an earlier audit's output")
        outdir, failure = self.audit(clean, outdir=reused)
        self.assertIsNone(failure)
        self.assertEqual(
            sorted(path.name for path in outdir.iterdir()),
            sorted(
                [
                    "audit-coverage.json",
                    *(f"audit-{stem}.json" for stem in LOCKS),
                    *(f"{stem}-all-platforms.txt" for stem in LOCKS),
                ]
            ),
        )
        manifest = json.loads((outdir / "audit-coverage.json").read_text())
        self.assertEqual(
            (manifest["python"], manifest["pip-audit"]),
            (sys.version, "2.10.1"),
        )
        self.assertEqual(
            {
                lock: (entry["result"], entry["report_sha256"])
                for lock, entry in manifest["locks"].items()
            },
            {
                f"{stem}.txt": (
                    "passed",
                    sha256(outdir / f"audit-{stem}.json"),
                )
                for stem in LOCKS
            },
        )

        skipped = report(LOCKS["runtime"])
        skipped["dependencies"][1] = {
            "name": "requests",
            "skip_reason": "Dependency not found on PyPI and could not be "
            "audited: requests (2.34.2)",
        }
        without_minimum = {
            stem: pins
            for stem, pins in LOCKS.items()
            if stem != "runtime-minimum"
        }
        earlier = self.scratch()
        (earlier / "audit-runtime.json").write_text(
            json.dumps(clean["runtime"])
        )
        for case, arguments, expected in (
            (
                "a required lock is missing",
                {"reports": clean, "locks": without_minimum},
                r"requirements/ has no runtime-minimum\.txt",
            ),
            (
                "only an earlier audit's report",
                {"reports": {**clean, "runtime": None}, "outdir": earlier},
                r"runtime\.txt: pip-audit wrote no report",
            ),
            (
                "an empty report",
                {"reports": {**clean, "runtime": ""}},
                r"runtime\.txt: audit-runtime\.json is not pip-audit JSON",
            ),
            (
                "a partial report",
                {"reports": {**clean, "runtime": report({"idna": "3.20"})}},
                r"runtime\.txt: requests 2\.34\.2 is not in the report",
            ),
            (
                "a skipped package",
                {"reports": {**clean, "runtime": skipped}},
                r"runtime\.txt: requests was skipped",
            ),
            (
                "the other runtime graph's version",
                {"reports": {**clean, "runtime-minimum": clean["runtime"]}},
                r"runtime-minimum\.txt: idna is reported at 3\.20, not the "
                r"pinned 3\.15",
            ),
        ):
            with self.subTest(case):
                _outdir, failure = self.audit(**arguments)
                self.assertRegex(failure or "the audit passed", expected)

        # A vulnerability fails the audit, and its report is kept and recorded.
        vulnerable = report(LOCKS["runtime"])
        vulnerable["dependencies"][1]["vulns"] = [
            {"id": "PYSEC-2026-1", "fix_versions": ["2.35.0"]}
        ]
        outdir, failure = self.audit(
            {**clean, "runtime": vulnerable}, vulnerable="audit-runtime.json"
        )
        self.assertRegex(
            failure or "the audit passed",
            r"runtime\.txt: pip-audit found vulnerabilities",
        )
        self.assertEqual(
            json.loads((outdir / "audit-runtime.json").read_text()), vulnerable
        )
        recorded = json.loads((outdir / "audit-coverage.json").read_text())
        runtime = recorded["locks"]["runtime.txt"]
        self.assertEqual(
            (runtime["report_sha256"], runtime["result"][:7]),
            (sha256(outdir / "audit-runtime.json"), "failed:"),
        )

    @unittest.skipIf(
        os.name == "nt", "symbolic links need privileges on Windows"
    )
    def test_an_output_directory_holding_other_files_is_refused_and_left_alone(
        self,
    ):
        clean = {stem: report(pins) for stem, pins in LOCKS.items()}
        outside = self.scratch()
        (outside / "kept.txt").write_text("a symbolic link's target")
        crowded = self.scratch()
        (crowded / "notes.txt").write_text("the caller's own file")
        (crowded / "audit-runtime.json").write_text(
            "an earlier audit's report"
        )
        (crowded / "link").symlink_to(outside / "kept.txt")
        linked = self.scratch() / "linked"
        linked.symlink_to(outside, target_is_directory=True)
        before = {
            directory: contents(directory) for directory in (crowded, outside)
        }
        for case, outdir in (
            ("a directory holding other files and a link", crowded),
            ("a link to a directory holding other files", linked),
        ):
            with self.subTest(case):
                _outdir, failure = self.audit(clean, outdir=outdir)
                self.assertRegex(
                    failure or "the audit passed",
                    r"holds files an audit did not write",
                )
                self.assertEqual(
                    {directory: contents(directory) for directory in before},
                    before,
                )
                self.assertTrue(linked.is_symlink())
