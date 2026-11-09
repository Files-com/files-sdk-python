"""The shared failure-case matrix against the mock server's failure-cases
scenario.

The scenario's launcher (python scripts/tasks.py scenarios) resets the
server to the scenario's users, adds its fault rules and sets
FILES_MOCK_SERVER_URL, FILES_MOCK_API_KEY, FILES_MOCK_SCENARIO_FILE and
FILES_MOCK_OUT. Each case's calls go through files_sdk.user.find and
files_sdk.user.update with max_network_retries set to the definition's,
and each call's result or error is compared with the case's expectation.
FILES_MOCK_OUT/failure-cases.json records each case's outcome; the
launcher's failure cases check then requires every case to have passed and
compares the journal and the fault rules' decisions with each case's
expected wire outcome. Run without that URL, the test is skipped; with it,
anything missing or wrong fails it.
"""

import json
import os
import platform
import unittest
from unittest.mock import patch

import files_sdk
from files_sdk.error import APIConnectionError, APIError

SERVER_URL = os.environ.get("FILES_MOCK_SERVER_URL")


def call(case, options):
    """What one call did, in the expectation's terms."""
    try:
        if case["call"] == "users.update":
            files_sdk.user.update(case["user_id"], case["params"], options)
            return {"updated": True}
        if case["call"] == "users.find":
            user = files_sdk.user.find(case["user_id"], {}, options)
            return {"user": {"id": user.id, "username": user.username}}
        return {"unknown call": case["call"]}
    except APIConnectionError:
        return {"error": {"network": True}}
    except APIError as error:
        return {
            "error": {
                "status": error.http_code,
                "type": error.error_type,
                "message": error.error,
            }
        }
    except Exception as error:
        return {"unexpected": f"{type(error).__name__}: {error}"}


@unittest.skipUnless(
    SERVER_URL,
    "needs the shared mock server's failure-cases scenario: "
    "python scripts/tasks.py scenarios",
)
class TestSharedFailureCases(unittest.TestCase):
    def test_every_failure_case(self):
        with open(
            os.environ["FILES_MOCK_SCENARIO_FILE"], encoding="utf-8"
        ) as scenario:
            definition = json.load(scenario)["failure_cases"]
        for name, value in {
            "base_url": SERVER_URL,
            "the_api_key": None,
            "session_id": None,
            "workspace_id": None,
            "max_network_retries": definition["max_network_retries"],
        }.items():
            patcher = patch.object(files_sdk, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(files_sdk.close)
        options = {"api_key": os.environ["FILES_MOCK_API_KEY"]}

        results = []
        for case in definition["cases"]:
            problems = []
            for index, expected in enumerate(case["expect"]):
                actual = call(case, options)
                if actual != expected:
                    problems.append(
                        f"call {index + 1} gave {json.dumps(actual)}, "
                        f"not {json.dumps(expected)}"
                    )
            results.append(
                {
                    "id": case["id"],
                    "outcome": "failed" if problems else "passed",
                    "failure": "; ".join(problems) or None,
                }
            )

        report = {
            "format": "files-failure-cases/1",
            "sdk": "python",
            "runtime": platform.python_version(),
            "cases": results,
        }
        out = os.path.join(os.environ["FILES_MOCK_OUT"], "failure-cases.json")
        with open(out, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)
            file.write("\n")
        self.assertEqual(
            [],
            [result for result in results if result["outcome"] != "passed"],
        )


if __name__ == "__main__":
    unittest.main()
