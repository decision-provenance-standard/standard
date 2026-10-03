# SPDX-License-Identifier: Apache-2.0
"""Checks for the portable verification extension, version 0.1.0 (a proposal).

Runs the cases in cases.json:

  schema cases   base_export or base_report, changed by a patch, against the extension's schemas
  digest cases   SHA-256 over exact bytes: seals, mutation, re-serialisation, the seal field itself
  chain cases    the link rule: omission, reordering, truncation, and which checkpoints count
  statement      the reference check of an entry's statements outside the seal, over its covered bytes
  pairing        a report read with its export: one entry result per export entry (JSON Schema cannot
                 compare two documents)
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
READABLE = {"application/json"}  # media types the reference statement check reads
PREDECESSORS = ("supersedes", "target_record_hash", "target_decision_id")
ZEROED = '"seal_hash":"' + "0" * 64 + '"'
# An example of signed bytes that bind the profile, its version and the key reference, as in the
# prototype behind the proposal. Version 0.1.0 of the extension does not fix a signature suite.
EXAMPLE_DOMAIN = b"dps-portable-verification\x000.1.0\x00"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def next_link(previous_hex, digest_hex):
    previous = bytes.fromhex(previous_hex) if previous_hex else ZERO_LINK
    return hashlib.sha256(previous + bytes.fromhex(digest_hex)).hexdigest()


def locate(doc, pointer):
    """The container and the key or index that a JSON Pointer names."""
    *parents, last = [p.replace("~1", "/").replace("~0", "~") for p in pointer.split("/")[1:]]
    for p in parents:
        doc = doc[int(p)] if isinstance(doc, list) else doc[p]
    return doc, (int(last) if isinstance(doc, list) else last)


def apply_patch(doc, patch):
    """Each operation sets, removes or copies the member at a JSON Pointer."""
    doc = copy.deepcopy(doc)
    for op in patch:
        if "remove" in op:
            parent, key = locate(doc, op["remove"])
            del parent[key]
            continue
        if "copy" in op:
            parent, key = locate(doc, op["copy"])
            value, pointer = parent[key], op["to"]
        else:
            value, pointer = op["value"], op["set"]
        parent, key = locate(doc, pointer)
        parent[key] = copy.deepcopy(value)
    return doc


def strict_json(raw):
    """UTF-8 JSON with duplicate keys and non-finite numbers rejected."""
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError(f"duplicate key {k!r}")
            out[k] = v
        return out

    def constant(name):
        raise ValueError(f"not JSON: {name}")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)


def statement_check(entry):
    """Reference check: an export entry's statements that sit outside the seal, against its covered bytes."""
    if entry["content"]["availability"] != "available":
        return "not_checked", ["the covered bytes are unavailable"]
    if entry["covered_representation"]["media_type"] not in READABLE:
        return "not_checked", ["this check cannot read the media type"]
    try:
        record = strict_json(base64.b64decode(entry["content"]["covered_bytes_b64"], validate=True))
    except ValueError as exc:
        return "not_checked", [f"the covered bytes cannot be read: {exc}"]
    if not isinstance(record, dict):
        return "not_checked", ["the covered bytes are not a JSON object"]
    wrong, notes = [], []
    if record.get("decision_id") != entry["decision_id"]:
        wrong.append("decision_id")
    if "record_type" not in record:
        notes.append("record_type is absent from the covered bytes and read as decision (Core §6.2)")
    if record.get("record_type", "decision") != entry["record_type"]:
        wrong.append("record_type")
    stated = entry.get("predecessors", {})
    for k in PREDECESSORS:
        a, b = record.get(k), stated.get(k)
        if k == "target_record_hash" and isinstance(a, str):
            a = a.lower()  # the export carries hex in lowercase
        if a != b:
            wrong.append(k)
    seal = entry.get("seal")
    if seal:
        value = record.get("seal_hash")
        if seal["seal_field_handling"] == "seal_hash_absent":
            handled = "seal_hash" not in record
        else:  # seal_hash_zeroed: a non-empty value made only of 0; other placeholders are not covered
            handled = isinstance(value, str) and value != "" and set(value) == {"0"}
        if not handled:
            wrong.append("seal_field_handling")
        if ("affirmation_record" in record) != seal["affirmation_record_covered"]:
            wrong.append("affirmation_record_covered")
    if wrong:
        return "failed", ["does not match the covered bytes: " + ", ".join(wrong)] + notes
    return "verified", notes


def read_with_export(report, export):
    """What a reader holding a report and its export checks; JSON Schema cannot compare two documents."""
    entries, results = export["entries"], report["entries"]
    problems = []
    if report["export_entry_count"] != len(entries):
        problems.append(f"export_entry_count is {report['export_entry_count']}; the export has {len(entries)} entries")
    indexes = sorted(r["export_index"] for r in results)
    if indexes != list(range(len(entries))):
        problems.append(f"results name export entries {indexes}; each of 0 to {len(entries) - 1} must appear once")
    for r in results:
        i = r["export_index"]
        if i >= len(entries):
            continue
        e = entries[i]
        if r["decision_id"] != e["decision_id"]:
            problems.append(f"entry {i}: decision_id differs from the export entry's")
        if (r["representation"] == "derived") != ("derived_from" in e):
            problems.append(f"entry {i}: representation differs from the export entry")
        if "seal" in e and r["statement_check"].get("affirmation_record_covered") != e["seal"]["affirmation_record_covered"]:
            problems.append(f"entry {i}: affirmation_record_covered not carried through")
        if r["statement_check"]["status"] == "verified" and statement_check(e)[0] != "verified":
            problems.append(f"entry {i}: statements reported verified, but they do not match the covered bytes")
    return problems


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


def statement_case(c, data, validators):
    export = apply_patch(data["base_export"], c["patch"])
    entry = export["entries"][c["entry"]]
    if "bytes_from" in c:
        entry["content"]["covered_bytes_b64"] = base64.b64encode(data["records"][c["bytes_from"]]["text"].encode()).decode()
    if list(validators["export"].iter_errors(export)):
        return "error", "the export must be schema-valid for this case"
    status, findings = statement_check(entry)
    if entry["content"]["availability"] != "available":
        seal = "unavailable"
    else:
        raw = base64.b64decode(entry["content"]["covered_bytes_b64"], validate=True)
        seal = "match" if sha256(raw) == entry["seal"]["seal_hash"] else "mismatch"
    return {"statements": status, "seal": seal}, "; ".join(findings)


def pairing_case(c, data, validators):
    report = apply_patch(data["base_report"], c["report_patch"])
    export = apply_patch(data["base_export"], c["export_patch"])
    if list(validators["report"].iter_errors(report)) or list(validators["export"].iter_errors(export)):
        return "error", "both documents must be schema-valid for this case"
    problems = read_with_export(report, export)
    return ("inconsistent" if problems else "consistent"), "; ".join(problems)


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
        ("statement", data["statement_cases"], lambda c: statement_case(c, data, validators)),
        ("pairing", data["pairing_cases"], lambda c: pairing_case(c, data, validators)),
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
            print(f"[{'ok' if ok else 'FAIL':4}] {c['id']:4} {label:9} {c['description']}")
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
