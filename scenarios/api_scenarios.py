"""The Files.com API scenarios of verification/scenarios/api.json, run with
the Python SDK against the shared mock server's simulator: each scenario is
a case, and each case a test.

The definition (SHA-256 5d9b8eff0ef0724a68a458db77dc85784bb7d24436f104b98c2a2fe67086bbe0)
is held below byte for byte and checked before anything runs.
helpers/python/api_scenarios.rb bound each of its steps to the SDK call that
carries it out, by the schema's operations, parameters, fields and errors.
Every value a step expects is read from the definition at the step's pointer
as the step runs, never copied here.

141 steps: 133 run on the simulator, and 8 are site-only, which the
simulator omits and which never count as passed. There is no site mode: on a
site, every entry a step returns for a fixture would also have to hold the
run's own user and API key as created_by_id and created_by_api_key_id, each a
raw JSON integer (api.json /backends/site).

python scripts/tasks.py scenarios runs this module under the shared mock
server's api-scenarios-canonical preset, with the launcher's
--startup-timeout 30, --consumer-timeout 180 and --settle-timeout 5. The
launcher starts the server and sets FILES_MOCK_SERVER_URL,
FILES_MOCK_API_KEY, FILES_MOCK_RUN_ID, FILES_MOCK_SCENARIO_FILE and
FILES_MOCK_OUT. Without that URL every case is skipped, which that task
counts as a failure. Each case writes every step's outcome, checks and
calls, with the status and raw JSON of each API response a call received, to
FILES_MOCK_OUT/api-scenarios/CASE.json, after each step that passes and at
its end; the cases' totals go to FILES_MOCK_OUT/api-scenarios/summary.json.

Time limits. Each call's options carry the case's absolute deadline (a
time.monotonic() value CASE_SECONDS after the case starts) and a
request_timeout of STEP_SECONDS, the earlier of which applies. A listing's
later pages belong to the call that fetched its first page, so its limits
cover them. A later operation of an object a call returned is an operation
of its own, with its own limits: download_file of a File a listing
returned takes no options, so it has only the client settings the File
keeps (OPEN_TIMEOUT and READ_TIMEOUT, and no request_timeout), not that
listing call's deadline or token; the case only checks first that its own
deadline has not passed. These limits are cooperative, not hard bounds:
requests go through the case's own requests.Session, which the SDK cannot
interrupt, so such a request stops only when its own timeouts (OPEN_TIMEOUT
to connect, READ_TIMEOUT for each read), shortened to a deadline if it has
one, return, and a response that keeps trickling in can outlast all of
them. The hard bound is the launcher's: after 180 seconds it ends this
consumer's process group (status 124). Its settle timeout, 5 seconds,
bounds each wait for a process group to stop, after TERM and after KILL,
not the launcher's whole cleanup; saving the journal has best-effort bounds
of its own, 2 seconds to connect and 30 to answer. A case ended that
way runs no cleanup of its own (the simulator, and everything in it, is
discarded with the server), and its evidence holds the steps it wrote
before then. What this adds to the Python job's time is not measured here.

Ownership. Each case runs in a folder of its own, under a new name, which it
looks up and finds absent, then creates. It owns that folder only once the
create's own answer proves it: the call returned, its one API response was
201, and both that response's raw JSON and the entry the SDK made of it are
a directory at the folder's exact path. An earlier absence and a random name
are not ownership. The case's last steps delete everything it made, without
recursion, and confirm each absent; once its own lookup confirms the folder
absent, it owns nothing. A case that fails while it owns the folder deletes
that folder, and nothing else, recursively, with a client, options and
deadline of its own, then confirms it absent; the delete's own error counts
as the folder being gone already only when it is exactly the confirming
lookup's error (its native class, 404 and raw JSON type). A create that
failed, or whose answer did not prove the folder the case's, is never
cleaned up: whether a folder is there is then unknown, and the evidence says
so. The first failure is reported first; a failed cleanup, or a client or
session that failed to close, is reported after it and fails the case too.

Observation. Each response is matched to the call, or the page of a listing,
that sent its request through its client's own requests.Session, one attempt
a request (max_network_retries=0). The Recorder adapter keeps every response
it receives, reading the raw JSON of the API's answers before the SDK does
and leaving storage's bodies (upload parts and downloads) untouched. That
every adapter send a call started had returned when it returned is a narrow
observation, checked so that no response of one call can fall in the next's
window; it is not the SDK's settlement. Settlement is Client.close(), which
returns once the client's operations have settled: the cancelled upload's
own client, the cleanup's client and the case's client are each closed that
way, then their sessions. A helper call's API answers are checked by their
public meaning: each a 2xx answer whose raw JSON names only the step's
paths, or an error the definition itself expects from that same operation
for one of its fixtures (its status and raw JSON type) at one of the step's
paths; a create's such answer, an existence answer, counts only for a folder
a listing finds there after a directory upload.

Cancellation. The upload a step cancels after its first acknowledged part
runs on a client and session of its own, one part at a time. A response hook
of that session cancels the step's token, synchronously, on the first
successful upload part response (a PUT): acknowledgement 1, at the
wire-response acknowledgement boundary, before the SDK has that response and
so before any progress or committed state it reports for the part. It is not
a progress callback, which the SDK delivers at most four times a second and
so cannot show which acknowledgement came first. That client is then closed,
and its session, before the case's own client goes on.
"""

import base64
import collections
import dataclasses
import datetime
import hashlib
import io
import json
import os
import re
import tempfile
import threading
import time
import unittest
import urllib.parse
import uuid
from pathlib import Path
from typing import Any, Callable

import requests
import requests.adapters

import files_sdk
import files_sdk.error

SERVER_URL = os.environ.get("FILES_MOCK_SERVER_URL")
API_KEY = os.environ.get("FILES_MOCK_API_KEY")
RUN_ID = os.environ.get("FILES_MOCK_RUN_ID", "")

DEFINITION_SHA256 = (
    "5d9b8eff0ef0724a68a458db77dc85784bb7d24436f104b98c2a2fe67086bbe0"
)
# The definition's exact bytes, base64-encoded.
DEFINITION_BASE64 = (
    "ewogICJmb3JtYXQiOiAiZmlsZXMtYXBpLXNjZW5hcmlvcyIsCiAgImZvcm1hdF92ZXJzaW9uIjog",
    "MSwKICAic3VtbWFyeSI6ICJGaWxlcy5jb20gQVBJIHNjZW5hcmlvcyBhbmQgdGhlaXIgZXhwZWN0",
    "ZWQgcmVzdWx0cywgZm9yIGV2ZXJ5IGNsaWVudDogdGhlIGdlbmVyYXRlZCBTREtzJyBuYXRpdmUg",
    "dGVzdHMsIHRoZSBwYWlyZWQgdmVyaWZpY2F0aW9uIGpvdXJuZXlzIGFuZCBhbnkgY3VzdG9tIGNs",
    "aWVudCBydW4gYWdhaW5zdCBGaWxlcy5jb20gb3IgdGhlIGdlbmVyYXRlZCBzaW11bGF0b3IuIE9w",
    "ZXJhdGlvbnMgYXJlIHRoZSBTd2FnZ2VyIGRvY3VtZW50J3Mgb3BlcmF0aW9uSWRzLCBhbmQgcGFy",
    "YW1ldGVycyBhbmQgcmVzdWx0IGZpZWxkcyBpdHMgbmFtZXM7IG5vdGhpbmcgaGVyZSBuYW1lcyBh",
    "biBTREssIGEgY2xhc3MsIGEgbWV0aG9kIG9yIGEgbmF0aXZlIGVycm9yLiBTZWUgdmVyaWZpY2F0",
    "aW9uL3NjZW5hcmlvcy9SRUFETUUubWQuIiwKICAiYmFja2VuZHMiOiB7CiAgICAic2ltdWxhdG9y",
    "IjogIlRoZSBnZW5lcmF0ZWQgbW9jayBzZXJ2ZXIgaW4gc2ltdWxhdGlvbiBtb2RlLiBTdGVwcyBt",
    "YXJrZWQgXCJiYWNrZW5kXCI6IFwic2l0ZVwiIGFyZSBleGNsdWRlZCBoZXJlLCBuZXZlciBwYXNz",
    "ZWQ6IHRoZSBzaW11bGF0b3IgaGFzIG5vIHBlcm1pc3Npb25zLCBpbmhlcml0ZWQgYmVoYXZpb3Jz",
    "IG9yIGNyZWF0b3JzLiIsCiAgICAic2l0ZSI6ICJBIEZpbGVzLmNvbSBzaXRlLiBFdmVyeSBzdGVw",
    "IGFwcGxpZXMsIGFuZCBldmVyeSBlbnRyeSBhIHN0ZXAgcmV0dXJucyBmb3IgYSBmaXh0dXJlIG11",
    "c3QgaGF2ZSBiZWVuIGNyZWF0ZWQgYnkgdGhlIHJ1bidzIG93biB1c2VyIGFuZCBBUEkga2V5IChj",
    "cmVhdGVkX2J5X2lkIGFuZCBjcmVhdGVkX2J5X2FwaV9rZXlfaWQpLiIKICB9LAogICJuYW1lc3Bh",
    "Y2UiOiAiRWFjaCBydW4gb3ducyBvbmUgZm9sZGVyICh0aGUgZml4dHVyZSB3aG9zZSBwYXRoIGlz",
    "IFwiXCIpLCB3aGljaCB0aGUgcnVubmVyIG5hbWVzIGFuZCB3aGljaCBtdXN0IG5vdCBleGlzdCBi",
    "ZWZvcmUgdGhlIHJ1bi4gRXZlcnkgb3RoZXIgZml4dHVyZSBwYXRoIGlzIHJlbGF0aXZlIHRvIGl0",
    "LiIsCiAgImNsZWFudXAiOiAiQSBzY2VuYXJpbydzIGxhc3Qgc3RlcHMgZGVsZXRlIGV2ZXJ5IGZp",
    "eHR1cmUgaXQgbWFkZSwgd2l0aG91dCByZWN1cnNpb24sIGFuZCBjb25maXJtIGVhY2ggYWJzZW50",
    "LiBBIHJ1bm5lciB3aG9zZSBzY2VuYXJpbyBzdG9wcGVkIGVhcmx5IGRlbGV0ZXMgdGhlIG93bmVk",
    "IGZvbGRlciByZWN1cnNpdmVseSBhbmQgY29uZmlybXMgaXQgYWJzZW50LCBhbmQgZGVsZXRlcyBu",
    "b3RoaW5nIG91dHNpZGUgaXQuIiwKICAicmVjaXBlcyI6IHsKICAgICIxIjogeyAibXVsdGlwbGll",
    "ciI6IDEzMSwgIm9mZnNldCI6IDE3LCAibW9kdWx1cyI6IDI1MSwgImxlbmd0aCI6IDY1NTM5LCAi",
    "c2hhMjU2IjogImI2NTA5NGQzNmFjMTAwOWRhYzljNzNjMjdiNDg2MzhhNDdlYjdmMjNkMjE5YTgw",
    "ZDFiNGQwNWI1OGY1MTQ0OTkiIH0sCiAgICAiMiI6IHsgIm11bHRpcGxpZXIiOiAxLCAib2Zmc2V0",
    "IjogMCwgIm1vZHVsdXMiOiAyNTYsICJsZW5ndGgiOiAwLCAic2hhMjU2IjogImUzYjBjNDQyOThm",
    "YzFjMTQ5YWZiZjRjODk5NmZiOTI0MjdhZTQxZTQ2NDliOTM0Y2E0OTU5OTFiNzg1MmI4NTUiIH0s",
    "CiAgICAiMyI6IHsgIm11bHRpcGxpZXIiOiAyOSwgIm9mZnNldCI6IDEwMSwgIm1vZHVsdXMiOiAy",
    "NTYsICJsZW5ndGgiOiA2NTUzNywgInNoYTI1NiI6ICJlZDVhODZkNWI2MTRkNTM4NWE4NWMxNzBj",
    "MTVmMjVmZTc1YzNmYWFiNmE4YjI5YWJiYjQ3MGE2YzUxZmFhN2Y5IiB9LAogICAgIjQiOiB7ICJt",
    "dWx0aXBsaWVyIjogMzcsICJvZmZzZXQiOiA1LCAibW9kdWx1cyI6IDI1NiwgImxlbmd0aCI6IDEw",
    "MzEsICJzaGEyNTYiOiAiMjlmNDgzYjg3MzlhZTJkZTk5NGQ0Nzk0MTMzYTdhODU4YTBmMDQxNmNh",
    "YTAzZTVhOTYxNjVhZjQxZWJkZjNlOCIgfSwKICAgICI1IjogeyAibXVsdGlwbGllciI6IDQxLCAi",
    "b2Zmc2V0IjogMTEsICJtb2R1bHVzIjogMjU2LCAibGVuZ3RoIjogMjA1MywgInNoYTI1NiI6ICI4",
    "MzI5ODEwNGZlMDFkOTA1ZWU5Y2U4ZmFlMmYyM2RhMDgwMDdiNWU4YWIzNTZkNWJmYzA2NGI0OWMy",
    "NjY0Yjk4IiB9LAogICAgIjYiOiB7ICJtdWx0aXBsaWVyIjogNDMsICJvZmZzZXQiOiAzLCAibW9k",
    "dWx1cyI6IDI1NiwgImxlbmd0aCI6IDUxNywgInNoYTI1NiI6ICJiNjY0MzU3YjMxNTFlNDhjYTRj",
    "NWM2YzQ1MmRkMjBkNTgyOTM4OTdmODg3NTM2ZjZlMGUwNjI3YzBkOGNkMjViIiB9LAogICAgIjci",
    "OiB7ICJtdWx0aXBsaWVyIjogNDcsICJvZmZzZXQiOiAxOSwgIm1vZHVsdXMiOiAyNTYsICJsZW5n",
    "dGgiOiA0MDk5LCAic2hhMjU2IjogIjlmMjUxNDc3NDU4NjIyZDlkYTg2OGUzMWI4NzA4ZWM2Mzhk",
    "OGJhOWEwMWM5YjU3NWJiOGMwYTA3NjQ3MzQ1MjEiIH0sCiAgICAiOCI6IHsgIm11bHRpcGxpZXIi",
    "OiA1MywgIm9mZnNldCI6IDIzLCAibW9kdWx1cyI6IDI1MSwgImxlbmd0aCI6IDYyOTE0NTksICJz",
    "aGEyNTYiOiAiNGFiMTYxNTkyNWNiNGIxZmE5YjlkZGMzMzQ1YTkyMDIwMDg4OGQ4YmE3ZDNhZTFi",
    "ODgwYWE2YzBjMTlmODdmYSIgfSwKICAgICI5IjogeyAibXVsdGlwbGllciI6IDU5LCAib2Zmc2V0",
    "IjogMjksICJtb2R1bHVzIjogMjUxLCAibGVuZ3RoIjogNjI5MTQ2MSwgInNoYTI1NiI6ICJkN2E3",
    "MTU3NGEyNGZhZWNiMmZlYTQ5MTViODA5NmE4NmE0M2IxOWRiOThkNDQwZjE2NzMwY2FhYzBhNjZj",
    "ZmQ0IiB9LAogICAgIjEwIjogeyAibXVsdGlwbGllciI6IDYxLCAib2Zmc2V0IjogNywgIm1vZHVs",
    "dXMiOiAyNTYsICJsZW5ndGgiOiAxNTQzLCAic2hhMjU2IjogIjk4M2YzMTM1NmNlYTMzODQ5MmM0",
    "N2Q2YzljOTc5ZGViM2E0NTkxNGZlNmFhOGVhZmE5NmNkNDRlMDJmMDhlOWQiIH0sCiAgICAiMTEi",
    "OiB7ICJtdWx0aXBsaWVyIjogNjcsICJvZmZzZXQiOiAxMywgIm1vZHVsdXMiOiAyNTYsICJsZW5n",
    "dGgiOiAyMDg5LCAic2hhMjU2IjogIjAzZTUyODY5MDY5NjA2NmU2MWQ4YTY1ZmEwZmFjMzg5NzRi",
    "Yjk1Y2IwZDMxODc0MjQwMjg3ZjMyNTQ4NGZkZGIiIH0KICB9LAogICJpbnRlbnRzIjogewogICAg",
    "InVwbG9hZCI6IHsgIm9wZXJhdGlvbnMiOiBbICJQT1NUIC9maWxlX2FjdGlvbnMvYmVnaW5fdXBs",
    "b2FkL3twYXRofSIsICJQT1NUIC9maWxlcy97cGF0aH0iIF0sICJzdW1tYXJ5IjogIlRoZSBjbGll",
    "bnQncyB1cGxvYWQgb2YgYSBmaXh0dXJlJ3MgcmVjaXBlIGJ5dGVzIHRvIGl0cyBwYXRoLCBmcm9t",
    "IHRoZSBzb3VyY2UgdGhlIHN0ZXAgbmFtZXMuIiB9LAogICAgImRvd25sb2FkIjogeyAib3BlcmF0",
    "aW9ucyI6IFsgIkdFVCAvZmlsZXMve3BhdGh9IiBdLCAic3VtbWFyeSI6ICJUaGUgY2xpZW50J3Mg",
    "ZG93bmxvYWQgb2YgYSBmaXh0dXJlJ3MgYnl0ZXMuIiB9LAogICAgImNvcHkiOiB7ICJvcGVyYXRp",
    "b25zIjogWyAiUE9TVCAvZmlsZV9hY3Rpb25zL2NvcHkve3BhdGh9IiwgIkdFVCAvZmlsZV9taWdy",
    "YXRpb25zL3tpZH0iIF0sICJzdW1tYXJ5IjogIkEgY29weSBvZiB0aGUgc3RlcCdzIHNvdXJjZSBm",
    "aXh0dXJlIHRvIGl0cyBmaXh0dXJlLCB3YWl0ZWQgZm9yIHVudGlsIGl0cyBtaWdyYXRpb24gKGlm",
    "IGFueSkgY29tcGxldGVzLiIgfSwKICAgICJtb3ZlIjogeyAib3BlcmF0aW9ucyI6IFsgIlBPU1Qg",
    "L2ZpbGVfYWN0aW9ucy9tb3ZlL3twYXRofSIsICJHRVQgL2ZpbGVfbWlncmF0aW9ucy97aWR9IiBd",
    "LCAic3VtbWFyeSI6ICJBIG1vdmUgb2YgdGhlIHN0ZXAncyBzb3VyY2UgZml4dHVyZSB0byBpdHMg",
    "Zml4dHVyZSwgd2FpdGVkIGZvciB1bnRpbCBpdHMgbWlncmF0aW9uIChpZiBhbnkpIGNvbXBsZXRl",
    "cy4iIH0sCiAgICAidXBsb2FkLWRpcmVjdG9yeSI6IHsgIm9wZXJhdGlvbnMiOiBbICJQT1NUIC9m",
    "b2xkZXJzL3twYXRofSIsICJQT1NUIC9maWxlX2FjdGlvbnMvYmVnaW5fdXBsb2FkL3twYXRofSIs",
    "ICJQT1NUIC9maWxlcy97cGF0aH0iIF0sICJzdW1tYXJ5IjogIlRoZSBjbGllbnQncyB1cGxvYWQg",
    "b2YgYSBsb2NhbCB0cmVlIGhvbGRpbmcgdGhlIHN0ZXAncyB0cmVlIGZpeHR1cmVzLCB0byBpdHMg",
    "Zml4dHVyZSdzIHBhdGguIiB9LAogICAgImRvd25sb2FkLWRpcmVjdG9yeSI6IHsgIm9wZXJhdGlv",
    "bnMiOiBbICJHRVQgL2ZvbGRlcnMve3BhdGh9IiwgIkdFVCAvZmlsZXMve3BhdGh9IiBdLCAic3Vt",
    "bWFyeSI6ICJUaGUgY2xpZW50J3MgZG93bmxvYWQgb2YgaXRzIGZpeHR1cmUncyBmb2xkZXIgdG8g",
    "YSBuZXcgbG9jYWwgZm9sZGVyLiIgfQogIH0sCiAgImdyb3VwcyI6IHsKICAgICJuYW1lc3BhY2Uu",
    "b3BlbiI6IFsKICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRh",
    "L3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6ICIvIiB9LCAiZXhwZWN0IjogeyAic3Rh",
    "dHVzIjogNDIyLCAiZXJyb3IiOiAiYmFkLXJlcXVlc3QvcmVxdWVzdC1wYXJhbXMtcmVxdWlyZWQi",
    "IH0gfSwKICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZm9sZGVycy97cGF0aH0iLCAicGFyYW1l",
    "dGVycyI6IHsgInBhdGgiOiAiLyIsICJwZXJfcGFnZSI6IDEwMDAgfSwgImV4cGVjdCI6IHsgInN0",
    "YXR1cyI6IDIwMCwgImxpc3RpbmciOiB7ICJtYXhfcGFnZXMiOiAxNiB9IH0gfSwKICAgICAgeyAi",
    "YmFja2VuZCI6ICJzaXRlIiwgIm9wZXJhdGlvbiI6ICJHRVQgL2JlaGF2aW9ycy9mb2xkZXJzL3tw",
    "YXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6ICIvIiwgImFuY2VzdG9yX2JlaGF2aW9ycyI6",
    "IHRydWUsICJwZXJfcGFnZSI6IDEwMCB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjAwLCAibGlz",
    "dGluZyI6IHsgImVudHJpZXMiOiBbXSwgIm1heF9wYWdlcyI6IDUsICJtYXhfcmVjb3JkcyI6IDUw",
    "MCB9IH0gfSwKICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRh",
    "L3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAiZm9sZGVyIiB9",
    "IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiIH0gfSwK",
    "ICAgICAgeyAib3BlcmF0aW9uIjogIlBPU1QgL2ZvbGRlcnMve3BhdGh9IiwgInBhcmFtZXRlcnMi",
    "OiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJmb2xkZXIiIH0sICJta2Rpcl9wYXJlbnRzIjogZmFs",
    "c2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMSwgImVudHJ5IjogeyAiZml4dHVyZSI6ICJm",
    "b2xkZXIiIH0gfSB9LAogICAgICB7ICJiYWNrZW5kIjogInNpdGUiLCAib3BlcmF0aW9uIjogIkdF",
    "VCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6",
    "IHsgImZpeHR1cmUiOiAiZm9sZGVyIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAsICJl",
    "bnRyeSI6IHsgImZpeHR1cmUiOiAiZm9sZGVyIiwgImZpZWxkcyI6IHsgInBlcm1pc3Npb25zIjog",
    "eyAiaW5jbHVkZXMiOiBbICJsIiwgInIiLCAidyIsICJkIiBdIH0sICJpc19sb2NrZWQiOiB7ICJu",
    "b3QiOiB0cnVlIH0sICJzdWJmb2xkZXJzX2xvY2tlZD8iOiB7ICJub3QiOiB0cnVlIH0gfSB9IH0g",
    "fQogICAgXSwKICAgICJuYW1lc3BhY2UuY2xvc2UiOiBbCiAgICAgIHsgIm9wZXJhdGlvbiI6ICJE",
    "RUxFVEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUi",
    "OiAiZm9sZGVyIiB9LCAicmVjdXJzaXZlIjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6",
    "IDIwNCB9IH0sCiAgICAgIHsgIm9wZXJhdGlvbiI6ICJHRVQgL2ZpbGVfYWN0aW9ucy9tZXRhZGF0",
    "YS97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogImZvbGRlciIg",
    "fSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogNDA0LCAiZXJyb3IiOiAibm90LWZvdW5kIiwgImF0",
    "dGVtcHRzIjogNSwgImludGVydmFsX3NlY29uZHMiOiAxIH0gfQogICAgXQogIH0sCiAgInNjZW5h",
    "cmlvcyI6IFsKICAgIHsKICAgICAgImlkIjogImZpbGVzLm93bmVkLWZvbGRlci1uYW1lc3BhY2Ui",
    "LAogICAgICAic3VtbWFyeSI6ICJGb2xkZXJzIG1hZGUgb25lIGF0IGEgdGltZSBpbnNpZGUgdGhl",
    "IG93bmVkIGZvbGRlcjogZWFjaCBmb3VuZCBieSBwYXRoLCBhbiBleGlzdGluZyBuYW1lIHJlZnVz",
    "ZWQsIHRoZSBvd25lZCBmb2xkZXIgbGlzdGVkIG9uZSBlbnRyeSBwZXIgcGFnZSB3aXRoIGV4YWN0",
    "bHkgaXRzIG93biBjaGlsZHJlbiwgYW5kIGV2ZXJ5IGZvbGRlciBkZWxldGVkIGFuZCBjb25maXJt",
    "ZWQgYWJzZW50LiBBUEkgb3BlcmF0aW9ucyBvbmx5LiIsCiAgICAgICJmaXh0dXJlcyI6IHsKICAg",
    "ICAgICAiZm9sZGVyIjogeyAidHlwZSI6ICJkaXJlY3RvcnkiLCAicGF0aCI6ICIiIH0sCiAgICAg",
    "ICAgImFscGhhIjogeyAidHlwZSI6ICJkaXJlY3RvcnkiLCAicGF0aCI6ICJhbHBoYSIgfSwKICAg",
    "ICAgICAiYnJhdm8iOiB7ICJ0eXBlIjogImRpcmVjdG9yeSIsICJwYXRoIjogImJyYXZvIiB9LAog",
    "ICAgICAgICJjaGFybGllIjogeyAidHlwZSI6ICJkaXJlY3RvcnkiLCAicGF0aCI6ICJjaGFybGll",
    "IiB9LAogICAgICAgICJhbHBoYS1pbm5lciI6IHsgInR5cGUiOiAiZGlyZWN0b3J5IiwgInBhdGgi",
    "OiAiYWxwaGEvaW5uZXIiIH0KICAgICAgfSwKICAgICAgInN0ZXBzIjogWwogICAgICAgIHsgImdy",
    "b3VwIjogIm5hbWVzcGFjZS5vcGVuIiB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJQT1NUIC9m",
    "b2xkZXJzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAiYWxw",
    "aGEiIH0sICJta2Rpcl9wYXJlbnRzIjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIw",
    "MSwgImVudHJ5IjogeyAiZml4dHVyZSI6ICJhbHBoYSIgfSB9IH0sCiAgICAgICAgeyAib3BlcmF0",
    "aW9uIjogIlBPU1QgL2ZvbGRlcnMve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAi",
    "Zml4dHVyZSI6ICJicmF2byIgfSwgIm1rZGlyX3BhcmVudHMiOiBmYWxzZSB9LCAiZXhwZWN0Ijog",
    "eyAic3RhdHVzIjogMjAxLCAiZW50cnkiOiB7ICJmaXh0dXJlIjogImJyYXZvIiB9IH0gfSwKICAg",
    "ICAgICB7ICJvcGVyYXRpb24iOiAiUE9TVCAvZm9sZGVycy97cGF0aH0iLCAicGFyYW1ldGVycyI6",
    "IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogImNoYXJsaWUiIH0sICJta2Rpcl9wYXJlbnRzIjogZmFs",
    "c2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMSwgImVudHJ5IjogeyAiZml4dHVyZSI6ICJj",
    "aGFybGllIiB9IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiUE9TVCAvZm9sZGVycy97cGF0",
    "aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogImFscGhhLWlubmVyIiB9",
    "LCAibWtkaXJfcGFyZW50cyI6IGZhbHNlIH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDEsICJl",
    "bnRyeSI6IHsgImZpeHR1cmUiOiAiYWxwaGEtaW5uZXIiIH0gfSB9LAogICAgICAgIHsgIm9wZXJh",
    "dGlvbiI6ICJQT1NUIC9mb2xkZXJzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsg",
    "ImZpeHR1cmUiOiAiYWxwaGEiIH0sICJta2Rpcl9wYXJlbnRzIjogZmFsc2UgfSwgImV4cGVjdCI6",
    "IHsgInN0YXR1cyI6IDQyMiwgImVycm9yIjogInByb2Nlc3NpbmctZmFpbHVyZS9kZXN0aW5hdGlv",
    "bi1leGlzdHMiIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMv",
    "bWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJh",
    "bHBoYSIgfSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjAwLCAiZW50cnkiOiB7ICJmaXh0dXJl",
    "IjogImFscGhhIiB9IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlv",
    "bnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6",
    "ICJhbHBoYS1pbm5lciIgfSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjAwLCAiZW50cnkiOiB7",
    "ICJmaXh0dXJlIjogImFscGhhLWlubmVyIiB9IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAi",
    "R0VUIC9mb2xkZXJzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUi",
    "OiAiZm9sZGVyIiB9LCAicGVyX3BhZ2UiOiAxIH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAs",
    "ICJsaXN0aW5nIjogeyAiZW50cmllcyI6IFsgImFscGhhIiwgImJyYXZvIiwgImNoYXJsaWUiIF0s",
    "ICJtYXhfcGFnZXMiOiAxNiB9IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9mb2xk",
    "ZXJzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAiYWxwaGEi",
    "IH0sICJwZXJfcGFnZSI6IDEwMDAgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMCwgImxpc3Rp",
    "bmciOiB7ICJlbnRyaWVzIjogWyAiYWxwaGEtaW5uZXIiIF0sICJtYXhfcGFnZXMiOiAxNiB9IH0g",
    "fSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiREVMRVRFIC9maWxlcy97cGF0aH0iLCAicGFyYW1l",
    "dGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogImFscGhhLWlubmVyIiB9LCAicmVjdXJzaXZl",
    "IjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwNCB9IH0sCiAgICAgICAgeyAib3Bl",
    "cmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJz",
    "IjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAiYWxwaGEtaW5uZXIiIH0gfSwgImV4cGVjdCI6IHsg",
    "InN0YXR1cyI6IDQwNCwgImVycm9yIjogIm5vdC1mb3VuZCIsICJhdHRlbXB0cyI6IDUsICJpbnRl",
    "cnZhbF9zZWNvbmRzIjogMSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkRFTEVURSAvZmls",
    "ZXMve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJhbHBoYSIg",
    "fSwgInJlY3Vyc2l2ZSI6IGZhbHNlIH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDQgfSB9LAog",
    "ICAgICAgIHsgIm9wZXJhdGlvbiI6ICJHRVQgL2ZpbGVfYWN0aW9ucy9tZXRhZGF0YS97cGF0aH0i",
    "LCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogImFscGhhIiB9IH0sICJleHBl",
    "Y3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1wdHMiOiA1",
    "LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJERUxF",
    "VEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAi",
    "YnJhdm8iIH0sICJyZWN1cnNpdmUiOiBmYWxzZSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjA0",
    "IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRhdGEv",
    "e3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJicmF2byIgfSB9",
    "LCAiZXhwZWN0IjogeyAic3RhdHVzIjogNDA0LCAiZXJyb3IiOiAibm90LWZvdW5kIiwgImF0dGVt",
    "cHRzIjogNSwgImludGVydmFsX3NlY29uZHMiOiAxIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24i",
    "OiAiREVMRVRFIC9maWxlcy97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0",
    "dXJlIjogImNoYXJsaWUiIH0sICJyZWN1cnNpdmUiOiBmYWxzZSB9LCAiZXhwZWN0IjogeyAic3Rh",
    "dHVzIjogMjA0IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMv",
    "bWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJj",
    "aGFybGllIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91",
    "bmQiLCAiYXR0ZW1wdHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsg",
    "Imdyb3VwIjogIm5hbWVzcGFjZS5jbG9zZSIgfQogICAgICBdCiAgICB9LAogICAgewogICAgICAi",
    "aWQiOiAiZmlsZXMub3duZWQtYmluYXJ5LXJvdW5kdHJpcCIsCiAgICAgICJzdW1tYXJ5IjogIlRo",
    "cmVlIG93bmVkIGZpbGVzIChmcm9tIGEgbG9jYWwgZmlsZSwgYSBzZWVrYWJsZSBzdHJlYW0gYW5k",
    "IGEgZm9yd2FyZC1vbmx5IHN0cmVhbSBnaXZpbmcgYXQgbW9zdCB0aHJlZSBieXRlcyBwZXIgcmVh",
    "ZCkgdXBsb2FkZWQgd2l0aCBhIHByb3ZpZGVkIG10aW1lLCBlYWNoIGZvdW5kIHdpdGggaXRzIGV4",
    "YWN0IHNpemUsIHRoZSBvd25lZCBmb2xkZXIgbGlzdGVkIG9uZSBlbnRyeSBwZXIgcGFnZSB3aXRo",
    "IGV4YWN0bHkgdGhvc2UgZmlsZXMsIGVhY2ggZG93bmxvYWRlZCBieXRlIGZvciBieXRlLCBhbmQg",
    "ZXZlcnl0aGluZyBkZWxldGVkIGFuZCBjb25maXJtZWQgYWJzZW50LiBDb25zZXJ2ZWQgZnJvbSB2",
    "ZXJpZmljYXRpb24vZmlsZXMtcGFpcmVkL2NvbnRyYWN0Lmpzb24gcmV2aXNpb24gMyBhbmQgaXRz",
    "IGpvdXJuZXlzLiIsCiAgICAgICJmaXh0dXJlcyI6IHsKICAgICAgICAiZm9sZGVyIjogeyAidHlw",
    "ZSI6ICJkaXJlY3RvcnkiLCAicGF0aCI6ICIiIH0sCiAgICAgICAgImJpbmFyeS5iaW4iOiB7ICJ0",
    "eXBlIjogImZpbGUiLCAicGF0aCI6ICJiaW5hcnkuYmluIiwgInJlY2lwZSI6IDEgfSwKICAgICAg",
    "ICAiZW1wdHkuYmluIjogeyAidHlwZSI6ICJmaWxlIiwgInBhdGgiOiAiZW1wdHkuYmluIiwgInJl",
    "Y2lwZSI6IDIgfSwKICAgICAgICAic2hvcnQtcmVhZC5iaW4iOiB7ICJ0eXBlIjogImZpbGUiLCAi",
    "cGF0aCI6ICJzaG9ydC1yZWFkLmJpbiIsICJyZWNpcGUiOiAzIH0KICAgICAgfSwKICAgICAgInN0",
    "ZXBzIjogWwogICAgICAgIHsgImdyb3VwIjogIm5hbWVzcGFjZS5vcGVuIiB9LAogICAgICAgIHsg",
    "ImludGVudCI6ICJ1cGxvYWQiLCAiZml4dHVyZSI6ICJiaW5hcnkuYmluIiwgInNvdXJjZSI6ICJs",
    "b2NhbC1maWxlIiwgInBhcmFtZXRlcnMiOiB7ICJwcm92aWRlZF9tdGltZSI6ICIyMDI2LTA5LTI0",
    "VDAwOjAwOjAwWiIgfSwgImV4cGVjdCI6IHsgImNvbXBsZXRlZCI6IHRydWUgfSB9LAogICAgICAg",
    "IHsgIm9wZXJhdGlvbiI6ICJHRVQgL2ZpbGVfYWN0aW9ucy9tZXRhZGF0YS97cGF0aH0iLCAicGFy",
    "YW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogImJpbmFyeS5iaW4iIH0gfSwgImV4cGVj",
    "dCI6IHsgInN0YXR1cyI6IDIwMCwgImVudHJ5IjogeyAiZml4dHVyZSI6ICJiaW5hcnkuYmluIiwg",
    "ImZpZWxkcyI6IHsgInByb3ZpZGVkX210aW1lIjogeyAib25lX29mIjogWyAiMjAyNi0wOS0yNFQw",
    "MDowMDowMFoiLCBudWxsIF0gfSB9IH0gfSB9LAogICAgICAgIHsgImludGVudCI6ICJ1cGxvYWQi",
    "LCAiZml4dHVyZSI6ICJlbXB0eS5iaW4iLCAic291cmNlIjogInNlZWthYmxlLXN0cmVhbSIsICJw",
    "YXJhbWV0ZXJzIjogeyAicHJvdmlkZWRfbXRpbWUiOiAiMjAyNi0wOS0yNFQwMDowMDowMFoiIH0s",
    "ICJleHBlY3QiOiB7ICJjb21wbGV0ZWQiOiB0cnVlIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24i",
    "OiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJw",
    "YXRoIjogeyAiZml4dHVyZSI6ICJlbXB0eS5iaW4iIH0gfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6",
    "IDIwMCwgImVudHJ5IjogeyAiZml4dHVyZSI6ICJlbXB0eS5iaW4iLCAiZmllbGRzIjogeyAicHJv",
    "dmlkZWRfbXRpbWUiOiB7ICJvbmVfb2YiOiBbICIyMDI2LTA5LTI0VDAwOjAwOjAwWiIsIG51bGwg",
    "XSB9IH0gfSB9IH0sCiAgICAgICAgeyAiaW50ZW50IjogInVwbG9hZCIsICJmaXh0dXJlIjogInNo",
    "b3J0LXJlYWQuYmluIiwgInNvdXJjZSI6ICJmb3J3YXJkLW9ubHktc3RyZWFtIiwgIm1heF9yZWFk",
    "IjogMywgInBhcmFtZXRlcnMiOiB7ICJwcm92aWRlZF9tdGltZSI6ICIyMDI2LTA5LTI0VDAwOjAw",
    "OjAwWiIgfSwgImV4cGVjdCI6IHsgImNvbXBsZXRlZCI6IHRydWUgfSB9LAogICAgICAgIHsgIm9w",
    "ZXJhdGlvbiI6ICJHRVQgL2ZpbGVfYWN0aW9ucy9tZXRhZGF0YS97cGF0aH0iLCAicGFyYW1ldGVy",
    "cyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogInNob3J0LXJlYWQuYmluIiB9IH0sICJleHBlY3Qi",
    "OiB7ICJzdGF0dXMiOiAyMDAsICJlbnRyeSI6IHsgImZpeHR1cmUiOiAic2hvcnQtcmVhZC5iaW4i",
    "LCAiZmllbGRzIjogeyAicHJvdmlkZWRfbXRpbWUiOiB7ICJvbmVfb2YiOiBbICIyMDI2LTA5LTI0",
    "VDAwOjAwOjAwWiIsIG51bGwgXSB9IH0gfSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdF",
    "VCAvZm9sZGVycy97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjog",
    "ImZvbGRlciIgfSwgInBlcl9wYWdlIjogMSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjAwLCAi",
    "bGlzdGluZyI6IHsgImVudHJpZXMiOiBbICJiaW5hcnkuYmluIiwgImVtcHR5LmJpbiIsICJzaG9y",
    "dC1yZWFkLmJpbiIgXSwgIm1heF9wYWdlcyI6IDE2IH0gfSB9LAogICAgICAgIHsgImludGVudCI6",
    "ICJkb3dubG9hZCIsICJmaXh0dXJlIjogImJpbmFyeS5iaW4iLCAiZXhwZWN0IjogeyAiYnl0ZXMi",
    "OiAicmVjaXBlIiB9IH0sCiAgICAgICAgeyAiaW50ZW50IjogImRvd25sb2FkIiwgImZpeHR1cmUi",
    "OiAiZW1wdHkuYmluIiwgImV4cGVjdCI6IHsgImJ5dGVzIjogInJlY2lwZSIgfSB9LAogICAgICAg",
    "IHsgImludGVudCI6ICJkb3dubG9hZCIsICJmaXh0dXJlIjogInNob3J0LXJlYWQuYmluIiwgImV4",
    "cGVjdCI6IHsgImJ5dGVzIjogInJlY2lwZSIgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJE",
    "RUxFVEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUi",
    "OiAiYmluYXJ5LmJpbiIgfSwgInJlY3Vyc2l2ZSI6IGZhbHNlIH0sICJleHBlY3QiOiB7ICJzdGF0",
    "dXMiOiAyMDQgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJHRVQgL2ZpbGVfYWN0aW9ucy9t",
    "ZXRhZGF0YS97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogImJp",
    "bmFyeS5iaW4iIH0gfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDQwNCwgImVycm9yIjogIm5vdC1m",
    "b3VuZCIsICJhdHRlbXB0cyI6IDUsICJpbnRlcnZhbF9zZWNvbmRzIjogMSB9IH0sCiAgICAgICAg",
    "eyAib3BlcmF0aW9uIjogIkRFTEVURSAvZmlsZXMve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJw",
    "YXRoIjogeyAiZml4dHVyZSI6ICJlbXB0eS5iaW4iIH0sICJyZWN1cnNpdmUiOiBmYWxzZSB9LCAi",
    "ZXhwZWN0IjogeyAic3RhdHVzIjogMjA0IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VU",
    "IC9maWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjog",
    "eyAiZml4dHVyZSI6ICJlbXB0eS5iaW4iIH0gfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDQwNCwg",
    "ImVycm9yIjogIm5vdC1mb3VuZCIsICJhdHRlbXB0cyI6IDUsICJpbnRlcnZhbF9zZWNvbmRzIjog",
    "MSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkRFTEVURSAvZmlsZXMve3BhdGh9IiwgInBh",
    "cmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJzaG9ydC1yZWFkLmJpbiIgfSwgInJl",
    "Y3Vyc2l2ZSI6IGZhbHNlIH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDQgfSB9LAogICAgICAg",
    "IHsgIm9wZXJhdGlvbiI6ICJHRVQgL2ZpbGVfYWN0aW9ucy9tZXRhZGF0YS97cGF0aH0iLCAicGFy",
    "YW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogInNob3J0LXJlYWQuYmluIiB9IH0sICJl",
    "eHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1wdHMi",
    "OiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgImdyb3VwIjogIm5hbWVz",
    "cGFjZS5jbG9zZSIgfQogICAgICBdCiAgICB9LAogICAgewogICAgICAiaWQiOiAiZmlsZXMub3du",
    "ZWQtbmFtZXNwYWNlLWV4dGVuZGVkIiwKICAgICAgInN1bW1hcnkiOiAiTGl0ZXJhbCBzcGVjaWFs",
    "LWNoYXJhY3RlciBuYW1lcyAoIywgJSwgYSBub24tQVNDSUkgbGV0dGVyIGFuZCBhIHNwYWNlKSwg",
    "YSBuZXN0ZWQgZm9sZGVyLCBhIG11bHRpcGFydCB1cGxvYWQgc3RvcmVkIGluIGF0IGxlYXN0IHR3",
    "byBwYXJ0cyB3aXRoIGl0cyBmaW5hbCBwcm9ncmVzcywgYSBjb3B5IGFuZCBhIG1vdmUgd2FpdGVk",
    "IGZvciwgYSBvbmUtZW50cnktcGVyLXBhZ2UgbGlzdGluZyB3aG9zZSByZXR1cm5lZCBlbnRyaWVz",
    "IGRvd25sb2FkIHRoZWlyIG93biBmaWxlcywgYnl0ZS1leGFjdCBkb3dubG9hZHMsIGFuIHVwbG9h",
    "ZCBjYW5jZWxsZWQgYWZ0ZXIgaXRzIGZpcnN0IGFja25vd2xlZGdlZCBwYXJ0IHRoYXQgcHVibGlz",
    "aGVzIG5vdGhpbmcsIGFuZCBub24tcmVjdXJzaXZlIGRlbGV0ZXMgY29uZmlybWVkIGJ5IGFic2Vu",
    "Y2UuIENvbnNlcnZlZCBmcm9tIHZlcmlmaWNhdGlvbi9maWxlcy1wYWlyZWQvY29udHJhY3QtZXh0",
    "ZW5kZWQuanNvbiByZXZpc2lvbiAyIGFuZCBpdHMgam91cm5leXMuIiwKICAgICAgImZpeHR1cmVz",
    "IjogewogICAgICAgICJmb2xkZXIiOiB7ICJ0eXBlIjogImRpcmVjdG9yeSIsICJwYXRoIjogIiIg",
    "fSwKICAgICAgICAiaGFzaC1uYW1lIjogeyAidHlwZSI6ICJmaWxlIiwgInBhdGgiOiAiYSNiLnR4",
    "dCIsICJyZWNpcGUiOiA0IH0sCiAgICAgICAgInBlcmNlbnQtbmFtZSI6IHsgInR5cGUiOiAiZmls",
    "ZSIsICJwYXRoIjogIjEwMCUudHh0IiwgInJlY2lwZSI6IDUgfSwKICAgICAgICAidW5pY29kZS1u",
    "YW1lIjogeyAidHlwZSI6ICJmaWxlIiwgInBhdGgiOiAiw6kgKy50eHQiLCAicmVjaXBlIjogNiB9",
    "LAogICAgICAgICJuZXN0ZWQiOiB7ICJ0eXBlIjogImRpcmVjdG9yeSIsICJwYXRoIjogIm5lc3Rl",
    "ZCIgfSwKICAgICAgICAiaW5uZXIuYmluIjogeyAidHlwZSI6ICJmaWxlIiwgInBhdGgiOiAibmVz",
    "dGVkL2lubmVyLmJpbiIsICJyZWNpcGUiOiA3IH0sCiAgICAgICAgImxhcmdlLmJpbiI6IHsgInR5",
    "cGUiOiAiZmlsZSIsICJwYXRoIjogImxhcmdlLmJpbiIsICJyZWNpcGUiOiA4IH0sCiAgICAgICAg",
    "ImNvcGllZC5iaW4iOiB7ICJ0eXBlIjogImZpbGUiLCAicGF0aCI6ICJjb3BpZWQuYmluIiwgInJl",
    "Y2lwZSI6IDcgfSwKICAgICAgICAibW92ZWQuYmluIjogeyAidHlwZSI6ICJmaWxlIiwgInBhdGgi",
    "OiAibmVzdGVkL21vdmVkLmJpbiIsICJyZWNpcGUiOiA3IH0sCiAgICAgICAgImNhbmNlbGxlZC5i",
    "aW4iOiB7ICJ0eXBlIjogImZpbGUiLCAicGF0aCI6ICJjYW5jZWxsZWQuYmluIiwgInJlY2lwZSI6",
    "IDkgfQogICAgICB9LAogICAgICAic3RlcHMiOiBbCiAgICAgICAgeyAiZ3JvdXAiOiAibmFtZXNw",
    "YWNlLm9wZW4iIH0sCiAgICAgICAgeyAiaW50ZW50IjogInVwbG9hZCIsICJmaXh0dXJlIjogImhh",
    "c2gtbmFtZSIsICJzb3VyY2UiOiAibG9jYWwtZmlsZSIsICJleHBlY3QiOiB7ICJjb21wbGV0ZWQi",
    "OiB0cnVlIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0",
    "YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJoYXNo",
    "LW5hbWUiIH0gfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMCwgImVudHJ5IjogeyAiZml4dHVy",
    "ZSI6ICJoYXNoLW5hbWUiIH0gfSB9LAogICAgICAgIHsgImludGVudCI6ICJ1cGxvYWQiLCAiZml4",
    "dHVyZSI6ICJwZXJjZW50LW5hbWUiLCAic291cmNlIjogImxvY2FsLWZpbGUiLCAiZXhwZWN0Ijog",
    "eyAiY29tcGxldGVkIjogdHJ1ZSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmls",
    "ZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZp",
    "eHR1cmUiOiAicGVyY2VudC1uYW1lIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAsICJl",
    "bnRyeSI6IHsgImZpeHR1cmUiOiAicGVyY2VudC1uYW1lIiB9IH0gfSwKICAgICAgICB7ICJpbnRl",
    "bnQiOiAidXBsb2FkIiwgImZpeHR1cmUiOiAidW5pY29kZS1uYW1lIiwgInNvdXJjZSI6ICJsb2Nh",
    "bC1maWxlIiwgImV4cGVjdCI6IHsgImNvbXBsZXRlZCI6IHRydWUgfSB9LAogICAgICAgIHsgIm9w",
    "ZXJhdGlvbiI6ICJHRVQgL2ZpbGVfYWN0aW9ucy9tZXRhZGF0YS97cGF0aH0iLCAicGFyYW1ldGVy",
    "cyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogInVuaWNvZGUtbmFtZSIgfSB9LCAiZXhwZWN0Ijog",
    "eyAic3RhdHVzIjogMjAwLCAiZW50cnkiOiB7ICJmaXh0dXJlIjogInVuaWNvZGUtbmFtZSIgfSB9",
    "IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIlBPU1QgL2ZvbGRlcnMve3BhdGh9IiwgInBhcmFt",
    "ZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJuZXN0ZWQiIH0sICJta2Rpcl9wYXJlbnRz",
    "IjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMSwgImVudHJ5IjogeyAiZml4dHVy",
    "ZSI6ICJuZXN0ZWQiIH0gfSB9LAogICAgICAgIHsgImludGVudCI6ICJ1cGxvYWQiLCAiZml4dHVy",
    "ZSI6ICJpbm5lci5iaW4iLCAic291cmNlIjogInNlZWthYmxlLXN0cmVhbSIsICJleHBlY3QiOiB7",
    "ICJjb21wbGV0ZWQiOiB0cnVlIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxl",
    "X2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4",
    "dHVyZSI6ICJpbm5lci5iaW4iIH0gfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMCwgImVudHJ5",
    "IjogeyAiZml4dHVyZSI6ICJpbm5lci5iaW4iIH0gfSB9LAogICAgICAgIHsgImludGVudCI6ICJ1",
    "cGxvYWQiLCAiZml4dHVyZSI6ICJsYXJnZS5iaW4iLCAic291cmNlIjogImxvY2FsLWZpbGUiLCAi",
    "ZXhwZWN0IjogeyAiY29tcGxldGVkIjogdHJ1ZSwgInByb2dyZXNzX2ZpbmFsIjogeyAidG90YWxf",
    "Ynl0ZXMiOiAicmVjaXBlLWxlbmd0aCIsICJhY2tub3dsZWRnZWRfYnl0ZXMiOiAicmVjaXBlLWxl",
    "bmd0aCIgfSwgIm1pbl9wYXJ0cyI6IDIgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJHRVQg",
    "L2ZpbGVfYWN0aW9ucy9tZXRhZGF0YS97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7",
    "ICJmaXh0dXJlIjogImxhcmdlLmJpbiIgfSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjAwLCAi",
    "ZW50cnkiOiB7ICJmaXh0dXJlIjogImxhcmdlLmJpbiIgfSB9IH0sCiAgICAgICAgeyAiaW50ZW50",
    "IjogImNvcHkiLCAiZnJvbSI6ICJpbm5lci5iaW4iLCAiZml4dHVyZSI6ICJjb3BpZWQuYmluIiwg",
    "ImV4cGVjdCI6IHsgImNvbXBsZXRlZCI6IHRydWUgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6",
    "ICJHRVQgL2ZpbGVfYWN0aW9ucy9tZXRhZGF0YS97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBh",
    "dGgiOiB7ICJmaXh0dXJlIjogImNvcGllZC5iaW4iIH0gfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6",
    "IDIwMCwgImVudHJ5IjogeyAiZml4dHVyZSI6ICJjb3BpZWQuYmluIiB9IH0gfSwKICAgICAgICB7",
    "ICJpbnRlbnQiOiAibW92ZSIsICJmcm9tIjogImNvcGllZC5iaW4iLCAiZml4dHVyZSI6ICJtb3Zl",
    "ZC5iaW4iLCAiZXhwZWN0IjogeyAiY29tcGxldGVkIjogdHJ1ZSB9IH0sCiAgICAgICAgeyAib3Bl",
    "cmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJz",
    "IjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAiY29waWVkLmJpbiIgfSB9LCAiZXhwZWN0IjogeyAi",
    "c3RhdHVzIjogNDA0LCAiZXJyb3IiOiAibm90LWZvdW5kIiwgImF0dGVtcHRzIjogNSwgImludGVy",
    "dmFsX3NlY29uZHMiOiAxIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2Fj",
    "dGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVy",
    "ZSI6ICJtb3ZlZC5iaW4iIH0gfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMCwgImVudHJ5Ijog",
    "eyAiZml4dHVyZSI6ICJtb3ZlZC5iaW4iIH0gfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJH",
    "RVQgL2ZvbGRlcnMve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6",
    "ICJmb2xkZXIiIH0sICJwZXJfcGFnZSI6IDEgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMCwg",
    "Imxpc3RpbmciOiB7ICJlbnRyaWVzIjogWyAiaGFzaC1uYW1lIiwgInBlcmNlbnQtbmFtZSIsICJ1",
    "bmljb2RlLW5hbWUiLCAibmVzdGVkIiwgImxhcmdlLmJpbiIgXSwgIm1heF9wYWdlcyI6IDE2IH0g",
    "fSB9LAogICAgICAgIHsgImludGVudCI6ICJkb3dubG9hZCIsICJmaXh0dXJlIjogImhhc2gtbmFt",
    "ZSIsICJzb3VyY2UiOiAibGlzdGVkLWVudHJ5IiwgImV4cGVjdCI6IHsgImJ5dGVzIjogInJlY2lw",
    "ZSIgfSB9LAogICAgICAgIHsgImludGVudCI6ICJkb3dubG9hZCIsICJmaXh0dXJlIjogInBlcmNl",
    "bnQtbmFtZSIsICJzb3VyY2UiOiAibGlzdGVkLWVudHJ5IiwgImV4cGVjdCI6IHsgImJ5dGVzIjog",
    "InJlY2lwZSIgfSB9LAogICAgICAgIHsgImludGVudCI6ICJkb3dubG9hZCIsICJmaXh0dXJlIjog",
    "InVuaWNvZGUtbmFtZSIsICJzb3VyY2UiOiAibGlzdGVkLWVudHJ5IiwgImV4cGVjdCI6IHsgImJ5",
    "dGVzIjogInJlY2lwZSIgfSB9LAogICAgICAgIHsgImludGVudCI6ICJkb3dubG9hZCIsICJmaXh0",
    "dXJlIjogImxhcmdlLmJpbiIsICJzb3VyY2UiOiAibGlzdGVkLWVudHJ5IiwgImV4cGVjdCI6IHsg",
    "ImJ5dGVzIjogInJlY2lwZSIgfSB9LAogICAgICAgIHsgImludGVudCI6ICJkb3dubG9hZCIsICJm",
    "aXh0dXJlIjogImlubmVyLmJpbiIsICJleHBlY3QiOiB7ICJieXRlcyI6ICJyZWNpcGUiIH0gfSwK",
    "ICAgICAgICB7ICJpbnRlbnQiOiAiZG93bmxvYWQiLCAiZml4dHVyZSI6ICJtb3ZlZC5iaW4iLCAi",
    "ZXhwZWN0IjogeyAiYnl0ZXMiOiAicmVjaXBlIiB9IH0sCiAgICAgICAgeyAiaW50ZW50IjogImRv",
    "d25sb2FkIiwgImZpeHR1cmUiOiAibGFyZ2UuYmluIiwgImV4cGVjdCI6IHsgImJ5dGVzIjogInJl",
    "Y2lwZSIgfSB9LAogICAgICAgIHsgImludGVudCI6ICJ1cGxvYWQiLCAiZml4dHVyZSI6ICJjYW5j",
    "ZWxsZWQuYmluIiwgInNvdXJjZSI6ICJsb2NhbC1maWxlIiwgImNhbmNlbCI6ICJhZnRlci1maXJz",
    "dC1hY2tub3dsZWRnZWQtcGFydCIsICJleHBlY3QiOiB7ICJjYW5jZWxsZWQiOiB0cnVlIH0gfSwK",
    "ICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9",
    "IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJjYW5jZWxsZWQuYmluIiB9",
    "IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0",
    "ZW1wdHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlv",
    "biI6ICJERUxFVEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZp",
    "eHR1cmUiOiAibW92ZWQuYmluIiB9LCAicmVjdXJzaXZlIjogZmFsc2UgfSwgImV4cGVjdCI6IHsg",
    "InN0YXR1cyI6IDIwNCB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rp",
    "b25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUi",
    "OiAibW92ZWQuYmluIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJu",
    "b3QtZm91bmQiLCAiYXR0ZW1wdHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAg",
    "ICAgIHsgIm9wZXJhdGlvbiI6ICJERUxFVEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjog",
    "eyAicGF0aCI6IHsgImZpeHR1cmUiOiAiaW5uZXIuYmluIiB9LCAicmVjdXJzaXZlIjogZmFsc2Ug",
    "fSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwNCB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjog",
    "IkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0",
    "aCI6IHsgImZpeHR1cmUiOiAiaW5uZXIuYmluIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0",
    "MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1wdHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25k",
    "cyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJERUxFVEUgL2ZpbGVzL3twYXRofSIs",
    "ICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAibmVzdGVkIiB9LCAicmVjdXJz",
    "aXZlIjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwNCB9IH0sCiAgICAgICAgeyAi",
    "b3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0",
    "ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAibmVzdGVkIiB9IH0sICJleHBlY3QiOiB7ICJz",
    "dGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1wdHMiOiA1LCAiaW50ZXJ2",
    "YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJERUxFVEUgL2ZpbGVz",
    "L3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAibGFyZ2UuYmlu",
    "IiB9LCAicmVjdXJzaXZlIjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwNCB9IH0s",
    "CiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRo",
    "fSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAibGFyZ2UuYmluIiB9IH0s",
    "ICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1w",
    "dHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6",
    "ICJERUxFVEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1",
    "cmUiOiAiaGFzaC1uYW1lIiB9LCAicmVjdXJzaXZlIjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0",
    "YXR1cyI6IDIwNCB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25z",
    "L21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAi",
    "aGFzaC1uYW1lIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3Qt",
    "Zm91bmQiLCAiYXR0ZW1wdHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAg",
    "IHsgIm9wZXJhdGlvbiI6ICJERUxFVEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAi",
    "cGF0aCI6IHsgImZpeHR1cmUiOiAicGVyY2VudC1uYW1lIiB9LCAicmVjdXJzaXZlIjogZmFsc2Ug",
    "fSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwNCB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjog",
    "IkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0",
    "aCI6IHsgImZpeHR1cmUiOiAicGVyY2VudC1uYW1lIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMi",
    "OiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1wdHMiOiA1LCAiaW50ZXJ2YWxfc2Vj",
    "b25kcyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJERUxFVEUgL2ZpbGVzL3twYXRo",
    "fSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAidW5pY29kZS1uYW1lIiB9",
    "LCAicmVjdXJzaXZlIjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwNCB9IH0sCiAg",
    "ICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIs",
    "ICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAidW5pY29kZS1uYW1lIiB9IH0s",
    "ICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1w",
    "dHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgImdyb3VwIjogIm5h",
    "bWVzcGFjZS5jbG9zZSIgfQogICAgICBdCiAgICB9LAogICAgewogICAgICAiaWQiOiAiZmlsZXMu",
    "b3duZWQtZGlyZWN0b3J5LWhlbHBlcnMiLAogICAgICAic3VtbWFyeSI6ICJBIGxvY2FsIHRyZWUg",
    "dXBsb2FkZWQgYXMgYSBkaXJlY3RvcnksIGVhY2ggZW50cnkgaXQgbWFkZSBmb3VuZCBhbmQgZWFj",
    "aCBmb2xkZXIgbGlzdGVkIHdpdGggZXhhY3RseSBpdHMgb3duIGVudHJpZXMsIHRoZSB0cmVlIGRv",
    "d25sb2FkZWQgYXMgYSBkaXJlY3RvcnkgYnl0ZSBmb3IgYnl0ZSwgYSBmb2xkZXIgY29waWVkIGFu",
    "ZCB0aGUgY29weSBtb3ZlZCAoZWFjaCB3YWl0ZWQgZm9yKSwgdGhlIG1vdmVkIGZpbGUgZG93bmxv",
    "YWRlZCwgYW5kIG5vbi1yZWN1cnNpdmUgZGVsZXRlcywgZGVlcGVzdCBmaXJzdCwgY29uZmlybWVk",
    "IGJ5IGFic2VuY2UuIENvbnNlcnZlZCBmcm9tIHZlcmlmaWNhdGlvbi9maWxlcy1wYWlyZWQvY29u",
    "dHJhY3QtaGVscGVycy5qc29uIHJldmlzaW9uIDEgYW5kIGl0cyBqb3VybmV5cy4iLAogICAgICAi",
    "Zml4dHVyZXMiOiB7CiAgICAgICAgImZvbGRlciI6IHsgInR5cGUiOiAiZGlyZWN0b3J5IiwgInBh",
    "dGgiOiAiIiB9LAogICAgICAgICJ1cCI6IHsgInR5cGUiOiAiZGlyZWN0b3J5IiwgInBhdGgiOiAi",
    "dXAiIH0sCiAgICAgICAgInVwLWEiOiB7ICJ0eXBlIjogImZpbGUiLCAicGF0aCI6ICJ1cC9hLmJp",
    "biIsICJyZWNpcGUiOiAxMCB9LAogICAgICAgICJ1cC1zdWIiOiB7ICJ0eXBlIjogImRpcmVjdG9y",
    "eSIsICJwYXRoIjogInVwL3N1YiIgfSwKICAgICAgICAidXAtYiI6IHsgInR5cGUiOiAiZmlsZSIs",
    "ICJwYXRoIjogInVwL3N1Yi9iLmJpbiIsICJyZWNpcGUiOiAxMSB9LAogICAgICAgICJ1cC1lbXB0",
    "eSI6IHsgInR5cGUiOiAiZGlyZWN0b3J5IiwgInBhdGgiOiAidXAvZW1wdHkiIH0sCiAgICAgICAg",
    "ImNvcHkiOiB7ICJ0eXBlIjogImRpcmVjdG9yeSIsICJwYXRoIjogImNvcHkiIH0sCiAgICAgICAg",
    "ImNvcHktYiI6IHsgInR5cGUiOiAiZmlsZSIsICJwYXRoIjogImNvcHkvYi5iaW4iLCAicmVjaXBl",
    "IjogMTEgfSwKICAgICAgICAibW92ZWQiOiB7ICJ0eXBlIjogImRpcmVjdG9yeSIsICJwYXRoIjog",
    "Im1vdmVkIiB9LAogICAgICAgICJtb3ZlZC1iIjogeyAidHlwZSI6ICJmaWxlIiwgInBhdGgiOiAi",
    "bW92ZWQvYi5iaW4iLCAicmVjaXBlIjogMTEgfQogICAgICB9LAogICAgICAic3RlcHMiOiBbCiAg",
    "ICAgICAgeyAiZ3JvdXAiOiAibmFtZXNwYWNlLm9wZW4iIH0sCiAgICAgICAgeyAiaW50ZW50Ijog",
    "InVwbG9hZC1kaXJlY3RvcnkiLCAiZml4dHVyZSI6ICJ1cCIsICJ0cmVlIjogWyAidXAtYSIsICJ1",
    "cC1zdWIiLCAidXAtYiIsICJ1cC1lbXB0eSIgXSwgImV4cGVjdCI6IHsgImNvbXBsZXRlZCI6IFsg",
    "InVwLWEiLCAidXAtYiIgXSwgImZpbGVzIjogMiwgImVtcHR5X2ZvbGRlcnMiOiAxLCAiYnl0ZXMi",
    "OiAzNjMyIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0",
    "YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJ1cCIg",
    "fSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjAwLCAiZW50cnkiOiB7ICJmaXh0dXJlIjogInVw",
    "IiB9IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRh",
    "dGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJ1cC1hIiB9",
    "IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAsICJlbnRyeSI6IHsgImZpeHR1cmUiOiAidXAt",
    "YSIgfSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFk",
    "YXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAidXAtc3Vi",
    "IiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAsICJlbnRyeSI6IHsgImZpeHR1cmUiOiAi",
    "dXAtc3ViIiB9IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMv",
    "bWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJ1",
    "cC1iIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAsICJlbnRyeSI6IHsgImZpeHR1cmUi",
    "OiAidXAtYiIgfSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25z",
    "L21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAi",
    "dXAtZW1wdHkiIH0gfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIwMCwgImVudHJ5IjogeyAiZml4",
    "dHVyZSI6ICJ1cC1lbXB0eSIgfSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZm9s",
    "ZGVycy97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogInVwIiB9",
    "LCAicGVyX3BhZ2UiOiAxMDAwIH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAsICJsaXN0aW5n",
    "IjogeyAiZW50cmllcyI6IFsgInVwLWEiLCAidXAtc3ViIiwgInVwLWVtcHR5IiBdLCAibWF4X3Bh",
    "Z2VzIjogMTYgfSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZm9sZGVycy97cGF0",
    "aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogInVwLXN1YiIgfSwgInBl",
    "cl9wYWdlIjogMTAwMCB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjAwLCAibGlzdGluZyI6IHsg",
    "ImVudHJpZXMiOiBbICJ1cC1iIiBdLCAibWF4X3BhZ2VzIjogMTYgfSB9IH0sCiAgICAgICAgeyAi",
    "b3BlcmF0aW9uIjogIkdFVCAvZm9sZGVycy97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgi",
    "OiB7ICJmaXh0dXJlIjogInVwLWVtcHR5IiB9LCAicGVyX3BhZ2UiOiAxMDAwIH0sICJleHBlY3Qi",
    "OiB7ICJzdGF0dXMiOiAyMDAsICJsaXN0aW5nIjogeyAiZW50cmllcyI6IFtdLCAibWF4X3BhZ2Vz",
    "IjogMTYgfSB9IH0sCiAgICAgICAgeyAiaW50ZW50IjogImRvd25sb2FkLWRpcmVjdG9yeSIsICJm",
    "aXh0dXJlIjogInVwIiwgImV4cGVjdCI6IHsgImZpbGVzIjogMiwgImVtcHR5X2ZvbGRlcnMiOiAx",
    "LCAiYnl0ZXMiOiAzNjMyLCAiYnl0ZXNfbWF0Y2giOiBbICJ1cC1hIiwgInVwLWIiIF0gfSB9LAog",
    "ICAgICAgIHsgImludGVudCI6ICJjb3B5IiwgImZyb20iOiAidXAtc3ViIiwgImZpeHR1cmUiOiAi",
    "Y29weSIsICJleHBlY3QiOiB7ICJjb21wbGV0ZWQiOiB0cnVlIH0gfSwKICAgICAgICB7ICJvcGVy",
    "YXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMi",
    "OiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJjb3B5IiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMi",
    "OiAyMDAsICJlbnRyeSI6IHsgImZpeHR1cmUiOiAiY29weSIgfSB9IH0sCiAgICAgICAgeyAib3Bl",
    "cmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJz",
    "IjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAiY29weS1iIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0",
    "dXMiOiAyMDAsICJlbnRyeSI6IHsgImZpeHR1cmUiOiAiY29weS1iIiB9IH0gfSwKICAgICAgICB7",
    "ICJvcGVyYXRpb24iOiAiR0VUIC9mb2xkZXJzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0",
    "aCI6IHsgImZpeHR1cmUiOiAiY29weSIgfSwgInBlcl9wYWdlIjogMTAwMCB9LCAiZXhwZWN0Ijog",
    "eyAic3RhdHVzIjogMjAwLCAibGlzdGluZyI6IHsgImVudHJpZXMiOiBbICJjb3B5LWIiIF0sICJt",
    "YXhfcGFnZXMiOiAxNiB9IH0gfSwKICAgICAgICB7ICJpbnRlbnQiOiAibW92ZSIsICJmcm9tIjog",
    "ImNvcHkiLCAiZml4dHVyZSI6ICJtb3ZlZCIsICJleHBlY3QiOiB7ICJjb21wbGV0ZWQiOiB0cnVl",
    "IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRhdGEv",
    "e3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJjb3B5LWIiIH0g",
    "fSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDQwNCwgImVycm9yIjogIm5vdC1mb3VuZCIsICJhdHRl",
    "bXB0cyI6IDUsICJpbnRlcnZhbF9zZWNvbmRzIjogMSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9u",
    "IjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRhL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAi",
    "cGF0aCI6IHsgImZpeHR1cmUiOiAiY29weSIgfSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogNDA0",
    "LCAiZXJyb3IiOiAibm90LWZvdW5kIiwgImF0dGVtcHRzIjogNSwgImludGVydmFsX3NlY29uZHMi",
    "OiAxIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRh",
    "dGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJtb3ZlZCIg",
    "fSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjAwLCAiZW50cnkiOiB7ICJmaXh0dXJlIjogIm1v",
    "dmVkIiB9IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0",
    "YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJtb3Zl",
    "ZC1iIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAsICJlbnRyeSI6IHsgImZpeHR1cmUi",
    "OiAibW92ZWQtYiIgfSB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZm9sZGVycy97",
    "cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogIm1vdmVkIiB9LCAi",
    "cGVyX3BhZ2UiOiAxMDAwIH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiAyMDAsICJsaXN0aW5nIjog",
    "eyAiZW50cmllcyI6IFsgIm1vdmVkLWIiIF0sICJtYXhfcGFnZXMiOiAxNiB9IH0gfSwKICAgICAg",
    "ICB7ICJvcGVyYXRpb24iOiAiR0VUIC9mb2xkZXJzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAi",
    "cGF0aCI6IHsgImZpeHR1cmUiOiAiZm9sZGVyIiB9LCAicGVyX3BhZ2UiOiAxMDAwIH0sICJleHBl",
    "Y3QiOiB7ICJzdGF0dXMiOiAyMDAsICJsaXN0aW5nIjogeyAiZW50cmllcyI6IFsgInVwIiwgIm1v",
    "dmVkIiBdLCAibWF4X3BhZ2VzIjogMTYgfSB9IH0sCiAgICAgICAgeyAiaW50ZW50IjogImRvd25s",
    "b2FkIiwgImZpeHR1cmUiOiAibW92ZWQtYiIsICJleHBlY3QiOiB7ICJieXRlcyI6ICJyZWNpcGUi",
    "IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiREVMRVRFIC9maWxlcy97cGF0aH0iLCAicGFy",
    "YW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogIm1vdmVkLWIiIH0sICJyZWN1cnNpdmUi",
    "OiBmYWxzZSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjA0IH0gfSwKICAgICAgICB7ICJvcGVy",
    "YXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMi",
    "OiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJtb3ZlZC1iIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0",
    "dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1wdHMiOiA1LCAiaW50ZXJ2YWxf",
    "c2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJERUxFVEUgL2ZpbGVzL3tw",
    "YXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAibW92ZWQiIH0sICJy",
    "ZWN1cnNpdmUiOiBmYWxzZSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjA0IH0gfSwKICAgICAg",
    "ICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBh",
    "cmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJtb3ZlZCIgfSB9LCAiZXhwZWN0Ijog",
    "eyAic3RhdHVzIjogNDA0LCAiZXJyb3IiOiAibm90LWZvdW5kIiwgImF0dGVtcHRzIjogNSwgImlu",
    "dGVydmFsX3NlY29uZHMiOiAxIH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiREVMRVRFIC9m",
    "aWxlcy97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsgInBhdGgiOiB7ICJmaXh0dXJlIjogInVwLWIi",
    "IH0sICJyZWN1cnNpdmUiOiBmYWxzZSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogMjA0IH0gfSwK",
    "ICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9",
    "IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6ICJ1cC1iIiB9IH0sICJleHBl",
    "Y3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0ZW1wdHMiOiA1",
    "LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlvbiI6ICJERUxF",
    "VEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAi",
    "dXAtc3ViIiB9LCAicmVjdXJzaXZlIjogZmFsc2UgfSwgImV4cGVjdCI6IHsgInN0YXR1cyI6IDIw",
    "NCB9IH0sCiAgICAgICAgeyAib3BlcmF0aW9uIjogIkdFVCAvZmlsZV9hY3Rpb25zL21ldGFkYXRh",
    "L3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAidXAtc3ViIiB9",
    "IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6ICJub3QtZm91bmQiLCAiYXR0",
    "ZW1wdHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAogICAgICAgIHsgIm9wZXJhdGlv",
    "biI6ICJERUxFVEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJzIjogeyAicGF0aCI6IHsgImZp",
    "eHR1cmUiOiAidXAtZW1wdHkiIH0sICJyZWN1cnNpdmUiOiBmYWxzZSB9LCAiZXhwZWN0IjogeyAi",
    "c3RhdHVzIjogMjA0IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9maWxlX2FjdGlv",
    "bnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAiZml4dHVyZSI6",
    "ICJ1cC1lbXB0eSIgfSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogNDA0LCAiZXJyb3IiOiAibm90",
    "LWZvdW5kIiwgImF0dGVtcHRzIjogNSwgImludGVydmFsX3NlY29uZHMiOiAxIH0gfSwKICAgICAg",
    "ICB7ICJvcGVyYXRpb24iOiAiREVMRVRFIC9maWxlcy97cGF0aH0iLCAicGFyYW1ldGVycyI6IHsg",
    "InBhdGgiOiB7ICJmaXh0dXJlIjogInVwLWEiIH0sICJyZWN1cnNpdmUiOiBmYWxzZSB9LCAiZXhw",
    "ZWN0IjogeyAic3RhdHVzIjogMjA0IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VUIC9m",
    "aWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjogeyAi",
    "Zml4dHVyZSI6ICJ1cC1hIiB9IH0sICJleHBlY3QiOiB7ICJzdGF0dXMiOiA0MDQsICJlcnJvciI6",
    "ICJub3QtZm91bmQiLCAiYXR0ZW1wdHMiOiA1LCAiaW50ZXJ2YWxfc2Vjb25kcyI6IDEgfSB9LAog",
    "ICAgICAgIHsgIm9wZXJhdGlvbiI6ICJERUxFVEUgL2ZpbGVzL3twYXRofSIsICJwYXJhbWV0ZXJz",
    "IjogeyAicGF0aCI6IHsgImZpeHR1cmUiOiAidXAiIH0sICJyZWN1cnNpdmUiOiBmYWxzZSB9LCAi",
    "ZXhwZWN0IjogeyAic3RhdHVzIjogMjA0IH0gfSwKICAgICAgICB7ICJvcGVyYXRpb24iOiAiR0VU",
    "IC9maWxlX2FjdGlvbnMvbWV0YWRhdGEve3BhdGh9IiwgInBhcmFtZXRlcnMiOiB7ICJwYXRoIjog",
    "eyAiZml4dHVyZSI6ICJ1cCIgfSB9LCAiZXhwZWN0IjogeyAic3RhdHVzIjogNDA0LCAiZXJyb3Ii",
    "OiAibm90LWZvdW5kIiwgImF0dGVtcHRzIjogNSwgImludGVydmFsX3NlY29uZHMiOiAxIH0gfSwK",
    "ICAgICAgICB7ICJncm91cCI6ICJuYW1lc3BhY2UuY2xvc2UiIH0KICAgICAgXQogICAgfQogIF0K",
    "fQo=",
)
# Its steps, groups expanded: all of them, those on the simulator, and the
# site-only ones.
POSITIONS = 141
SIMULATOR = 133
SITE_ONLY = 8

# Time limits, in seconds, all cooperative (see Time limits above): the case's
# deadline, each call's request_timeout, the cleanup's own deadline, the
# client's connect and per-read timeouts, and the longest wait for a returned
# call's adapter sends to return.
CASE_SECONDS = 90
STEP_SECONDS = 60
CLEANUP_SECONDS = 30
OPEN_TIMEOUT = 10
READ_TIMEOUT = 30
SETTLE_SECONDS = OPEN_TIMEOUT + READ_TIMEOUT
# The most folders an upload-directory step lists to see what it left empty.
OBSERVED_FOLDERS = 64
# Where the API is on the server, as the client is given it, and the URL path
# its requests start with.
API_BASE_PATH = "api/rest/v1"
API_PREFIX = "/" + API_BASE_PATH + "/"

# What a step may give and expect (lib/api_scenarios.rb and
# helpers/python/api_scenarios.rb). Anything else fails its step.
EXPECT_KEYS = [
    "status",
    "error",
    "attempts",
    "interval_seconds",
    "entry",
    "listing",
]
ENTRY_KEYS = ["fixture", "type", "path_one_of", "fields"]
LISTING_KEYS = ["entries", "max_pages", "max_records"]
MATCHERS = ["one_of", "includes", "not"]
INTENT_DETAILS = {
    "upload": ["source", "max_read", "cancel", "parameters"],
    "download": ["source"],
    "copy": ["from"],
    "move": ["from"],
    "upload-directory": ["tree", "parameters"],
    "download-directory": [],
}
INTENT_EXPECT_KEYS = {
    "upload": ["completed", "progress_final", "min_parts", "cancelled"],
    "download": ["bytes"],
    "copy": ["completed"],
    "move": ["completed"],
    "upload-directory": ["completed", "files", "empty_folders", "bytes"],
    "download-directory": ["files", "empty_folders", "bytes", "bytes_match"],
}
UPLOAD_SOURCES = ["local-file", "seekable-stream", "forward-only-stream"]
CANCELS = ["after-first-acknowledged-part"]
# The UploadProgress field that reports each progress_final value.
PROGRESS_FIELDS = {
    "total_bytes": "total_bytes",
    "acknowledged_bytes": "bytes_committed",
}


class Failure(AssertionError):
    """A check that failed, or a step that could not go on, named by its case
    and step and the definition's pointer."""


def describe(error):
    """An exception as evidence: its class and message, or None."""
    if error is None:
        return None
    kind = type(error)
    return f"{kind.__module__}.{kind.__qualname__}: {error}"


def shown(value, limit=2000):
    """value's repr for a failure's message, cut to limit characters."""
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "..."


def combined(failures):
    """The first of failures alone, or, with more, a Failure that reports the
    first first, then each of the others, with the first as its cause."""
    if len(failures) == 1:
        return failures[0]
    text = str(failures[0]) + "".join(
        f"\n\nThen also: {describe(failure)}" for failure in failures[1:]
    )
    failure = Failure(text)
    failure.__cause__ = failures[0]
    return failure


def load_definition():
    """The definition held here, once its bytes have their SHA-256."""
    data = base64.b64decode("".join(DEFINITION_BASE64), validate=True)
    digest = hashlib.sha256(data).hexdigest()
    if digest != DEFINITION_SHA256:
        raise Failure(
            f"the definition held here has SHA-256 {digest}, not {DEFINITION_SHA256}"
        )
    return json.loads(data.decode("utf-8"))


def escape(key):
    """key as one token of a JSON pointer."""
    return key.replace("~", "~0").replace("/", "~1")


def at(document, pointer):
    """The definition's value at a JSON pointer."""
    node = document
    for key in pointer.split("/")[1:]:
        key = key.replace("~1", "/").replace("~0", "~")
        node = node[int(key)] if isinstance(node, list) else node[key]
    return node


def expansion(document, index):
    """The pointer of each step of scenario index, in order, groups expanded."""
    pointers = []
    for position, step in enumerate(document["scenarios"][index]["steps"]):
        if "group" in step:
            members = document["groups"][step["group"]]
            pointers += [
                f"/groups/{escape(step['group'])}/{member}"
                for member in range(len(members))
            ]
        else:
            pointers.append(f"/scenarios/{index}/steps/{position}")
    return pointers


def operations_named(document):
    """Every operation the definition names, its steps' and its intents', as
    (verb, the literal start of its path, route), the longest start first;
    and the errors it expects of each for one of a scenario's fixtures, as
    {route: {(status, type)}}."""
    routes = set()
    errors: dict[str, set] = {}
    steps = [step for group in document["groups"].values() for step in group]
    steps += [
        step
        for scenario in document["scenarios"]
        for step in scenario["steps"]
    ]
    for step in steps:
        if "operation" not in step:
            continue
        routes.add(step["operation"])
        expect = step["expect"]
        if "error" in expect and isinstance(
            step.get("parameters", {}).get("path"), dict
        ):
            errors.setdefault(step["operation"], set()).add(
                (expect["status"], expect["error"])
            )
    for intent in document["intents"].values():
        routes.update(intent["operations"])
    named = [
        (
            route.split(" ", 1)[0],
            route.split(" ", 1)[1].split("{", 1)[0],
            route,
        )
        for route in routes
    ]
    return sorted(named, key=lambda each: -len(each[1])), errors


def route_of(response, named):
    """The definition's operation an API request was, if any, and the path
    its URL named."""
    tail = "/" + response.path[len(API_PREFIX) :]
    for verb, start, route in named:
        if response.method == verb and tail.startswith(start):
            return route, urllib.parse.unquote(tail[len(start) :])
    return None, None


def within(path, roots):
    """Whether path is one of roots or inside one."""
    return isinstance(path, str) and any(
        path == root or path.startswith(root + "/") for root in roots
    )


def paths_named(body):
    """The paths a raw JSON answer names: an object's, or each listed
    object's."""
    items = body if isinstance(body, list) else [body]
    return [
        item["path"]
        for item in items
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    ]


def instant(value):
    """A date-time's text as an aware datetime, or None if it is not one."""
    if not isinstance(value, str):
        return None
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        moment = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else None


def same(actual, expected, as_instant):
    """Whether actual is the definition's value: None only as None, a value
    only as one of the same type (so not True as 1), and a date-time, when
    as_instant, as the same instant."""
    if actual is None or expected is None:
        return actual is None and expected is None
    if as_instant:
        moments = instant(actual), instant(expected)
        return moments[0] is not None and moments[0] == moments[1]
    return type(actual) is type(expected) and actual == expected


def matches(kind, actual, given, as_instant):
    """Whether actual meets one field matcher of the definition. Compared as
    instants, a value that is not a date-time meets none of them."""
    if as_instant and actual is not None and instant(actual) is None:
        return False
    if kind == "one_of":
        return any(same(actual, option, as_instant) for option in given)
    if kind == "not":
        if as_instant and given is not None and instant(given) is None:
            return False
        return not same(actual, given, as_instant)
    if kind == "includes":
        return isinstance(actual, (str, list)) and all(
            item in actual for item in given
        )
    raise Failure(f"the matcher {kind} is not one this module runs")


def presents_file(response, path):
    """Whether an API response's raw JSON is the file entry at path."""
    body = response.json if response.has_json else None
    return (
        isinstance(body, dict)
        and body.get("type") == "file"
        and body.get("path") == path
    )


RECIPES: dict[int, bytes] = {}


def recipe_bytes(document, number):
    """A recipe's bytes, (index * multiplier + offset) % modulus for each
    index below length, checked against its SHA-256."""
    if number not in RECIPES:
        recipe = document["recipes"][str(number)]
        multiplier, offset, modulus, length = (
            recipe[key]
            for key in ("multiplier", "offset", "modulus", "length")
        )
        # The bytes repeat every modulus bytes.
        period = bytes(
            (index * multiplier + offset) % modulus for index in range(modulus)
        )
        data = (period * (length // modulus + 1))[:length]
        if hashlib.sha256(data).hexdigest() != recipe["sha256"]:
            raise Failure(
                f"recipe {number} (api.json /recipes/{number}) does not make its SHA-256"
            )
        RECIPES[number] = data
    return RECIPES[number]


class ForwardOnlyStream(io.RawIOBase):
    """Bytes read once, forward only, at most max_read a read (or any number
    without it): the stream cannot seek or tell and has no file. It counts
    its reads and the largest."""

    def __init__(self, data, max_read):
        super().__init__()
        self._data = memoryview(data)
        self._max_read = max_read
        self.consumed = 0
        self.reads = 0
        self.largest_read = 0

    def readable(self):
        return True

    def _take(self, size):
        size = min(size, len(self._data) - self.consumed)
        if self._max_read is not None:
            size = min(size, self._max_read)
        chunk = self._data[self.consumed : self.consumed + size]
        self.consumed += size
        self.reads += 1
        self.largest_read = max(self.largest_read, size)
        return chunk

    def read(self, size=-1):
        if size is None or size < 0:
            return self.readall()
        return bytes(self._take(size))

    def readinto(self, buffer):
        target = memoryview(buffer).cast("B")
        chunk = self._take(len(target))
        target[: len(chunk)] = chunk
        return len(chunk)


class Response:
    """What one request through a client's session got back: its method, URL
    path and status, whether it went to the API, and, for the API's JSON, the
    raw JSON as sent, read before the SDK saw the response."""

    def __init__(self, request, response, api):
        self.method = request.method
        self.path = urllib.parse.urlsplit(request.url or "").path
        self.status = response.status_code
        self.api = api
        self.has_json = False
        self.json: Any = None
        self.problem = None

    def read(self, content):
        """Keeps content, the response's whole body, as its raw JSON."""
        if not content:
            return
        try:
            self.json = json.loads(content.decode("utf-8"))
            self.has_json = True
        except ValueError as error:
            self.problem = f"not JSON: {error}"

    def evidence(self):
        kept: dict[str, Any] = {
            "method": self.method,
            "path": self.path,
            "status": self.status,
        }
        if self.has_json:
            kept["json"] = self.json
        if self.problem:
            kept["problem"] = self.problem
        return kept


class Recorder(requests.adapters.HTTPAdapter):
    """Requests' own adapter, which also keeps, in order, what every request
    it sends gets back. The body of each JSON answer of the API is read here,
    before the SDK sees the response, and the SDK reads the same bytes;
    storage's bodies (an upload part's answer, a PUT, and downloads) stay
    untouched. It counts the sends in progress: that they have returned says
    only that, not that the SDK's work has settled. Like HTTPAdapter by
    default, it never retries, so uploads may start through it."""

    def __init__(self, api_prefix):
        super().__init__(pool_maxsize=64)
        self._api_prefix = api_prefix
        self._changed = threading.Condition()
        self._responses: list[Response] = []
        self._in_flight = 0

    def send(
        self,
        request,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,
        proxies=None,
    ):
        with self._changed:
            self._in_flight += 1
        try:
            response = super().send(
                request,
                stream=stream,
                timeout=timeout,
                verify=verify,
                cert=cert,
                proxies=proxies,
            )
            path = urllib.parse.urlsplit(request.url or "").path
            kept = Response(
                request, response, path.startswith(self._api_prefix)
            )
            try:
                if (
                    kept.api
                    and request.method != "PUT"
                    and "json" in response.headers.get("Content-Type", "")
                ):
                    kept.read(response.content)
            except Exception as error:
                kept.problem = f"unreadable: {describe(error)}"
                raise
            finally:
                with self._changed:
                    self._responses.append(kept)
            return response
        finally:
            with self._changed:
                self._in_flight -= 1
                self._changed.notify_all()

    def mark(self):
        """Where the responses kept from now on start."""
        with self._changed:
            return len(self._responses)

    def since(self, mark):
        """The responses kept since mark."""
        with self._changed:
            return self._responses[mark:]

    def settle(self, timeout):
        """How many sends were in progress, and whether all of them returned
        within timeout seconds."""
        with self._changed:
            in_flight = self._in_flight
            returned = self._changed.wait_for(
                lambda: self._in_flight == 0, timeout
            )
            return in_flight, returned


def connect(hook=None):
    """A client of the launcher's server and API key that sends every request
    once, through a requests.Session of its own whose Recorder keeps what each
    got back, and whose response hook, if given, sees each response before
    the SDK does: the client, the session (which the client never closes) and
    the recorder."""
    recorder = Recorder(API_PREFIX)
    session = requests.Session()
    # The server is the launcher's, on this host: no proxy, CA bundle or
    # .netrc from the environment.
    session.trust_env = False
    session.mount("http://", recorder)
    session.mount("https://", recorder)
    if hook is not None:
        session.hooks["response"].append(hook)
    client = files_sdk.Client(
        api_key=API_KEY,
        base_url=SERVER_URL or "",
        base_path=API_BASE_PATH,
        open_timeout=OPEN_TIMEOUT,
        read_timeout=READ_TIMEOUT,
        max_network_retries=0,
        http_session=session,
    )
    return client, session, recorder


@dataclasses.dataclass(frozen=True)
class Binding:
    """One step as helpers/python/api_scenarios.rb bound it: its number in its
    case, its pointer into the definition, whether the simulator runs it, what
    it does, the SDK call that does it (given the names the module makes for
    the step), the native error it must raise, the entry fields it compares as
    instants, and, for a directory upload, the call that lists a folder after
    it."""

    number: int
    pointer: str
    simulator: bool
    action: str
    call: Callable[..., Any]
    error: Any = None
    instants: tuple = ()
    observe: Any = None


@dataclasses.dataclass(frozen=True)
class Case:
    """A scenario's bound steps, in order, and how a run of it that stopped
    early deletes its owned folder: cleanup, the operation of the scenario's
    own step that deletes that folder, sent with recursive true, then the
    lookup of step confirm until that folder's absence answers."""

    steps: tuple
    cleanup: Callable[..., Any]
    confirm: int


class CaseRun:
    """One case: its scenario's bound steps, run in order in a folder of its
    own, with every step's checks, calls and responses kept as evidence."""

    def __init__(self, document, case_id, out):
        self.document = document
        self.id = case_id
        self.out = out
        self.case = CASES[case_id]
        self.index = [
            scenario["id"] for scenario in document["scenarios"]
        ].index(case_id)
        self.fixtures = document["scenarios"][self.index]["fixtures"]
        self.namespace_fixture = next(
            name
            for name, fixture in self.fixtures.items()
            if fixture["path"] == ""
        )
        run = re.sub(r"[^A-Za-z0-9]+", "-", RUN_ID).strip("-") or "run"
        # The owned folder's name: for the run and the case, and new.
        self.namespace = (
            f"api-scenarios-{run}-{self.index + 1}-{uuid.uuid4().hex[:12]}"
        )
        self.owned = {
            name: (
                f"{self.namespace}/{fixture['path']}"
                if fixture["path"]
                else self.namespace
            )
            for name, fixture in self.fixtures.items()
        }
        self.named, self.errors = operations_named(document)
        self.listed: dict[str, Any] = {}
        self.listed_by: dict[str, str] = {}
        # Whether the case owns its folder: only once its create's own answer
        # proved it, and no longer once its own lookup confirmed it absent.
        self.acquired = False
        self.ownership: dict[str, Any] = {"state": "no create sent"}
        self.local = Path()
        self.client: Any = None
        self.recorder: Any = None
        self.deadline = 0.0
        self.identity = case_id
        self.pointer = f"/scenarios/{self.index}"
        self.records: list[dict[str, Any]] = [
            {
                "number": binding.number,
                "pointer": binding.pointer,
                "action": binding.action,
                "backend": "simulator" if binding.simulator else "site",
                "outcome": (
                    "not reached"
                    if binding.simulator
                    else "omitted: site-only"
                ),
                "checks": [],
                "calls": [],
                "details": {},
            }
            for binding in self.case.steps
        ]
        self.evidence: dict[str, Any] = {
            "case": case_id,
            "scenario": self.pointer,
            "definition_sha256": DEFINITION_SHA256,
            "run_id": RUN_ID,
            "namespace": self.namespace,
            "ownership": self.ownership,
            "time_limits": {
                "cooperative": True,
                "case_seconds": CASE_SECONDS,
                "request_timeout": STEP_SECONDS,
                "cleanup_seconds": CLEANUP_SECONDS,
                "open_timeout": OPEN_TIMEOUT,
                "read_timeout": READ_TIMEOUT,
                "adapter_settle_seconds": SETTLE_SECONDS,
            },
            "outcome": None,
            "failure": None,
            "seconds": None,
            "checks": [],
            "calls": [],
            "details": {},
            "steps": self.records,
            "cleanup": None,
        }
        self.current = self.evidence

    def run(self):
        """Runs every simulator step on the case's client, then closes it; if
        the case failed, runs its cleanup. Writes the evidence after each step
        that passes and at the end, then raises the case's first failure, with
        any later one (a cleanup's, or a client's or session's close) reported
        after it."""
        started = time.monotonic()
        failures: list[Exception] = []
        try:
            self.check_bindings()
            self.write()
            with tempfile.TemporaryDirectory(prefix="api-scenarios-") as local:
                self.local = Path(local)
                self.client, session, self.recorder = connect()
                self.deadline = time.monotonic() + CASE_SECONDS
                try:
                    for binding in self.case.steps:
                        if binding.simulator:
                            self.step(binding)
                except Exception as error:
                    failures.append(error)
                failures += self.close(
                    self.client, session, "the case's client"
                )
            if not failures:
                self.current, self.identity = self.evidence, self.id
                self.pointer = f"/scenarios/{self.index}"
                outcomes = collections.Counter(
                    record["outcome"] for record in self.records
                )
                simulator = sum(
                    1 for binding in self.case.steps if binding.simulator
                )
                self.check(
                    outcomes["passed"] == simulator
                    and outcomes["omitted: site-only"]
                    == len(self.records) - simulator,
                    "every simulator step passed, and every site-only step was omitted",
                    self.pointer,
                    dict(outcomes),
                )
        except Exception as error:
            failures.append(error)
        if failures:
            record: dict[str, Any] = {
                "outcome": None,
                "checks": [],
                "calls": [],
                "details": {},
            }
            self.evidence["cleanup"] = record
            try:
                failures += self.cleanup(record)
            except Exception as error:
                record["outcome"] = f"failed: {describe(error)}"
                failures.append(error)
        failure = combined(failures) if failures else None
        self.evidence["outcome"] = "passed" if failure is None else "failed"
        self.evidence["failure"] = describe(failure)
        self.evidence["seconds"] = round(time.monotonic() - started, 3)
        self.write()
        if failure is not None:
            raise failure

    def check_bindings(self):
        """Fails unless the case's bound steps are the definition's: one for
        each position, groups expanded, in order, each on the simulator unless
        the definition marks it for a site."""
        bound = [binding.pointer for binding in self.case.steps]
        self.check(
            bound == expansion(self.document, self.index),
            "its bound steps are the definition's, groups expanded",
            self.pointer,
            bound,
        )
        for number, binding in enumerate(self.case.steps, 1):
            backend = at(self.document, binding.pointer).get("backend")
            self.check(
                binding.number == number
                and binding.simulator == (backend in (None, "simulator")),
                f"step {number} is bound in its place, on the simulator unless the definition marks it for a site",
                binding.pointer,
                [binding.number, binding.simulator, backend],
            )

    def step(self, binding):
        record = self.records[binding.number - 1]
        self.current, self.pointer = record, binding.pointer
        self.identity = f"{self.id} step {binding.number}"
        raw = at(self.document, binding.pointer)
        started = time.monotonic()
        try:
            if "operation" in raw:
                self.operation(binding, raw)
            elif "intent" in raw:
                self.intent(binding, raw)
            else:
                self.check(
                    False,
                    "an operation or an intent",
                    binding.pointer,
                    sorted(raw),
                )
        except Exception as error:
            record["outcome"] = "failed"
            record["failure"] = describe(error)
            raise
        finally:
            record["seconds"] = round(time.monotonic() - started, 3)
        record["outcome"] = "passed"
        self.write()

    def check(self, passed, what, pointer, observed=None):
        """Keeps a check of the current step, failing the step unless passed."""
        self.current["checks"].append(
            {
                "check": what,
                "pointer": pointer,
                "passed": bool(passed),
                "observed": observed,
            }
        )
        if not passed:
            raise Failure(
                f"{self.identity}: {what} (api.json {pointer}); observed {shown(observed)}"
            )

    def known(self, given, allowed, pointer):
        unknown = sorted(set(given) - set(allowed))
        self.check(
            not unknown, "gives only what this module runs", pointer, unknown
        )

    def budget(self):
        """Fails the step once the case's (or the cleanup's) deadline has passed."""
        left = self.deadline - time.monotonic()
        self.check(
            left > 0,
            "the deadline has not passed",
            self.pointer,
            round(left, 3),
        )

    def options(self, token=None):
        """A call's RequestOptions: the case's (or the cleanup's) absolute
        deadline, a time.monotonic() value, and a request_timeout of
        STEP_SECONDS, the earlier of which applies, and a cancel_token of its
        own, token if given."""
        self.budget()
        return {
            "deadline": self.deadline,
            "request_timeout": STEP_SECONDS,
            "cancel_token": (
                token if token is not None else files_sdk.CancellationToken()
            ),
        }

    def names(self, options, **given):
        """The names a bound call uses (CALL_NAMES), with given's."""
        names = {
            "client": self.client,
            "options": options,
            "owned": self.owned,
            "listed": self.listed,
            "local_file": None,
            "local_directory": None,
            "stream": None,
            "progress": None,
        }
        names.update(given)
        return names

    def pause(self, seconds, pointer):
        left = self.deadline - time.monotonic()
        self.check(
            seconds < left,
            f"waiting {seconds} s ends before the deadline",
            pointer,
            round(left, 3),
        )
        time.sleep(seconds)

    def observe(self, label, function, recorder=None):
        """Calls function, and returns what it returned, what it raised (or
        None) and the responses its requests got through recorder (the case
        client's by default), all kept as evidence. It waits, at most
        SETTLE_SECONDS, for every adapter send started during the call to
        return, and fails the step otherwise, so that no response of the call
        can fall in a later call's window: a narrow observation of the
        adapter, not of the SDK's work, which only Client.close() settles."""
        recorder = recorder or self.recorder
        mark = recorder.mark()
        result = error = None
        try:
            result = function()
        except Exception as raised:
            error = raised
        in_flight, returned = recorder.settle(SETTLE_SECONDS)
        responses = recorder.since(mark)
        self.current["calls"].append(
            {
                "call": label,
                "raised": describe(error),
                "adapter_sends_in_progress_on_return": in_flight,
                "responses": [response.evidence() for response in responses],
            }
        )
        self.check(
            returned,
            f"{label}: every adapter send it started had returned",
            self.pointer,
            in_flight,
        )
        return result, error, responses

    def close(self, client, session, label):
        """Closes client, whose close() returns once its operations have
        settled (its public lifecycle barrier), then its own session, which
        the client never closes. Returns, rather than raises, what either
        raised, so that neither replaces an earlier failure."""
        failures = []
        for what, closer in (
            (f"{label}.close()", client.close),
            (f"{label}'s session.close()", session.close),
        ):
            try:
                closer()
            except Exception as error:
                failure = Failure(
                    f"{self.id}: {what} raised {describe(error)}"
                )
                failure.__cause__ = error
                failures.append(failure)
        return failures

    def one(self, label, responses):
        """The one API response a call or page received."""
        api = [response for response in responses if response.api]
        self.check(
            len(api) == 1,
            f"{label}: one API response, to one request",
            self.pointer,
            [
                (response.method, response.path, response.status)
                for response in api
            ],
        )
        return api[0]

    def answered(self, label, responses, pointer):
        failed = [
            (response.method, response.path, response.status)
            for response in responses
            if response.api and not 200 <= response.status < 300
        ]
        self.check(
            not failed,
            f"{label}: every API response answered 2xx",
            pointer,
            failed,
        )

    def returned(self, error, label):
        self.check(
            error is None, f"{label} returns", self.pointer, describe(error)
        )

    def names_namespace(self, raw):
        """Whether an operation step's path is the owned folder."""
        return raw.get("parameters", {}).get("path") == {
            "fixture": self.namespace_fixture
        }

    def operation(self, binding, raw):
        expect = raw["expect"]
        pointer = f"{binding.pointer}/expect"
        self.known(expect, EXPECT_KEYS, pointer)
        if "error" in expect:
            self.error_lookup(binding, raw)
            return
        retries = sorted(set(expect) & {"attempts", "interval_seconds"})
        self.check(
            not retries,
            "retries only a lookup that expects an error",
            pointer,
            retries,
        )
        options = self.options()
        names = self.names(options)
        if "listing" in expect:
            self.pages(binding, raw, names)
            return
        entry = expect.get("entry") or {}
        creates = (
            self.names_namespace(raw)
            and expect["status"] == 201
            and entry.get("fixture") == self.namespace_fixture
        )
        if creates:
            self.ownership.update(
                state="create sent, not proved", create=self.identity
            )
        result, error, responses = self.observe(
            "call", lambda: binding.call(**names)
        )
        if creates:
            self.acquire(error, result, responses)
        self.returned(error, "the call")
        response = self.one("the call", responses)
        self.check(
            response.status == expect["status"],
            "the status of its API response",
            f"{pointer}/status",
            response.status,
        )
        if "entry" in expect:
            self.entry(binding, raw, result, response)

    def acquire(self, error, entry, responses):
        """Owns the case's folder only on its create's own proof: the call
        returned, its one API response was 201, and both that response's raw
        JSON and the entry the SDK made of it are a directory (the owned
        fixture's type) at the folder's exact path. Anything else leaves the
        folder unowned, whether or not a folder is there."""
        kind = self.fixtures[self.namespace_fixture]["type"]
        api = [response for response in responses if response.api]
        body = api[0].json if len(api) == 1 and api[0].has_json else None
        sent: dict[str, Any] = body if isinstance(body, dict) else {}
        native = {
            "type": getattr(entry, "type", None),
            "path": getattr(entry, "path", None),
        }
        proved = (
            error is None
            and len(api) == 1
            and api[0].status == 201
            and same(sent.get("type"), kind, False)
            and same(sent.get("path"), self.namespace, False)
            and same(native["type"], kind, False)
            and same(native["path"], self.namespace, False)
        )
        self.ownership["proof"] = {
            "raised": describe(error),
            "remote_outcome_unknown": getattr(
                error, "remote_outcome_unknown", None
            ),
            "responses": [
                (response.method, response.path, response.status)
                for response in api
            ],
            "raw": {"type": sent.get("type"), "path": sent.get("path")},
            "native": native,
        }
        self.ownership["state"] = (
            "acquired" if proved else "create sent, not proved"
        )
        self.acquired = proved

    def error_lookup(self, binding, raw):
        """Calls until the error expected answers: at most attempts times,
        interval_seconds apart, or once without attempts. The call's one API
        response must be the error's."""
        expect = raw["expect"]
        pointer = f"{binding.pointer}/expect"
        self.check(
            binding.error is not None,
            "a native error is bound to the error expected",
            f"{pointer}/error",
        )
        self.check(
            "entry" not in expect and "listing" not in expect,
            "expects an error and no result",
            pointer,
            sorted(expect),
        )
        attempts = expect.get("attempts", 1)
        interval = expect.get("interval_seconds", 0)
        for attempt in range(1, attempts + 1):
            options = self.options()
            names = self.names(options)
            label = f"lookup {attempt}"
            result, error, responses = self.observe(
                label, lambda: binding.call(**names)
            )
            if error is None:
                # Still there: look again, interval_seconds later.
                self.check(
                    attempt < attempts,
                    f"raises {binding.error.__name__} within {attempts} calls",
                    (
                        f"{pointer}/attempts"
                        if "attempts" in expect
                        else f"{pointer}/error"
                    ),
                    f"{label} returned {type(result).__name__}",
                )
                self.answered(label, responses, pointer)
                self.pause(interval, f"{pointer}/interval_seconds")
                continue
            self.lookup_error(
                binding, expect, error, responses, label, pointer
            )
            self.current["details"]["attempts"] = attempt
            if self.acquired and self.names_namespace(raw):
                # Its own lookup confirmed the case's folder absent: the case
                # owns nothing now.
                self.acquired = False
                self.ownership.update(state="released", released=self.identity)
            return

    def lookup_error(self, binding, expect, error, responses, label, pointer):
        self.check(
            type(error) is binding.error,
            f"{label} raises exactly files_sdk.error.{binding.error.__name__}",
            f"{pointer}/error",
            describe(error),
        )
        response = self.one(label, responses)
        self.check(
            response.status == expect["status"],
            f"{label}: the status of its API response",
            f"{pointer}/status",
            response.status,
        )
        body = response.json if response.has_json else None
        self.check(
            isinstance(body, dict) and body.get("type") == expect["error"],
            f"{label}: the raw JSON type of its API response",
            f"{pointer}/error",
            body,
        )
        status = getattr(error, "http_status", None)
        self.check(
            status == response.status,
            f"{label}: error.http_status, that response's status",
            f"{pointer}/status",
            status,
        )
        error_type = getattr(error, "error_type", None)
        self.check(
            error_type == expect["error"],
            f"{label}: error.error_type",
            f"{pointer}/error",
            error_type,
        )

    def entry(self, binding, raw, entry, response):
        """The entry a call returned, both its raw JSON and the entry the SDK
        made of it: the fixture's type, path and size, the type or paths
        expected, and each field's matchers."""
        expected = raw["expect"]["entry"]
        pointer = f"{binding.pointer}/expect/entry"
        self.known(expected, ENTRY_KEYS, pointer)
        body = response.json if response.has_json else None
        self.check(
            isinstance(body, dict),
            "its API response's raw JSON is an object, the entry",
            pointer,
            body,
        )
        sent: dict[str, Any] = body if isinstance(body, dict) else {}
        if "fixture" in expected:
            name = expected["fixture"]
            fixture = self.fixtures[name]
            at_fixture = f"/scenarios/{self.index}/fixtures/{escape(name)}"
            self.field(
                entry, sent, "type", fixture["type"], f"{at_fixture}/type"
            )
            self.field(
                entry, sent, "path", self.owned[name], f"{at_fixture}/path"
            )
            if fixture["type"] == "directory":
                self.field(entry, sent, "size", None, f"{at_fixture}/type")
            else:
                number = fixture["recipe"]
                length = self.document["recipes"][str(number)]["length"]
                self.field(
                    entry, sent, "size", length, f"/recipes/{number}/length"
                )
        if "type" in expected:
            self.field(
                entry, sent, "type", expected["type"], f"{pointer}/type"
            )
        if "path_one_of" in expected:
            path = sent.get("path")
            self.check(
                any(
                    same(path, option, False)
                    for option in expected["path_one_of"]
                ),
                "the raw JSON path is one of the paths expected",
                f"{pointer}/path_one_of",
                path,
            )
            decoded = getattr(entry, "path", None)
            self.check(
                same(decoded, path, False),
                "the entry's path is the raw JSON's",
                f"{pointer}/path_one_of",
                decoded,
            )
        for name, matcher in expected.get("fields", {}).items():
            at_field = f"{pointer}/fields/{escape(name)}"
            self.known(matcher, MATCHERS, at_field)
            as_instant = name in binding.instants
            how = " as an instant" if as_instant else ""
            value, decoded = sent.get(name), getattr(entry, name, None)
            for kind, given in matcher.items():
                self.check(
                    matches(kind, value, given, as_instant),
                    f"the raw JSON {name} matches {kind}{how}",
                    at_field,
                    value if name in sent else "(absent)",
                )
                self.check(
                    matches(kind, decoded, given, as_instant),
                    f"the entry's {name} matches {kind}{how}",
                    at_field,
                    decoded,
                )

    def field(self, entry, sent, name, expected, pointer):
        """One field that the raw JSON and the entry the SDK made of it must
        both hold as expected: an integer only as a JSON integer, and None as
        null or absent."""
        value = sent.get(name)
        self.check(
            same(value, expected, False),
            f"the raw JSON {name}",
            pointer,
            value if name in sent else "(absent)",
        )
        decoded = getattr(entry, name, None)
        self.check(
            same(decoded, expected, False),
            f"the entry's {name}",
            pointer,
            decoded,
        )

    def pages(self, binding, raw, names):
        """Reads a listing a page at a time: each page one API response of the
        status expected, whose raw JSON items are the page's, in order, by
        type and path; at most max_pages pages (and max_records items), the
        last with no next page; with entries, each of those fixtures exactly
        once and nothing else, each kept as listed[fixture]."""
        expect = raw["expect"]
        listing = expect["listing"]
        pointer = f"{binding.pointer}/expect/listing"
        self.known(listing, LISTING_KEYS, pointer)
        per_page = raw.get("parameters", {}).get("per_page")
        at_per_page = f"{binding.pointer}/parameters/per_page"
        self.check(
            type(per_page) is int and per_page > 0,
            "per_page bounds every page",
            at_per_page,
            per_page,
        )
        max_pages = listing["max_pages"]
        pager: list[Any] = []

        def first():
            pager.append(binding.call(**names))
            return list(pager[0])

        def following():
            pager[0].load_next_page()
            return list(pager[0])

        found: list[Any] = []
        fetch = first
        number = 0
        while True:
            number += 1
            label = f"page {number}"
            items, error, responses = self.observe(label, fetch)
            self.returned(error, label)
            response = self.one(label, responses)
            self.check(
                response.status == expect["status"],
                f"{label}: the status of its API response",
                f"{binding.pointer}/expect/status",
                response.status,
            )
            body = response.json if response.has_json else None
            self.check(
                isinstance(body, list),
                f"{label}: its API response's raw JSON is a list",
                pointer,
                body,
            )
            sent = [
                (
                    (item.get("type"), item.get("path"))
                    if isinstance(item, dict)
                    else item
                )
                for item in (body if isinstance(body, list) else [])
            ]
            read = [
                (getattr(item, "type", None), getattr(item, "path", None))
                for item in items or []
            ]
            self.check(
                len(read) <= per_page,
                f"{label}: at most per_page items",
                at_per_page,
                len(read),
            )
            self.check(
                sent == read,
                f"{label}: its items are its raw JSON's, in order, by type and path",
                pointer,
                {"raw": sent, "items": read},
            )
            found += list(zip(items or [], read))
            if not pager[0].has_next_page:
                break
            self.check(
                number < max_pages,
                "at most max_pages pages, the last with no next page",
                f"{pointer}/max_pages",
                number,
            )
            fetch = following
        self.check(
            number <= max_pages,
            "at most max_pages pages",
            f"{pointer}/max_pages",
            number,
        )
        self.current["details"]["pages"] = number
        self.current["details"]["listed"] = [path for _, (_, path) in found]
        if "max_records" in listing:
            self.check(
                len(found) <= listing["max_records"],
                "at most max_records items in all",
                f"{pointer}/max_records",
                len(found),
            )
        if "entries" in listing:
            wanted = collections.Counter(
                (self.fixtures[name]["type"], self.owned[name])
                for name in listing["entries"]
            )
            got = collections.Counter(pair for _, pair in found)
            self.check(
                got == wanted,
                "each fixture of entries exactly once, and nothing else",
                f"{pointer}/entries",
                [list(pair) for pair in got.elements()],
            )
            for name in listing["entries"]:
                pair = (self.fixtures[name]["type"], self.owned[name])
                self.listed[name] = next(
                    item for item, listed in found if listed == pair
                )
                self.listed_by[name] = self.identity

    def intent(self, binding, raw):
        intent = raw["intent"]
        self.check(
            intent in INTENT_DETAILS,
            "an intent this module runs",
            binding.pointer,
            intent,
        )
        self.known(
            set(raw) - {"intent", "fixture", "expect", "backend"},
            INTENT_DETAILS[intent],
            binding.pointer,
        )
        self.known(
            raw["expect"],
            INTENT_EXPECT_KEYS[intent],
            f"{binding.pointer}/expect",
        )
        getattr(self, "intent_" + intent.replace("-", "_"))(binding, raw)

    def helper_responses(
        self, label, responses, roots, pointer, existing=None
    ):
        """Checks every API response a helper call got, by the public meaning
        of its answer. A 2xx answer's raw JSON may name only paths that are one
        of roots or inside one. Any other answer must be an error the
        definition itself expects from that same operation for one of its
        fixtures (its status and raw JSON type), for a path in its URL that is
        one of roots or inside one: an absence a lookup answers, or an
        existence a create (a POST) answers, which counts only for a folder in
        existing, what a listing found there after the call. Anything else
        fails the step; every response stays in the call's evidence."""
        for response in responses:
            if not response.api:
                continue
            what = f"{label}: {response.method} {response.path} answered {response.status}"
            body = response.json if response.has_json else None
            if 200 <= response.status < 300:
                outside = [
                    path
                    for path in paths_named(body)
                    if not within(path, roots)
                ]
                self.check(
                    not outside,
                    f"{what}, its raw JSON naming only the step's paths",
                    pointer,
                    outside,
                )
                continue
            route, target = route_of(response, self.named)
            kind = body.get("type") if isinstance(body, dict) else None
            expected = (response.status, kind) in self.errors.get(
                route or "", set()
            )
            creates = route is not None and route.startswith("POST ")
            known = (
                expected
                and within(target, roots)
                and (
                    not creates
                    or (existing is not None and target in existing)
                )
            )
            self.check(
                known,
                f"{what}, an error the definition expects from that operation at one of the step's paths"
                + (
                    ", for a folder a listing found there after it"
                    if creates
                    else ""
                ),
                pointer,
                {"route": route, "path": target, "json": body},
            )

    def intent_upload(self, binding, raw):
        """Uploads the fixture's recipe bytes from the source the step names:
        a local file, a seekable stream, or a forward-only stream giving at
        most max_read bytes a read. An upload the step cancels runs on a client
        of its own (cancelled_upload)."""
        pointer = binding.pointer
        expect = raw["expect"]
        name = raw["fixture"]
        number = self.fixtures[name]["recipe"]
        data = self.recipe(number)
        path = self.owned[name]
        source = raw["source"]
        cancel = raw.get("cancel")
        self.check(
            source in UPLOAD_SOURCES,
            "an upload source this module makes",
            f"{pointer}/source",
            source,
        )
        self.check(
            cancel is None or cancel in CANCELS,
            "a cancellation this module makes",
            f"{pointer}/cancel",
            cancel,
        )
        if cancel is None:
            self.check(
                expect.get("completed") is True,
                "expects completed true",
                f"{pointer}/expect/completed",
                expect.get("completed"),
            )
        else:
            self.check(
                expect == {"cancelled": True},
                "expects only cancelled true",
                f"{pointer}/expect",
                expect,
            )
        updates: list[Any] = []
        given: dict[str, Any] = {"progress": updates.append}
        stream: Any = None
        if source == "local-file":
            local_file = (
                self.local_path(f"upload-{binding.number}") / "source.bin"
            )
            local_file.write_bytes(data)
            given["local_file"] = str(local_file)
        elif source == "seekable-stream":
            stream = given["stream"] = io.BytesIO(data)
        else:
            stream = given["stream"] = ForwardOnlyStream(
                data, raw.get("max_read")
            )
        if cancel is not None:
            self.cancelled_upload(binding, path, given, updates)
            return
        options = self.options()
        result, error, responses = self.observe(
            "upload", lambda: binding.call(**self.names(options, **given))
        )
        details = self.current["details"]
        details["progress_updates"] = len(updates)
        if updates:
            details["last_progress"] = dataclasses.asdict(updates[-1])
        if isinstance(stream, ForwardOnlyStream):
            details["stream"] = {
                "reads": stream.reads,
                "largest_read": stream.largest_read,
                "bytes_read": stream.consumed,
            }
        self.returned(error, "upload")
        self.check(
            isinstance(result, files_sdk.File)
            and getattr(result, "path", None) == path,
            "returns the fixture's File",
            f"{pointer}/expect/completed",
            getattr(result, "path", type(result).__name__),
        )
        presented = [
            (response.method, response.path)
            for response in responses
            if response.api
            and 200 <= response.status < 300
            and presents_file(response, path)
        ]
        self.check(
            bool(presented),
            "an API response presented the fixture as a file, by its raw JSON type and path",
            f"{pointer}/expect/completed",
            [
                (response.method, response.path, response.status)
                for response in responses
                if response.api
            ],
        )
        self.helper_responses(
            "upload", responses, [path], f"{pointer}/expect/completed"
        )
        if stream is not None:
            read = (
                stream.tell()
                if isinstance(stream, io.BytesIO)
                else stream.consumed
            )
            self.check(
                read == len(data),
                "the stream was read to the end of the recipe's bytes, and no further",
                f"/recipes/{number}/length",
                read,
            )
            stream.close()
        if (
            isinstance(stream, ForwardOnlyStream)
            and raw.get("max_read") is not None
        ):
            self.check(
                stream.largest_read <= raw["max_read"],
                "the stream gave at most max_read bytes a read",
                f"{pointer}/max_read",
                stream.largest_read,
            )
        for key, value in expect.get("progress_final", {}).items():
            at_key = f"{pointer}/expect/progress_final/{escape(key)}"
            self.check(
                key in PROGRESS_FIELDS and value == "recipe-length",
                "a final progress this module reads",
                at_key,
                value,
            )
            field = PROGRESS_FIELDS[key]
            last = getattr(updates[-1], field) if updates else None
            self.check(
                last == len(data),
                f"the last UploadProgress's {field} is the recipe's length",
                at_key,
                last,
            )
        if "min_parts" in expect:
            last = updates[-1].parts_committed if updates else None
            self.check(
                last is not None and last >= expect["min_parts"],
                "the last UploadProgress's parts_committed is at least min_parts",
                f"{pointer}/expect/min_parts",
                last,
            )

    def cancelled_upload(self, binding, path, given, updates):
        """The upload a step cancels after its first acknowledged part, on a
        client and session of the step's own; the case's client, and the Files
        its listings returned, are untouched. That session's response hook
        cancels the step's token, synchronously, on the first successful
        upload part response (a PUT): acknowledgement 1, the wire-response
        acknowledgement boundary, before the SDK has that response and so
        before any progress or committed state it reports for the part. The
        hook reads only the response's status and its request's method, URL
        and length; the body stays untouched. Then that client's close(), its
        settlement barrier, and its session's close() end it, before the
        step's checks."""
        pointer = binding.pointer
        token = files_sdk.CancellationToken()
        acknowledgements: list[dict[str, Any]] = []
        lock = threading.Lock()

        def hook(response, *args, **kwargs):
            request = response.request
            if (
                request.method != "PUT"
                or not 200 <= response.status_code < 300
            ):
                return
            with lock:
                acknowledgement = {
                    "index": len(acknowledgements) + 1,
                    "path": urllib.parse.urlsplit(request.url or "").path,
                    "status": response.status_code,
                    "part_bytes": request.headers.get("Content-Length"),
                    "token_cancelled_before": token.cancelled,
                    "progress_updates_before": len(updates),
                    "parts_committed_before": max(
                        (update.parts_committed for update in list(updates)),
                        default=0,
                    ),
                }
                acknowledgements.append(acknowledgement)
                if acknowledgement["index"] == 1:
                    token.cancel()
                    acknowledgement["token_cancelled_after"] = token.cancelled

        options = self.options(token)
        client, session, recorder = connect(hook)
        names = self.names(options, client=client, **given)
        result = error = None
        responses: list[Response] = []
        failure = None
        try:
            result, error, responses = self.observe(
                "upload", lambda: binding.call(**names), recorder
            )
        except Exception as raised:
            failure = raised
        closing = self.close(client, session, "the cancelled upload's client")
        details = self.current["details"]
        details["closing"] = [describe(item) for item in closing]
        if failure is not None:
            raise combined([failure, *closing])
        late = recorder.since(len(responses))
        if late:
            self.current["calls"].append(
                {
                    "call": "upload, once its client had closed",
                    "responses": [response.evidence() for response in late],
                }
            )
        responses = [*responses, *late]
        details["acknowledgements"] = acknowledgements
        details["token_cancelled"] = token.cancelled
        details["progress_updates"] = len(updates)
        if updates:
            details["last_progress"] = dataclasses.asdict(updates[-1])
        first = acknowledgements[0] if acknowledgements else {}
        self.check(
            type(error) is files_sdk.error.OperationCancelledError,
            "raises exactly files_sdk.error.OperationCancelledError, not its subclass ClientClosedError",
            f"{pointer}/expect/cancelled",
            describe(error) or f"returned {type(result).__name__}",
        )
        self.check(
            token.cancelled,
            "the step's own cancel_token is cancelled",
            f"{pointer}/expect/cancelled",
            token.cancelled,
        )
        self.check(
            first.get("index") == 1
            and first.get("token_cancelled_before") is False
            and first.get("token_cancelled_after") is True,
            "the response hook cancelled the token at acknowledgement 1, the first successful upload part response, the token not cancelled before it",
            f"{pointer}/cancel",
            acknowledgements[:2],
        )
        self.check(
            first.get("parts_committed_before") == 0,
            "no UploadProgress had reported a committed part at acknowledgement 1",
            f"{pointer}/cancel",
            first.get("parts_committed_before"),
        )
        presented = [
            (response.method, response.path)
            for response in responses
            if response.api
            and 200 <= response.status < 300
            and presents_file(response, path)
        ]
        self.check(
            not presented,
            "no API response presented the fixture as a file: it published nothing",
            f"{pointer}/expect/cancelled",
            presented,
        )
        self.helper_responses(
            "upload", responses, [path], f"{pointer}/expect/cancelled"
        )
        self.check(
            not closing,
            "its own client closed (close() returns once its operations have settled), then its session",
            f"{pointer}/expect/cancelled",
            details["closing"],
        )

    def intent_download(self, binding, raw):
        """Downloads the fixture by its path, with options of the step's own,
        or from the File a listing returned for it, whose download_file takes
        only its path, to a new local file, which must hold its recipe's
        bytes."""
        pointer = binding.pointer
        name = raw["fixture"]
        number = self.fixtures[name]["recipe"]
        path = self.owned[name]
        self.check(
            raw["expect"].get("bytes") == "recipe",
            "expects the recipe's bytes",
            f"{pointer}/expect/bytes",
            raw["expect"].get("bytes"),
        )
        source = raw.get("source")
        self.check(
            source in (None, "listed-entry"),
            "a download source this module runs",
            f"{pointer}/source",
            source,
        )
        local_file = (
            self.local_path(f"download-{binding.number}") / "download.bin"
        )
        if source == "listed-entry":
            listed = self.listed.get(name)
            self.check(
                listed is not None and getattr(listed, "path", None) == path,
                "a listing before it returned the fixture's own entry",
                f"{pointer}/source",
                getattr(listed, "path", None),
            )
            # download_file takes no options: it is an operation of its own,
            # with the limits of the client settings the File keeps
            # (OPEN_TIMEOUT and READ_TIMEOUT, no request_timeout), not the
            # deadline or token of the listing call that returned it. The case
            # only checks first that its own deadline has not passed.
            self.budget()
            options = None
            self.current["details"]["options"] = (
                f"none: a new operation with the client settings the File keeps "
                f"(open_timeout {OPEN_TIMEOUT}, read_timeout {READ_TIMEOUT}, no request_timeout), "
                f"not the deadline or token of the listing of {self.listed_by.get(name)}"
            )
        else:
            options = self.options()
        result, error, responses = self.observe(
            "download",
            lambda: binding.call(
                **self.names(options, local_file=str(local_file))
            ),
        )
        self.returned(error, "download")
        self.check(
            getattr(result, "path", None) == path,
            "returns the fixture's File",
            f"{pointer}/expect/bytes",
            getattr(result, "path", None),
        )
        self.helper_responses(
            "download", responses, [path], f"{pointer}/expect/bytes"
        )
        got = local_file.read_bytes() if local_file.is_file() else None
        self.check(
            got == self.recipe(number),
            "the local file holds the recipe's bytes",
            f"/recipes/{number}",
            (
                None
                if got is None
                else {
                    "bytes": len(got),
                    "sha256": hashlib.sha256(got).hexdigest(),
                }
            ),
        )

    def intent_copy(self, binding, raw):
        self.migrate(binding, raw)

    def intent_move(self, binding, raw):
        self.migrate(binding, raw)

    def migrate(self, binding, raw):
        """A copy or move, waited for until its migration (if any) completes."""
        pointer = f"{binding.pointer}/expect/completed"
        self.check(
            raw["expect"].get("completed") is True,
            "expects completed true",
            pointer,
            raw["expect"].get("completed"),
        )
        roots = [self.owned[raw["from"]], self.owned[raw["fixture"]]]
        options = self.options()
        result, error, responses = self.observe(
            raw["intent"], lambda: binding.call(**self.names(options))
        )
        self.returned(error, raw["intent"])
        status = None if result is None else getattr(result, "status", None)
        self.current["details"]["migration"] = (
            "finished at once" if result is None else status
        )
        self.check(
            result is None or status == "completed",
            "returns the completed FileMigration, or None if it finished at once",
            pointer,
            status,
        )
        self.helper_responses(raw["intent"], responses, roots, pointer)

    def intent_upload_directory(self, binding, raw):
        """Uploads a local tree of the step's tree fixtures into the fixture's
        folder, then lists that folder's folders to see what is there and which
        it left empty."""
        pointer = binding.pointer
        expect = raw["expect"]
        folder = raw["fixture"]
        root = self.owned[folder]
        local_directory = (
            self.local_path(f"upload-directory-{binding.number}") / "tree"
        )
        local_directory.mkdir()
        for name in raw["tree"]:
            target = local_directory / self.inside(
                folder, name, f"{pointer}/tree"
            )
            if self.fixtures[name]["type"] == "directory":
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(self.recipe(self.fixtures[name]["recipe"]))
        options = self.options()
        result, error, responses = self.observe(
            "upload_directory",
            lambda: binding.call(
                **self.names(options, local_directory=str(local_directory))
            ),
        )
        self.returned(error, "upload_directory")
        files = self.transfer(result, f"{pointer}/expect/completed")
        remote = sorted(outcome.remote_path for outcome in files)
        self.check(
            remote == sorted(self.owned[name] for name in expect["completed"]),
            "its completed file outcomes, by remote_path, are exactly the completed fixtures'",
            f"{pointer}/expect/completed",
            remote,
        )
        self.check(
            len(files) == expect["files"],
            "the number of its completed file outcomes",
            f"{pointer}/expect/files",
            len(files),
        )
        total = sum(outcome.bytes for outcome in files)
        self.check(
            total == expect["bytes"],
            "the sum of its completed file outcomes' bytes",
            f"{pointer}/expect/bytes",
            total,
        )
        empty, existing = self.remote_tree(binding, root)
        self.helper_responses(
            "upload_directory",
            responses,
            [root],
            f"{pointer}/expect/completed",
            existing,
        )
        self.check(
            len(empty) == expect["empty_folders"],
            "the folders under the fixture's folder that a listing finds empty after the upload",
            f"{pointer}/expect/empty_folders",
            empty,
        )

    def intent_download_directory(self, binding, raw):
        """Downloads the fixture's folder to a new local folder, then looks
        there for the bytes and the empty folders expected."""
        pointer = binding.pointer
        expect = raw["expect"]
        folder = raw["fixture"]
        local_directory = (
            self.local_path(f"download-directory-{binding.number}") / "tree"
        )
        options = self.options()
        result, error, responses = self.observe(
            "download_directory",
            lambda: binding.call(
                **self.names(options, local_directory=str(local_directory))
            ),
        )
        self.returned(error, "download_directory")
        files = self.transfer(result, f"{pointer}/expect/files")
        self.check(
            len(files) == expect["files"],
            "the number of its completed file outcomes",
            f"{pointer}/expect/files",
            len(files),
        )
        total = sum(outcome.bytes for outcome in files)
        self.check(
            total == expect["bytes"],
            "the sum of its completed file outcomes' bytes",
            f"{pointer}/expect/bytes",
            total,
        )
        self.helper_responses(
            "download_directory",
            responses,
            [self.owned[folder]],
            f"{pointer}/expect/files",
        )
        for name in expect["bytes_match"]:
            target = local_directory / self.inside(
                folder, name, f"{pointer}/expect/bytes_match"
            )
            got = target.read_bytes() if target.is_file() else None
            self.check(
                got == self.recipe(self.fixtures[name]["recipe"]),
                f"the local file of {name} holds its recipe's bytes",
                f"{pointer}/expect/bytes_match",
                (
                    None
                    if got is None
                    else {
                        "bytes": len(got),
                        "sha256": hashlib.sha256(got).hexdigest(),
                    }
                ),
            )
        empty = sorted(
            Path(directory).relative_to(local_directory).as_posix()
            for directory, folders, entries in os.walk(local_directory)
            if directory != str(local_directory)
            and not folders
            and not entries
        )
        self.check(
            len(empty) == expect["empty_folders"],
            "the folders under the new local folder that hold nothing after the download",
            f"{pointer}/expect/empty_folders",
            empty,
        )

    def transfer(self, result, pointer):
        """A TransferResult's completed file outcomes, once none failed or was
        skipped; every outcome is kept as evidence."""
        self.check(
            isinstance(result, files_sdk.TransferResult),
            "returns a TransferResult",
            pointer,
            type(result).__name__,
        )
        self.current["details"]["outcomes"] = [
            {
                "kind": outcome.kind,
                "remote_path": outcome.remote_path,
                "local_path": outcome.local_path,
                "status": outcome.status,
                "bytes": outcome.bytes,
                "reason": outcome.reason,
                "error": describe(outcome.error),
            }
            for outcome in result.outcomes
        ]
        problems = [
            (outcome.remote_path, outcome.status)
            for outcome in result.failed + result.skipped
        ]
        self.check(
            not problems, "nothing failed or was skipped", pointer, problems
        )
        return [
            outcome for outcome in result.completed if outcome.kind == "file"
        ]

    def inside(self, folder, name, pointer):
        """A fixture's path relative to a folder fixture it is inside."""
        root = self.fixtures[folder]["path"]
        prefix = root + "/" if root else ""
        path = self.fixtures[name]["path"]
        self.check(
            path.startswith(prefix) and len(path) > len(prefix),
            f"{name} is inside {folder}",
            pointer,
            path,
        )
        return path[len(prefix) :]

    def remote_tree(self, binding, root):
        """The folders under root that a listing of each, with the bound folder
        listing, finds empty, and every folder it lists, root included; at
        most OBSERVED_FOLDERS are listed, each listing's answers checked as a
        helper call's."""
        self.check(
            binding.observe is not None,
            "a folder listing is bound to the step",
            binding.pointer,
        )
        empty: list[str] = []
        folders = [root]
        for count, folder in enumerate(folders, 1):
            self.check(
                count <= OBSERVED_FOLDERS,
                f"at most {OBSERVED_FOLDERS} folders to list",
                binding.pointer,
                count,
            )
            options = self.options()
            label = f"listing {folder}"
            entries, error, responses = self.observe(
                label,
                lambda: list(
                    binding.observe(
                        client=self.client, options=options, folder=folder
                    ).auto_paging_iter()
                ),
            )
            self.returned(error, label)
            self.helper_responses(label, responses, [root], binding.pointer)
            if not entries and folder != root:
                empty.append(folder)
            folders += [
                entry.path
                for entry in entries or []
                if entry.type == "directory"
            ]
        return empty, set(folders)

    def local_path(self, name):
        """A new folder in the case's own local folder."""
        folder = self.local / name
        folder.mkdir()
        return folder

    def recipe(self, number):
        return recipe_bytes(self.document, number)

    def cleanup(self, record):
        """After a failure, while the case owns its folder: deletes that folder
        recursively, with a client, options, token and deadline of its own,
        then confirms it absent with the case's own lookup (step confirm). A
        delete that raises counts as the folder being gone already only as
        exactly that lookup's error: its native class, 404 and raw JSON type.
        Deletes nothing else, and nothing at all when the case does not own
        the folder. Returns what closing the cleanup's client and session
        raised; raises what the cleanup itself failed on, with those after
        it."""
        record["ownership"] = dict(self.ownership)
        if not self.acquired:
            record["outcome"] = {
                "no create sent": "nothing deleted: the case sent no create for its owned folder",
                "released": "nothing deleted: the case's own steps deleted its owned folder and confirmed it absent",
            }.get(
                self.ownership["state"],
                "nothing deleted: a create of the owned folder was sent, but its answer did not prove "
                "the folder the case's (see ownership), so whether a folder is there is unknown",
            )
            return []
        confirm = self.case.steps[self.case.confirm - 1]
        confirm_raw = at(self.document, confirm.pointer)
        client, session, recorder = connect()
        self.client, self.recorder, self.current = client, recorder, record
        self.identity, self.pointer = f"{self.id} cleanup", "/cleanup"
        self.deadline = time.monotonic() + CLEANUP_SECONDS
        failure = None
        try:
            names = self.names(self.options())
            _, error, responses = self.observe(
                "recursive delete", lambda: self.case.cleanup(**names)
            )
            if error is None:
                response = self.one("recursive delete", responses)
                self.check(
                    200 <= response.status < 300,
                    "recursive delete: its API response answered 2xx",
                    self.pointer,
                    response.status,
                )
            else:
                # Gone already only as exactly the confirming lookup's error.
                self.lookup_error(
                    confirm,
                    confirm_raw["expect"],
                    error,
                    responses,
                    "recursive delete",
                    f"{confirm.pointer}/expect",
                )
                record["details"]["already_gone"] = True
            self.pointer = confirm.pointer
            self.error_lookup(confirm, confirm_raw)
            record["outcome"] = "deleted recursively and confirmed absent"
        except Exception as error:
            failure = error
        closing = self.close(client, session, "the cleanup's client")
        if failure is not None:
            raise combined([failure, *closing])
        return closing

    def totals(self):
        outcomes = collections.Counter(
            record["outcome"] for record in self.records
        )
        return {
            "outcome": self.evidence["outcome"],
            "positions": len(self.records),
            "passed": outcomes["passed"],
            "failed": outcomes["failed"],
            "omitted_site_only": outcomes["omitted: site-only"],
            "not_reached": outcomes["not reached"],
            "ownership": self.ownership["state"],
            "seconds": self.evidence["seconds"],
        }

    def write(self):
        self.out.mkdir(parents=True, exist_ok=True)
        text = json.dumps(
            self.evidence, indent=1, ensure_ascii=False, default=repr
        )
        (self.out / f"{self.id}.json").write_text(
            text + "\n", encoding="utf-8"
        )


# Each scenario's steps, by its id, as helpers/python/api_scenarios.rb bound
# them, and its cleanup. Each call is given the names client, options, owned, listed, local_file, local_directory, stream, progress;
# the comment before it says what each argument stands for and what the module
# checks of the step.
CASES = {
    "files.owned-folder-namespace": Case(
        cleanup=lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
            owned["folder"], {"recursive": True}, options
        ),
        confirm=25,
        steps=(
            # files.owned-folder-namespace step 1: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/0)
            #   "/": api.json /groups/namespace.open/0/parameters/path
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.RequestParamsRequiredError (a subclass of BadRequestError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.open/0/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.open/0/expect/status
            Binding(
                1,
                "/groups/namespace.open/0",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    "/", {}, options
                ),
                error=files_sdk.error.RequestParamsRequiredError,
            ),
            # files.owned-folder-namespace step 2: GET /folders/{path} (api.json /groups/namespace.open/1)
            #   "/": api.json /groups/namespace.open/1/parameters/path
            #   {"per_page": 1000}: per_page: api.json /groups/namespace.open/1/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /groups/namespace.open/1/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /groups/namespace.open/1/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /groups/namespace.open/1/expect/listing/max_pages
            #   checks its members are not asserted (they belong to the site): api.json /groups/namespace.open/1/expect/listing
            Binding(
                2,
                "/groups/namespace.open/1",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    "/", {"per_page": 1000}, options
                ),
            ),
            # files.owned-folder-namespace step 3: GET /behaviors/folders/{path} (api.json /groups/namespace.open/2). Site-only: omitted on the simulator, never run or passed here
            #   "/": api.json /groups/namespace.open/2/parameters/path
            #   {"ancestor_behaviors": True, "per_page": 100}: ancestor_behaviors: api.json /groups/namespace.open/2/parameters/ancestor_behaviors; per_page: api.json /groups/namespace.open/2/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[Behavior]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /groups/namespace.open/2/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /groups/namespace.open/2/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /groups/namespace.open/2/expect/listing/max_pages
            #   checks at most max_records items in all: api.json /groups/namespace.open/2/expect/listing/max_records
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /groups/namespace.open/2/expect/listing/entries
            Binding(
                3,
                "/groups/namespace.open/2",
                False,
                "GET /behaviors/folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.behavior.list_for(
                    "/", {"ancestor_behaviors": True, "per_page": 100}, options
                ),
            ),
            # files.owned-folder-namespace step 4: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/3)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/0/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.open/3/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.open/3/expect/status
            Binding(
                4,
                "/groups/namespace.open/3",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-folder-namespace step 5: POST /folders/{path} (api.json /groups/namespace.open/4)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/0/fixtures/folder)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /groups/namespace.open/4/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /groups/namespace.open/4/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/0/fixtures/folder/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/0/fixtures/folder/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/0/fixtures/folder/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                5,
                "/groups/namespace.open/4",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["folder"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-folder-namespace step 6: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/5). Site-only: omitted on the simulator, never run or passed here
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/0/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /groups/namespace.open/5/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/0/fixtures/folder/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/0/fixtures/folder/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/0/fixtures/folder/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            #   checks entry.permissions and the raw JSON permissions each match includes: api.json /groups/namespace.open/5/expect/entry/fields/permissions
            #   checks entry.is_locked and the raw JSON is_locked each match not: api.json /groups/namespace.open/5/expect/entry/fields/is_locked
            #   checks getattr(entry, "subfolders_locked?") and the raw JSON subfolders_locked? each match not: api.json /groups/namespace.open/5/expect/entry/fields/subfolders_locked?
            Binding(
                6,
                "/groups/namespace.open/5",
                False,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
            ),
            # files.owned-folder-namespace step 7: POST /folders/{path} (api.json /scenarios/0/steps/1)
            #   owned["alpha"]: the path of fixture alpha, "alpha" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /scenarios/0/steps/1/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/1/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/0/fixtures/alpha/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/0/fixtures/alpha/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/0/fixtures/alpha/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                7,
                "/scenarios/0/steps/1",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["alpha"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-folder-namespace step 8: POST /folders/{path} (api.json /scenarios/0/steps/2)
            #   owned["bravo"]: the path of fixture bravo, "bravo" inside the run's owned folder (api.json /scenarios/0/fixtures/bravo)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /scenarios/0/steps/2/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/2/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/0/fixtures/bravo/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/0/fixtures/bravo/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/0/fixtures/bravo/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                8,
                "/scenarios/0/steps/2",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["bravo"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-folder-namespace step 9: POST /folders/{path} (api.json /scenarios/0/steps/3)
            #   owned["charlie"]: the path of fixture charlie, "charlie" inside the run's owned folder (api.json /scenarios/0/fixtures/charlie)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /scenarios/0/steps/3/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/3/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/0/fixtures/charlie/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/0/fixtures/charlie/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/0/fixtures/charlie/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                9,
                "/scenarios/0/steps/3",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["charlie"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-folder-namespace step 10: POST /folders/{path} (api.json /scenarios/0/steps/4)
            #   owned["alpha-inner"]: the path of fixture alpha-inner, "alpha/inner" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha-inner)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /scenarios/0/steps/4/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/4/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/0/fixtures/alpha-inner/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/0/fixtures/alpha-inner/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/0/fixtures/alpha-inner/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                10,
                "/scenarios/0/steps/4",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["alpha-inner"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-folder-namespace step 11: POST /folders/{path} (api.json /scenarios/0/steps/5)
            #   owned["alpha"]: the path of fixture alpha, "alpha" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /scenarios/0/steps/5/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.DestinationExistsError (a subclass of ProcessingFailureError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/0/steps/5/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/0/steps/5/expect/status
            Binding(
                11,
                "/scenarios/0/steps/5",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["alpha"], {"mkdir_parents": False}, options
                ),
                error=files_sdk.error.DestinationExistsError,
            ),
            # files.owned-folder-namespace step 12: GET /file_actions/metadata/{path} (api.json /scenarios/0/steps/6)
            #   owned["alpha"]: the path of fixture alpha, "alpha" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/6/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/0/fixtures/alpha/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/0/fixtures/alpha/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/0/fixtures/alpha/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                12,
                "/scenarios/0/steps/6",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["alpha"], {}, options
                ),
            ),
            # files.owned-folder-namespace step 13: GET /file_actions/metadata/{path} (api.json /scenarios/0/steps/7)
            #   owned["alpha-inner"]: the path of fixture alpha-inner, "alpha/inner" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha-inner)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/7/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/0/fixtures/alpha-inner/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/0/fixtures/alpha-inner/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/0/fixtures/alpha-inner/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                13,
                "/scenarios/0/steps/7",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["alpha-inner"], {}, options
                ),
            ),
            # files.owned-folder-namespace step 14: GET /folders/{path} (api.json /scenarios/0/steps/8)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/0/fixtures/folder)
            #   {"per_page": 1}: per_page: api.json /scenarios/0/steps/8/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/0/steps/8/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/0/steps/8/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/0/steps/8/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/0/steps/8/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                14,
                "/scenarios/0/steps/8",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["folder"], {"per_page": 1}, options
                ),
            ),
            # files.owned-folder-namespace step 15: GET /folders/{path} (api.json /scenarios/0/steps/9)
            #   owned["alpha"]: the path of fixture alpha, "alpha" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha)
            #   {"per_page": 1000}: per_page: api.json /scenarios/0/steps/9/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/0/steps/9/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/0/steps/9/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/0/steps/9/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/0/steps/9/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                15,
                "/scenarios/0/steps/9",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["alpha"], {"per_page": 1000}, options
                ),
            ),
            # files.owned-folder-namespace step 16: DELETE /files/{path} (api.json /scenarios/0/steps/10)
            #   owned["alpha-inner"]: the path of fixture alpha-inner, "alpha/inner" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha-inner)
            #   {"recursive": False}: recursive: api.json /scenarios/0/steps/10/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/10/expect/status
            Binding(
                16,
                "/scenarios/0/steps/10",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["alpha-inner"], {"recursive": False}, options
                ),
            ),
            # files.owned-folder-namespace step 17: GET /file_actions/metadata/{path} (api.json /scenarios/0/steps/11)
            #   owned["alpha-inner"]: the path of fixture alpha-inner, "alpha/inner" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha-inner)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/0/steps/11/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/0/steps/11/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/0/steps/11/expect/attempts
            Binding(
                17,
                "/scenarios/0/steps/11",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["alpha-inner"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-folder-namespace step 18: DELETE /files/{path} (api.json /scenarios/0/steps/12)
            #   owned["alpha"]: the path of fixture alpha, "alpha" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha)
            #   {"recursive": False}: recursive: api.json /scenarios/0/steps/12/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/12/expect/status
            Binding(
                18,
                "/scenarios/0/steps/12",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["alpha"], {"recursive": False}, options
                ),
            ),
            # files.owned-folder-namespace step 19: GET /file_actions/metadata/{path} (api.json /scenarios/0/steps/13)
            #   owned["alpha"]: the path of fixture alpha, "alpha" inside the run's owned folder (api.json /scenarios/0/fixtures/alpha)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/0/steps/13/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/0/steps/13/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/0/steps/13/expect/attempts
            Binding(
                19,
                "/scenarios/0/steps/13",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["alpha"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-folder-namespace step 20: DELETE /files/{path} (api.json /scenarios/0/steps/14)
            #   owned["bravo"]: the path of fixture bravo, "bravo" inside the run's owned folder (api.json /scenarios/0/fixtures/bravo)
            #   {"recursive": False}: recursive: api.json /scenarios/0/steps/14/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/14/expect/status
            Binding(
                20,
                "/scenarios/0/steps/14",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["bravo"], {"recursive": False}, options
                ),
            ),
            # files.owned-folder-namespace step 21: GET /file_actions/metadata/{path} (api.json /scenarios/0/steps/15)
            #   owned["bravo"]: the path of fixture bravo, "bravo" inside the run's owned folder (api.json /scenarios/0/fixtures/bravo)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/0/steps/15/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/0/steps/15/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/0/steps/15/expect/attempts
            Binding(
                21,
                "/scenarios/0/steps/15",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["bravo"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-folder-namespace step 22: DELETE /files/{path} (api.json /scenarios/0/steps/16)
            #   owned["charlie"]: the path of fixture charlie, "charlie" inside the run's owned folder (api.json /scenarios/0/fixtures/charlie)
            #   {"recursive": False}: recursive: api.json /scenarios/0/steps/16/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/0/steps/16/expect/status
            Binding(
                22,
                "/scenarios/0/steps/16",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["charlie"], {"recursive": False}, options
                ),
            ),
            # files.owned-folder-namespace step 23: GET /file_actions/metadata/{path} (api.json /scenarios/0/steps/17)
            #   owned["charlie"]: the path of fixture charlie, "charlie" inside the run's owned folder (api.json /scenarios/0/fixtures/charlie)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/0/steps/17/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/0/steps/17/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/0/steps/17/expect/attempts
            Binding(
                23,
                "/scenarios/0/steps/17",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["charlie"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-folder-namespace step 24: DELETE /files/{path} (api.json /groups/namespace.close/0)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/0/fixtures/folder)
            #   {"recursive": False}: recursive: api.json /groups/namespace.close/0/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /groups/namespace.close/0/expect/status
            Binding(
                24,
                "/groups/namespace.close/0",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["folder"], {"recursive": False}, options
                ),
            ),
            # files.owned-folder-namespace step 25: GET /file_actions/metadata/{path} (api.json /groups/namespace.close/1)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/0/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.close/1/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.close/1/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /groups/namespace.close/1/expect/attempts
            Binding(
                25,
                "/groups/namespace.close/1",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
        ),
    ),
    "files.owned-binary-roundtrip": Case(
        cleanup=lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
            owned["folder"], {"recursive": True}, options
        ),
        confirm=24,
        steps=(
            # files.owned-binary-roundtrip step 1: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/0)
            #   "/": api.json /groups/namespace.open/0/parameters/path
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.RequestParamsRequiredError (a subclass of BadRequestError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.open/0/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.open/0/expect/status
            Binding(
                1,
                "/groups/namespace.open/0",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    "/", {}, options
                ),
                error=files_sdk.error.RequestParamsRequiredError,
            ),
            # files.owned-binary-roundtrip step 2: GET /folders/{path} (api.json /groups/namespace.open/1)
            #   "/": api.json /groups/namespace.open/1/parameters/path
            #   {"per_page": 1000}: per_page: api.json /groups/namespace.open/1/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /groups/namespace.open/1/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /groups/namespace.open/1/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /groups/namespace.open/1/expect/listing/max_pages
            #   checks its members are not asserted (they belong to the site): api.json /groups/namespace.open/1/expect/listing
            Binding(
                2,
                "/groups/namespace.open/1",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    "/", {"per_page": 1000}, options
                ),
            ),
            # files.owned-binary-roundtrip step 3: GET /behaviors/folders/{path} (api.json /groups/namespace.open/2). Site-only: omitted on the simulator, never run or passed here
            #   "/": api.json /groups/namespace.open/2/parameters/path
            #   {"ancestor_behaviors": True, "per_page": 100}: ancestor_behaviors: api.json /groups/namespace.open/2/parameters/ancestor_behaviors; per_page: api.json /groups/namespace.open/2/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[Behavior]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /groups/namespace.open/2/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /groups/namespace.open/2/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /groups/namespace.open/2/expect/listing/max_pages
            #   checks at most max_records items in all: api.json /groups/namespace.open/2/expect/listing/max_records
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /groups/namespace.open/2/expect/listing/entries
            Binding(
                3,
                "/groups/namespace.open/2",
                False,
                "GET /behaviors/folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.behavior.list_for(
                    "/", {"ancestor_behaviors": True, "per_page": 100}, options
                ),
            ),
            # files.owned-binary-roundtrip step 4: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/3)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/1/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.open/3/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.open/3/expect/status
            Binding(
                4,
                "/groups/namespace.open/3",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-binary-roundtrip step 5: POST /folders/{path} (api.json /groups/namespace.open/4)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/1/fixtures/folder)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /groups/namespace.open/4/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /groups/namespace.open/4/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/1/fixtures/folder/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/1/fixtures/folder/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/1/fixtures/folder/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                5,
                "/groups/namespace.open/4",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["folder"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-binary-roundtrip step 6: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/5). Site-only: omitted on the simulator, never run or passed here
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/1/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /groups/namespace.open/5/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/1/fixtures/folder/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/1/fixtures/folder/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/1/fixtures/folder/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            #   checks entry.permissions and the raw JSON permissions each match includes: api.json /groups/namespace.open/5/expect/entry/fields/permissions
            #   checks entry.is_locked and the raw JSON is_locked each match not: api.json /groups/namespace.open/5/expect/entry/fields/is_locked
            #   checks getattr(entry, "subfolders_locked?") and the raw JSON subfolders_locked? each match not: api.json /groups/namespace.open/5/expect/entry/fields/subfolders_locked?
            Binding(
                6,
                "/groups/namespace.open/5",
                False,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
            ),
            # files.owned-binary-roundtrip step 7: upload (intent) (api.json /scenarios/1/steps/1)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   local_file: a local file in the case's own folder holding the bytes of recipe 1 (api.json /recipes/1)
            #   owned["binary.bin"]: the path of fixture binary.bin, "binary.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/binary.bin)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   {"provided_mtime": "2026-09-24T00:00:00Z"}: provided_mtime: api.json /scenarios/1/steps/1/parameters/provided_mtime
            #   returns File
            #   checks returns the fixture's File, which an API response presented as a file (raw JSON type and path): api.json /scenarios/1/steps/1/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/1/steps/1/expect/completed
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                7,
                "/scenarios/1/steps/1",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_file(
                    local_file,
                    owned["binary.bin"],
                    options,
                    {"provided_mtime": "2026-09-24T00:00:00Z"},
                ),
            ),
            # files.owned-binary-roundtrip step 8: GET /file_actions/metadata/{path} (api.json /scenarios/1/steps/2)
            #   owned["binary.bin"]: the path of fixture binary.bin, "binary.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/binary.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/1/steps/2/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/1/fixtures/binary.bin/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/1/fixtures/binary.bin/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/1/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            #   checks entry.provided_mtime and the raw JSON provided_mtime each match one_of, compared as an instant (a value that is not one meets none): api.json /scenarios/1/steps/2/expect/entry/fields/provided_mtime
            Binding(
                8,
                "/scenarios/1/steps/2",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["binary.bin"], {}, options
                ),
                instants=("provided_mtime",),
            ),
            # files.owned-binary-roundtrip step 9: upload (intent) (api.json /scenarios/1/steps/3)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   stream: a seekable binary stream at the start of the bytes of recipe 2 (api.json /recipes/2)
            #   owned["empty.bin"]: the path of fixture empty.bin, "empty.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/empty.bin)
            #   0: size: the length of recipe 2 (api.json /recipes/2)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   {"provided_mtime": "2026-09-24T00:00:00Z"}: provided_mtime: api.json /scenarios/1/steps/3/parameters/provided_mtime
            #   returns File
            #   checks returns the fixture's File, which an API response presented as a file (raw JSON type and path): api.json /scenarios/1/steps/3/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/1/steps/3/expect/completed
            #   checks the stream was read to the end of the recipe's bytes, and no further: api.json /recipes/2/length
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                9,
                "/scenarios/1/steps/3",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_stream(
                    stream,
                    owned["empty.bin"],
                    0,
                    options,
                    {"provided_mtime": "2026-09-24T00:00:00Z"},
                ),
            ),
            # files.owned-binary-roundtrip step 10: GET /file_actions/metadata/{path} (api.json /scenarios/1/steps/4)
            #   owned["empty.bin"]: the path of fixture empty.bin, "empty.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/empty.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/1/steps/4/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/1/fixtures/empty.bin/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/1/fixtures/empty.bin/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/2/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            #   checks entry.provided_mtime and the raw JSON provided_mtime each match one_of, compared as an instant (a value that is not one meets none): api.json /scenarios/1/steps/4/expect/entry/fields/provided_mtime
            Binding(
                10,
                "/scenarios/1/steps/4",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["empty.bin"], {}, options
                ),
                instants=("provided_mtime",),
            ),
            # files.owned-binary-roundtrip step 11: upload (intent) (api.json /scenarios/1/steps/5)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   stream: a forward-only binary stream at the start of the bytes of recipe 3 (api.json /recipes/3), giving at most max_read bytes a read (api.json /scenarios/1/steps/5/max_read)
            #   owned["short-read.bin"]: the path of fixture short-read.bin, "short-read.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/short-read.bin)
            #   65537: size: the length of recipe 3 (api.json /recipes/3)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   {"provided_mtime": "2026-09-24T00:00:00Z"}: provided_mtime: api.json /scenarios/1/steps/5/parameters/provided_mtime
            #   returns File
            #   checks returns the fixture's File, which an API response presented as a file (raw JSON type and path): api.json /scenarios/1/steps/5/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/1/steps/5/expect/completed
            #   checks the stream was read to the end of the recipe's bytes, and no further: api.json /recipes/3/length
            #   checks the stream gave at most max_read bytes a read: api.json /scenarios/1/steps/5/max_read
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                11,
                "/scenarios/1/steps/5",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_stream(
                    stream,
                    owned["short-read.bin"],
                    65537,
                    options,
                    {"provided_mtime": "2026-09-24T00:00:00Z"},
                ),
            ),
            # files.owned-binary-roundtrip step 12: GET /file_actions/metadata/{path} (api.json /scenarios/1/steps/6)
            #   owned["short-read.bin"]: the path of fixture short-read.bin, "short-read.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/short-read.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/1/steps/6/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/1/fixtures/short-read.bin/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/1/fixtures/short-read.bin/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/3/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            #   checks entry.provided_mtime and the raw JSON provided_mtime each match one_of, compared as an instant (a value that is not one meets none): api.json /scenarios/1/steps/6/expect/entry/fields/provided_mtime
            Binding(
                12,
                "/scenarios/1/steps/6",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["short-read.bin"], {}, options
                ),
                instants=("provided_mtime",),
            ),
            # files.owned-binary-roundtrip step 13: GET /folders/{path} (api.json /scenarios/1/steps/7)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/1/fixtures/folder)
            #   {"per_page": 1}: per_page: api.json /scenarios/1/steps/7/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/1/steps/7/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/1/steps/7/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/1/steps/7/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/1/steps/7/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                13,
                "/scenarios/1/steps/7",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["folder"], {"per_page": 1}, options
                ),
            ),
            # files.owned-binary-roundtrip step 14: download (intent) (api.json /scenarios/1/steps/8)
            #   relies on GET /files/{path}: File.download
            #   owned["binary.bin"]: the path of fixture binary.bin, "binary.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/binary.bin)
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File: api.json /scenarios/1/steps/8/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/1/steps/8/expect/bytes
            #   checks local_file holds the bytes of recipe 1 (api.json /recipes/1): api.json /scenarios/1/steps/8/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                14,
                "/scenarios/1/steps/8",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.download_file(
                    owned["binary.bin"], local_file, options
                ),
            ),
            # files.owned-binary-roundtrip step 15: download (intent) (api.json /scenarios/1/steps/9)
            #   relies on GET /files/{path}: File.download
            #   owned["empty.bin"]: the path of fixture empty.bin, "empty.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/empty.bin)
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File: api.json /scenarios/1/steps/9/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/1/steps/9/expect/bytes
            #   checks local_file holds the bytes of recipe 2 (api.json /recipes/2): api.json /scenarios/1/steps/9/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                15,
                "/scenarios/1/steps/9",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.download_file(
                    owned["empty.bin"], local_file, options
                ),
            ),
            # files.owned-binary-roundtrip step 16: download (intent) (api.json /scenarios/1/steps/10)
            #   relies on GET /files/{path}: File.download
            #   owned["short-read.bin"]: the path of fixture short-read.bin, "short-read.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/short-read.bin)
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File: api.json /scenarios/1/steps/10/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/1/steps/10/expect/bytes
            #   checks local_file holds the bytes of recipe 3 (api.json /recipes/3): api.json /scenarios/1/steps/10/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                16,
                "/scenarios/1/steps/10",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.download_file(
                    owned["short-read.bin"], local_file, options
                ),
            ),
            # files.owned-binary-roundtrip step 17: DELETE /files/{path} (api.json /scenarios/1/steps/11)
            #   owned["binary.bin"]: the path of fixture binary.bin, "binary.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/binary.bin)
            #   {"recursive": False}: recursive: api.json /scenarios/1/steps/11/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/1/steps/11/expect/status
            Binding(
                17,
                "/scenarios/1/steps/11",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["binary.bin"], {"recursive": False}, options
                ),
            ),
            # files.owned-binary-roundtrip step 18: GET /file_actions/metadata/{path} (api.json /scenarios/1/steps/12)
            #   owned["binary.bin"]: the path of fixture binary.bin, "binary.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/binary.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/1/steps/12/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/1/steps/12/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/1/steps/12/expect/attempts
            Binding(
                18,
                "/scenarios/1/steps/12",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["binary.bin"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-binary-roundtrip step 19: DELETE /files/{path} (api.json /scenarios/1/steps/13)
            #   owned["empty.bin"]: the path of fixture empty.bin, "empty.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/empty.bin)
            #   {"recursive": False}: recursive: api.json /scenarios/1/steps/13/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/1/steps/13/expect/status
            Binding(
                19,
                "/scenarios/1/steps/13",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["empty.bin"], {"recursive": False}, options
                ),
            ),
            # files.owned-binary-roundtrip step 20: GET /file_actions/metadata/{path} (api.json /scenarios/1/steps/14)
            #   owned["empty.bin"]: the path of fixture empty.bin, "empty.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/empty.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/1/steps/14/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/1/steps/14/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/1/steps/14/expect/attempts
            Binding(
                20,
                "/scenarios/1/steps/14",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["empty.bin"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-binary-roundtrip step 21: DELETE /files/{path} (api.json /scenarios/1/steps/15)
            #   owned["short-read.bin"]: the path of fixture short-read.bin, "short-read.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/short-read.bin)
            #   {"recursive": False}: recursive: api.json /scenarios/1/steps/15/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/1/steps/15/expect/status
            Binding(
                21,
                "/scenarios/1/steps/15",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["short-read.bin"], {"recursive": False}, options
                ),
            ),
            # files.owned-binary-roundtrip step 22: GET /file_actions/metadata/{path} (api.json /scenarios/1/steps/16)
            #   owned["short-read.bin"]: the path of fixture short-read.bin, "short-read.bin" inside the run's owned folder (api.json /scenarios/1/fixtures/short-read.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/1/steps/16/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/1/steps/16/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/1/steps/16/expect/attempts
            Binding(
                22,
                "/scenarios/1/steps/16",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["short-read.bin"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-binary-roundtrip step 23: DELETE /files/{path} (api.json /groups/namespace.close/0)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/1/fixtures/folder)
            #   {"recursive": False}: recursive: api.json /groups/namespace.close/0/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /groups/namespace.close/0/expect/status
            Binding(
                23,
                "/groups/namespace.close/0",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["folder"], {"recursive": False}, options
                ),
            ),
            # files.owned-binary-roundtrip step 24: GET /file_actions/metadata/{path} (api.json /groups/namespace.close/1)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/1/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.close/1/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.close/1/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /groups/namespace.close/1/expect/attempts
            Binding(
                24,
                "/groups/namespace.close/1",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
        ),
    ),
    "files.owned-namespace-extended": Case(
        cleanup=lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
            owned["folder"], {"recursive": True}, options
        ),
        confirm=48,
        steps=(
            # files.owned-namespace-extended step 1: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/0)
            #   "/": api.json /groups/namespace.open/0/parameters/path
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.RequestParamsRequiredError (a subclass of BadRequestError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.open/0/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.open/0/expect/status
            Binding(
                1,
                "/groups/namespace.open/0",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    "/", {}, options
                ),
                error=files_sdk.error.RequestParamsRequiredError,
            ),
            # files.owned-namespace-extended step 2: GET /folders/{path} (api.json /groups/namespace.open/1)
            #   "/": api.json /groups/namespace.open/1/parameters/path
            #   {"per_page": 1000}: per_page: api.json /groups/namespace.open/1/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /groups/namespace.open/1/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /groups/namespace.open/1/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /groups/namespace.open/1/expect/listing/max_pages
            #   checks its members are not asserted (they belong to the site): api.json /groups/namespace.open/1/expect/listing
            Binding(
                2,
                "/groups/namespace.open/1",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    "/", {"per_page": 1000}, options
                ),
            ),
            # files.owned-namespace-extended step 3: GET /behaviors/folders/{path} (api.json /groups/namespace.open/2). Site-only: omitted on the simulator, never run or passed here
            #   "/": api.json /groups/namespace.open/2/parameters/path
            #   {"ancestor_behaviors": True, "per_page": 100}: ancestor_behaviors: api.json /groups/namespace.open/2/parameters/ancestor_behaviors; per_page: api.json /groups/namespace.open/2/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[Behavior]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /groups/namespace.open/2/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /groups/namespace.open/2/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /groups/namespace.open/2/expect/listing/max_pages
            #   checks at most max_records items in all: api.json /groups/namespace.open/2/expect/listing/max_records
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /groups/namespace.open/2/expect/listing/entries
            Binding(
                3,
                "/groups/namespace.open/2",
                False,
                "GET /behaviors/folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.behavior.list_for(
                    "/", {"ancestor_behaviors": True, "per_page": 100}, options
                ),
            ),
            # files.owned-namespace-extended step 4: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/3)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/2/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.open/3/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.open/3/expect/status
            Binding(
                4,
                "/groups/namespace.open/3",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 5: POST /folders/{path} (api.json /groups/namespace.open/4)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/2/fixtures/folder)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /groups/namespace.open/4/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /groups/namespace.open/4/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/folder/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/folder/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/2/fixtures/folder/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                5,
                "/groups/namespace.open/4",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["folder"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-namespace-extended step 6: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/5). Site-only: omitted on the simulator, never run or passed here
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/2/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /groups/namespace.open/5/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/folder/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/folder/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/2/fixtures/folder/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            #   checks entry.permissions and the raw JSON permissions each match includes: api.json /groups/namespace.open/5/expect/entry/fields/permissions
            #   checks entry.is_locked and the raw JSON is_locked each match not: api.json /groups/namespace.open/5/expect/entry/fields/is_locked
            #   checks getattr(entry, "subfolders_locked?") and the raw JSON subfolders_locked? each match not: api.json /groups/namespace.open/5/expect/entry/fields/subfolders_locked?
            Binding(
                6,
                "/groups/namespace.open/5",
                False,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
            ),
            # files.owned-namespace-extended step 7: upload (intent) (api.json /scenarios/2/steps/1)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   local_file: a local file in the case's own folder holding the bytes of recipe 4 (api.json /recipes/4)
            #   owned["hash-name"]: the path of fixture hash-name, "a#b.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/hash-name)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File, which an API response presented as a file (raw JSON type and path): api.json /scenarios/2/steps/1/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/1/expect/completed
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                7,
                "/scenarios/2/steps/1",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_file(
                    local_file, owned["hash-name"], options
                ),
            ),
            # files.owned-namespace-extended step 8: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/2)
            #   owned["hash-name"]: the path of fixture hash-name, "a#b.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/hash-name)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/2/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/hash-name/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/hash-name/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/4/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                8,
                "/scenarios/2/steps/2",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["hash-name"], {}, options
                ),
            ),
            # files.owned-namespace-extended step 9: upload (intent) (api.json /scenarios/2/steps/3)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   local_file: a local file in the case's own folder holding the bytes of recipe 5 (api.json /recipes/5)
            #   owned["percent-name"]: the path of fixture percent-name, "100%.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/percent-name)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File, which an API response presented as a file (raw JSON type and path): api.json /scenarios/2/steps/3/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/3/expect/completed
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                9,
                "/scenarios/2/steps/3",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_file(
                    local_file, owned["percent-name"], options
                ),
            ),
            # files.owned-namespace-extended step 10: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/4)
            #   owned["percent-name"]: the path of fixture percent-name, "100%.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/percent-name)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/4/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/percent-name/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/percent-name/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/5/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                10,
                "/scenarios/2/steps/4",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["percent-name"], {}, options
                ),
            ),
            # files.owned-namespace-extended step 11: upload (intent) (api.json /scenarios/2/steps/5)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   local_file: a local file in the case's own folder holding the bytes of recipe 6 (api.json /recipes/6)
            #   owned["unicode-name"]: the path of fixture unicode-name, "é +.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/unicode-name)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File, which an API response presented as a file (raw JSON type and path): api.json /scenarios/2/steps/5/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/5/expect/completed
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                11,
                "/scenarios/2/steps/5",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_file(
                    local_file, owned["unicode-name"], options
                ),
            ),
            # files.owned-namespace-extended step 12: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/6)
            #   owned["unicode-name"]: the path of fixture unicode-name, "é +.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/unicode-name)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/6/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/unicode-name/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/unicode-name/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/6/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                12,
                "/scenarios/2/steps/6",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["unicode-name"], {}, options
                ),
            ),
            # files.owned-namespace-extended step 13: POST /folders/{path} (api.json /scenarios/2/steps/7)
            #   owned["nested"]: the path of fixture nested, "nested" inside the run's owned folder (api.json /scenarios/2/fixtures/nested)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /scenarios/2/steps/7/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/7/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/nested/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/nested/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/2/fixtures/nested/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                13,
                "/scenarios/2/steps/7",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["nested"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-namespace-extended step 14: upload (intent) (api.json /scenarios/2/steps/8)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   stream: a seekable binary stream at the start of the bytes of recipe 7 (api.json /recipes/7)
            #   owned["inner.bin"]: the path of fixture inner.bin, "nested/inner.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/inner.bin)
            #   4099: size: the length of recipe 7 (api.json /recipes/7)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File, which an API response presented as a file (raw JSON type and path): api.json /scenarios/2/steps/8/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/8/expect/completed
            #   checks the stream was read to the end of the recipe's bytes, and no further: api.json /recipes/7/length
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                14,
                "/scenarios/2/steps/8",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_stream(
                    stream, owned["inner.bin"], 4099, options
                ),
            ),
            # files.owned-namespace-extended step 15: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/9)
            #   owned["inner.bin"]: the path of fixture inner.bin, "nested/inner.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/inner.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/9/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/inner.bin/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/inner.bin/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/7/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                15,
                "/scenarios/2/steps/9",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["inner.bin"], {}, options
                ),
            ),
            # files.owned-namespace-extended step 16: upload (intent) (api.json /scenarios/2/steps/10)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   local_file: a local file in the case's own folder holding the bytes of recipe 8 (api.json /recipes/8)
            #   owned["large.bin"]: the path of fixture large.bin, "large.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/large.bin)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   progress=progress: a callback given each UploadProgress
            #   returns File
            #   checks returns the fixture's File, which an API response presented as a file (raw JSON type and path): api.json /scenarios/2/steps/10/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/10/expect/completed
            #   checks the last UploadProgress's total_bytes is the length of the recipe: api.json /scenarios/2/steps/10/expect/progress_final/total_bytes
            #   checks the last UploadProgress's bytes_committed is the length of the recipe: api.json /scenarios/2/steps/10/expect/progress_final/acknowledged_bytes
            #   checks the last UploadProgress's parts_committed is at least min_parts: api.json /scenarios/2/steps/10/expect/min_parts
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                16,
                "/scenarios/2/steps/10",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_file(
                    local_file, owned["large.bin"], options, progress=progress
                ),
            ),
            # files.owned-namespace-extended step 17: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/11)
            #   owned["large.bin"]: the path of fixture large.bin, "large.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/large.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/11/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/large.bin/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/large.bin/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/8/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                17,
                "/scenarios/2/steps/11",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["large.bin"], {}, options
                ),
            ),
            # files.owned-namespace-extended step 18: copy (intent) (api.json /scenarios/2/steps/12)
            #   relies on POST /file_actions/copy/{path}: File.copy
            #   relies on GET /file_migrations/{id}: FileMigration.find
            #   owned["inner.bin"]: the path of fixture inner.bin, "nested/inner.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/inner.bin)
            #   {"destination": owned["copied.bin"]}: destination: the path of fixture copied.bin, "copied.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/copied.bin)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns FileMigration | None
            #   checks returns the completed FileMigration, or None if it finished at once; a failed or cancelled migration raises files_sdk.error.FileMigrationError: api.json /scenarios/2/steps/12/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of its from fixture and its fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of its from fixture and its fixture; none from a POST: api.json /scenarios/2/steps/12/expect/completed
            Binding(
                18,
                "/scenarios/2/steps/12",
                True,
                "copy (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.copy_and_wait(
                    owned["inner.bin"],
                    {"destination": owned["copied.bin"]},
                    options,
                ),
            ),
            # files.owned-namespace-extended step 19: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/13)
            #   owned["copied.bin"]: the path of fixture copied.bin, "copied.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/copied.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/13/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/copied.bin/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/copied.bin/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/7/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                19,
                "/scenarios/2/steps/13",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["copied.bin"], {}, options
                ),
            ),
            # files.owned-namespace-extended step 20: move (intent) (api.json /scenarios/2/steps/14)
            #   relies on POST /file_actions/move/{path}: File.move
            #   relies on GET /file_migrations/{id}: FileMigration.find
            #   owned["copied.bin"]: the path of fixture copied.bin, "copied.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/copied.bin)
            #   {"destination": owned["moved.bin"]}: destination: the path of fixture moved.bin, "nested/moved.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/moved.bin)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns FileMigration | None
            #   checks returns the completed FileMigration, or None if it finished at once; a failed or cancelled migration raises files_sdk.error.FileMigrationError: api.json /scenarios/2/steps/14/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of its from fixture and its fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of its from fixture and its fixture; none from a POST: api.json /scenarios/2/steps/14/expect/completed
            Binding(
                20,
                "/scenarios/2/steps/14",
                True,
                "move (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.move_and_wait(
                    owned["copied.bin"],
                    {"destination": owned["moved.bin"]},
                    options,
                ),
            ),
            # files.owned-namespace-extended step 21: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/15)
            #   owned["copied.bin"]: the path of fixture copied.bin, "copied.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/copied.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/15/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/15/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/15/expect/attempts
            Binding(
                21,
                "/scenarios/2/steps/15",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["copied.bin"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 22: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/16)
            #   owned["moved.bin"]: the path of fixture moved.bin, "nested/moved.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/moved.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/16/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/2/fixtures/moved.bin/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/2/fixtures/moved.bin/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/7/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                22,
                "/scenarios/2/steps/16",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["moved.bin"], {}, options
                ),
            ),
            # files.owned-namespace-extended step 23: GET /folders/{path} (api.json /scenarios/2/steps/17)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/2/fixtures/folder)
            #   {"per_page": 1}: per_page: api.json /scenarios/2/steps/17/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/2/steps/17/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/2/steps/17/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/2/steps/17/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/2/steps/17/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                23,
                "/scenarios/2/steps/17",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["folder"], {"per_page": 1}, options
                ),
            ),
            # files.owned-namespace-extended step 24: download (intent) (api.json /scenarios/2/steps/18)
            #   relies on GET /files/{path}: File.download
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   returns File
            #   checks listed["hash-name"] is the File the listing of step 23 returned for fixture hash-name, at its path; download_file takes only its path, so the call passes no options: it is an operation of its own, with the limits of the client settings the File keeps (no request_timeout), not that listing call's deadline or token, once the case has checked that its own deadline has not passed: api.json /scenarios/2/steps/17
            #   checks returns the fixture's File: api.json /scenarios/2/steps/18/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/18/expect/bytes
            #   checks local_file holds the bytes of recipe 4 (api.json /recipes/4): api.json /scenarios/2/steps/18/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                24,
                "/scenarios/2/steps/18",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: listed[
                    "hash-name"
                ].download_file(
                    local_file
                ),
            ),
            # files.owned-namespace-extended step 25: download (intent) (api.json /scenarios/2/steps/19)
            #   relies on GET /files/{path}: File.download
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   returns File
            #   checks listed["percent-name"] is the File the listing of step 23 returned for fixture percent-name, at its path; download_file takes only its path, so the call passes no options: it is an operation of its own, with the limits of the client settings the File keeps (no request_timeout), not that listing call's deadline or token, once the case has checked that its own deadline has not passed: api.json /scenarios/2/steps/17
            #   checks returns the fixture's File: api.json /scenarios/2/steps/19/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/19/expect/bytes
            #   checks local_file holds the bytes of recipe 5 (api.json /recipes/5): api.json /scenarios/2/steps/19/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                25,
                "/scenarios/2/steps/19",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: listed[
                    "percent-name"
                ].download_file(
                    local_file
                ),
            ),
            # files.owned-namespace-extended step 26: download (intent) (api.json /scenarios/2/steps/20)
            #   relies on GET /files/{path}: File.download
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   returns File
            #   checks listed["unicode-name"] is the File the listing of step 23 returned for fixture unicode-name, at its path; download_file takes only its path, so the call passes no options: it is an operation of its own, with the limits of the client settings the File keeps (no request_timeout), not that listing call's deadline or token, once the case has checked that its own deadline has not passed: api.json /scenarios/2/steps/17
            #   checks returns the fixture's File: api.json /scenarios/2/steps/20/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/20/expect/bytes
            #   checks local_file holds the bytes of recipe 6 (api.json /recipes/6): api.json /scenarios/2/steps/20/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                26,
                "/scenarios/2/steps/20",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: listed[
                    "unicode-name"
                ].download_file(
                    local_file
                ),
            ),
            # files.owned-namespace-extended step 27: download (intent) (api.json /scenarios/2/steps/21)
            #   relies on GET /files/{path}: File.download
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   returns File
            #   checks listed["large.bin"] is the File the listing of step 23 returned for fixture large.bin, at its path; download_file takes only its path, so the call passes no options: it is an operation of its own, with the limits of the client settings the File keeps (no request_timeout), not that listing call's deadline or token, once the case has checked that its own deadline has not passed: api.json /scenarios/2/steps/17
            #   checks returns the fixture's File: api.json /scenarios/2/steps/21/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/21/expect/bytes
            #   checks local_file holds the bytes of recipe 8 (api.json /recipes/8): api.json /scenarios/2/steps/21/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                27,
                "/scenarios/2/steps/21",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: listed[
                    "large.bin"
                ].download_file(
                    local_file
                ),
            ),
            # files.owned-namespace-extended step 28: download (intent) (api.json /scenarios/2/steps/22)
            #   relies on GET /files/{path}: File.download
            #   owned["inner.bin"]: the path of fixture inner.bin, "nested/inner.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/inner.bin)
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File: api.json /scenarios/2/steps/22/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/22/expect/bytes
            #   checks local_file holds the bytes of recipe 7 (api.json /recipes/7): api.json /scenarios/2/steps/22/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                28,
                "/scenarios/2/steps/22",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.download_file(
                    owned["inner.bin"], local_file, options
                ),
            ),
            # files.owned-namespace-extended step 29: download (intent) (api.json /scenarios/2/steps/23)
            #   relies on GET /files/{path}: File.download
            #   owned["moved.bin"]: the path of fixture moved.bin, "nested/moved.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/moved.bin)
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File: api.json /scenarios/2/steps/23/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/23/expect/bytes
            #   checks local_file holds the bytes of recipe 7 (api.json /recipes/7): api.json /scenarios/2/steps/23/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                29,
                "/scenarios/2/steps/23",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.download_file(
                    owned["moved.bin"], local_file, options
                ),
            ),
            # files.owned-namespace-extended step 30: download (intent) (api.json /scenarios/2/steps/24)
            #   relies on GET /files/{path}: File.download
            #   owned["large.bin"]: the path of fixture large.bin, "large.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/large.bin)
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File: api.json /scenarios/2/steps/24/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/24/expect/bytes
            #   checks local_file holds the bytes of recipe 8 (api.json /recipes/8): api.json /scenarios/2/steps/24/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                30,
                "/scenarios/2/steps/24",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.download_file(
                    owned["large.bin"], local_file, options
                ),
            ),
            # files.owned-namespace-extended step 31: upload (intent) (api.json /scenarios/2/steps/25)
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   local_file: a local file in the case's own folder holding the bytes of recipe 9 (api.json /recipes/9)
            #   owned["cancelled.bin"]: the path of fixture cancelled.bin, "cancelled.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/cancelled.bin)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   progress=progress: a callback given each UploadProgress
            #   max_concurrency=1: one part at a time, so that cancelling at the first acknowledged part stops the parts after it
            #   tuning=files_sdk.UploadTuning(adaptive=False): no adapting: max_concurrency parts at once throughout
            #   returns File
            #   checks on a client and session of the step's own, whose response hook cancels the step's cancel_token at the first successful upload part response (a PUT): acknowledgement 1, the wire-response acknowledgement boundary, before any UploadProgress reports a committed part; raises exactly files_sdk.error.OperationCancelledError, not its subclass ClientClosedError, its token cancelled; no API response presented the fixture as a file; then that client's close() returns and its session closes: api.json /scenarios/2/steps/25/expect/cancelled
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/2/steps/25/expect/cancelled
            Binding(
                31,
                "/scenarios/2/steps/25",
                True,
                "upload (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_file(
                    local_file,
                    owned["cancelled.bin"],
                    options,
                    progress=progress,
                    max_concurrency=1,
                    tuning=files_sdk.UploadTuning(adaptive=False),
                ),
            ),
            # files.owned-namespace-extended step 32: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/26)
            #   owned["cancelled.bin"]: the path of fixture cancelled.bin, "cancelled.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/cancelled.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/26/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/26/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/26/expect/attempts
            Binding(
                32,
                "/scenarios/2/steps/26",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["cancelled.bin"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 33: DELETE /files/{path} (api.json /scenarios/2/steps/27)
            #   owned["moved.bin"]: the path of fixture moved.bin, "nested/moved.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/moved.bin)
            #   {"recursive": False}: recursive: api.json /scenarios/2/steps/27/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/27/expect/status
            Binding(
                33,
                "/scenarios/2/steps/27",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["moved.bin"], {"recursive": False}, options
                ),
            ),
            # files.owned-namespace-extended step 34: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/28)
            #   owned["moved.bin"]: the path of fixture moved.bin, "nested/moved.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/moved.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/28/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/28/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/28/expect/attempts
            Binding(
                34,
                "/scenarios/2/steps/28",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["moved.bin"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 35: DELETE /files/{path} (api.json /scenarios/2/steps/29)
            #   owned["inner.bin"]: the path of fixture inner.bin, "nested/inner.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/inner.bin)
            #   {"recursive": False}: recursive: api.json /scenarios/2/steps/29/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/29/expect/status
            Binding(
                35,
                "/scenarios/2/steps/29",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["inner.bin"], {"recursive": False}, options
                ),
            ),
            # files.owned-namespace-extended step 36: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/30)
            #   owned["inner.bin"]: the path of fixture inner.bin, "nested/inner.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/inner.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/30/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/30/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/30/expect/attempts
            Binding(
                36,
                "/scenarios/2/steps/30",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["inner.bin"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 37: DELETE /files/{path} (api.json /scenarios/2/steps/31)
            #   owned["nested"]: the path of fixture nested, "nested" inside the run's owned folder (api.json /scenarios/2/fixtures/nested)
            #   {"recursive": False}: recursive: api.json /scenarios/2/steps/31/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/31/expect/status
            Binding(
                37,
                "/scenarios/2/steps/31",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["nested"], {"recursive": False}, options
                ),
            ),
            # files.owned-namespace-extended step 38: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/32)
            #   owned["nested"]: the path of fixture nested, "nested" inside the run's owned folder (api.json /scenarios/2/fixtures/nested)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/32/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/32/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/32/expect/attempts
            Binding(
                38,
                "/scenarios/2/steps/32",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["nested"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 39: DELETE /files/{path} (api.json /scenarios/2/steps/33)
            #   owned["large.bin"]: the path of fixture large.bin, "large.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/large.bin)
            #   {"recursive": False}: recursive: api.json /scenarios/2/steps/33/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/33/expect/status
            Binding(
                39,
                "/scenarios/2/steps/33",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["large.bin"], {"recursive": False}, options
                ),
            ),
            # files.owned-namespace-extended step 40: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/34)
            #   owned["large.bin"]: the path of fixture large.bin, "large.bin" inside the run's owned folder (api.json /scenarios/2/fixtures/large.bin)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/34/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/34/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/34/expect/attempts
            Binding(
                40,
                "/scenarios/2/steps/34",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["large.bin"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 41: DELETE /files/{path} (api.json /scenarios/2/steps/35)
            #   owned["hash-name"]: the path of fixture hash-name, "a#b.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/hash-name)
            #   {"recursive": False}: recursive: api.json /scenarios/2/steps/35/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/35/expect/status
            Binding(
                41,
                "/scenarios/2/steps/35",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["hash-name"], {"recursive": False}, options
                ),
            ),
            # files.owned-namespace-extended step 42: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/36)
            #   owned["hash-name"]: the path of fixture hash-name, "a#b.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/hash-name)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/36/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/36/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/36/expect/attempts
            Binding(
                42,
                "/scenarios/2/steps/36",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["hash-name"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 43: DELETE /files/{path} (api.json /scenarios/2/steps/37)
            #   owned["percent-name"]: the path of fixture percent-name, "100%.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/percent-name)
            #   {"recursive": False}: recursive: api.json /scenarios/2/steps/37/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/37/expect/status
            Binding(
                43,
                "/scenarios/2/steps/37",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["percent-name"], {"recursive": False}, options
                ),
            ),
            # files.owned-namespace-extended step 44: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/38)
            #   owned["percent-name"]: the path of fixture percent-name, "100%.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/percent-name)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/38/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/38/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/38/expect/attempts
            Binding(
                44,
                "/scenarios/2/steps/38",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["percent-name"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 45: DELETE /files/{path} (api.json /scenarios/2/steps/39)
            #   owned["unicode-name"]: the path of fixture unicode-name, "é +.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/unicode-name)
            #   {"recursive": False}: recursive: api.json /scenarios/2/steps/39/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/2/steps/39/expect/status
            Binding(
                45,
                "/scenarios/2/steps/39",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["unicode-name"], {"recursive": False}, options
                ),
            ),
            # files.owned-namespace-extended step 46: GET /file_actions/metadata/{path} (api.json /scenarios/2/steps/40)
            #   owned["unicode-name"]: the path of fixture unicode-name, "é +.txt" inside the run's owned folder (api.json /scenarios/2/fixtures/unicode-name)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/2/steps/40/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/2/steps/40/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/2/steps/40/expect/attempts
            Binding(
                46,
                "/scenarios/2/steps/40",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["unicode-name"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-namespace-extended step 47: DELETE /files/{path} (api.json /groups/namespace.close/0)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/2/fixtures/folder)
            #   {"recursive": False}: recursive: api.json /groups/namespace.close/0/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /groups/namespace.close/0/expect/status
            Binding(
                47,
                "/groups/namespace.close/0",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["folder"], {"recursive": False}, options
                ),
            ),
            # files.owned-namespace-extended step 48: GET /file_actions/metadata/{path} (api.json /groups/namespace.close/1)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/2/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.close/1/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.close/1/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /groups/namespace.close/1/expect/attempts
            Binding(
                48,
                "/groups/namespace.close/1",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
        ),
    ),
    "files.owned-directory-helpers": Case(
        cleanup=lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
            owned["folder"], {"recursive": True}, options
        ),
        confirm=44,
        steps=(
            # files.owned-directory-helpers step 1: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/0)
            #   "/": api.json /groups/namespace.open/0/parameters/path
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.RequestParamsRequiredError (a subclass of BadRequestError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.open/0/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.open/0/expect/status
            Binding(
                1,
                "/groups/namespace.open/0",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    "/", {}, options
                ),
                error=files_sdk.error.RequestParamsRequiredError,
            ),
            # files.owned-directory-helpers step 2: GET /folders/{path} (api.json /groups/namespace.open/1)
            #   "/": api.json /groups/namespace.open/1/parameters/path
            #   {"per_page": 1000}: per_page: api.json /groups/namespace.open/1/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /groups/namespace.open/1/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /groups/namespace.open/1/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /groups/namespace.open/1/expect/listing/max_pages
            #   checks its members are not asserted (they belong to the site): api.json /groups/namespace.open/1/expect/listing
            Binding(
                2,
                "/groups/namespace.open/1",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    "/", {"per_page": 1000}, options
                ),
            ),
            # files.owned-directory-helpers step 3: GET /behaviors/folders/{path} (api.json /groups/namespace.open/2). Site-only: omitted on the simulator, never run or passed here
            #   "/": api.json /groups/namespace.open/2/parameters/path
            #   {"ancestor_behaviors": True, "per_page": 100}: ancestor_behaviors: api.json /groups/namespace.open/2/parameters/ancestor_behaviors; per_page: api.json /groups/namespace.open/2/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[Behavior]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /groups/namespace.open/2/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /groups/namespace.open/2/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /groups/namespace.open/2/expect/listing/max_pages
            #   checks at most max_records items in all: api.json /groups/namespace.open/2/expect/listing/max_records
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /groups/namespace.open/2/expect/listing/entries
            Binding(
                3,
                "/groups/namespace.open/2",
                False,
                "GET /behaviors/folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.behavior.list_for(
                    "/", {"ancestor_behaviors": True, "per_page": 100}, options
                ),
            ),
            # files.owned-directory-helpers step 4: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/3)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/3/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.open/3/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.open/3/expect/status
            Binding(
                4,
                "/groups/namespace.open/3",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 5: POST /folders/{path} (api.json /groups/namespace.open/4)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/3/fixtures/folder)
            #   {"mkdir_parents": False}: mkdir_parents: api.json /groups/namespace.open/4/parameters/mkdir_parents
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /groups/namespace.open/4/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/folder/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/folder/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/3/fixtures/folder/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                5,
                "/groups/namespace.open/4",
                True,
                "POST /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.create(
                    owned["folder"], {"mkdir_parents": False}, options
                ),
            ),
            # files.owned-directory-helpers step 6: GET /file_actions/metadata/{path} (api.json /groups/namespace.open/5). Site-only: omitted on the simulator, never run or passed here
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/3/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /groups/namespace.open/5/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/folder/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/folder/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/3/fixtures/folder/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            #   checks entry.permissions and the raw JSON permissions each match includes: api.json /groups/namespace.open/5/expect/entry/fields/permissions
            #   checks entry.is_locked and the raw JSON is_locked each match not: api.json /groups/namespace.open/5/expect/entry/fields/is_locked
            #   checks getattr(entry, "subfolders_locked?") and the raw JSON subfolders_locked? each match not: api.json /groups/namespace.open/5/expect/entry/fields/subfolders_locked?
            Binding(
                6,
                "/groups/namespace.open/5",
                False,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 7: upload-directory (intent) (api.json /scenarios/3/steps/1)
            #   relies on POST /folders/{path}: Folder.create
            #   relies on POST /file_actions/begin_upload/{path}: File.begin_upload
            #   relies on POST /files/{path}: File.create
            #   local_directory: a local folder in the case's own folder holding the tree's files a.bin, sub/b.bin and folders empty, sub
            #   owned["up"]: the path of fixture up, "up" inside the run's owned folder (api.json /scenarios/3/fixtures/up)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns TransferResult
            #   checks result.completed outcomes of kind "file", by remote_path: exactly the completed fixtures: api.json /scenarios/3/steps/1/expect/completed
            #   checks result.failed and result.skipped are empty: api.json /scenarios/3/steps/1/expect/completed
            #   checks the number of completed file outcomes: api.json /scenarios/3/steps/1/expect/files
            #   checks the sum of the completed file outcomes' bytes: api.json /scenarios/3/steps/1/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture's folder, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture's folder; a POST's only for a folder a listing after the upload finds there: api.json /scenarios/3/steps/1/expect/completed
            #   checks the folders under the fixture's folder that a listing of each (client.folder.list_for(folder, {"per_page": 1000}, options)) finds empty after the upload: exactly empty_folders: api.json /scenarios/3/steps/1/expect/empty_folders
            Binding(
                7,
                "/scenarios/3/steps/1",
                True,
                "upload-directory (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.upload_directory(
                    local_directory, owned["up"], options
                ),
                observe=lambda client, options, folder: client.folder.list_for(
                    folder, {"per_page": 1000}, options
                ),
            ),
            # files.owned-directory-helpers step 8: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/2)
            #   owned["up"]: the path of fixture up, "up" inside the run's owned folder (api.json /scenarios/3/fixtures/up)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/2/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/up/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/up/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/3/fixtures/up/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                8,
                "/scenarios/3/steps/2",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 9: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/3)
            #   owned["up-a"]: the path of fixture up-a, "up/a.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/up-a)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/3/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/up-a/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/up-a/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/10/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                9,
                "/scenarios/3/steps/3",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up-a"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 10: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/4)
            #   owned["up-sub"]: the path of fixture up-sub, "up/sub" inside the run's owned folder (api.json /scenarios/3/fixtures/up-sub)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/4/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/up-sub/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/up-sub/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/3/fixtures/up-sub/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                10,
                "/scenarios/3/steps/4",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up-sub"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 11: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/5)
            #   owned["up-b"]: the path of fixture up-b, "up/sub/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/up-b)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/5/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/up-b/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/up-b/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/11/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                11,
                "/scenarios/3/steps/5",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up-b"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 12: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/6)
            #   owned["up-empty"]: the path of fixture up-empty, "up/empty" inside the run's owned folder (api.json /scenarios/3/fixtures/up-empty)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/6/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/up-empty/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/up-empty/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/3/fixtures/up-empty/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                12,
                "/scenarios/3/steps/6",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up-empty"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 13: GET /folders/{path} (api.json /scenarios/3/steps/7)
            #   owned["up"]: the path of fixture up, "up" inside the run's owned folder (api.json /scenarios/3/fixtures/up)
            #   {"per_page": 1000}: per_page: api.json /scenarios/3/steps/7/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/3/steps/7/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/3/steps/7/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/3/steps/7/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/3/steps/7/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                13,
                "/scenarios/3/steps/7",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["up"], {"per_page": 1000}, options
                ),
            ),
            # files.owned-directory-helpers step 14: GET /folders/{path} (api.json /scenarios/3/steps/8)
            #   owned["up-sub"]: the path of fixture up-sub, "up/sub" inside the run's owned folder (api.json /scenarios/3/fixtures/up-sub)
            #   {"per_page": 1000}: per_page: api.json /scenarios/3/steps/8/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/3/steps/8/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/3/steps/8/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/3/steps/8/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/3/steps/8/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                14,
                "/scenarios/3/steps/8",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["up-sub"], {"per_page": 1000}, options
                ),
            ),
            # files.owned-directory-helpers step 15: GET /folders/{path} (api.json /scenarios/3/steps/9)
            #   owned["up-empty"]: the path of fixture up-empty, "up/empty" inside the run's owned folder (api.json /scenarios/3/fixtures/up-empty)
            #   {"per_page": 1000}: per_page: api.json /scenarios/3/steps/9/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/3/steps/9/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/3/steps/9/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/3/steps/9/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/3/steps/9/expect/listing/entries
            Binding(
                15,
                "/scenarios/3/steps/9",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["up-empty"], {"per_page": 1000}, options
                ),
            ),
            # files.owned-directory-helpers step 16: download-directory (intent) (api.json /scenarios/3/steps/10)
            #   relies on GET /folders/{path}: Folder.list_for
            #   relies on GET /files/{path}: File.download
            #   owned["up"]: the path of fixture up, "up" inside the run's owned folder (api.json /scenarios/3/fixtures/up)
            #   local_directory: a new local folder in the case's own folder
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns TransferResult
            #   checks result.failed and result.skipped are empty: api.json /scenarios/3/steps/10/expect/files
            #   checks the number of completed file outcomes: api.json /scenarios/3/steps/10/expect/files
            #   checks the sum of the completed file outcomes' bytes: api.json /scenarios/3/steps/10/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture's folder, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture's folder; none from a POST: api.json /scenarios/3/steps/10/expect/files
            #   checks each bytes_match fixture's local file holds its recipe's bytes: api.json /scenarios/3/steps/10/expect/bytes_match
            #   checks the folders under the new local folder that hold nothing after the download: exactly empty_folders: api.json /scenarios/3/steps/10/expect/empty_folders
            Binding(
                16,
                "/scenarios/3/steps/10",
                True,
                "download-directory (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.download_directory(
                    owned["up"], local_directory, options
                ),
            ),
            # files.owned-directory-helpers step 17: copy (intent) (api.json /scenarios/3/steps/11)
            #   relies on POST /file_actions/copy/{path}: File.copy
            #   relies on GET /file_migrations/{id}: FileMigration.find
            #   owned["up-sub"]: the path of fixture up-sub, "up/sub" inside the run's owned folder (api.json /scenarios/3/fixtures/up-sub)
            #   {"destination": owned["copy"]}: destination: the path of fixture copy, "copy" inside the run's owned folder (api.json /scenarios/3/fixtures/copy)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns FileMigration | None
            #   checks returns the completed FileMigration, or None if it finished at once; a failed or cancelled migration raises files_sdk.error.FileMigrationError: api.json /scenarios/3/steps/11/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of its from fixture and its fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of its from fixture and its fixture; none from a POST: api.json /scenarios/3/steps/11/expect/completed
            Binding(
                17,
                "/scenarios/3/steps/11",
                True,
                "copy (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.copy_and_wait(
                    owned["up-sub"], {"destination": owned["copy"]}, options
                ),
            ),
            # files.owned-directory-helpers step 18: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/12)
            #   owned["copy"]: the path of fixture copy, "copy" inside the run's owned folder (api.json /scenarios/3/fixtures/copy)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/12/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/copy/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/copy/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/3/fixtures/copy/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                18,
                "/scenarios/3/steps/12",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["copy"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 19: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/13)
            #   owned["copy-b"]: the path of fixture copy-b, "copy/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/copy-b)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/13/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/copy-b/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/copy-b/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/11/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                19,
                "/scenarios/3/steps/13",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["copy-b"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 20: GET /folders/{path} (api.json /scenarios/3/steps/14)
            #   owned["copy"]: the path of fixture copy, "copy" inside the run's owned folder (api.json /scenarios/3/fixtures/copy)
            #   {"per_page": 1000}: per_page: api.json /scenarios/3/steps/14/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/3/steps/14/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/3/steps/14/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/3/steps/14/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/3/steps/14/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                20,
                "/scenarios/3/steps/14",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["copy"], {"per_page": 1000}, options
                ),
            ),
            # files.owned-directory-helpers step 21: move (intent) (api.json /scenarios/3/steps/15)
            #   relies on POST /file_actions/move/{path}: File.move
            #   relies on GET /file_migrations/{id}: FileMigration.find
            #   owned["copy"]: the path of fixture copy, "copy" inside the run's owned folder (api.json /scenarios/3/fixtures/copy)
            #   {"destination": owned["moved"]}: destination: the path of fixture moved, "moved" inside the run's owned folder (api.json /scenarios/3/fixtures/moved)
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns FileMigration | None
            #   checks returns the completed FileMigration, or None if it finished at once; a failed or cancelled migration raises files_sdk.error.FileMigrationError: api.json /scenarios/3/steps/15/expect/completed
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of its from fixture and its fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of its from fixture and its fixture; none from a POST: api.json /scenarios/3/steps/15/expect/completed
            Binding(
                21,
                "/scenarios/3/steps/15",
                True,
                "move (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.move_and_wait(
                    owned["copy"], {"destination": owned["moved"]}, options
                ),
            ),
            # files.owned-directory-helpers step 22: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/16)
            #   owned["copy-b"]: the path of fixture copy-b, "copy/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/copy-b)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/16/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/16/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/16/expect/attempts
            Binding(
                22,
                "/scenarios/3/steps/16",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["copy-b"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 23: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/17)
            #   owned["copy"]: the path of fixture copy, "copy" inside the run's owned folder (api.json /scenarios/3/fixtures/copy)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/17/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/17/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/17/expect/attempts
            Binding(
                23,
                "/scenarios/3/steps/17",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["copy"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 24: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/18)
            #   owned["moved"]: the path of fixture moved, "moved" inside the run's owned folder (api.json /scenarios/3/fixtures/moved)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/18/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/moved/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/moved/path
            #   checks entry.size is None and the raw JSON size null or absent, as for a folder: api.json /scenarios/3/fixtures/moved/type
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                24,
                "/scenarios/3/steps/18",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["moved"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 25: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/19)
            #   owned["moved-b"]: the path of fixture moved-b, "moved/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/moved-b)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/19/expect/status
            #   checks entry.type and the raw JSON type are the fixture's type: api.json /scenarios/3/fixtures/moved-b/type
            #   checks entry.path and the raw JSON path are the fixture's path inside the run's owned folder: api.json /scenarios/3/fixtures/moved-b/path
            #   checks entry.size and the raw JSON size, a JSON integer, are the length of the fixture's recipe: api.json /recipes/11/length
            #   checks on a site only, which this module does not run: entry.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: entry.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                25,
                "/scenarios/3/steps/19",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["moved-b"], {}, options
                ),
            ),
            # files.owned-directory-helpers step 26: GET /folders/{path} (api.json /scenarios/3/steps/20)
            #   owned["moved"]: the path of fixture moved, "moved" inside the run's owned folder (api.json /scenarios/3/fixtures/moved)
            #   {"per_page": 1000}: per_page: api.json /scenarios/3/steps/20/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/3/steps/20/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/3/steps/20/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/3/steps/20/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/3/steps/20/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                26,
                "/scenarios/3/steps/20",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["moved"], {"per_page": 1000}, options
                ),
            ),
            # files.owned-directory-helpers step 27: GET /folders/{path} (api.json /scenarios/3/steps/21)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/3/fixtures/folder)
            #   {"per_page": 1000}: per_page: api.json /scenarios/3/steps/21/parameters/per_page
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns ListObj[File]
            #   checks each page is one API response of the status expected, whose raw JSON items are the page's items, in order, by type and path: api.json /scenarios/3/steps/21/expect/status
            #   checks each page (iterating pages) holds at most per_page items: api.json /scenarios/3/steps/21/parameters/per_page
            #   checks pages.has_next_page and pages.load_next_page: at most max_pages pages, the last with no next page: api.json /scenarios/3/steps/21/expect/listing/max_pages
            #   checks the raw JSON type and path of every page's items: each fixture of entries exactly once, and nothing else; each one's item is kept as listed[fixture]: api.json /scenarios/3/steps/21/expect/listing/entries
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: for each listed fixture, item.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                27,
                "/scenarios/3/steps/21",
                True,
                "GET /folders/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.folder.list_for(
                    owned["folder"], {"per_page": 1000}, options
                ),
            ),
            # files.owned-directory-helpers step 28: download (intent) (api.json /scenarios/3/steps/22)
            #   relies on GET /files/{path}: File.download
            #   owned["moved-b"]: the path of fixture moved-b, "moved/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/moved-b)
            #   local_file: a new local path in the case's own folder, replaced only once the whole file has arrived
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks returns the fixture's File: api.json /scenarios/3/steps/22/expect/bytes
            #   checks every API response it received answered 2xx, its raw JSON naming only paths of the fixture, or with an error the definition itself expects from that same operation, by status and raw JSON type, for a path of the fixture; none from a POST: api.json /scenarios/3/steps/22/expect/bytes
            #   checks local_file holds the bytes of recipe 11 (api.json /recipes/11): api.json /scenarios/3/steps/22/expect/bytes
            #   checks on a site only, which this module does not run: file.created_by_id is the run's own user's, as a raw JSON integer: api.json /backends/site
            #   checks on a site only, which this module does not run: file.created_by_api_key_id is the run's own API key's, as a raw JSON integer: api.json /backends/site
            Binding(
                28,
                "/scenarios/3/steps/22",
                True,
                "download (intent)",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.download_file(
                    owned["moved-b"], local_file, options
                ),
            ),
            # files.owned-directory-helpers step 29: DELETE /files/{path} (api.json /scenarios/3/steps/23)
            #   owned["moved-b"]: the path of fixture moved-b, "moved/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/moved-b)
            #   {"recursive": False}: recursive: api.json /scenarios/3/steps/23/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/23/expect/status
            Binding(
                29,
                "/scenarios/3/steps/23",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["moved-b"], {"recursive": False}, options
                ),
            ),
            # files.owned-directory-helpers step 30: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/24)
            #   owned["moved-b"]: the path of fixture moved-b, "moved/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/moved-b)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/24/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/24/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/24/expect/attempts
            Binding(
                30,
                "/scenarios/3/steps/24",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["moved-b"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 31: DELETE /files/{path} (api.json /scenarios/3/steps/25)
            #   owned["moved"]: the path of fixture moved, "moved" inside the run's owned folder (api.json /scenarios/3/fixtures/moved)
            #   {"recursive": False}: recursive: api.json /scenarios/3/steps/25/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/25/expect/status
            Binding(
                31,
                "/scenarios/3/steps/25",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["moved"], {"recursive": False}, options
                ),
            ),
            # files.owned-directory-helpers step 32: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/26)
            #   owned["moved"]: the path of fixture moved, "moved" inside the run's owned folder (api.json /scenarios/3/fixtures/moved)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/26/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/26/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/26/expect/attempts
            Binding(
                32,
                "/scenarios/3/steps/26",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["moved"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 33: DELETE /files/{path} (api.json /scenarios/3/steps/27)
            #   owned["up-b"]: the path of fixture up-b, "up/sub/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/up-b)
            #   {"recursive": False}: recursive: api.json /scenarios/3/steps/27/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/27/expect/status
            Binding(
                33,
                "/scenarios/3/steps/27",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["up-b"], {"recursive": False}, options
                ),
            ),
            # files.owned-directory-helpers step 34: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/28)
            #   owned["up-b"]: the path of fixture up-b, "up/sub/b.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/up-b)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/28/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/28/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/28/expect/attempts
            Binding(
                34,
                "/scenarios/3/steps/28",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up-b"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 35: DELETE /files/{path} (api.json /scenarios/3/steps/29)
            #   owned["up-sub"]: the path of fixture up-sub, "up/sub" inside the run's owned folder (api.json /scenarios/3/fixtures/up-sub)
            #   {"recursive": False}: recursive: api.json /scenarios/3/steps/29/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/29/expect/status
            Binding(
                35,
                "/scenarios/3/steps/29",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["up-sub"], {"recursive": False}, options
                ),
            ),
            # files.owned-directory-helpers step 36: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/30)
            #   owned["up-sub"]: the path of fixture up-sub, "up/sub" inside the run's owned folder (api.json /scenarios/3/fixtures/up-sub)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/30/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/30/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/30/expect/attempts
            Binding(
                36,
                "/scenarios/3/steps/30",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up-sub"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 37: DELETE /files/{path} (api.json /scenarios/3/steps/31)
            #   owned["up-empty"]: the path of fixture up-empty, "up/empty" inside the run's owned folder (api.json /scenarios/3/fixtures/up-empty)
            #   {"recursive": False}: recursive: api.json /scenarios/3/steps/31/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/31/expect/status
            Binding(
                37,
                "/scenarios/3/steps/31",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["up-empty"], {"recursive": False}, options
                ),
            ),
            # files.owned-directory-helpers step 38: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/32)
            #   owned["up-empty"]: the path of fixture up-empty, "up/empty" inside the run's owned folder (api.json /scenarios/3/fixtures/up-empty)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/32/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/32/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/32/expect/attempts
            Binding(
                38,
                "/scenarios/3/steps/32",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up-empty"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 39: DELETE /files/{path} (api.json /scenarios/3/steps/33)
            #   owned["up-a"]: the path of fixture up-a, "up/a.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/up-a)
            #   {"recursive": False}: recursive: api.json /scenarios/3/steps/33/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/33/expect/status
            Binding(
                39,
                "/scenarios/3/steps/33",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["up-a"], {"recursive": False}, options
                ),
            ),
            # files.owned-directory-helpers step 40: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/34)
            #   owned["up-a"]: the path of fixture up-a, "up/a.bin" inside the run's owned folder (api.json /scenarios/3/fixtures/up-a)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/34/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/34/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/34/expect/attempts
            Binding(
                40,
                "/scenarios/3/steps/34",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up-a"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 41: DELETE /files/{path} (api.json /scenarios/3/steps/35)
            #   owned["up"]: the path of fixture up, "up" inside the run's owned folder (api.json /scenarios/3/fixtures/up)
            #   {"recursive": False}: recursive: api.json /scenarios/3/steps/35/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /scenarios/3/steps/35/expect/status
            Binding(
                41,
                "/scenarios/3/steps/35",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["up"], {"recursive": False}, options
                ),
            ),
            # files.owned-directory-helpers step 42: GET /file_actions/metadata/{path} (api.json /scenarios/3/steps/36)
            #   owned["up"]: the path of fixture up, "up" inside the run's owned folder (api.json /scenarios/3/fixtures/up)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /scenarios/3/steps/36/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /scenarios/3/steps/36/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /scenarios/3/steps/36/expect/attempts
            Binding(
                42,
                "/scenarios/3/steps/36",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["up"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
            # files.owned-directory-helpers step 43: DELETE /files/{path} (api.json /groups/namespace.close/0)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/3/fixtures/folder)
            #   {"recursive": False}: recursive: api.json /groups/namespace.close/0/parameters/recursive
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns None
            #   checks the status of the one API response the call received: api.json /groups/namespace.close/0/expect/status
            Binding(
                43,
                "/groups/namespace.close/0",
                True,
                "DELETE /files/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.delete(
                    owned["folder"], {"recursive": False}, options
                ),
            ),
            # files.owned-directory-helpers step 44: GET /file_actions/metadata/{path} (api.json /groups/namespace.close/1)
            #   owned["folder"]: the path of fixture folder, the run's owned folder (api.json /scenarios/3/fixtures/folder)
            #   {}: no params
            #   options: the step's RequestOptions: the case's absolute deadline (a time.monotonic() value), a request_timeout and a cancel_token of its own
            #   returns File
            #   checks raises exactly files_sdk.error.NotFoundError (a subclass of APIError), whose error_type is the raw JSON type of its one API response: api.json /groups/namespace.close/1/expect/error
            #   checks error.http_status and the status of the one API response the call received: api.json /groups/namespace.close/1/expect/status
            #   checks called again until it raises, at most attempts calls, interval_seconds apart: api.json /groups/namespace.close/1/expect/attempts
            Binding(
                44,
                "/groups/namespace.close/1",
                True,
                "GET /file_actions/metadata/{path}",
                lambda client, options, owned, listed, local_file, local_directory, stream, progress: client.file.find(
                    owned["folder"], {}, options
                ),
                error=files_sdk.error.NotFoundError,
            ),
        ),
    ),
}


@unittest.skipUnless(
    SERVER_URL,
    "needs the shared mock server's api-scenarios-canonical scenario: "
    "python scripts/tasks.py scenarios",
)
class TestApiScenarios(unittest.TestCase):
    """Each case of the definition, against the launcher's simulator."""

    document: Any = None
    out = Path()
    totals: dict[str, Any] = {}

    @classmethod
    def setUpClass(cls):
        cls.document = load_definition()
        with open(
            os.environ["FILES_MOCK_SCENARIO_FILE"], encoding="utf-8"
        ) as preset:
            reset = json.load(preset)["reset"]["profile"]["api_scenarios"]
        if reset.get("definition_sha256") != DEFINITION_SHA256:
            raise Failure(
                f"the launcher's preset resets the server for the definition "
                f"{reset.get('definition_sha256')}, not {DEFINITION_SHA256}"
            )
        ids = [scenario["id"] for scenario in cls.document["scenarios"]]
        if sorted(ids) != sorted(CASES):
            raise Failure(
                f"the definition's scenarios are {ids}, but the cases are {sorted(CASES)}"
            )
        bound = [binding for case in CASES.values() for binding in case.steps]
        counts = (
            len(bound),
            sum(1 for binding in bound if binding.simulator),
            sum(1 for binding in bound if not binding.simulator),
        )
        if counts != (POSITIONS, SIMULATOR, SITE_ONLY):
            raise Failure(
                f"the cases bind {counts} steps, not {(POSITIONS, SIMULATOR, SITE_ONLY)}"
            )
        cls.out = Path(os.environ["FILES_MOCK_OUT"]) / "api-scenarios"
        cls.out.mkdir(parents=True, exist_ok=True)
        cls.totals = {}

    @classmethod
    def tearDownClass(cls):
        cases = cls.totals
        summary = {
            "definition_sha256": DEFINITION_SHA256,
            "positions": POSITIONS,
            "simulator": SIMULATOR,
            "site_only": SITE_ONLY,
            "passed": sum(case["passed"] for case in cases.values()),
            "failed": sum(case["failed"] for case in cases.values()),
            "omitted_site_only": sum(
                case["omitted_site_only"] for case in cases.values()
            ),
            "not_reached": sum(case["not_reached"] for case in cases.values()),
            "cases": cases,
        }
        text = json.dumps(summary, indent=1, ensure_ascii=False)
        (cls.out / "summary.json").write_text(text + "\n", encoding="utf-8")
        counted = ("passed", "failed", "omitted_site_only", "not_reached")
        print(
            "api scenarios:",
            json.dumps({key: summary[key] for key in counted}),
            flush=True,
        )

    def run_case(self, case_id):
        run = CaseRun(self.document, case_id, self.out)
        try:
            run.run()
        finally:
            type(self).totals[case_id] = run.totals()
            print(f"{case_id}: {json.dumps(run.totals())}", flush=True)

    def test_files_owned_folder_namespace(self):
        self.run_case("files.owned-folder-namespace")

    def test_files_owned_binary_roundtrip(self):
        self.run_case("files.owned-binary-roundtrip")

    def test_files_owned_namespace_extended(self):
        self.run_case("files.owned-namespace-extended")

    def test_files_owned_directory_helpers(self):
        self.run_case("files.owned-directory-helpers")


if __name__ == "__main__":
    unittest.main()
