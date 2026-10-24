"""Formats, checks, tests, packages and audits the Files.com Python SDK.

    python scripts/tasks.py format    # rewrite the sources with pinned Black
    python scripts/tasks.py check     # formatting, lint, types, then test
    python scripts/tasks.py types     # type check as every supported platform
                                      # and Python version would
    python scripts/tasks.py test [--dependencies minimum] [--artifact WHEEL]
    python scripts/tasks.py install-check --artifact WHEEL [--dependencies minimum]
                                      # install and check an artifact as
                                      # test --artifact does, then run only
                                      # its install tests, not the suite
    python scripts/tasks.py scenarios --out DIR [--launcher WITH_SCENARIO]
                                      # the tests of the shared mock server's
                                      # scenarios, under its launcher
    python scripts/tasks.py build     # build and inspect the sdist and wheel
    python scripts/tasks.py package   # build, inspect and test the artifacts
    python scripts/tasks.py audit     # audit every requirements/*.txt and
                                      # check each report covers its lock
    python scripts/tasks.py twine ... # run the pinned twine

Only format changes files. Every environment is built with the interpreter
that runs this script, so "python3.11 scripts/tasks.py test --dependencies
minimum" tests the oldest supported Python with the oldest allowed
dependencies. Environments are installed from the hash-pinned files in
requirements/ into .tools/ (or $FILES_SDK_TOOLS_DIR) and reused until those
files change. Type checking needs Node.js and npm on PATH; it runs Pyright
once for each platform (Linux, macOS, Windows) at each Python version that
pyproject.toml's classifiers list, because os and other modules differ between
them, and fails naming each that reported an error. This is static analysis,
not a run on those platforms. check, test and package need the Files.com mock
server that tests/base.py names; build and install-check do not, so a release
can build and check its artifacts without it.

test --artifact and install-check install a wheel or sdist, hash-checked,
into a new environment holding exactly the locked runtime graph, run pip
check, and confirm the installed files_sdk is byte for byte the artifact's,
imported from that environment, and that its installed metadata requires
what pyproject.toml does. test --artifact then runs every test against the
installed package from outside the source tree; install-check runs only
INSTALL_CHECK_TESTS there. The artifact's code is the source tree's, so a
full suite of the source tree and one of an installed artifact cover its
behavior; install-check is the check for the other artifacts, not a run of
the suite.

Tests that need a scenario of the shared mock server, such as
tests/test_shared_folder_list.py, are skipped by check, test and package.
scenarios runs them under the scenario's launcher, the generated mock
server's with-scenario.rb beside this package unless --launcher names
another, which starts the server for them and keeps its evidence in
DIR/SCENARIO. It fails unless the launcher succeeds and every one of those
tests ran.

audit writes the requirements it audited, pip-audit's reports and
audit-coverage.json to --outdir (.tools/reports by default). That directory
must be new, empty or hold only an earlier audit's output, which audit
replaces; audit refuses any other directory and deletes nothing in it.
"""

import argparse
import base64
import email.parser
import hashlib
import importlib.metadata
import json
import os
import re
import shutil
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
import venv
import zipfile
from pathlib import Path

from lock import normalize

if sys.version_info < (3, 11):
    sys.exit(f"tasks.py needs Python 3.11 or newer, not {sys.version}")

import tomllib  # noqa: E402 (needs the version check above)

PACKAGE = Path(__file__).resolve().parent.parent
REQUIREMENTS = PACKAGE / "requirements"
TOOLS = Path(
    os.environ.get("FILES_SDK_TOOLS_DIR", PACKAGE / ".tools")
).absolute()
SOURCES = ("files_sdk", "tests", "examples", "scripts", "scenarios")
# The files the sdist holds besides files_sdk/.
BUILD_INPUTS = ("pyproject.toml", "MANIFEST.in", "README.md", "LICENSE")
PYTHON_TAG = f"py{sys.version_info.major}{sys.version_info.minor}"
RUN_TESTS = PACKAGE / "scripts" / "run_tests.py"
PIP_INSTALL = ("-m", "pip", "--disable-pip-version-check", "--no-input")
LOCKED = ("install", "--quiet", "--require-hashes", "--only-binary", ":all:")


class TaskFailed(Exception):
    pass


def run(*command, **options):
    command = [str(part) for part in command]
    print("+", " ".join(command), flush=True)
    status = subprocess.run(command, **options).returncode
    if status != 0:
        raise TaskFailed(
            f"{Path(command[0]).name} exited with status {status}"
        )


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def python_in(environment):
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def tool_environment(name, *locks):
    """The path of the locked tool environment called name, and the stamp
    it holds once this interpreter has built it from today's locks."""
    path = TOOLS / f"{name}-{PYTHON_TAG}"
    stamp = {
        "python": sys.version,
        "executable": sys.executable,
        "locks": {
            lock: sha256(REQUIREMENTS / lock) for lock in ("pip.txt", *locks)
        },
    }
    return path, stamp


def record_unchanged(distribution):
    """Whether every file distribution's RECORD hashes still has that
    SHA-256."""
    hashed = [
        (file, digest)
        for file in distribution.files or ()
        if (digest := file.hash)
    ]
    return bool(hashed) and all(
        digest.mode == "sha256"
        and digest.value
        == base64.urlsafe_b64encode(
            hashlib.sha256(file.read_binary()).digest()
        )
        .rstrip(b"=")
        .decode()
        for file, digest in hashed
    )


def pip_seed(path):
    """The python of the check tool environment, whose pip can install
    pip.txt into path, a new environment made without pip, so that path
    needs no pip of its own first; or None, and path bootstraps pip as venv
    does.

    format and check build the check environment first, so every
    environment built after it can use it. It is used only as environment()
    would reuse it, with this interpreter's stamp of today's pip.txt and
    check.txt, while its python exists, and when it is not path, in it or
    around it, which venv clears. Its site-packages must hold one pip, at
    the version pip.txt pins, whose files still match its RECORD: a check
    that the tool environment is consistent, not proof of where its pip
    came from. One that cannot be read is not used. Windows has not been
    qualified, and pip ignores --python when it runs inside pip, so neither
    uses it."""
    if os.name != "posix" or "_PIP_RUNNING_IN_SUBPROCESS" in os.environ:
        return None
    try:
        seed, stamp = tool_environment("check", "check.txt")
        seed, path = seed.resolve(), Path(path).resolve()
        if seed.is_relative_to(path) or path.is_relative_to(seed):
            return None
        site = sysconfig.get_path(
            "purelib", "venv", {"base": seed, "platbase": seed}
        )
        pin = pinned_versions((REQUIREMENTS / "pip.txt").read_text())
        pips = list(importlib.metadata.distributions(name="pip", path=[site]))
        usable = (
            json.loads((seed / "files-sdk-locks.json").read_text()) == stamp
            and python_in(seed).is_file()
            and len(pips) == 1
            and pips[0].version == pin.get("pip")
            and record_unchanged(pips[0])
        )
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return python_in(seed) if usable else None


def fresh_environment(path, *locks):
    """A new virtual environment holding exactly the locked packages."""
    seed = pip_seed(path)
    venv.EnvBuilder(clear=True, with_pip=seed is None).create(path)
    python = python_in(path)
    if seed:
        # The seed's pip installs the locked pip into the new environment
        # (pip --python), in place of the pip venv would install first.
        seed_pip = (seed, "-m", "pip", "--python", python, *PIP_INSTALL[2:])
        run(*seed_pip, *LOCKED, "-r", REQUIREMENTS / "pip.txt")
    else:
        run(python, *PIP_INSTALL, *LOCKED, "-r", REQUIREMENTS / "pip.txt")
    if sys.version_info < (3, 12):
        # Python 3.11's venv also installs setuptools, which nothing here uses.
        run(
            python, *PIP_INSTALL, "uninstall", "--yes", "--quiet", "setuptools"
        )
    if locks:
        requirements = [
            arg for lock in locks for arg in ("-r", REQUIREMENTS / lock)
        ]
        run(python, *PIP_INSTALL, *LOCKED, *requirements)
    run(python, *PIP_INSTALL, "check")
    run(python, *PIP_INSTALL, "list", "--format=freeze")
    return python


def environment(name, *locks):
    """The locked tool environment called name, rebuilt when its locks or
    this interpreter change."""
    path, stamp = tool_environment(name, *locks)
    stamp_file = path / "files-sdk-locks.json"
    if stamp_file.exists() and json.loads(stamp_file.read_text()) == stamp:
        return python_in(path)
    python = fresh_environment(path, *locks)
    stamp_file.write_text(json.dumps(stamp, indent=2))
    return python


def pyright():
    """The command that runs the Pyright version tools/pyright locks."""
    node, npm = shutil.which("node"), shutil.which("npm")
    if not node or not npm:
        raise TaskFailed("Type checking needs Node.js and npm on PATH.")
    node_version = subprocess.run(
        [node, "--version"], capture_output=True, text=True, check=True
    ).stdout.strip()
    print(f"Node.js {node_version}")

    lock_dir = PACKAGE / "tools" / "pyright"
    path = TOOLS / "pyright"
    stamp = json.dumps(
        {"lock": sha256(lock_dir / "package-lock.json"), "node": node_version}
    )
    stamp_file = path / "files-sdk-lock.json"
    if not stamp_file.exists() or stamp_file.read_text() != stamp:
        shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True)
        for name in ("package.json", "package-lock.json"):
            shutil.copy(lock_dir / name, path)
        # fsevents is optional and only watches files; skip it and its
        # install script. Refuse packages published in the last 14 days.
        run(
            npm,
            "ci",
            "--omit=optional",
            "--ignore-scripts",
            "--no-audit",
            "--no-fund",
            "--min-release-age=14",
            cwd=path,
        )
        stamp_file.write_text(stamp)
    return [node, path / "node_modules" / "pyright" / "index.js"]


def supported_python():
    """Fail unless this interpreter meets the package's requires-python."""
    project = tomllib.loads((PACKAGE / "pyproject.toml").read_text())[
        "project"
    ]
    floor = re.fullmatch(r">=\s*(\d+)\.(\d+)", project["requires-python"])
    if not floor:
        raise TaskFailed(
            f"Cannot read requires-python {project['requires-python']!r}"
        )
    if sys.version_info[:2] < tuple(map(int, floor.groups())):
        raise TaskFailed(
            f"Python {sys.version.split()[0]} is older than this package's "
            f"requires-python {project['requires-python']}"
        )


def black(*arguments):
    # Keep Black's cache with the other tool state, not in the user's cache.
    run(
        environment("check", "check.txt"),
        "-m",
        "black",
        *arguments,
        *SOURCES,
        cwd=PACKAGE,
        env={**os.environ, "BLACK_CACHE_DIR": str(TOOLS / "black-cache")},
    )


def format_sources():
    black("--quiet")


def check():
    black("--check", "--diff")
    run(
        environment("check", "check.txt"),
        "-m",
        "flake8",
        *SOURCES,
        cwd=PACKAGE,
    )
    type_check()
    test("current")


# The platforms Pyright checks the sources as, by its --pythonplatform names.
TYPE_CHECK_PLATFORMS = ("Linux", "Darwin", "Windows")


def supported_versions():
    """The Python versions pyproject.toml's classifiers list, such as 3.11.
    Fails unless it lists one, so type checking never checks nothing."""
    project = tomllib.loads((PACKAGE / "pyproject.toml").read_text())[
        "project"
    ]
    versions = [
        match.group(1)
        for classifier in project.get("classifiers", [])
        if (
            match := re.fullmatch(
                r"Programming Language :: Python :: (3\.\d+)", classifier
            )
        )
    ]
    if not versions:
        raise TaskFailed(
            "pyproject.toml's classifiers name no Python version to type "
            'check for, such as "Programming Language :: Python :: 3.11"'
        )
    return versions


def type_check():
    """Run Pyright with the test environment's packages for every supported
    platform and Python version, then fail naming each that reported an
    error. The versions are read first, before any tool is prepared."""
    versions = supported_versions()
    runtime = environment("test-current", "runtime.txt")
    command = [*pyright(), "--pythonpath", runtime]
    failed = []
    for platform in TYPE_CHECK_PLATFORMS:
        for version in versions:
            print(f"Pyright as {platform}, Python {version}", flush=True)
            try:
                run(
                    *command,
                    "--pythonplatform",
                    platform,
                    "--pythonversion",
                    version,
                    cwd=PACKAGE,
                )
            except TaskFailed:
                failed.append(f"{platform} with Python {version}")
    if failed:
        raise TaskFailed("Pyright found errors for " + ", ".join(failed))


def runtime_lock(dependencies):
    return {"current": "runtime.txt", "minimum": "runtime-minimum.txt"}[
        dependencies
    ]


def test(dependencies, artifact=None):
    supported_python()
    if artifact:
        test_installed(Path(artifact).resolve(), runtime_lock(dependencies))
    else:
        python = environment(
            f"test-{dependencies}", runtime_lock(dependencies)
        )
        run(python, "-X", "dev", RUN_TESTS, cwd=PACKAGE)


# What install-check runs against the installed package: the documented
# example's whole tour and the resource examples a caller copies, through
# the installed code against a local API, and path handling, which reads the
# package's own data file.
INSTALL_CHECK_TESTS = ("tests.test_examples", "tests.test_path_util")


def install_check(dependencies, artifact):
    supported_python()
    test_installed(
        Path(artifact).resolve(),
        runtime_lock(dependencies),
        INSTALL_CHECK_TESTS,
    )


# The shared mock server's scenarios, each with the tests that need it, and
# its launcher, which the generator writes beside this package. Under the
# api-scenarios-canonical preset, scenarios/api_scenarios.py runs the shared
# API scenarios (verification/scenarios/api.json) as four cases against one
# server, each in a folder of its own, and writes each case's evidence to
# the launcher's DIR/api-scenarios.
SCENARIOS = {
    "folder-list": "tests.test_shared_folder_list",
    "api-scenarios-canonical": "scenarios.api_scenarios",
}
# The launcher options a scenario's run adds before its "--", if any. The
# canonical cases' own time limits are cooperative (see
# scenarios/api_scenarios.py), so their run has the launcher's hard ones: 30
# seconds for the server to start, and 180 for the consumer, after which the
# launcher ends the consumer's process group (status 124) and the case in
# progress runs no cleanup of its own. The settle timeout, 5 seconds, bounds
# each wait for a process group to stop, after TERM and after KILL, not the
# launcher's whole cleanup; saving the journal has best-effort bounds of its
# own, 2 seconds to connect and 30 to answer. How long this adds to the
# Python job is measured only by running it.
SCENARIO_OPTIONS = {
    "api-scenarios-canonical": (
        "--startup-timeout",
        30,
        "--consumer-timeout",
        180,
        "--settle-timeout",
        5,
    ),
}
LAUNCHER = PACKAGE.parent / "mock-server" / "with-scenario.rb"


def scenarios(launcher, outdir):
    """Run each scenario's tests under the shared mock server's launcher,
    which starts the server, gives the tests its URL, API key and scenario
    file, and keeps its evidence in outdir/SCENARIO."""
    supported_python()
    launcher, outdir = Path(launcher).resolve(), Path(outdir).resolve()
    if not launcher.is_file():
        raise TaskFailed(
            f"{launcher} does not exist; generate the mock-server target"
        )
    python = environment("test-current", runtime_lock("current"))
    TOOLS.mkdir(parents=True, exist_ok=True)
    for scenario, tests in SCENARIOS.items():
        with tempfile.TemporaryDirectory(dir=TOOLS) as scratch:
            report = Path(scratch) / "report.json"
            run(
                *("ruby", launcher, "--scenario", scenario),
                *("--out", outdir / scenario),
                *SCENARIO_OPTIONS.get(scenario, ()),
                "--",
                *(python, "-X", "dev", RUN_TESTS, "--report", report, tests),
                cwd=PACKAGE,
            )
            if not report.exists():
                raise TaskFailed(
                    f"the launcher did not run the {scenario} tests"
                )
            # Without the launcher's server URL, the tests skip themselves.
            if json.loads(report.read_text())["skipped"]:
                raise TaskFailed(f"the {scenario} tests were skipped")


# Packaging


def copy_tree_files(source, destination, pattern):
    for path in sorted(source.rglob(pattern)):
        if "__pycache__" in path.parts or not path.is_file():
            continue
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def stage_build_inputs(staging):
    """Copy only the files the build reads, so nothing else in this
    directory can reach an artifact."""
    for name in BUILD_INPUTS:
        shutil.copy2(PACKAGE / name, staging / name)
    copy_tree_files(PACKAGE / "files_sdk", staging / "files_sdk", "*")


def build_environment():
    """The environment of a pip install of the sdist, and of python -m
    build: an isolated build installs exactly the verified setuptools.
    The pinned pip ignores PIP_CONSTRAINT inside the isolated build
    environment it makes for an sdist (only build constraints apply there),
    so the lock is given as both."""
    return {
        **os.environ,
        "PIP_CONSTRAINT": str(REQUIREMENTS / "build-backend.txt"),
        "PIP_BUILD_CONSTRAINT": str(REQUIREMENTS / "build-backend.txt"),
        "PIP_ONLY_BINARY": ":all:",
    }


def only(paths, description):
    paths = list(paths)
    if len(paths) != 1:
        raise TaskFailed(f"Expected one {description}, found {paths}")
    return paths[0]


def wheel_contents(wheel):
    with zipfile.ZipFile(wheel) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def sdist_contents(sdist):
    with tarfile.open(sdist) as archive:
        return {
            member.name: archive.extractfile(member).read()
            for member in archive.getmembers()
            if member.isfile()
        }


def payload_files(staging):
    return {
        path.relative_to(staging).as_posix(): path.read_bytes()
        for path in sorted((staging / "files_sdk").rglob("*"))
        if path.is_file()
    }


def verify_names(artifact, names):
    for name in names:
        if not name.isascii():
            raise TaskFailed(
                f"{artifact.name} contains a non-ASCII path: {name!r}"
            )


def verify_wheel(wheel, payload, dist_info):
    contents = wheel_contents(wheel)
    verify_names(wheel, contents)
    expected = set(payload) | {
        f"{dist_info}/{name}"
        for name in (
            "METADATA",
            "WHEEL",
            "RECORD",
            "top_level.txt",
            "licenses/LICENSE",
        )
    }
    if set(contents) != expected:
        raise TaskFailed(
            f"{wheel.name} contents differ from the build inputs: "
            f"unexpected {sorted(set(contents) - expected)}, "
            f"missing {sorted(expected - set(contents))}"
        )
    changed = [name for name in payload if contents[name] != payload[name]]
    if changed:
        raise TaskFailed(f"{wheel.name} changed these build inputs: {changed}")
    return contents


def verify_sdist(sdist, payload, root):
    contents = sdist_contents(sdist)
    verify_names(sdist, contents)
    egg_info = (
        "PKG-INFO",
        "SOURCES.txt",
        "dependency_links.txt",
        "requires.txt",
        "top_level.txt",
    )
    expected = (
        {f"{root}/{name}" for name in (*BUILD_INPUTS, "PKG-INFO", "setup.cfg")}
        | {f"{root}/files_com.egg-info/{name}" for name in egg_info}
        | {f"{root}/{name}" for name in payload}
    )
    if set(contents) != expected:
        raise TaskFailed(
            f"{sdist.name} contents differ from the build inputs: "
            f"unexpected {sorted(set(contents) - expected)}, "
            f"missing {sorted(expected - set(contents))}"
        )
    changed = [
        name for name in payload if contents[f"{root}/{name}"] != payload[name]
    ]
    if changed:
        raise TaskFailed(f"{sdist.name} changed these build inputs: {changed}")


def verify_metadata(metadata):
    """The published requirements match pyproject.toml, and each dependency's
    lower bound is the version requirements/runtime-minimum.in tests."""
    project = tomllib.loads((PACKAGE / "pyproject.toml").read_text())[
        "project"
    ]
    headers = email.parser.HeaderParser().parsestr(metadata)
    requires_python = headers.get_all("Requires-Python", [])
    if requires_python != [project["requires-python"]]:
        raise TaskFailed(f"Requires-Python is {requires_python}")
    requires = dict(
        re.fullmatch(r"([A-Za-z0-9._-]+)\s*(.*)", value.lower()).groups()
        for value in headers.get_all("Requires-Dist", [])
    )
    if len(requires) != len(project["dependencies"]):
        raise TaskFailed(f"Requires-Dist is {sorted(requires.values())}")
    minimum = (REQUIREMENTS / "runtime-minimum.in").read_text()
    for name, version in re.findall(
        r"^([A-Za-z0-9._-]+)==(\S+)", minimum, re.M
    ):
        if f">={version}" not in requires.get(name.lower(), "").split(","):
            raise TaskFailed(
                f"Requires-Dist for {name} does not start at {version}"
            )


def artifact_payload(artifact):
    """The files_sdk files in a wheel or sdist, by path in the package."""
    if artifact.suffix == ".whl":
        contents = wheel_contents(artifact)
    else:
        root = artifact.name.removesuffix(".tar.gz") + "/"
        contents = {
            name.removeprefix(root): data
            for name, data in sdist_contents(artifact).items()
        }
    return {
        name: data
        for name, data in contents.items()
        if name.startswith("files_sdk/")
    }


def installed_payload(environment):
    """The files_sdk files installed in environment. The import runs in
    isolated mode (-I) from the environment's own directory, so neither
    PYTHONPATH, the user site-packages nor a source tree in the working
    directory can stand in for the installed package. It runs in UTF-8 mode
    (-X utf8, since -I ignores PYTHONUTF8) and its output is read as UTF-8,
    so the location comes back whole whatever the locale's encoding."""
    imported = subprocess.run(
        [
            python_in(environment),
            "-I",
            "-X",
            "utf8",
            "-c",
            "import files_sdk; print(files_sdk.__path__[0])",
        ],
        cwd=environment,
        capture_output=True,
        encoding="utf-8",
    )
    if imported.returncode != 0:
        raise TaskFailed(f"Cannot import files_sdk: {imported.stderr.strip()}")
    location = Path(imported.stdout.strip()).resolve()
    if not location.is_relative_to(environment.resolve()):
        raise TaskFailed(
            f"files_sdk was imported from {location}, not {environment}"
        )
    return {
        path.relative_to(location.parent).as_posix(): path.read_bytes()
        for path in sorted(location.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def verify_installed(environment, artifact):
    """Fail unless environment holds exactly the files_sdk files of artifact."""
    if installed_payload(environment) != artifact_payload(artifact):
        raise TaskFailed(
            f"The installed files_sdk differs from {artifact.name}"
        )


def verify_installed_metadata(environment):
    """Fail unless the files_com distribution installed in environment, read
    there in isolated mode, is this package's name and version and requires
    what pyproject.toml does (verify_metadata). Core metadata is UTF-8, which
    a locale's encoding such as Windows' cp1252 cannot always write, so the
    reader runs in UTF-8 mode (-X utf8, since -I ignores PYTHONUTF8) and its
    output is read as UTF-8."""
    read = subprocess.run(
        [
            python_in(environment),
            "-I",
            "-X",
            "utf8",
            "-c",
            "import importlib.metadata, sys; sys.stdout.write("
            "importlib.metadata.distribution('files_com').read_text('METADATA'))",
        ],
        cwd=environment,
        capture_output=True,
        encoding="utf-8",
    )
    if read.returncode != 0:
        raise TaskFailed(
            f"Cannot read the installed metadata: {read.stderr.strip()}"
        )
    project = tomllib.loads((PACKAGE / "pyproject.toml").read_text())[
        "project"
    ]
    headers = email.parser.HeaderParser().parsestr(read.stdout)
    installed = (headers.get("Name"), headers.get("Version"))
    if installed != (project["name"], project["version"]):
        raise TaskFailed(f"The installed distribution is {installed}")
    verify_metadata(read.stdout)


def test_installed(artifact, lock, names=()):
    """Install artifact with a locked runtime graph into a new environment,
    confirm what was installed, and run the tests (names, or every one)
    against it from outside the source tree."""
    TOOLS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=TOOLS) as scratch:
        scratch = Path(scratch)
        environment = scratch / "environment"
        python = fresh_environment(environment, lock)
        # Hash-check the artifact too. An sdist is built in pip's isolated
        # build environment, whose setuptools build_environment pins.
        requirement = scratch / "artifact.txt"
        requirement.write_text(
            f"files_com @ {artifact.as_uri()} --hash=sha256:{sha256(artifact)}\n"
        )
        run(
            python,
            *PIP_INSTALL,
            "install",
            "--no-deps",
            "-r",
            requirement,
            env=build_environment(),
        )
        run(python, *PIP_INSTALL, "check")
        verify_installed(environment, artifact)
        verify_installed_metadata(environment)

        tests = scratch / "tests"
        copy_tree_files(PACKAGE / "tests", tests / "tests", "*.py")
        copy_tree_files(PACKAGE / "shared", tests / "shared", "*")
        # The documented example runs against the installed package too.
        copy_tree_files(PACKAGE / "examples", tests / "examples", "*.py")
        run(python, "-X", "dev", RUN_TESTS, "--installed", *names, cwd=tests)


def build_and_check(tools, outdir):
    TOOLS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=TOOLS) as scratch:
        scratch = Path(scratch)
        staging = scratch / "staging"
        staging.mkdir()
        stage_build_inputs(staging)
        payload = payload_files(staging)

        # The package environment holds the verified setuptools (installed
        # with --require-hashes from build-backend.txt), so builds run in it
        # rather than in an environment build would make with whatever pip
        # the interpreter bundles, whose handling of constraint hashes is
        # that pip's.
        run(
            tools,
            "-m",
            "build",
            "--no-isolation",
            "--sdist",
            "--wheel",
            "--outdir",
            outdir,
            staging,
            env=build_environment(),
        )
        sdist = only(outdir.glob("*.tar.gz"), "sdist")
        wheel = only(outdir.glob("*.whl"), "wheel")
        root = sdist.name.removesuffix(".tar.gz")
        dist_info = root + ".dist-info"
        verify_sdist(sdist, payload, root)
        contents = verify_wheel(wheel, payload, dist_info)
        verify_metadata(contents[f"{dist_info}/METADATA"].decode())

        # Rebuild the wheel from the sdist alone, as pip does for sdist users.
        with tarfile.open(sdist) as archive:
            archive.extractall(scratch / "sdist", filter="data")
        rebuilt_dir = outdir / "from-sdist"
        run(
            tools,
            "-m",
            "build",
            "--no-isolation",
            "--wheel",
            "--outdir",
            rebuilt_dir,
            scratch / "sdist" / root,
            env=build_environment(),
        )
        rebuilt = only(rebuilt_dir.glob("*.whl"), "wheel built from the sdist")
        rebuilt_contents = verify_wheel(rebuilt, payload, dist_info)
        if (
            rebuilt_contents[f"{dist_info}/METADATA"]
            != contents[f"{dist_info}/METADATA"]
        ):
            raise TaskFailed(
                "The wheel built from the sdist has different metadata"
            )

        run(tools, "-m", "twine", "check", "--strict", sdist, wheel, rebuilt)
    return sdist, wheel, rebuilt


# What build writes to its --outdir: the artifacts, their checksums, and
# the from-sdist directory holding the wheel rebuilt from the sdist.
BUILD_OUTPUT = re.compile(r"files_com-.*\.(tar\.gz|whl)|SHA256SUMS\.json")
BUILD_REBUILT = "from-sdist"


def build_output(outdir):
    """outdir, ready for a build: created if it does not exist, and
    otherwise cleared of an earlier build's output, so every file in it
    will be from this build. An outdir holding anything else, such as other
    files, folders or symbolic links, is refused and left as it is."""
    outdir = Path(outdir).absolute()
    if not outdir.exists() and not outdir.is_symlink():
        outdir.mkdir(parents=True)
        return outdir
    if not outdir.is_dir():
        raise TaskFailed(f"The build's --outdir {outdir} is not a directory")

    def earlier_output(entry, nested=False):
        if entry.is_symlink():
            return False
        if entry.is_file():
            return bool(BUILD_OUTPUT.fullmatch(entry.name))
        return (
            not nested
            and entry.name == BUILD_REBUILT
            and entry.is_dir()
            and all(earlier_output(item, True) for item in entry.iterdir())
        )

    entries = list(outdir.iterdir())
    others = sorted(
        entry.name for entry in entries if not earlier_output(entry)
    )
    if others:
        raise TaskFailed(
            f"The build's --outdir {outdir} holds files a build did not "
            f"write, such as {', '.join(others[:5])}. Give it a new or empty "
            "directory, or one only an earlier build wrote to."
        )
    for entry in entries:
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    return outdir


def build(outdir):
    """Build the sdist and wheel from the build inputs alone, rebuild the
    wheel from the sdist, and check all three. Returns (sdist, wheel).
    outdir must be new, empty or hold only an earlier build's output, which
    is removed first (see build_output). A failed check empties outdir, so
    nothing unchecked is left to upload."""
    supported_python()
    tools = environment("package", "package.txt", "build-backend.txt")
    outdir = build_output(outdir)
    try:
        sdist, wheel, rebuilt = build_and_check(tools, outdir)
    except BaseException:  # Whatever stopped the checks, drop the output.
        try:
            build_output(outdir)
        except TaskFailed:
            pass  # Something else is there now; what stopped the build is raised.
        raise

    manifest = {
        artifact.relative_to(outdir).as_posix(): sha256(artifact)
        for artifact in (sdist, wheel, rebuilt)
    }
    (outdir / "SHA256SUMS.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    print(json.dumps(manifest, indent=2))
    return sdist, wheel


def package(outdir):
    sdist, wheel = build(outdir)
    test_installed(wheel, "runtime.txt")
    test_installed(sdist, "runtime.txt")


def twine(arguments):
    """Run the twine that requirements/package.txt pins, for example to upload
    what build checked."""
    run(environment("package", "package.txt"), "-m", "twine", *arguments)


# Auditing


# The locks every audit must cover. Any other requirements/*.txt is audited
# too.
AUDITED_LOCKS = (
    "runtime.txt",
    "runtime-minimum.txt",
    "pip.txt",
    "build-backend.txt",
    "check.txt",
    "package.txt",
    "audit.txt",
)
# The files an audit writes in its output directory: the requirements it
# audited, pip-audit's reports and audit-coverage.json.
AUDIT_OUTPUT = re.compile(r"audit-.+\.json|.+-all-platforms\.txt")


def pinned_versions(requirements):
    """{normalized name: version} for each name==version line of
    requirements, the text of a hash-pinned file as scripts/lock.py writes
    it."""
    return {
        normalize(name): version
        for name, version in re.findall(
            r"^([A-Za-z0-9._-]+)==([^\s;\\]+)", requirements, re.M
        )
    }


def installed_version(python, distribution):
    """The version of distribution that python imports."""
    shown = subprocess.run(
        [
            python,
            "-c",
            "import importlib.metadata as metadata; "
            f"print(metadata.version({distribution!r}))",
        ],
        capture_output=True,
        text=True,
    )
    if shown.returncode != 0:
        raise TaskFailed(
            f"Cannot read the installed {distribution}: {shown.stderr.strip()}"
        )
    return shown.stdout.strip()


def verify_audit_report(report, pins):
    """Fail unless report, pip-audit's JSON (as pip_audit/_format/json.py
    writes it in the release requirements/audit.txt pins), lists each
    package of pins ({name: version}) audited at its pinned version with no
    known vulnerability, and nothing else."""
    if not report.exists():
        raise TaskFailed("pip-audit wrote no report")
    try:
        listed = [
            (normalize(entry["name"]), entry)
            for entry in json.loads(report.read_text())["dependencies"]
        ]
    except (ValueError, KeyError, TypeError) as error:
        raise TaskFailed(f"{report.name} is not pip-audit JSON: {error!r}")
    problems = []
    audited = {}
    for name, entry in listed:
        if "skip_reason" in entry:
            problems.append(f"{name} was skipped: {entry['skip_reason']}")
        elif name in audited:
            problems.append(f"{name} is in the report twice")
        else:
            audited[name] = entry.get("version")
            if entry.get("vulns") != []:
                problems.append(
                    f"{name} {audited[name]} is reported with vulns "
                    f"{entry.get('vulns')!r}"
                )
    problems += [
        f"{name} {pins[name]} is not in the report"
        for name in sorted(pins.keys() - audited.keys())
    ]
    problems += [
        f"{name} is in the report but not pinned"
        for name in sorted(audited.keys() - pins.keys())
    ]
    problems += [
        f"{name} is reported at {audited[name]}, not the pinned {pins[name]}"
        for name in sorted(pins.keys() & audited.keys())
        if audited[name] != pins[name]
    ]
    if problems:
        raise TaskFailed("; ".join(problems))


def audit_requirements(tools, requirements, report):
    """Audit requirements, a hash-pinned file, with pip-audit into report,
    then fail unless the report covers every package it pins."""
    pins = pinned_versions(requirements.read_text())
    if not pins:
        raise TaskFailed("it pins no packages")
    try:
        run(
            tools,
            "-m",
            "pip_audit",
            "--requirement",
            requirements,
            "--require-hashes",
            "--disable-pip",
            "--cache-dir",
            TOOLS / "pip-audit-cache",
            "--progress-spinner",
            "off",
            "--format",
            "json",
            "--output",
            report,
        )
    except TaskFailed as failure:
        raise TaskFailed(
            f"pip-audit found vulnerabilities or could not audit ({failure})"
        )
    verify_audit_report(report, pins)


def audit_output(outdir):
    """outdir, ready for an audit: created if it does not exist, and
    otherwise cleared of an earlier audit's output, so every file in it will
    be from this audit. An outdir holding anything else, such as other
    files, folders or symbolic links, is refused and left as it is."""
    outdir = Path(outdir).absolute()
    if not outdir.exists() and not outdir.is_symlink():
        outdir.mkdir(parents=True)
        return outdir
    if not outdir.is_dir():
        raise TaskFailed(f"The audit's --outdir {outdir} is not a directory")
    entries = list(outdir.iterdir())
    others = sorted(
        entry.name
        for entry in entries
        if entry.is_symlink()
        or not entry.is_file()
        or not AUDIT_OUTPUT.fullmatch(entry.name)
    )
    if others:
        raise TaskFailed(
            f"The audit's --outdir {outdir} holds files an audit did not "
            f"write, such as {', '.join(others[:5])}. Give it a new or empty "
            "directory, or one only an earlier audit wrote to."
        )
    for entry in entries:
        entry.unlink()
    return outdir


def audit(outdir):
    """Audit every lock with pip-audit into outdir, and fail unless each
    lock's report lists every package it pins, on every platform, with no
    known vulnerability. outdir must be new, empty or hold only an earlier
    audit's output, which is removed first (see audit_output), so it then
    holds only this audit: the requirements audited, pip-audit's reports,
    and audit-coverage.json, which records their hashes and each lock's
    result with this Python and the pip-audit version. pip-audit's advisory
    data comes from PyPI and can lag a project's own security advisories, so
    read those too before a release."""
    outdir = audit_output(outdir)
    locks = sorted(REQUIREMENTS.glob("*.txt"))
    missing = sorted(set(AUDITED_LOCKS) - {lock.name for lock in locks})
    if missing:
        raise TaskFailed(f"requirements/ has no {', '.join(missing)}")

    tools = environment("audit", "audit.txt")
    scanner = installed_version(tools, "pip-audit")
    pinned = pinned_versions((REQUIREMENTS / "audit.txt").read_text())
    if scanner != pinned.get("pip-audit"):
        raise TaskFailed(
            f"The audit environment has pip-audit {scanner}, not the "
            f"{pinned.get('pip-audit')} requirements/audit.txt pins"
        )

    coverage = {}
    failed = []
    for lock in locks:
        # Audit every pinned package, including those whose marker excludes
        # this machine: a vulnerable release is vulnerable everywhere.
        audited = outdir / f"{lock.stem}-all-platforms.txt"
        audited.write_text(re.sub(r" ; [^\\\n]*", "", lock.read_text()))
        report = outdir / f"audit-{lock.stem}.json"
        try:
            audit_requirements(tools, audited, report)
            result = "passed"
        except TaskFailed as failure:
            failed.append(f"{lock.name}: {failure}")
            result = f"failed: {failure}"
        coverage[lock.name] = {
            "sha256": sha256(lock),
            "audited_sha256": sha256(audited),
            "report_sha256": sha256(report) if report.exists() else None,
            "result": result,
        }

    manifest = {"python": sys.version, "pip-audit": scanner, "locks": coverage}
    (outdir / "audit-coverage.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    print(json.dumps(manifest, indent=2))
    if failed:
        raise TaskFailed(
            "\n  ".join(["Audit failed for:", *failed, f"See {outdir}"])
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    tasks = parser.add_subparsers(dest="task", required=True)
    tasks.add_parser("format", help="rewrite the sources with pinned Black")
    tasks.add_parser("check", help="run every check without changing files")
    tasks.add_parser(
        "types", help="type check for every supported platform and Python"
    )
    test_parser = tasks.add_parser("test", help="run the unit tests")
    test_parser.add_argument(
        "--dependencies", choices=("current", "minimum"), default="current"
    )
    test_parser.add_argument(
        "--artifact",
        help="test this installed wheel or sdist instead of the source",
    )
    install_check_parser = tasks.add_parser(
        "install-check",
        help="install a wheel or sdist, check it and run its install tests",
    )
    install_check_parser.add_argument(
        "--dependencies", choices=("current", "minimum"), default="current"
    )
    install_check_parser.add_argument("--artifact", required=True)
    scenarios_parser = tasks.add_parser(
        "scenarios", help="run the shared mock server's scenario tests"
    )
    scenarios_parser.add_argument(
        "--out",
        required=True,
        help="where the launcher keeps each scenario's evidence",
    )
    scenarios_parser.add_argument(
        "--launcher",
        default=LAUNCHER,
        help="the mock server's with-scenario.rb",
    )
    for name, description in (
        ("build", "build and check the sdist and wheel"),
        ("package", "build, check and test the sdist and wheel"),
    ):
        tasks.add_parser(name, help=description).add_argument(
            "--outdir", default=TOOLS / "dist"
        )
    audit_parser = tasks.add_parser(
        "audit", help="audit the locked requirements"
    )
    audit_parser.add_argument(
        "--outdir",
        default=TOOLS / "reports",
        help="a new or empty directory, or one only an earlier audit wrote to",
    )
    twine_parser = tasks.add_parser("twine", help="run the pinned twine")
    twine_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    try:
        if args.task == "format":
            format_sources()
        elif args.task == "check":
            check()
        elif args.task == "types":
            type_check()
        elif args.task == "test":
            test(args.dependencies, args.artifact)
        elif args.task == "install-check":
            install_check(args.dependencies, args.artifact)
        elif args.task == "scenarios":
            scenarios(args.launcher, args.out)
        elif args.task == "build":
            build(args.outdir)
        elif args.task == "package":
            package(args.outdir)
        elif args.task == "twine":
            twine(args.arguments)
        else:
            audit(args.outdir)
    except TaskFailed as failure:
        sys.exit(f"{args.task} failed: {failure}")


if __name__ == "__main__":
    main()
