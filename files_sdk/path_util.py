import io
import json
import os

with io.open(
    os.path.join(os.path.dirname(__file__), "path_comparison.json"),
    encoding="utf-8",
) as comparison_file:
    _COMPARISON_MAP = {
        int(key, 16): value
        for key, value in json.load(comparison_file)["mapping"].items()
    }


def _cleanpath(path_element: str) -> bool:
    return path_element not in ["", ".", ".."]


def is_same(a: str, b: str) -> bool:
    return normalize_for_comparison(a) == normalize_for_comparison(b)


def normalize_for_comparison(path_str: str) -> str:
    return normalize(path_str).translate(_COMPARISON_MAP)


def normalize(path_str: str) -> str:
    return "/".join(
        filter(
            _cleanpath,
            path_str.replace("\x00", "").replace("\\", "/").split("/"),
        )
    )
