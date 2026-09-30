# SPDX-License-Identifier: Apache-2.0
"""Test vectors for reporter signals that the schemas cannot check.

The signal every_mode_2_record_carries_disclosure_pointer needs the Charter's §4.6.1 declaration,
which the decision-record schema cannot see. This runner applies the signal's rule, as written in
standard/v5.0/conformance/signal-vocabulary.md, to the cases in cases.json and compares the outcome
and the Charter reference with what each case expects. Each record must also be valid against the
decision-record schema. References between schemas are resolved as the files sit in this
repository, because the schemas' $id addresses do not match their locations (known defect KD-01).

Usage:  python tests/reporter-signals/run_checks.py
Exit code 0 = every case behaves as expected, 1 = at least one does not.
"""
import json
import pathlib
import sys
from urllib.parse import urljoin

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
SCHEMA = ROOT / "standard/v5.0/schemas/decision-record.schema.json"
MODES = {"mode-2", "mode-1-with-embedded-mode-2-summary"}
FROM_DRAFTED = {"drafted", "review-required", "closed", "re-opened-with-mode-migration"}


def signal(charter, record):
    """every_mode_2_record_carries_disclosure_pointer, as the vocabulary states it."""
    if record["dispatch_mode"] not in MODES or record["record_state"] not in FROM_DRAFTED:
        return {"outcome": "not_applicable", "charter_reference": None}
    outside = charter["outside_4_6_declared"] or (charter["written_before_v1_1"] and bool(charter.get("transition_record")))
    if outside:
        return {"outcome": "outside_requirement", "charter_reference": charter["reference"]}
    met = bool(record.get("disclosure_metadata_pointer"))
    return {"outcome": "met" if met else "finding", "charter_reference": charter["reference"]}


def file_layout_registry():
    """Every schema under standard/, by its $id and by the address its neighbours' relative $refs give it."""
    files = sorted((ROOT / "standard").rglob("*.json"))
    loaded = {f: json.loads(f.read_text(encoding="utf-8")) for f in files}
    reg = Registry()
    for f, schema in loaded.items():
        reg = reg.with_resource(schema["$id"], Resource.from_contents(schema))

    def refs(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "$ref" and isinstance(v, str) and not v.startswith("#"):
                    yield v
                else:
                    yield from refs(v)
        elif isinstance(node, list):
            for v in node:
                yield from refs(v)

    for f, schema in loaded.items():
        for ref in refs(schema):
            target = (f.parent / ref.split("#")[0]).resolve()
            if target in loaded:
                reg = reg.with_resource(urljoin(schema["$id"], ref.split("#")[0]), Resource.from_contents(loaded[target]))
    return reg


def main():
    data = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")),
                                     registry=file_layout_registry(), format_checker=FormatChecker())
    failed = []
    for case in data["cases"]:
        got = signal(case["charter"], case["record"])
        problems = [e.message[:110] for e in validator.iter_errors(case["record"])]
        if case["record"]["charter_id"] != case["charter"]["charter_id"]:
            problems.append("record's charter_id does not match the case's Charter")
        ok = got == case["expected"] and not problems
        print(f"[{'ok' if ok else 'FAIL':4}] {case['id']:4} {got['outcome']:20} {case['description']}")
        if not ok:
            print(f"       expected {case['expected']}, got {got}; record problems: {problems or 'none'}")
            failed.append(case["id"])
    if failed:
        print(f"\nFAIL: {len(failed)} case(s) misbehave: {', '.join(failed)}")
        return 1
    print(f"\nPASS: {len(data['cases'])} cases for {data['signal']} behave as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
