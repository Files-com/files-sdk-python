"""Runs the SDK's unit tests. Fails if any test fails, if a test module
cannot be imported, or if no tests are found.

Run it from a directory containing tests/ and shared/, with the interpreter
and dependencies under test:

    python scripts/run_tests.py                 # every test
    python scripts/run_tests.py tests.test_api_errors
    python scripts/run_tests.py --installed     # the installed package

The generated model tests call the Files.com mock server named in
tests/base.py, so running every test needs that server, and a route it
cannot serve fails its test.

The TLS tests make a throwaway certificate authority with the openssl
command first on PATH (tests/network_fixtures.py). They are skipped without
one, and fail at once, naming it, if this Python cannot use what it makes.
"""

import argparse
import collections
import json
import sys
import unittest
import urllib.error
import urllib.request
from pathlib import Path


def mock_server_problem():
    from tests.base import BASE_URL

    try:
        urllib.request.urlopen(BASE_URL, timeout=5).close()
    except urllib.error.HTTPError as error:
        error.close()  # The error is also the response; release it.
        # Any answer below 500, such as 404 for the root path, means it runs.
        if error.code >= 500:
            return (
                f"The Files.com mock server at {BASE_URL} answered "
                f"{error.code} {error.reason}"
            )
    except OSError as error:
        return (
            f"The Files.com mock server at {BASE_URL} is unavailable: {error}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*", help="test modules to run")
    parser.add_argument(
        "--installed",
        action="store_true",
        help="fail unless files_sdk is imported from outside this directory",
    )
    parser.add_argument("--report", help="write the counts as JSON here")
    args = parser.parse_args()

    # Import the tests, and files_sdk unless it is installed, from here.
    sys.path.insert(0, str(Path.cwd()))
    import files_sdk

    location = Path(files_sdk.__file__).resolve().parent
    print(f"files_sdk {files_sdk.__version__} from {location}")
    print(f"Python {sys.version}")
    if args.installed and Path.cwd().resolve() in location.parents:
        sys.exit("files_sdk was imported from the source tree, not installed")

    if not args.names:
        problem = mock_server_problem()
        if problem:
            sys.exit(problem)

    loader = unittest.TestLoader()
    if args.names:
        suite = loader.loadTestsFromNames(args.names)
    else:
        suite = loader.discover("tests", top_level_dir=".")
    discovered = suite.countTestCases()
    for error in loader.errors:
        print(error, file=sys.stderr)

    result = unittest.TextTestRunner(verbosity=1).run(suite)

    skip_reasons = collections.Counter(
        reason for _test, reason in result.skipped
    )
    counts = {
        "discovered": discovered,
        "import_errors": len(loader.errors),
        # unittest counts a skipped test as run; report what actually ran.
        "executed": result.testsRun - len(result.skipped),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "skip_reasons": dict(skip_reasons),
    }
    print(json.dumps(counts))
    if args.report:
        Path(args.report).write_text(json.dumps(counts, indent=2) + "\n")

    if discovered == 0:
        sys.exit("No tests were found.")
    if loader.errors or not result.wasSuccessful():
        sys.exit(1)
    if result.testsRun != discovered:
        sys.exit(
            f"Started {result.testsRun} of {discovered} discovered tests."
        )


if __name__ == "__main__":
    main()
