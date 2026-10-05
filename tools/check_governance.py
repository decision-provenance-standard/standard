# SPDX-License-Identifier: Apache-2.0
"""Governance records check: the Charters and the decision records in governance/ are well-formed.

The Charters are governance/charter.md and every governance/charter-*.md (a successor Charter sits next to
the one it replaces). Charter ids must be unique, and each record is checked against the Charter its
charter_id names.

1. Schema check: render each Charter and each record to JSON from the Markdown itself, and validate it
   with the reference schemas in standard/v5.0/ (the same registry build as tests/known-defects/run_checks.py).
   Disclosure blocks are validated against the disclosure schema; every error must fall in one of the
   categories listed below (the ones governance/README.md describes). A category that belongs to a known
   defect follows that defect's status in tests/known-defects/cases.json: it must occur while the defect is
   open, and must not occur once it is fixed. A category that belongs to no known defect must occur.
2. Field-list check against the text: each Charter against §3.2 (at fields-completed; closed_at is null unless
   the Charter is closed); each record against §6.2.1 to §6.2.3 (at drafted) and against its own Charter
   (owner, decision class, mode; dispatched while that Charter was open), with a review_log on every record
   under any Charter but the first; plus, for a closed record, the closing fields governance/README.md defines:
   the merge named in the record is on main's first-parent history, was made by the account the affirmation
   names, and added the record; nothing but the closing fields and record_state changed since that merge; the
   seal recomputes; and the Steward's fixed values are those of the first closed record: the same affirming
   account, and the same signed attestation text with only the Charter id changed to the record's own.
3. Release check: for every release tag spec/editions.json lists, every record in governance/decisions/ at that
   tag still exists; a record closed at that tag is byte-identical today; a record drafted at that tag is
   identical today, or identical once its closing rows are removed. A listed tag may be missing only if it is the
   newest release (the one being made); otherwise fetch the tags. A closed record's sealing release comes from
   its record_location, or, where record_location says it is sealed by a later release, from the index's
   "Sealed at tag" column; either way it must be a listed release.

Usage: python tools/check_governance.py [REPO-ROOT] [--json-out DIR]
REPO-ROOT defaults to the folder above the one this file is in, so a copy placed in any folder at the top
of a checkout checks that checkout. Merge commits and release tags are read with git, so a full clone with
its tags is needed (git fetch --tags). Exit 0 only if every check passes.
"""
import copy
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


def _args():
    import argparse
    ap = argparse.ArgumentParser(description="Check the Charter and the decision records in governance/.")
    ap.add_argument("root", nargs="?", help="repository root (default: the folder above the one this file is in)")
    ap.add_argument("--json-out", metavar="DIR", help="also write each rendered record as JSON into DIR")
    ap.add_argument("--main-ref", metavar="REF",
                    help="the branch whose first-parent history affirming merges must be on (default: origin/main, else main)")
    return ap.parse_args()


_A = _args()
ROOT = pathlib.Path(_A.root).resolve() if _A.root else pathlib.Path(__file__).resolve().parent.parent
GOV = ROOT / "governance"
if not (GOV / "decisions").is_dir() or not (ROOT / "spec" / "editions.json").is_file():
    sys.exit(f"FAIL: {ROOT} is not a checkout of the repository (no governance/decisions/ or spec/editions.json)")
JSON_OUT = pathlib.Path(_A.json_out) if _A.json_out else None
TAG = re.compile(r"tag `(v\d+\.\d+-rev\d+)`")

RECORD_HEADER = ("> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. "
                 "This record makes no conformance claim, and Etsion Brands is not listed as an adopter.")
CHARTER_HEADER = ("> Affiliated: the Standard's own use of itself by its Steward. The Charter declares a target of "
                  "Level 1 because the text requires every complete Charter to declare one. This is not a conformance "
                  "declaration. Etsion Brands is not listed as an adopter.")
CLOSING = ("Carried because this Standard requires it for AI-drafted records; this says nothing about whether "
           "any law applies.")

# The first Charter. Its records DR-2026-0001 to DR-2026-0007 were affirmed without a review_log and are never
# edited (governance/README.md), so it is the one Charter whose records are not all required to carry one.
# Every other Charter, now or later, is held to the text's field (Standard §6.2.3).
FIRST_CHARTER = "dps-text-authoring"

ROW = re.compile(r"^\| `([a-z0-9_\-]+)` \| (.*) \|\s*$")
DUPLICATES = []  # (file, field, line) for a field row that appears twice in one section
REVIEW_ENTRY = re.compile(r"^reviewer: (?P<reviewer>[^;]+); reviewed_at: (?P<reviewed_at>[^;]+); outcome: (?P<outcome>.+)$")


# ---------------------------------------------------------------- parsing
def parse(path):
    """Return {section: {field: (raw_value, line_no)}}; section 'main' or 'disclosure'."""
    out, section = {"main": {}, "disclosure": {}}, "main"
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines, 1):
        if line.startswith("## Disclosure block") or line.startswith("## The disclosure block"):
            section = "disclosure"
        elif line.startswith("## "):
            section = "other"
        m = ROW.match(line)
        if m and section in out:
            if m.group(1) in out[section]:
                DUPLICATES.append((path.name, m.group(1), i))
            out[section][m.group(1)] = (m.group(2), i)
    return out, lines


def parts(raw):
    return [p.strip() for p in raw.split("<br>")]


def plain(raw):
    return raw.replace("`", "").replace("<br>", "\n").strip()


def items(raw):
    return [re.sub(r"^• ", "", p).replace("`", "") for p in parts(raw)]


def obj(raw):
    d = {}
    for p in parts(raw):
        k, v = p.split(": ", 1)
        d[k.strip()] = v.strip().replace("`", "")
    return d


def first_code(raw):
    m = re.search(r"`([^`]+)`", raw)
    return m.group(1) if m else plain(raw)


def triggers(raw):
    out = []
    for p in parts(raw):
        kind, desc = p.split(": ", 1)
        out.append({"trigger_type": {"Outcome evidence": "outcome_evidence",
                                     "Market evidence": "market_evidence"}[kind],
                    "trigger_description": desc})
    return out


def render_charter(f):
    m = {k: v for k, (v, _) in f["main"].items()}
    conv = {
        "accountable_owner": obj, "cadence": obj,
        "inside_decisions": items, "outside_decisions": items, "schedule_of_records": items,
        "re_decision_triggers": triggers, "record_location": first_code,
        "conformance_level_declared": lambda r: int(re.match(r"\d+", r).group(0)),
        "closed_at": lambda r: None if r.startswith("null") else plain(r),
        "charter_state": lambda r: r.split()[0],
    }
    return {k: conv.get(k, plain)(v) for k, v in m.items()}


def render_record(f):
    m = {k: v for k, (v, _) in f["main"].items()}
    conv = {
        "accountable_owner": obj, "drafting_authority": obj,
        # closing fields (governance/README.md "How a record is affirmed, closed and sealed")
        "accountable_owner_signoff": obj, "affirmation_record": obj, "mode_classification_attestation": obj,
        "context_at_decision": lambda r: "\n".join("- " + x for x in items(r)),
        "options_considered": items, "required_inputs_used": items, "assumptions_depended_on": items,
        "success_criteria": items, "related_decisions": items,
        "record_location": first_code,
        # review_log: one bullet per review (Standard §6.2.3; schema array); an entry that does not parse is kept
        # as {"unparsed": ...} and fails the field check below instead of stopping the checker
        "review_log": lambda r: [(m.groupdict() if (m := REVIEW_ENTRY.match(e.strip())) else {"unparsed": e})
                                 for e in items(r)],
    }
    return {k: conv.get(k, plain)(v) for k, v in m.items()}


DISCLOSURE_KEYS = {"declaring-authority": "declaring_authority", "ai-system-identity": "ai_system_identity",
                   "jurisdictional-applicability-tag": "jurisdictional_applicability",
                   "content-type-tag": "content_type_tag", "generation-timestamp": "generation_timestamp"}


def render_disclosure(f):
    d = {}
    for k, (v, _) in f["disclosure"].items():
        key = DISCLOSURE_KEYS[k]
        if key in ("jurisdictional_applicability", "content_type_tag"):
            d[key] = [x.strip() for x in v.split(",")]
        else:
            d[key] = plain(v)
    return d


# ---------------------------------------------------------------- schema check
def load_registry():
    schemas, reg = {}, Registry()
    for p in sorted((ROOT / "standard").rglob("*.json")):
        s = json.loads(p.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(s)
        schemas[p.relative_to(ROOT).as_posix()] = s
        reg = reg.with_resource(s["$id"], Resource.from_contents(s))
    return schemas, reg


def errors(schema, reg, inst):
    v = Draft202012Validator(schema, registry=reg, format_checker=FormatChecker())
    return sorted(v.iter_errors(inst), key=lambda e: (list(e.absolute_path), e.message))


def classify(e):
    path = list(e.absolute_path)
    if e.validator == "required" and "'disclosure_text_pointer'" in e.message:
        return "KD-06: schema requires disclosure_text_pointer (text has 5 fields)"
    if e.validator == "required" and "'attached_at'" in e.message:
        return "KD-06: schema requires attached_at (text has 5 fields)"
    if path and path[0] == "jurisdictional_applicability" and e.validator == "enum":
        return "KD-06: text's jurisdiction spelling rejected"
    if path == ["declaring_authority"] and e.validator == "type":
        return "Plain value: declaring_authority written as the text's plain value"
    if path == ["ai_system_identity"] and e.validator == "type":
        return "Plain value: ai_system_identity written as the text's plain value"
    return None


# Each category above, and the known defect in tests/known-defects/cases.json it belongs to. While that defect
# is open its category must occur; once it is fixed, it must not (so a fix that is only partly made fails).
# None: no known defect. The records write these two fields as the text's plain values where the schema has an
# object (governance/README.md, "Plain values"); that shape difference stays whatever the schema's object
# requires inside, so these categories must always occur, or the README's description has gone stale.
CATEGORY_KD = {
    "KD-06: schema requires disclosure_text_pointer (text has 5 fields)": "KD-06",
    "KD-06: schema requires attached_at (text has 5 fields)": "KD-06",
    "KD-06: text's jurisdiction spelling rejected": "KD-06",
    "Plain value: declaring_authority written as the text's plain value": None,
    "Plain value: ai_system_identity written as the text's plain value": None,
}


def defect_status():
    """{defect id: status} from tests/known-defects/cases.json ({} if it cannot be read)."""
    try:
        data = json.loads((ROOT / "tests" / "known-defects" / "cases.json").read_text(encoding="utf-8"))
        return {k: v.get("status") for k, v in data["defects"].items()}
    except (OSError, ValueError, KeyError, AttributeError):
        return {}


# ---------------------------------------------------------------- field-list check (the text)
CHARTER_FIELDS = [  # §3.2: field, required-at-state
    ("charter_id", "open"), ("charter_name", "open"), ("decision_class", "open"), ("accountable_owner", "open"),
    ("inside_decisions", "mode-declared"), ("outside_decisions", "mode-declared"),
    ("mode_declaration", "mode-declared"), ("cadence", "fields-required"), ("record_location", "fields-required"),
    ("re_decision_triggers", "fields-required"), ("escalation_rule", "fields-required"),
    ("schedule_of_records", "fields-completed"), ("conformance_level_declared", "fields-completed"),
    ("disclosure_metadata_pointer", "fields-completed (mode-2)"), ("created_at", "open"),
    ("closed_at", "closed (nullable until then)"),
]
RECORD_FIELDS = [  # field, text source, required-at
    ("decision_id", "§6.2.1", "dispatched"), ("charter_id", "§6.2.1", "dispatched"),
    ("accountable_owner", "§6.2.1", "dispatched"), ("decision_class", "§6.2.1", "dispatched"),
    ("dispatch_mode", "§6.2.1", "dispatched"), ("dispatched_at", "§6.2.1", "dispatched"),
    ("record_type", "§6.2.3 row", "dispatched"),
    ("decision_statement", "§6.2.2", "drafted"), ("context_at_decision", "§6.2.2", "drafted"),
    ("options_considered", "§6.2.2", "drafted"), ("required_inputs_used", "§6.2.2", "drafted"),
    ("assumptions_depended_on", "§6.2.2", "drafted"), ("success_criteria", "§6.2.2", "drafted"),
    ("disclosure_metadata_pointer", "§6.2.2", "drafted (mode-2)"),
    ("altitude", "§6.2.3 row", "draft onward"), ("drafting_authority", "§6.2.3 row", "mode-2"),
    ("re_decision_trigger", "§6.2.3", "closed (written now)"), ("record_location", "§6.2.3", "closed (written now)"),
    ("related_decisions", "§6.2.3", "closed (written now)"),
]
TEXT_JURIS = {"eu", "us-federal", "us-delaware", "uk", "israel"}
TEXT_CTYPE = {"decision-summary", "recommendation", "decision-aid", "draft", "classification", "synthetic-media"}
SCHEDULE_TYPES = ["Decision records", "Re-decision records", "Escalation records", "Charter-amendment records",
                  "Disclosure-review records"]


def iso_utc(s):
    try:
        return bool(re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", s)) and bool(
            datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))
    except ValueError:
        return False


def sentences(s):
    return len([x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z])", s.strip()) if x])


class Report:
    def __init__(self):
        self.rows, self.fails = [], []

    def row(self, fname, field, ok, where, note=""):
        self.rows.append((fname, field, "yes" if ok else "NO", where, note))
        if not ok:
            self.fails.append(f"{fname}: {field} ({note})")


def field_check_charter(rep, path, f, lines, charter, record_files, all_files):
    """One Charter. record_files: the records whose charter_id names it; all_files: every record file name."""
    fn = path.name
    rep.row(fn, "(header line)", CHARTER_HEADER in lines, f"{fn}:{lines.index(CHARTER_HEADER)+1 if CHARTER_HEADER in lines else '-'}")
    main = f["main"]
    w = lambda k: f"{fn}:{main[k][1]}" if k in main else "-"
    closed = charter.get("charter_state") == "closed"
    for field, state in CHARTER_FIELDS:
        ok = field in main
        where = f"{fn}:{main[field][1]}" if ok else "-"
        note = f"§3.2, required at {state}"
        if ok and field == "closed_at":
            ca = charter["closed_at"]
            if closed:  # §3.3: a closed Charter records when it closed; no record may be dispatched under it after
                ok = iso_utc(ca or "") and ca >= charter.get("created_at", "")
                note += f"; charter_state is closed, so a UTC time not before created_at ({ca})"
            else:
                ok = ca is None
                note += "; null (not closed)"
        rep.row(fn, field, ok, where, note)
    # content rules the text sets on those fields
    ao = charter.get("accountable_owner", {})
    rep.row(fn, "  accountable_owner = one named human", bool(ao.get("full_name")) and "," not in ao.get("full_name", ","),
            w("accountable_owner"), ao.get("full_name", ""))
    rep.row(fn, "  mode_declaration enum", charter.get("mode_declaration") in ("mode-1", "mode-2", "mode-1-with-embedded-mode-2-summary"),
            w("mode_declaration"), charter.get("mode_declaration", ""))
    kinds = [t["trigger_type"] for t in charter.get("re_decision_triggers", [])]
    rep.row(fn, "  re_decision_triggers: outcome + market", "outcome_evidence" in kinds and "market_evidence" in kinds,
            w("re_decision_triggers"), ", ".join(kinds))
    sched = " | ".join(charter.get("schedule_of_records", []))
    missing = [t for t in SCHEDULE_TYPES if t not in sched]
    rep.row(fn, "  schedule_of_records: 5 record types (§6.3.1, §7.2.1)", not missing,
            w("schedule_of_records"), "missing " + ", ".join(missing) if missing else "all 5")
    rep.row(fn, "  schedule_of_records: retention per type (§6.4.2)", "Retention, for every record type" in sched,
            w("schedule_of_records"), "declared as 'permanent'")
    rep.row(fn, "  conformance_level_declared in {1,2,3}", charter.get("conformance_level_declared") in (1, 2, 3),
            w("conformance_level_declared"), str(charter.get("conformance_level_declared")))
    rep.row(fn, "  created_at ISO 8601 UTC", iso_utc(charter.get("created_at", "")), w("created_at"), charter.get("created_at", ""))
    # record_location resolves to an index listing every record by id, type, state and date (§6.3.2, §7.2.1)
    idx = ROOT / charter.get("record_location", "")
    idx_text = idx.read_text(encoding="utf-8") if idx.is_file() else ""
    rep.row(fn, "  record_location resolves (index file exists)", idx.is_file(), w("record_location"), charter.get("record_location", ""))
    for rf, rec in record_files:
        pat = re.compile(r"^\| \[" + re.escape(rec["decision_id"]) + r"\]\(decisions/" + re.escape(rf.name) + r"\) \| "
                         + re.escape(rec["record_type"]) + r" \| " + re.escape(rec["record_state"]) + r" \| "
                         + re.escape(rec["dispatched_at"]) + r" \|", re.M)
        rep.row(fn, f"  index lists {rec['decision_id']} (id, type, state, date match the record)", bool(pat.search(idx_text)),
                "README.md", "")
    listed = set(re.findall(r"^\| \[DR-\d{4}-\d+\]\(decisions/([^)]+)\)", idx_text, re.M))
    files = {rf.name for rf, _ in record_files}
    # Charters may share one index, so a row may belong to another Charter; it must still link a record.
    odd = sorted((listed - set(all_files)) | (files - listed))
    rep.row(fn, "  every index row links an existing record, and every record under this Charter is in the index",
            not odd, "README.md", ", ".join(odd) or f"{len(files)} records")
    # §3.1 conditional fields
    below_exec = [r["decision_id"] for _, r in record_files if r.get("altitude") != "executive"]
    rep.row(fn, "  use_case_scope_limit_declaration (§3.1)", not below_exec, "-",
            "not triggered: every record is at executive altitude" if not below_exec else "TRIGGERED by " + ", ".join(below_exec))
    rep.row(fn, "  works_council_consultation_record (§3.1)", not below_exec, "-",
            "not triggered: no record at function-leader altitude or below" if not below_exec
            else "TRIGGERED by " + ", ".join(below_exec))


CLOSING_FIELDS = ["closed_at", "accountable_owner_signoff", "affirmation_record", "mode_classification_attestation",
                  "seal_algorithm", "seal_hash"]
ATT_FIELDS = ["attestor_full_name", "attestor_role_title", "attestor_employer", "attestation_timestamp",
              "jurisdiction", "attestation_language_version", "attestation_text_signed", "attestor_capacity"]
MERGE_METHOD = re.compile(r"merge of pull request #(\d+), which added this record to the repository "
                          r"\(merge commit ([0-9a-f]{40})\)")
SEAL_LINE = re.compile(rb"^(\| `seal_hash` \| )([0-9a-f]{64})( \|)$", re.M)


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True)


def release_tags():
    """The release tags spec/editions.json lists, oldest first."""
    try:
        m = json.loads((ROOT / "spec" / "editions.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    out = []
    for e in m.get("editions", []):
        for r in e.get("releases", []):
            if r.get("tag") and r["tag"] not in out:
                out.append(r["tag"])
    return out


RELEASES = release_tags()
MISSING_TAG = ("missing here: fetch the tags (git fetch --tags); a release being made must be listed last in "
               "spec/editions.json")


def tag_exists(tag):
    return git("rev-parse", "--verify", "-q", f"refs/tags/{tag}^{{commit}}").returncode == 0


def main_ref():
    if _A.main_ref:
        return _A.main_ref
    for ref in ("refs/remotes/origin/main", "refs/heads/main"):
        if git("rev-parse", "--verify", "-q", ref).returncode == 0:
            return ref
    return "HEAD"


MAIN_REF = main_ref()
_FIRST_PARENT = None


def on_main(sha):
    global _FIRST_PARENT
    if _FIRST_PARENT is None:
        _FIRST_PARENT = set(git("rev-list", "--first-parent", MAIN_REF).stdout.decode().split())
    return sha in _FIRST_PARENT


def sealed_at_column():
    """{decision_id: cell} from the index's "Sealed at tag" column ('' for a blank cell); {} with no column."""
    out, cols = {}, None
    readme = GOV / "README.md"
    if not readme.is_file():
        return out
    for line in readme.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else None
        if cells and cells[0] == "Record":
            cols = cells
        elif cells and cols and "Sealed at tag" in cols and len(cells) == len(cols):
            m = re.match(r"\[(DR-\d{4}-\d+)\]", cells[0])
            if m:
                out[m.group(1)] = cells[cols.index("Sealed at tag")].strip("`")
    return out


SEALED_AT = sealed_at_column()
PIN = {}  # the Steward's fixed values, from the first closed record


def signed_text_for(charter_id):
    """The signed attestation text for a record under charter_id: the first closed record's text with its own
    Charter id, which it must name exactly once, replaced by charter_id. The Steward approved the same text with
    only the Charter id changed; tools/close_record.py writes it the same way. None if it cannot be derived."""
    pat = r"(?<![\w-])" + re.escape(PIN["charter_id"]) + r"(?![\w-])"
    if not PIN["charter_id"] or len(re.findall(pat, PIN["text"])) != 1:
        return None
    return re.sub(pat, lambda _: charter_id, PIN["text"])


def unclose(data):
    """A closed record's bytes with the closing rows removed and record_state set back to drafted."""
    text = data.decode("utf-8")
    kept = "".join(l for l in text.splitlines(keepends=True)
                   if not ((m := ROW.match(l.rstrip("\n"))) and m.group(1) in CLOSING_FIELDS))
    return kept.replace("| `record_state` | closed |\n", "| `record_state` | drafted |\n", 1).encode("utf-8")


def closed_record_checks(rep, path, f, lines, rec, w):
    """A closed record, as governance/README.md defines it: every closing value read from the merge that
    affirmed the record; nothing else changed since that merge; the seal recomputes; after the release that
    sealed it, the file is unchanged from its copy at that release's tag."""
    fn, g, main = path.name, rec.get, f["main"]
    for k in CLOSING_FIELDS:
        rep.row(fn, k, k in main, w(k), "closing field (governance/README.md), required at closed")
    if any(k not in main for k in CLOSING_FIELDS):
        return
    ao, ca = rec["accountable_owner"], g("closed_at", "")
    rep.row(fn, "  closed_at ISO 8601 UTC", iso_utc(ca), w("closed_at"), ca)
    so = g("accountable_owner_signoff", {})
    rep.row(fn, "  signoff: signed_by + signed_at only (schema)", set(so) == {"signed_by", "signed_at"}, w("accountable_owner_signoff"))
    rep.row(fn, "  signoff.signed_by = accountable owner, with role (§6.2.3)",
            so.get("signed_by") == f"{ao['full_name']}, {ao['role']}", w("accountable_owner_signoff"), so.get("signed_by", ""))
    rep.row(fn, "  signoff.signed_at = closed_at", so.get("signed_at") == ca, w("accountable_owner_signoff"))
    ar = g("affirmation_record", {})
    rep.row(fn, "  affirmation_record: timestamp, actor_identity, method", set(ar) == {"timestamp", "actor_identity", "method"},
            w("affirmation_record"))
    rep.row(fn, "  affirmation_record.timestamp = closed_at", ar.get("timestamp") == ca, w("affirmation_record"))
    rep.row(fn, "  affirmation_record.actor_identity = the accountable owner (§6.2 lifecycle row)",
            ar.get("actor_identity", "").startswith(ao["full_name"] + " "), w("affirmation_record"), ar.get("actor_identity", ""))
    m = MERGE_METHOD.fullmatch(ar.get("method", ""))
    rep.row(fn, "  affirmation_record.method names the merge and its commit", bool(m), w("affirmation_record"))
    if m:
        pr, sha = m.groups()
        info = git("log", "-1", "--format=%ct%x09%P%x09%s", sha)
        ok = info.returncode == 0
        ct, parents, subject = (info.stdout.decode().strip().split("\t") + ["", "", ""])[:3] if ok else ("0", "", "")
        parents = parents.split()
        when = datetime.datetime.fromtimestamp(int(ct), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if ok else ""
        rep.row(fn, f"  merge commit {sha[:7]} is the merge of pull request #{pr}",
                ok and subject.startswith(f"Merge pull request #{pr} ") and len(parents) == 2, "git", subject)
        rep.row(fn, "  merge commit time = affirmation timestamp", when == ar.get("timestamp"), "git", when)
        rel = path.relative_to(ROOT).as_posix()
        added = ok and git("cat-file", "-e", f"{sha}:{rel}").returncode == 0 and \
            git("cat-file", "-e", f"{parents[0]}:{rel}").returncode != 0
        rep.row(fn, "  that merge added this record (absent before it, present after)", added, "git")
        rep.row(fn, f"  that merge is on main's first-parent history ({MAIN_REF})", ok and on_main(sha), "git")
        author = git("log", "-1", "--format=%ae", sha).stdout.decode().strip() if ok else ""
        acct = re.search(r"\(GitHub account ([A-Za-z0-9-]+)\)", ar.get("actor_identity", ""))
        rep.row(fn, "  that merge was made by the GitHub account the affirmation names",
                bool(acct) and re.fullmatch(r"(\d+\+)?" + re.escape(acct.group(1)) + r"@users\.noreply\.github\.com",
                                            author) is not None, "git", author)
        affirmed = git("show", f"{sha}:{rel}").stdout
        rep.row(fn, "  nothing but the closing fields and record_state changed since that merge",
                unclose(path.read_bytes()) == affirmed, "git", f"affirmed version {len(affirmed)} bytes")
    at = g("mode_classification_attestation", {})
    rep.row(fn, "  attestation: exactly the 8 Layer 4 fields", sorted(at) == sorted(ATT_FIELDS), w("mode_classification_attestation"))
    rep.row(fn, "  attestor = accountable owner (name, role, employer)",
            (at.get("attestor_full_name"), at.get("attestor_role_title"), at.get("attestor_employer"))
            == (ao["full_name"], ao["role"], ao.get("employer")), w("mode_classification_attestation"))
    rep.row(fn, "  attestation_timestamp ISO 8601 UTC = affirmation time",
            iso_utc(at.get("attestation_timestamp", "")) and at.get("attestation_timestamp") == ca, w("mode_classification_attestation"))
    txt = at.get("attestation_text_signed", "")
    rep.row(fn, "  attestation text: first person, >= 200 chars, says the mode-2 classification is accurate",
            txt.startswith(f"I, {ao['full_name']},") and len(txt) >= 200 and "mode-2" in txt and "accurately reflects" in txt,
            w("mode_classification_attestation"), f"{len(txt)} chars")
    if not PIN:
        PIN.update(text=txt, actor=ar.get("actor_identity", ""), source=fn, charter_id=g("charter_id", ""))
    expected = signed_text_for(g("charter_id", ""))
    src = PIN["source"][:12]
    rep.row(fn, f"  affirming account = {src}'s", ar.get("actor_identity", "") == PIN["actor"],
            w("affirmation_record"), ar.get("actor_identity", ""))
    rep.row(fn, f"  signed attestation text = {src}'s, with only the Charter id changed to the record's",
            expected is not None and txt == expected, w("mode_classification_attestation"),
            f"Charter {g('charter_id', '')}" if expected is not None
            else f"{src}'s text does not name its Charter id {PIN['charter_id']!r} exactly once")
    rep.row(fn, "  attestation: IL, v1.0, director",
            (at.get("jurisdiction"), at.get("attestation_language_version"), at.get("attestor_capacity")) == ("IL", "v1.0", "director"),
            w("mode_classification_attestation"))
    rep.row(fn, "  seal_algorithm = SHA-256", g("seal_algorithm") == "SHA-256", w("seal_algorithm"))
    b = path.read_bytes()
    found = SEAL_LINE.findall(b)
    ok = len(found) == 1
    if ok:
        zero = SEAL_LINE.sub(lambda mm: mm.group(1) + b"0" * 64 + mm.group(3), b)
        ok = hashlib.sha256(zero).hexdigest() == found[0][1].decode() == g("seal_hash")
    rep.row(fn, "  seal_hash = SHA-256 of the file with seal_hash zeroed (README)", ok, w("seal_hash"))
    # The release that sealed it. record_location names the release that first published the record. Where it
    # says the record is sealed by "the tag of the release that closes it", the index column names that later
    # release; otherwise a column cell, if there is one, must repeat record_location's tag.
    rloc = main.get("record_location", ("", 0))[0]
    m = TAG.search(rloc)
    named = m.group(1) if m else None
    cell = SEALED_AT.get(g("decision_id", ""))
    if "the tag of the release that closes it" in rloc:
        tag = cell or None
        ok = (tag in RELEASES and named in RELEASES and RELEASES.index(tag) > RELEASES.index(named))
        note = f"{tag} (index column; first released at {named})"
    else:
        tag = named
        ok = tag in RELEASES and (cell is None or cell == tag)
        note = f"{tag} (record_location)" + (f"; index column says {cell!r}" if cell not in (None, tag) else "")
    rep.row(fn, "  the release that sealed it is named, and listed in spec/editions.json", ok, w("record_location"), note)
    if ok and not tag_exists(tag):
        newest = tag == RELEASES[-1]
        rep.row(fn, f"  tag {tag} is here, or is the newest release (the one being made)", newest, "git",
                "not created yet" if newest else MISSING_TAG)
    elif ok:
        at_tag = git("show", f"{tag}:{path.relative_to(ROOT).as_posix()}")
        rep.row(fn, f"  tag {tag} holds this record, closed and byte-identical", at_tag.returncode == 0
                and b"| `record_state` | closed |" in at_tag.stdout and at_tag.stdout == path.read_bytes(), "git",
                "" if at_tag.returncode == 0 else f"not in {tag}")


def release_checks(rep, rec_paths):
    """Every release tag spec/editions.json lists: its records still exist and are unchanged (closing aside)."""
    now = {p.relative_to(ROOT).as_posix(): p for p in rec_paths}
    try:
        baseline = json.loads((ROOT / "spec" / "editions.json").read_text(encoding="utf-8")).get("baseline_tag")
    except (OSError, ValueError):
        baseline = None
    rep.row("releases", f"  the first published tag ({baseline}) is here, so release tags were fetched",
            bool(baseline) and tag_exists(baseline), "git", "" if baseline and tag_exists(baseline)
            else "missing here: fetch the tags (git fetch --tags)")
    for tag in RELEASES:
        if not tag_exists(tag):
            newest = tag == RELEASES[-1]
            rep.row("releases", f"  tag {tag} is here, or is the newest release (the one being made)", newest, "git",
                    "not created yet" if newest else MISSING_TAG)
            continue
        listing = git("ls-tree", "--name-only", tag, "governance/decisions/").stdout.decode().split()
        rep.row("releases", f"  tag {tag}: {len(listing)} record(s) to compare", True, "git")
        for rel in (r for r in listing if r.endswith(".md")):
            name = rel.rsplit("/", 1)[1]
            if rel not in now:
                rep.row(name, f"  still present (it is in tag {tag})", False, "git", "a released record was removed")
                continue
            then, cur = git("show", f"{tag}:{rel}").stdout, now[rel].read_bytes()
            if b"| `record_state` | closed |" in then:
                rep.row(name, f"  unchanged since tag {tag}, where it was closed", then == cur, "git")
            else:
                rep.row(name, f"  unchanged since tag {tag}, where it was drafted (closing rows aside)",
                        cur == then or (b"| `record_state` | closed |" in cur and unclose(cur) == then), "git")


def field_check_record(rep, path, f, lines, rec, charters, all_ids):
    """One record; charters: {charter_id: rendered Charter}."""
    fn = path.name
    main = f["main"]
    rep.row(fn, "(header line)", RECORD_HEADER in lines, f"{fn}:{lines.index(RECORD_HEADER)+1 if RECORD_HEADER in lines else '-'}")
    for field, src, state in RECORD_FIELDS:
        ok = field in main
        rep.row(fn, field, ok, f"{fn}:{main[field][1]}" if ok else "-", f"{src}, required at {state}")
    g = rec.get
    w = lambda k: f"{fn}:{main[k][1]}" if k in main else "-"
    charter = charters.get(g("charter_id"))
    if charter is not None and charter["charter_id"] != FIRST_CHARTER:
        rep.row(fn, "  review_log present (required on every record under this Charter; Standard §6.2.3)",
                "review_log" in main, w("review_log"), f"Charter {charter['charter_id']}")
    if "review_log" in main:
        entries = rec.get("review_log") or []
        good = bool(entries) and all(set(e) == {"reviewer", "reviewed_at", "outcome"} and e["reviewer"].strip()
                                     and e["outcome"].strip() and iso_utc(e["reviewed_at"].strip()) for e in entries)
        rep.row(fn, "  review_log: each entry names a reviewer, a UTC review time and the outcome", good,
                w("review_log"), f"{len(entries)} review(s)")
    rep.row(fn, "  record_state = drafted or closed", g("record_state") in ("drafted", "closed"), w("record_state"), g("record_state", ""))
    if g("record_state") == "closed":
        closed_record_checks(rep, path, f, lines, rec, w)
    else:
        present = [k for k in CLOSING_FIELDS if k in main]
        rep.row(fn, "  drafted: carries no closing field", not present, "-", ", ".join(present) or "none")
        m = TAG.search(main.get("record_location", ("", 0))[0])
        if m and tag_exists(m.group(1)):
            at_tag = git("show", f"{m.group(1)}:{path.relative_to(ROOT).as_posix()}")
            rep.row(fn, f"  the tag its record_location names ({m.group(1)}) holds this record", at_tag.returncode == 0,
                    "git", "" if at_tag.returncode == 0 else f"not in {m.group(1)}")
    rep.row(fn, "  decision_id format DR-YYYY-NNN (3+ digits)", bool(re.fullmatch(r"DR-\d{4}-\d{3,}", g("decision_id", ""))),
            w("decision_id"), g("decision_id", "") + " (four digits on purpose)")
    rep.row(fn, "  decision_id matches file name", fn.startswith(g("decision_id", "@") + "-"), w("decision_id"))
    rep.row(fn, "  charter_id names a Charter in governance/ (charter.md or charter-*.md)", charter is not None,
            w("charter_id"), g("charter_id", ""))
    if charter is not None:
        rep.row(fn, "  accountable_owner = its Charter's", g("accountable_owner") == charter.get("accountable_owner"), w("accountable_owner"))
        rep.row(fn, "  decision_class inherited from its Charter", g("decision_class") == charter.get("decision_class"), w("decision_class"))
        rep.row(fn, "  dispatch_mode = its Charter's mode", g("dispatch_mode") == charter.get("mode_declaration"), w("dispatch_mode"), g("dispatch_mode", ""))
        # §3.3: a record is dispatched under an open Charter. Closing a record later is not a new dispatch, so a
        # record dispatched before its Charter closed may still be closed after it.
        da, cc, cx = g("dispatched_at", ""), charter.get("created_at", ""), charter.get("closed_at")
        if iso_utc(da) and iso_utc(cc):
            rep.row(fn, "  dispatched_at not before its Charter's created_at", da >= cc, w("dispatched_at"), f"Charter created {cc}")
        if iso_utc(da) and cx is not None:
            rep.row(fn, "  dispatched_at not after its Charter's closed_at (no new dispatch under a closed Charter)",
                    iso_utc(cx) and da <= cx, w("dispatched_at"), f"Charter closed {cx}")
    rep.row(fn, "  dispatched_at ISO 8601 UTC", iso_utc(g("dispatched_at", "")), w("dispatched_at"), g("dispatched_at", ""))
    rep.row(fn, "  created_at ISO 8601 UTC", iso_utc(g("created_at", "")), w("created_at"), g("created_at", ""))
    rep.row(fn, "  record_type enum", g("record_type") in ("decision", "re_decision", "escalation", "charter_amendment",
                                                          "disclosure_review", "redaction_event"), w("record_type"), g("record_type", ""))
    n = sentences(g("decision_statement", ""))
    rep.row(fn, "  decision_statement 2-3 sentences", 2 <= n <= 3, w("decision_statement"), f"{n} sentences")
    n = len(g("context_at_decision", "").splitlines())
    rep.row(fn, "  context_at_decision 3-5 bullets", 3 <= n <= 5, w("context_at_decision"), f"{n} bullets")
    opts = g("options_considered", [])
    chosen = [o for o in opts if "Chosen:" in o]
    reasons = all(("Considered" in o or "Chosen:" in o) and ("Rejected:" in o or "Chosen:" in o) for o in opts)
    rep.row(fn, "  options_considered >= 2, one chosen, each with reasons", len(opts) >= 2 and len(chosen) == 1 and reasons,
            w("options_considered"), f"{len(opts)} options, {len(chosen)} chosen")
    ins = g("required_inputs_used", [])
    dated = [bool(re.search(r"\d{4}-\d\d-\d\d|tag `?rev8|release \d|\bfirst version\b", i)) for i in ins]
    verbatim = ("observations from an outside reviewer (credited in the release notes in a form they approve, "
                "or without a name if they have not answered)")
    undated_ok = all(d or i == verbatim for d, i in zip(dated, ins))
    rep.row(fn, "  required_inputs_used: version or date on each", undated_ok, w("required_inputs_used"),
            f"{len(ins)} inputs" + ("; outside-reviewer input kept verbatim, no date by design" if verbatim in ins else ""))
    n = len(g("assumptions_depended_on", []))
    rep.row(fn, "  assumptions_depended_on 2-4", 2 <= n <= 4, w("assumptions_depended_on"), f"{n} assumptions")
    sc = g("success_criteria", [])
    for t in ("T+2 ", "T+6 ", "T+12 "):
        hit = [s for s in sc if s.startswith(t)]
        rep.row(fn, f"  success_criteria {t.strip()} with named metric", len(hit) == 1 and "(metric:" in hit[0],
                w("success_criteria"), "")
    tp = [re.sub(r"^T\+\d+ \([^)]*\): ", "", s) for s in sc if s.startswith("T+")]
    rep.row(fn, "  success_criteria: T+2/6/12 worded distinctly", len(set(tp)) == len(tp) == 3, w("success_criteria"))
    rep.row(fn, "  success_criteria: an at-release check", sum(s.startswith("At release:") for s in sc) == 1, w("success_criteria"))
    da = g("drafting_authority", {})
    rep.row(fn, "  drafting_authority.deployer_role_pointer", bool(da.get("deployer_role_pointer")), w("drafting_authority"))
    rep.row(fn, "  altitude enum", g("altitude") in ("executive", "function-leader", "team-leader", "individual-professional"),
            w("altitude"), g("altitude", ""))
    rdt = g("re_decision_trigger", "")
    rep.row(fn, "  re_decision_trigger: outcome AND market", "Outcome evidence:" in rdt and "Market evidence:" in rdt, w("re_decision_trigger"))
    rel = g("related_decisions", [])
    # Links run from new to old: an affirmed record is never edited (Standard §2.2.19), so a record lists
    # every OLDER record; it may also list records drafted with it; every id it lists must exist.
    me = g("decision_id", "")
    older = [i for i in all_ids if i < me]
    ok_rel = (all(i in rel for i in older) and all(i in all_ids and i != me for i in rel)
              and len(rel) == len(set(rel)))
    rep.row(fn, "  related_decisions lists every older record, all exist", ok_rel,
            w("related_decisions"), ", ".join(rel) + (f"  (older: {', '.join(older) or 'none'})"))
    rloc_raw = main.get("record_location", ("", 0))[0]
    rep.row(fn, "  record_location = this file's repository path", g("record_location") == "governance/decisions/" + fn
            and (ROOT / g("record_location", "@")).is_file(), w("record_location"), g("record_location", ""))
    m = TAG.search(rloc_raw)
    rep.row(fn, "  record_location names a release tag", bool(m), w("record_location"), m.group(1) if m else "")
    # disclosure block (§4.6.2 five fields)
    d = f["disclosure"]
    for k in DISCLOSURE_KEYS:
        rep.row(fn, f"disclosure: {k}", k in d, f"{fn}:{d[k][1]}" if k in d else "-", "§4.6.2")
    dj = render_disclosure(f)
    rep.row(fn, "  jurisdiction values in the text's vocabulary",
            all(v in TEXT_JURIS or v.startswith("other:") for v in dj.get("jurisdictional_applicability", ["?"])), "", ", ".join(dj.get("jurisdictional_applicability", [])))
    rep.row(fn, "  content-type values in the text's vocabulary",
            all(v in TEXT_CTYPE or v.startswith("other:") for v in dj.get("content_type_tag", ["?"])), "", ", ".join(dj.get("content_type_tag", [])))
    rep.row(fn, "  generation-timestamp = created_at (drafting time)", dj.get("generation_timestamp") == g("created_at"), "")
    rep.row(fn, "  closing sentence after the block", CLOSING in lines, f"{fn}:{lines.index(CLOSING)+1 if CLOSING in lines else '-'}")


# ---------------------------------------------------------------- main
def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    schemas, reg = load_registry()
    cs = schemas["standard/v5.0/schemas/charter.schema.json"]
    ds = schemas["standard/v5.0/schemas/decision-record.schema.json"]
    a50 = schemas["standard/v5.0/schemas/article-50-disclosure-metadata.json"]
    try:
        import rfc3339_validator  # noqa: F401
        fmt = "active"
    except ImportError:
        fmt = "NOT active (rfc3339-validator not installed; the repo pins none), so the field check parses timestamps itself"
    print(f"jsonschema FormatChecker date-time: {fmt}\n")

    schema_fail = []
    cpaths = ([GOV / "charter.md"] if (GOV / "charter.md").is_file() else []) + sorted(GOV.glob("charter-*.md"))
    if not cpaths:
        print("FAIL: no Charter in governance/ (charter.md or charter-*.md)")
        return 1
    charters = []  # (path, parsed, lines, rendered), one per Charter file
    for cpath in cpaths:
        cf, clines = parse(cpath)
        charters.append((cpath, cf, clines, render_charter(cf)))
    print("Charters: " + ", ".join(f"{p.name} ({c.get('charter_id', '?')})" for p, _, _, c in charters))
    rec_paths = sorted((GOV / "decisions").glob("DR-*.md"))
    recs = []
    for p in rec_paths:
        f, lines = parse(p)
        recs.append((p, f, lines, render_record(f), render_disclosure(f)))
    if JSON_OUT:
        JSON_OUT.mkdir(parents=True, exist_ok=True)
        for cpath, _, _, charter in charters:
            (JSON_OUT / (cpath.stem + ".json")).write_text(json.dumps(charter, indent=2, ensure_ascii=False), encoding="utf-8")
        for p, _, _, r, dj in recs:
            (JSON_OUT / (p.stem[:12] + ".json")).write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
            (JSON_OUT / (p.stem[:12] + ".disclosure.json")).write_text(json.dumps(dj, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== CHECK 1: schema validation (repo registry, Draft 2020-12) ===")
    for cpath, _, _, charter in charters:
        errs = errors(cs, reg, charter)
        print(f"{cpath.name} -> charter.schema.json: {'VALID' if not errs else 'INVALID'} ({len(errs)} errors)")
        for e in errs:
            print("   ", list(e.absolute_path), e.message[:150])
        if errs:
            schema_fail.append(cpath.name)
    seen_cats = set()
    l4 = schemas["standard/v5.0/mode-drift/layer-4-attestation.schema.json"]
    # The decision-record schema's $ref to the attestation schema cannot be resolved (KD-01), so a
    # closed record is checked in two parts: the attestation object on its own against the Layer 4 schema, and
    # the rest against the decision-record schema with that $ref removed (the property kept as a plain object).
    ds_noref = copy.deepcopy(ds)
    assert ds_noref["properties"]["mode_classification_attestation"] == {"$ref": "../mode-drift/layer-4-attestation.schema.json"}
    ds_noref["properties"]["mode_classification_attestation"] = {"type": "object"}
    for p, f, lines, r, dj in recs:
        if r.get("record_state") == "closed":
            try:
                full = errors(ds, reg, r)
                print(f"{p.name[:12]} -> full decision-record.schema.json: {len(full)} errors (the $ref resolved; KD-01 may be fixed)")
            except Exception as ex:  # referencing.exceptions.Unresolvable
                print(f"{p.name[:12]} -> full decision-record.schema.json: cannot run, {type(ex).__name__} (KD-01, as expected)")
            att = r.get("mode_classification_attestation")
            aerrs = errors(l4, reg, att)
            print(f"{p.name[:12]} attestation -> layer-4-attestation.schema.json: {'VALID' if not aerrs else 'INVALID'} ({len(aerrs)} errors)")
            for e in aerrs:
                print("   ", list(e.absolute_path), e.message[:150])
            if aerrs:
                schema_fail.append(p.name + " attestation")
            errs = errors(ds_noref, reg, r)
            print(f"{p.name[:12]} -> decision-record.schema.json with the attestation $ref removed: "
                  f"{'VALID' if not errs else 'INVALID'} ({len(errs)} errors)")
        else:
            errs = errors(ds, reg, r)
            print(f"{p.name[:12]} -> decision-record.schema.json: {'VALID' if not errs else 'INVALID'} ({len(errs)} errors)")
        for e in errs:
            print("   ", list(e.absolute_path), e.message[:150])
        if errs:
            schema_fail.append(p.name)
        errs = errors(a50, reg, dj)
        cats = [(classify(e), e) for e in errs]
        unexpected = [e for c, e in cats if c is None]
        print(f"{p.name[:12]} disclosure -> article-50-disclosure-metadata.json: {len(errs)} errors, "
              f"{len(errs) - len(unexpected)} in listed categories, {len(unexpected)} unexpected")
        for c, e in cats:
            print(f"    [{c or 'UNEXPECTED'}] {list(e.absolute_path)} {e.message[:110]}")
            if c:
                seen_cats.add(c.split(":")[0] + ":" + c.split(":")[1])
        if unexpected:
            schema_fail.append(p.name + " disclosure (unexpected errors)")
    got = {c for _, _, _, _, dj in recs for c in (classify(e) for e in errors(a50, reg, dj)) if c}
    status = defect_status()
    print("Disclosure categories (each must occur, unless its known defect is fixed in tests/known-defects/cases.json):")
    for cat, kd in CATEGORY_KD.items():
        st = status.get(kd) if kd else None
        if kd and st not in ("open", "fixed"):
            ok, why = False, f"{kd} has status {st!r} in tests/known-defects/cases.json (open or fixed expected)"
        elif st == "fixed":
            ok, why = cat not in got, f"{kd} is fixed, so it must not occur: " + ("it does not" if cat not in got else "IT OCCURS")
        else:
            ok = cat in got
            why = (f"{kd} is open" if kd else "no known defect; governance/README.md describes it") + \
                  ", so it must occur: " + ("it does" if ok else "IT DOES NOT")
        print(f"    [{'ok' if ok else 'FAIL'}] {cat}: {why}")
        if not ok:
            schema_fail.append(f"disclosure category [{cat}]: {why}")
    print("CHECK 1:", "PASS" if not schema_fail else "FAIL " + "; ".join(schema_fail))

    print("\n=== CHECK 2: field lists from the text (Charter §3.2 at fields-completed; records §6.2.1-§6.2.3 at drafted, plus the closing fields at closed) ===")
    rep = Report()
    cids = [c.get("charter_id", "") for _, _, _, c in charters]
    dup = sorted({i for i in cids if cids.count(i) > 1})
    rep.row("charters", "  each Charter file has its own charter_id", not dup, "-",
            ("repeated: " + ", ".join(dup)) if dup else ", ".join(cids))
    by_id = {c["charter_id"]: c for _, _, _, c in charters if c.get("charter_id") and c["charter_id"] not in dup}
    all_files = [p.name for p, _, _, _, _ in recs]
    for cpath, cf, clines, charter in charters:
        field_check_charter(rep, cpath, cf, clines, charter,
                            [(p, r) for p, _, _, r, _ in recs if r.get("charter_id") == charter.get("charter_id")], all_files)
    ids = [r["decision_id"] for _, _, _, r, _ in recs if "decision_id" in r]
    for p, f, lines, r, dj in recs:
        field_check_record(rep, p, f, lines, r, by_id, ids)
    release_checks(rep, [p for p, _, _, _, _ in recs])
    for fname, field, line in DUPLICATES:
        rep.row(fname, f"  the field row {field} appears only once", False, f"line {line}", "a repeated row")
    # README disclosure block: the five fields
    rf, rlines = parse(GOV / "README.md")
    for k in DISCLOSURE_KEYS:
        rep.row("README.md", f"disclosure: {k}", k in rf["disclosure"],
                f"README.md:{rf['disclosure'][k][1]}" if k in rf["disclosure"] else "-", "§4.6.2")
    rep.row("README.md", "closing sentence after the block", CLOSING in rlines, f"README.md:{rlines.index(CLOSING)+1 if CLOSING in rlines else '-'}")
    w = max(len(r[1]) for r in rep.rows)
    cur = None
    for fn, field, ok, where, note in rep.rows:
        if fn != cur:
            print(f"\n-- {fn}")
            print(f"   {'field':<{w}}  present  where / note")
            cur = fn
        where = where.split(":")[-1] if where not in ("-", "") and where.startswith(fn) else where
        print(f"   {field:<{w}}  {ok:<7}  {('line ' + where) if where.isdigit() else where}{('  ' + note) if note else ''}")
    print("\nCHECK 2:", "PASS" if not rep.fails else f"FAIL ({len(rep.fails)}): " + "; ".join(rep.fails))
    states = [r.get("record_state", "?") for _, _, _, r, _ in recs]
    print(f"\nrecords: {len(states)} ({states.count('closed')} closed, {states.count('drafted')} drafted)")
    print("PASS" if not schema_fail and not rep.fails else "FAIL")
    return 0 if not schema_fail and not rep.fails else 1


if __name__ == "__main__":
    sys.exit(main())
