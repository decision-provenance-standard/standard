# SPDX-License-Identifier: Apache-2.0
"""Checks for the portable verification extension, version 0.1.0 (a proposal).

Runs the cases in cases.json:

  schema cases   base_export or base_report, changed by a patch, against the extension's schemas
  digest cases   SHA-256 over exact bytes: seals, mutation, re-serialisation, the seal field itself
  chain cases    the link rule: omission, reordering, truncation, and which checkpoints count
  trust cases    where the verifier takes the issuer's key from (labels only: no keys, no signatures)

Standard library and jsonschema only. Signature vectors are future work.

Usage:  python extensions/portable-verification/tests/run_checks.py
Exit code 0 = every case behaves as expected, 1 = a case does not.
"""
import base64
import copy
import hashlib
import json
import pathlib
import sys

from jsonschema import Draft202012Validator

HERE = pathlib.Path(__file__).resolve().parent
SCHEMAS = {
    "export": HERE.parent / "schemas" / "verification-export.schema.json",
    "report": HERE.parent / "schemas" / "verification-report.schema.json",
}
ZERO_LINK = bytes(32)
ZEROED = '"seal_hash":"' + "0" * 64 + '"'
# An example of signed bytes that bind the profile, its version and the key reference, as in the
# prototype behind the proposal. Version 0.1.0 of the extension does not fix a signature suite.
EXAMPLE_DOMAIN = b"dps-portable-verification\x000.1.0\x00"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def next_link(previous_hex, digest_hex):
    previous = bytes.fromhex(previous_hex) if previous_hex else ZERO_LINK
    return hashlib.sha256(previous + bytes.fromhex(digest_hex)).hexdigest()


def apply_patch(doc, patch):
    """Each operation sets or removes the member at a JSON Pointer."""
    doc = copy.deepcopy(doc)
    for op in patch:
        pointer = op["set"] if "set" in op else op["remove"]
        *parents, last = [p.replace("~1", "/").replace("~0", "~") for p in pointer.split("/")[1:]]
        target = doc
        for p in parents:
            target = target[int(p)] if isinstance(target, list) else target[p]
        key = int(last) if isinstance(target, list) else last
        if "set" in op:
            target[key] = copy.deepcopy(op["value"])
        else:
            del target[key]
    return doc


def schema_case(c, data, validators):
    instance = apply_patch(data["base_" + c["schema"]], c["patch"])
    errors = list(validators[c["schema"]].iter_errors(instance))
    msgs = [f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message[:100]}" for e in errors]
    return ("pass" if not errors else "fail"), msgs


def digest_case(c, data):
    recs, chain = data["records"], data["chain"]
    kind = c["check"]
    if kind == "known_vector":
        return ("match" if sha256(c["text"].encode()) == c["digest"] else "mismatch"), ""
    if kind == "record_seals":
        bad = [k for k, r in recs.items() if sha256(r["text"].encode()) != r["seal_hash"]]
        return ("mismatch" if bad else "match"), ", ".join(bad)
    if kind == "chain_links":
        got, head = [], None
        for k in chain["order"]:
            head = next_link(head, recs[k]["seal_hash"])
            got.append(head)
        return ("match" if got == chain["links"] else "mismatch"), ""
    if kind == "base_export":
        problems = []
        for i, e in enumerate(data["base_export"]["entries"]):
            raw = base64.b64decode(e["content"]["covered_bytes_b64"], validate=True)
            if raw != recs[chain["order"][i]]["text"].encode():
                problems.append(f"entry {i}: bytes")
            if sha256(raw) != e["seal"]["seal_hash"]:
                problems.append(f"entry {i}: seal")
            if e["chain"]["previous_link"] != (chain["links"][i - 1] if i else None):
                problems.append(f"entry {i}: previous_link")
        return ("mismatch" if problems else "match"), "; ".join(problems)

    rec = recs[c["record"]]
    text, note = rec["text"], ""
    if "edit" in c:
        found = text.count(c["edit"]["replace"])
        if found != 1:
            raise ValueError(f"the edit must match once; it matches {found} times")
        text = text.replace(c["edit"]["replace"], c["edit"]["with"])
    if "reserialise" in c:
        value = json.loads(text)
        if c["reserialise"] == "indent_2":
            text = json.dumps(value, indent=2)
        else:
            text = json.dumps(value, sort_keys=True, separators=(",", ":"))
        if json.loads(text) != json.loads(rec["text"]) or text == rec["text"]:
            raise ValueError("the copy must be equal as JSON and differ in bytes")
        note = "equal as JSON: yes"
    if kind == "seal":
        return ("match" if sha256(text.encode()) == rec["seal_hash"] else "mismatch"), note
    if kind == "reseal":
        # Whoever changed the record also replaces the seal in the export with one over the new bytes.
        new_seal = sha256(text.encode())
        same_export = "match" if sha256(text.encode()) == new_seal else "mismatch"
        original = "match" if new_seal == rec["seal_hash"] else "mismatch"
        return {"same_export_seal": same_export, "original_seal": original}, ""
    if kind == "zeroed_seal":
        if text.count(ZEROED) != 1:
            raise ValueError("the record must carry one zeroed seal_hash")
        stored = text.replace(ZEROED, '"seal_hash":"' + rec["seal_hash"] + '"')
        hashed = stored.replace('"seal_hash":"' + rec["seal_hash"] + '"', ZEROED) if c["hash_as"] == "zeroed" else stored
        return ("match" if sha256(hashed.encode()) == rec["seal_hash"] else "mismatch"), ""
    raise ValueError(f"unknown check {kind!r}")


def chain_case(c, data):
    order, links = data["chain"]["order"], data["chain"]["links"]
    # Each supplied entry keeps the seal and the previous link it was exported with.
    entries = [(data["records"][order[i]]["seal_hash"], links[i - 1] if i else None) for i in c["supplied"]]
    head = None
    for seal, previous_link in entries:
        if previous_link != head:
            return "inconsistent", ""
        head = next_link(head, seal)
    cp = c["checkpoint"]
    if cp is None or cp["source"] != "independent":
        return "consistent", "completeness not established"
    if (cp["count"], cp["head_link"]) == (len(entries), head):
        return "consistent_with_checkpoint", ""
    return "inconsistent_with_checkpoint", ""


def select_key(policy, key_ref, export_key_material=None):
    """The key comes only from the verifier's own policy; key material in the export is ignored."""
    del export_key_material
    key = policy["trusted_keys"].get(key_ref)
    return {"trust": "trusted" if key else "untrusted", "key": key}


def signed_bytes(key_ref, payload):
    k = key_ref.encode("utf-8")
    return EXAMPLE_DOMAIN + len(k).to_bytes(4, "big") + k + len(payload).to_bytes(8, "big") + payload


def trust_case(c, data):
    if c["check"] == "select_key":
        return select_key(data["trust_policy"], c["key_ref"], c.get("export_key_material")), ""
    if c["check"] == "signed_bytes":
        payload = data["records"][c["record"]]["text"].encode()
        variants = {signed_bytes(k, payload) for k in c["key_refs"]}
        return ("differ" if len(variants) == len(c["key_refs"]) else "same"), ""
    raise ValueError(f"unknown check {c['check']!r}")


def main():
    data = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    validators = {}
    for name, p in SCHEMAS.items():
        schema = json.loads(p.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(schema)
        print(f"[ok  ] schemas/{p.name}: valid JSON Schema 2020-12")

    groups = [
        ("schema", data["schema_cases"], lambda c: schema_case(c, data, validators)),
        ("digest", data["digest_cases"], lambda c: digest_case(c, data)),
        ("chain", data["chain_cases"], lambda c: chain_case(c, data)),
        ("trust", data["trust_cases"], lambda c: trust_case(c, data)),
    ]
    failed, total, limits = [], 0, []
    for group, cases, run in groups:
        print(f"\n{group} cases:")
        for c in cases:
            total += 1
            try:
                got, detail = run(c)
            except Exception as exc:  # a malformed case fails, it does not stop the run
                got, detail = "error", f"{type(exc).__name__}: {exc}"
            ok = got == c["expected"]
            label = c.get("schema", group)
            print(f"[{'ok' if ok else 'FAIL':4}] {c['id']:4} {label:6} {c['description']}")
            if not ok:
                failed.append(c["id"])
                shown = "; ".join(detail[:2]) if isinstance(detail, list) else detail
                print(f"         expected {c['expected']}, got {got}" + (f": {shown}" if shown else ""))
            if c.get("limitation"):
                limits.append((c["id"], c["limitation"]))

    print("\nLimitations these cases show (they pass by design):")
    for cid, text in limits:
        print(f"  {cid}: {text}")
    print("  Signatures are not tested here: signature vectors across languages are future work.")
    if failed:
        print(f"\nFAIL: {len(failed)} of {total} case(s) do not behave as expected: {', '.join(failed)}")
        return 1
    print(f"\nPASS: all {total} cases behave as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
