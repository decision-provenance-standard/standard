# SPDX-License-Identifier: Apache-2.0
"""Checks for the action binding extension, version 0.1.0 (a proposal).

Runs the cases in cases.json:

  schema cases    a base attachment or the base report, changed by a patch, against the extension's
                  schemas; and the fixture records against the core decision-record schema
  digest cases    SHA-256 over the exact bytes of action specifications: changes and re-serialisation
  binding cases   the reference check of one attachment, with or without its decision record
  pairing cases   a report read with its attachments: one result per attachment, per specification and
                  per attempt (JSON Schema cannot compare two documents)

Standard library and jsonschema only. Times are the issuer's; the cases include no signature.

Usage:  python extensions/action-binding/tests/run_checks.py
Exit code 0 = every case behaves as expected, 1 = a case does not.
"""
import base64
import copy
import hashlib
import json
import pathlib
import sys
from datetime import datetime

from jsonschema import Draft202012Validator

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCHEMAS = {
    "attachment": HERE.parent / "schemas" / "execution-evidence.schema.json",
    "report": HERE.parent / "schemas" / "verification-report.schema.json",
}
CORE_RECORD_SCHEMA = ROOT / "standard" / "v5.0" / "schemas" / "decision-record.schema.json"
READABLE = {"application/json"}  # media types the reference statement checks read
SPEC_MEMBERS = ("operation", "target", "parameters", "input_version_refs", "policy_version")
SUMMARY_MEMBERS = ("operation", "target", "policy_version", "input_version_refs")
DIMENSIONS = (
    "specification_digests", "specification_statements", "record_statements", "action_binding",
    "stage_order", "authorisation_recheck", "observed_results", "rationale_provenance",
)
RANK = {"verified": 0, "not_checked": 1, "unavailable": 2, "failed": 3}
REFS = ("review_ref", "from_ref", "authorised_by", "request_ref", "recheck_ref", "attempt_ref")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def when(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def locate(doc, pointer):
    """The container and the key or index that a JSON Pointer names."""
    *parents, last = [p.replace("~1", "/").replace("~0", "~") for p in pointer.split("/")[1:]]
    for p in parents:
        doc = doc[int(p)] if isinstance(doc, list) else doc[p]
    return doc, (int(last) if isinstance(doc, list) else last)


def apply_patch(doc, patch):
    """Each operation sets, removes, copies, inserts or moves the member at a JSON Pointer."""
    doc = copy.deepcopy(doc)
    for op in patch:
        if "remove" in op:
            parent, key = locate(doc, op["remove"])
            del parent[key]
        elif "insert" in op:
            parent, key = locate(doc, op["insert"])
            parent.insert(key, copy.deepcopy(op["value"]))
        elif "move" in op:
            parent, key = locate(doc, op["move"])
            value = parent.pop(key)
            parent, key = locate(doc, op["to"])
            parent.insert(key, value)
        else:
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


def check_specification(spec):
    """One specification: its bytes against its digest, and its summary (outside the digest) against its bytes."""
    if spec["content"]["availability"] != "available":
        return ("unavailable", ["the bytes are unavailable"]), ("not_checked", ["the bytes are unavailable"])
    raw = base64.b64decode(spec["content"]["bytes_b64"], validate=True)
    digest = ("verified", []) if sha256(raw) == spec["spec_digest"] else ("failed", ["the bytes do not match spec_digest"])
    if spec["representation"]["media_type"] not in READABLE:
        return digest, ("not_checked", ["this check cannot read the media type"])
    try:
        body = strict_json(raw)
    except ValueError as exc:
        return digest, ("not_checked", [f"the bytes cannot be read: {exc}"])
    if not isinstance(body, dict):
        return digest, ("not_checked", ["the bytes are not a JSON object"])
    wrong = [m for m in SPEC_MEMBERS if m not in body]
    wrong += [m for m in SUMMARY_MEMBERS if m in body and body[m] != spec["summary"][m]]
    if wrong:
        return digest, ("failed", ["the summary does not match the bytes: " + ", ".join(wrong)])
    return digest, ("verified", [])


def check_record(att, record_raw):
    """The stages' statements about core fields, against the decision record the verifier holds."""
    if record_raw is None:
        return "not_checked", ["the decision record was not supplied"]
    try:
        record = strict_json(record_raw)
    except ValueError as exc:
        return "not_checked", [f"the record cannot be read: {exc}"]
    if not isinstance(record, dict):
        return "not_checked", ["the record is not a JSON object"]
    wrong = []
    if record.get("decision_id") != att["decision_id"]:
        wrong.append("decision_id")
    for s in att["stages"]:
        if s["kind"] == "proposal" and s["origin"] == "ai":
            if (record.get("drafting_authority") or {}).get("deployer_role_pointer") != s["deployer_role_pointer"]:
                wrong.append(f"{s['stage_id']}: drafting_authority")
        if s["kind"] != "outcome" or "core_ref" not in s:
            continue
        ref = s["core_ref"]
        if ref["field"] == "affirmation_record":
            a = record.get("affirmation_record") or {}
            pairs = [("actor_identity", "actor_ref"), ("timestamp", "at"), ("method", "method")]
        else:
            log = record.get("review_log") or []
            a = log[ref["index"]] if ref["index"] < len(log) else {}
            pairs = [("reviewer", "actor_ref"), ("reviewed_at", "at"), ("outcome", "outcome")]
        for core_key, stage_key in pairs:
            if a.get(core_key) != s[stage_key]:
                wrong.append(f"{s['stage_id']}: {ref['field']}.{core_key}")
    if wrong:
        return "failed", ["does not match the decision record: " + ", ".join(wrong)]
    return "verified", []


def check_attachment(att, record_raw=None):
    """Reference check of one schema-valid attachment. Every dimension is reported on its own."""
    stages = att["stages"]
    pos, by_id, dupes = {}, {}, []
    for i, s in enumerate(stages):
        if s["stage_id"] in by_id:
            dupes.append(s["stage_id"])
            continue
        pos[s["stage_id"]], by_id[s["stage_id"]] = i, s
    kinds = {k: [s for s in stages if s["kind"] == k] for k in
             ("outcome", "change_authorisation", "request", "recheck", "attempt", "result")}
    out = {}

    # Specifications: each digest, and each summary, on its own; the dimension keeps the worst status.
    per_spec = [check_specification(spec) for spec in att["action_specifications"]]
    for n, dim in enumerate(("specification_digests", "specification_statements")):
        results = [r[n] for r in per_spec]
        status = max((r[0] for r in results), key=RANK.get)
        out[dim] = (status, [f"specification {i}: {f}" for i, r in enumerate(results) for f in r[1]])
    out["record_statements"] = check_record(att, record_raw)

    # Binding: what was shown, approved, requested and attempted is the same specification.
    bad = []
    carried = {spec["spec_digest"] for spec in att["action_specifications"]}
    for s in stages:
        for key in ("spec_digest", "shown_spec_digest", "approved_spec_digest"):
            if key in s and s[key] not in carried:
                bad.append(f"{s['stage_id']}: names a specification the attachment does not carry")

    def ref(s, key, kind):
        target = by_id.get(s[key])
        if target is None or target["kind"] not in kind:
            bad.append(f"{s['stage_id']}: {key} names no {' or '.join(kind)} stage")
            return None
        return target

    bound = {}  # stage id of an approval or authorised change -> (digest it binds, request limit)
    for s in kinds["outcome"]:
        review = ref(s, "review_ref", ("review",))
        if review and s["actor_ref"] != review["reviewer_ref"]:
            bad.append(f"{s['stage_id']}: the outcome is not given by the person shown the specification")
        if s["outcome"] == "approved":
            if review and s["approved_spec_digest"] != review["shown_spec_digest"]:
                bad.append(f"{s['stage_id']}: the approved specification differs from the one shown")
            bound[s["stage_id"]] = (s["approved_spec_digest"], s.get("request_limit", 1))
    for s in kinds["change_authorisation"]:
        source = ref(s, "from_ref", ("outcome", "change_authorisation"))
        if source is None:
            continue
        if source["stage_id"] not in bound:
            bad.append(f"{s['stage_id']}: changes an outcome that is not an approval")
            continue
        bound[s["stage_id"]] = (s["spec_digest"], s.get("request_limit", 1))
    seen_ids, uses = set(), {}
    for s in kinds["request"]:
        if s["request_id"] in seen_ids:
            bad.append(f"{s['stage_id']}: duplicate request_id {s['request_id']!r}")
        seen_ids.add(s["request_id"])
        auth = ref(s, "authorised_by", ("outcome", "change_authorisation"))
        if auth is None:
            continue
        if auth["stage_id"] not in bound:
            bad.append(f"{s['stage_id']}: rests on {auth['stage_id']} ({auth.get('outcome', 'unbound change')}); only "
                       "an approval or an authorised change authorises a request")
            continue
        digest, limit = bound[auth["stage_id"]]
        uses[auth["stage_id"]] = uses.get(auth["stage_id"], 0) + 1
        if uses[auth["stage_id"]] > limit:
            bad.append(f"{s['stage_id']}: {auth['stage_id']} covers {limit} request(s)")
        if s["spec_digest"] != digest:
            bad.append(f"{s['stage_id']}: the requested specification differs from the one approved")
    for s in kinds["attempt"]:
        request = ref(s, "request_ref", ("request",))
        if request and s["spec_digest"] != request["spec_digest"]:
            bad.append(f"{s['stage_id']}: the attempted specification differs from the one requested")
    out["action_binding"] = ("failed", bad) if bad else ("verified", [])

    # Order: each stage comes after the stages it names, in the list and in the issuer's times.
    bad = [f"stage_id {d!r} is used more than once" for d in dupes]
    for s in stages:
        for key in REFS:
            target = by_id.get(s.get(key))
            if target is None or s["stage_id"] in dupes:
                continue
            if pos[target["stage_id"]] > pos.get(s["stage_id"], -1):
                bad.append(f"{s['stage_id']} is listed before {target['stage_id']}, which it names")
            elif when(target["at"]) > when(s["at"]):
                bad.append(f"{s['stage_id']} is dated before {target['stage_id']}, which it names")
    out["stage_order"] = ("failed", bad) if bad else ("verified", [])

    # Recheck: the latest recheck of the request before each attempt authorises it, and serves only it.
    bad, used = [], {}
    for s in kinds["attempt"]:
        rc = by_id.get(s["recheck_ref"])
        if rc is None or rc["kind"] != "recheck" or rc["request_ref"] != s["request_ref"]:
            bad.append(f"{s['stage_id']}: no recheck of its request is recorded")
            continue
        if pos[rc["stage_id"]] > pos[s["stage_id"]] or when(rc["at"]) > when(s["at"]):
            bad.append(f"{s['stage_id']}: the recheck comes after the attempt")
        if rc["result"] != "authorised":
            bad.append(f"{s['stage_id']}: attempted after a recheck that found {rc['result']}")
        later = [r for r in kinds["recheck"] if r["request_ref"] == s["request_ref"]
                 and pos[rc["stage_id"]] < pos.get(r["stage_id"], -1) < pos[s["stage_id"]]]
        if any(r["result"] != "authorised" for r in later):
            bad.append(f"{s['stage_id']}: a later recheck before the attempt did not authorise it")
        if rc["stage_id"] in used:
            bad.append(f"{s['stage_id']}: reuses the recheck of {used[rc['stage_id']]}")
        used[rc["stage_id"]] = s["stage_id"]
    if bad:
        out["authorisation_recheck"] = ("failed", bad)
    elif kinds["attempt"] or kinds["recheck"]:
        out["authorisation_recheck"] = ("verified", [])
    else:
        out["authorisation_recheck"] = ("not_checked", ["no recheck or attempt is recorded"])

    # Results: exactly one observed result for each attempt, carried through as recorded.
    bad, observed = [], []
    attempt_ids = {s["stage_id"] for s in kinds["attempt"]}
    for r in kinds["result"]:
        if r["attempt_ref"] not in attempt_ids:
            bad.append(f"{r['stage_id']}: names no attempt")
    for s in kinds["attempt"]:
        found = [r["observed"] for r in kinds["result"] if r["attempt_ref"] == s["stage_id"]]
        value = found[0] if len(found) == 1 else ("missing" if not found else "multiple")
        if value in ("missing", "multiple"):
            bad.append(f"{s['stage_id']}: {'no' if value == 'missing' else 'more than one'} observed result")
        observed.append([s["stage_id"], value])
    if bad:
        out["observed_results"] = ("failed", bad)
    elif kinds["attempt"]:
        out["observed_results"] = ("verified", [])
    else:
        out["observed_results"] = ("not_checked", ["no execution attempt is recorded"])
    out["execution_state"] = ("attempted" if kinds["attempt"] else
                              "requested_not_attempted" if kinds["request"] else "not_requested")
    out["observed"] = observed

    # Rationale: a rationale recorded after its outcome is never presented as contemporaneous.
    bad = []
    for s in kinds["outcome"] + kinds["change_authorisation"]:
        r = s["rationale"]
        if r["timing"] == "contemporaneous" and when(r["recorded_at"]) > when(s["at"]):
            bad.append(f"{s['stage_id']}: recorded after the outcome, presented as contemporaneous")
        if r["timing"] == "later_supplemented" and when(r["recorded_at"]) <= when(s["at"]):
            bad.append(f"{s['stage_id']}: said to be supplemented later, but dated with the outcome")
    out["rationale_provenance"] = ("failed", bad) if bad else ("verified", [])
    out["per_spec"] = per_spec
    return out


def record_bytes(data, name):
    return None if name is None else data["records"][name].encode("utf-8")


def schema_case(c, data, validators):
    if c["schema"] == "core_record":
        instance = json.loads(data["records"][c["record"]])
    else:
        base = data["base_attachments"][c["base"]] if c["schema"] == "attachment" else data["base_report"]
        instance = apply_patch(base, c["patch"])
    errors = list(validators[c["schema"]].iter_errors(instance))
    msgs = [f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message[:100]}" for e in errors]
    return ("pass" if not errors else "fail"), msgs


def digest_case(c, data):
    specs = data["specifications"]
    if c["check"] == "known_vector":
        return ("match" if sha256(c["text"].encode()) == c["digest"] else "mismatch"), ""
    if c["check"] == "spec_digests":
        bad = [k for k, s in specs.items() if sha256(s["text"].encode()) != s["spec_digest"]]
        return ("mismatch" if bad else "match"), ", ".join(bad)
    if c["check"] == "base_attachments":
        problems = []
        for name, att in data["base_attachments"].items():
            for i, spec in enumerate(att["action_specifications"]):
                raw = base64.b64decode(spec["content"]["bytes_b64"], validate=True)
                if raw != specs[c["carries"][name][i]]["text"].encode() or sha256(raw) != spec["spec_digest"]:
                    problems.append(f"{name} specification {i}")
        return ("mismatch" if problems else "match"), "; ".join(problems)
    if c["check"] != "spec":
        raise ValueError(f"unknown check {c['check']!r}")
    spec = specs[c["spec"]]
    text, note = spec["text"], ""
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
        if json.loads(text) != json.loads(spec["text"]) or text == spec["text"]:
            raise ValueError("the copy must be equal as JSON and differ in bytes")
        note = "equal as JSON: yes"
    # Compared with the specification's own digest, or with a named variant's (a one-change copy of it).
    against = specs[c.get("variant", c["spec"])]["spec_digest"]
    return ("match" if sha256(text.encode()) == against else "mismatch"), note


def binding_case(c, data, validators):
    att = apply_patch(data["base_attachments"][c["attachment"]], c["patch"])
    errors = list(validators["attachment"].iter_errors(att))
    if errors:
        return "error", f"the attachment must be schema-valid for this case: {errors[0].message[:120]}"
    got = check_attachment(att, record_bytes(data, c["record"]))
    findings = [f"{d}: {f}" for d in DIMENSIONS for f in got[d][1]]
    summary = {d: got[d][0] for d in DIMENSIONS}
    summary["execution_state"] = got["execution_state"]
    if "observed" in c["expected"]:
        summary["observed"] = got["observed"]
    return summary, "; ".join(findings)


def expected_binding(c):
    """Every dimension is expected verified, with an attempt, unless the case says otherwise."""
    full = {d: "verified" for d in DIMENSIONS}
    full["execution_state"] = "attempted"
    full.update(c["expected"])
    return full


def read_with_attachments(report, attachments, records):
    """What a reader holding a report and its attachments checks; JSON Schema cannot compare two documents."""
    problems = []
    if report["attachment_count"] != len(attachments):
        problems.append(f"attachment_count is {report['attachment_count']}; there are {len(attachments)} attachments")
    indexes = sorted(r["attachment_index"] for r in report["results"])
    if indexes != list(range(len(attachments))):
        problems.append(f"results name attachments {indexes}; each of 0 to {len(attachments) - 1} must appear once")
    for r in report["results"]:
        i = r["attachment_index"]
        if i >= len(attachments):
            continue
        a = attachments[i]
        if r["decision_id"] != a["decision_id"]:
            problems.append(f"result {i}: decision_id differs from the attachment's")
        ref = check_attachment(a, records.get(a["decision_id"]))
        specs = a["action_specifications"]
        if sorted(s["spec_index"] for s in r["specifications"]) != list(range(len(specs))):
            problems.append(f"result {i}: one specification result for each of its {len(specs)} specifications")
        for s in r["specifications"]:
            k = s["spec_index"]
            if k >= len(specs):
                continue
            if s["spec_digest"] != specs[k]["spec_digest"]:
                problems.append(f"result {i}: specification {k} digest differs from the attachment's")
            for n, key in enumerate(("digest", "statements")):
                if s[key]["status"] == "verified" and ref["per_spec"][k][n][0] != "verified":
                    problems.append(f"result {i}: specification {k} {key} reported verified, but it is not")
        for key in ("record_statements", "action_binding", "stage_order", "authorisation_recheck",
                    "observed_results", "rationale_provenance"):
            if r[key]["status"] == "verified" and ref[key][0] != "verified":
                problems.append(f"result {i}: {key} reported verified, but the reference check finds {ref[key][0]}")
        o = r["observed_results"]
        if o["execution_state"] != ref["execution_state"]:
            problems.append(f"result {i}: execution_state is {o['execution_state']}; the attachment shows {ref['execution_state']}")
        if [[x["attempt_stage_id"], x["observed"]] for x in o["attempts"]] != ref["observed"]:
            problems.append(f"result {i}: observed results not carried through as the attachment records them")
    return problems


def pairing_case(c, data, validators):
    report = apply_patch(data["base_report"], c["report_patch"])
    attachments = [apply_patch(data["base_attachments"][n], c.get("attachment_patches", {}).get(n, []))
                   for n in data["report_covers"]]
    if list(validators["report"].iter_errors(report)) or any(
            list(validators["attachment"].iter_errors(a)) for a in attachments):
        return "error", "every document must be schema-valid for this case"
    records = {json.loads(t)["decision_id"]: t.encode("utf-8") for t in data["records"].values()}
    problems = read_with_attachments(report, attachments, records)
    return ("inconsistent" if problems else "consistent"), "; ".join(problems)


def main():
    data = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    validators = {}
    for name, p in SCHEMAS.items():
        schema = json.loads(p.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(schema)
        print(f"[ok  ] schemas/{p.name}: valid JSON Schema 2020-12")
    validators["core_record"] = Draft202012Validator(json.loads(CORE_RECORD_SCHEMA.read_text(encoding="utf-8")))

    groups = [
        ("schema", data["schema_cases"], lambda c: schema_case(c, data, validators), lambda c: c["expected"]),
        ("digest", data["digest_cases"], lambda c: digest_case(c, data), lambda c: c["expected"]),
        ("binding", data["binding_cases"], lambda c: binding_case(c, data, validators), expected_binding),
        ("pairing", data["pairing_cases"], lambda c: pairing_case(c, data, validators), lambda c: c["expected"]),
    ]
    failed, total, limits = [], 0, []
    for group, cases, run, expect in groups:
        print(f"\n{group} cases:")
        for c in cases:
            total += 1
            try:
                got, detail = run(c)
            except Exception as exc:  # a malformed case fails, it does not stop the run
                got, detail = "error", f"{type(exc).__name__}: {exc}"
            ok = got == expect(c)
            label = c.get("schema", group)
            print(f"[{'ok' if ok else 'FAIL':4}] {c['id']:4} {label:11} {c['description']}")
            if not ok:
                failed.append(c["id"])
                shown = "; ".join(detail[:2]) if isinstance(detail, list) else detail
                if isinstance(got, dict) and isinstance(expect(c), dict):
                    got = {k: v for k, v in got.items() if expect(c).get(k) != v}
                print(f"         expected {c['expected']}, got {got}" + (f": {shown[:300]}" if shown else ""))
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
