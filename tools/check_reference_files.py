# SPDX-License-Identifier: Apache-2.0
"""Validity check for every machine-readable reference file under standard/.

  - every .json file parses (duplicate keys rejected) and is a valid JSON Schema (Draft 2020-12)
  - every .yaml / .yml file parses; an OpenAPI file declares a 3.x version
  - every .md file is valid UTF-8
  - no file type is left unchecked

This checks that each file is well-formed on its own. Whether the files agree with the text
and with each other is reported separately by tests/known-defects/run_checks.py.
Exit code 0 = pass, 1 = fail.
"""
import json
import pathlib
import sys

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"


def no_duplicate_keys(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError(f"duplicate key {k!r}")
        seen[k] = v
    return seen


def main():
    problems, counts = [], {}
    files = sorted(p for p in (ROOT / "standard").rglob("*") if p.is_file())
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        suffix = p.suffix.lower() if p.name != "LICENSE" else "LICENSE"
        counts[suffix] = counts.get(suffix, 0) + 1
        try:
            raw = p.read_bytes()
            text = raw.decode("utf-8")
            if suffix == ".json":
                doc = json.loads(text, object_pairs_hook=no_duplicate_keys)
                if doc.get("$schema") != DRAFT_2020_12:
                    problems.append(f"{rel}: $schema is not Draft 2020-12")
                Draft202012Validator.check_schema(doc)
                print(f"[ok] {rel}: valid JSON Schema 2020-12 ($id {doc.get('$id')})")
            elif suffix in (".yaml", ".yml"):
                doc = yaml.safe_load(text)
                if "openapi" in doc and not str(doc["openapi"]).startswith("3."):
                    problems.append(f"{rel}: OpenAPI version is not 3.x")
                print(f"[ok] {rel}: parses" + (f" (OpenAPI {doc['openapi']})" if "openapi" in doc else ""))
            elif suffix in (".md", "LICENSE"):
                print(f"[ok] {rel}: UTF-8 text")
            else:
                problems.append(f"{rel}: no check defined for this file type")
        except (ValueError, SchemaError, yaml.YAMLError, UnicodeDecodeError) as exc:
            problems.append(f"{rel}: {type(exc).__name__}: {str(exc)[:200]}")
    print("\nfiles checked by type:", counts)
    if problems:
        print("FAIL")
        for p in problems:
            print("  -", p)
        return 1
    print("PASS: every reference file is well-formed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
