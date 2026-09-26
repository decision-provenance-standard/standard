# SPDX-License-Identifier: Apache-2.0
"""Known-defects report for the reference files.

Runs the synthetic records in cases.json through the schemas in standard/ with a standard
JSON Schema validator (Draft 2020-12) and compares the result with what the Standard's text says.

  control cases        must behave as expected; a mismatch fails (exit 1)
  known-defect cases   while the defect is 'open', a mismatch is reported only (exit 0);
                       once the defect is marked 'fixed', its cases are enforced like controls

Usage:  python tests/known-defects/run_checks.py
"""
import json
import pathlib
import sys

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent


def load_registry():
    schemas, reg = {}, Registry()
    for p in sorted((ROOT / "standard").rglob("*.json")):
        s = json.loads(p.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(s)
        rel = p.relative_to(ROOT).as_posix()
        schemas[rel] = s
        reg = reg.with_resource(s["$id"], Resource.from_contents(s))
    return schemas, reg


def outcome(schema, reg, instance):
    v = Draft202012Validator(schema, registry=reg, format_checker=FormatChecker())
    try:
        errs = list(v.iter_errors(instance))
    except Exception as exc:  # e.g. a reference that cannot be resolved
        return "fail", [f"{type(exc).__name__}: {str(exc)[:120]}"]
    return ("pass" if not errs else "fail"), [e.message[:110] for e in errs]


def main():
    data = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    schemas, reg = load_registry()
    defects = data["defects"]
    blocking, still_open, looks_fixed = [], {}, set()
    for c in data["cases"]:
        got, msgs = outcome(schemas[c["schema"]], reg, c["instance"])
        ok = got == c["expected"] and not (c["must_not_mention"] and any(c["must_not_mention"] in m for m in msgs))
        enforced = c["kind"] == "control" or defects.get(c["defect"], {}).get("status") == "fixed"
        tag = "ok" if ok else ("FAIL" if enforced else "known")
        print(f"[{tag:5}] {c['id']:4} {c['kind']:12} {c['defect'] or '':6} {c['description']}")
        if not ok:
            print(f"         expected {c['expected']}, got {got}: {'; '.join(msgs[:2])}")
            if enforced:
                blocking.append(c["id"])
            else:
                still_open.setdefault(c["defect"], []).append(c["id"])
        elif c["kind"] == "known-defect" and not enforced:
            looks_fixed.add(c["defect"])

    print("\nKnown defects (reference release vs the text):")
    for k, d in defects.items():
        state = d["status"]
        if state == "open" and k in still_open:
            state = f"open, still present (cases {', '.join(still_open[k])})"
        elif state == "open" and k in looks_fixed:
            state = "open, but its cases now behave as the text says: mark it 'fixed' in cases.json"
        print(f"  {k}: {state}. {d['summary']}")
    if blocking:
        print(f"\nFAIL: {len(blocking)} enforced case(s) misbehave: {', '.join(blocking)}")
        return 1
    print("\nPASS (report mode): every control behaves as expected; open known defects are reported above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
