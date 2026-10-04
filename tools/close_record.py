# SPDX-License-Identifier: Apache-2.0
"""Close and seal decision records from the merge that affirmed them (governance/README.md).

Used by the Steward in a release pull request. It is not run by the automated checks; it is here so any
reader can see how every closing value is derived. Every value is read from the merge commit and, unless
--no-github is given, cross-checked with GitHub's own record of the pull request. Nothing is typed in.

  python tools/close_record.py --pr N --merge SHA --ids 0008 0009 ...

It refuses to run, and writes nothing, unless for every record:
  - SHA is "Merge pull request #N ..." with two parents (a squash or rebase merge is refused), and GitHub
    names SHA as that pull request's merge commit, merged into main within 5 seconds of the commit's time,
    by the GitHub account named in the Steward's affirmation record;
  - that merge added the record (absent at its first parent, present at the merge);
  - the file is byte-identical to its version at the merge (the affirmed version).
It then writes only the closing rows governance/README.md defines, moves record_state from drafted to
closed, and seals the file: SHA-256 of the complete file with the seal_hash value replaced by 64 zeros.
Finally it checks that removing those rows and moving the state back gives back the affirmed bytes.

The Steward's fixed values (name, role, employer, jurisdiction, capacity, the GitHub account and the
signed attestation text) are copied byte for byte from an already closed record: by default the most
recent one, or the one named with --values-from. The one exception is the Charter id inside the signed
text: the Steward approved the same text with only the Charter id changed, so each record gets the text
with that record's own charter_id in place of the source record's (which the text must name exactly once).
tools/check_governance.py checks the text the same way.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

SEAL_LINE = re.compile(rb"^(\| `seal_hash` \| )([0-9a-f]{64})( \|)$", re.M)
ROW = re.compile(r"^\| `([a-z0-9_]+)` \| (.*) \|$", re.M)
CLOSING = ["closed_at", "accountable_owner_signoff", "affirmation_record", "mode_classification_attestation",
           "seal_algorithm", "seal_hash"]
ACTOR = re.compile(r"^(?P<name>.+) \(GitHub account (?P<login>[A-Za-z0-9-]+)\), the accountable owner$")


def fail(msg):
    sys.exit(f"ABORT: {msg}")


def rows(text):
    return {m.group(1): m.group(2) for m in ROW.finditer(text)}


def fields(cell):
    out = {}
    for part in cell.split("<br>"):
        k, v = part.split(": ", 1)
        out[k] = v
    return out


def charter_id(text):
    return rows(text).get("charter_id", "").replace("`", "").strip()


def text_for(text, source_id, target_id):
    """The signed text with the source record's Charter id (named exactly once) replaced by target_id."""
    pat = r"(?<![\w-])" + re.escape(source_id) + r"(?![\w-])"
    if not source_id or not target_id or len(re.findall(pat, text)) != 1:
        return None
    return re.sub(pat, lambda _: target_id, text)


def main():
    ap = argparse.ArgumentParser(description="Close and seal records from the merge that affirmed them.")
    ap.add_argument("--pr", required=True, type=int, help="the pull request whose merge affirmed the records")
    ap.add_argument("--merge", required=True, help="that pull request's merge commit")
    ap.add_argument("--ids", required=True, nargs="+", help="record numbers, for example 0008 0009")
    ap.add_argument("--values-from", help="the closed record to copy the Steward's fixed values from, e.g. DR-2026-0006")
    ap.add_argument("--repo", default=str(pathlib.Path(__file__).resolve().parent.parent))
    ap.add_argument("--github-repo", default="decision-provenance-standard/standard")
    ap.add_argument("--no-github", action="store_true", help="skip the GitHub cross-check (a dry run only)")
    a = ap.parse_args()
    root = pathlib.Path(a.repo)
    dec = root / "governance" / "decisions"

    def git(*x):
        r = subprocess.run(["git", "-C", str(root), *x], capture_output=True)
        if r.returncode:
            fail(f"git {' '.join(x)}: {r.stderr.decode(errors='replace').strip()}")
        return r.stdout

    def exists(rev_path):
        return subprocess.run(["git", "-C", str(root), "cat-file", "-e", rev_path], capture_output=True).returncode == 0

    # The Steward's fixed values, from an already closed record.
    closed = sorted(p for p in dec.glob("DR-*.md") if "| `record_state` | closed |" in p.read_text(encoding="utf-8"))
    if a.values_from:
        closed = [p for p in closed if p.name.startswith(a.values_from + "-")]
    if not closed:
        fail("no closed record to copy the Steward's fixed values from")
    src = closed[-1]
    sr = rows(src.read_text(encoding="utf-8"))
    signoff, affirm, attest = (fields(sr[k]) for k in ("accountable_owner_signoff", "affirmation_record",
                                                        "mode_classification_attestation"))
    actor = ACTOR.match(affirm["actor_identity"])
    if not actor:
        fail(f"{src.name}: actor_identity is not in the expected form")
    text = attest["attestation_text_signed"]
    if len(text) < 200:
        fail(f"{src.name}: attestation text is shorter than 200 characters")
    src_charter = charter_id(src.read_text(encoding="utf-8"))
    if text_for(text, src_charter, src_charter) is None:
        fail(f"{src.name}: its signed text does not name its Charter id {src_charter!r} exactly once")
    print(f"fixed values from {src.name} (Charter {src_charter}); attestation text {len(text)} characters, "
          f"sha256 {hashlib.sha256(text.encode('utf-8')).hexdigest()}")

    # The merge.
    full = git("rev-parse", "--verify", a.merge + "^{commit}").decode().strip()
    epoch = int(git("log", "-1", "--format=%ct", full).decode().strip())
    merged_at = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    parents = git("log", "-1", "--format=%P", full).decode().split()
    subject = git("log", "-1", "--format=%s", full).decode().strip()
    if not subject.startswith(f"Merge pull request #{a.pr} ") or len(parents) != 2:
        fail(f"{full[:7]} is not a merge commit of pull request #{a.pr}: {subject!r}, {len(parents)} parent(s). "
             "Records are closed only from a merge made with 'Create a merge commit'.")
    print(f"merge commit {full}  time {merged_at}  subject: {subject}")
    if a.no_github:
        print("WARNING: --no-github: GitHub's record of the pull request was not checked; do not publish this result.")
    else:
        r = subprocess.run(["gh", "pr", "view", str(a.pr), "--repo", a.github_repo,
                            "--json", "mergedAt,mergedBy,mergeCommit,state,baseRefName"],
                           cwd=root, capture_output=True, text=True)
        if r.returncode:
            fail(f"gh pr view {a.pr}: {r.stderr.strip()}")
        pr = json.loads(r.stdout)
        gh_at = datetime.datetime.strptime(pr["mergedAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        if pr["state"] != "MERGED" or (pr["mergeCommit"] or {}).get("oid") != full:
            fail(f"GitHub does not name {full[:7]} as the merge commit of pull request #{a.pr}")
        if pr.get("baseRefName") != "main":
            fail(f"pull request #{a.pr} was merged into {pr.get('baseRefName')!r}, not main")
        if abs(gh_at.timestamp() - epoch) > 5:
            fail(f"GitHub's merge time {pr['mergedAt']} is more than 5 seconds from the commit time {merged_at}")
        if (pr["mergedBy"] or {}).get("login") != actor.group("login"):
            fail(f"merged by {(pr['mergedBy'] or {}).get('login')}, not {actor.group('login')}")
        print(f"GitHub: merged at {pr['mergedAt']} by {pr['mergedBy']['login']}; merge commit agrees")

    def closing_rows(signed):
        attest_cell = "<br>".join([
            f"attestor_full_name: {attest['attestor_full_name']}",
            f"attestor_role_title: {attest['attestor_role_title']}",
            f"attestor_employer: {attest['attestor_employer']}",
            f"attestation_timestamp: {merged_at}",
            f"jurisdiction: {attest['jurisdiction']}",
            f"attestation_language_version: {attest['attestation_language_version']}",
            f"attestation_text_signed: {signed}",
            f"attestor_capacity: {attest['attestor_capacity']}",
        ])
        before_redecision = (
            f"| `closed_at` | {merged_at} |\n"
            f"| `accountable_owner_signoff` | signed_by: {signoff['signed_by']}<br>signed_at: {merged_at} |\n"
        )
        after_related = (
            f"| `affirmation_record` | timestamp: {merged_at}<br>actor_identity: {affirm['actor_identity']}<br>"
            f"method: merge of pull request #{a.pr}, which added this record to the repository (merge commit {full}) |\n"
            f"| `mode_classification_attestation` | {attest_cell} |\n"
            "| `seal_algorithm` | SHA-256 |\n"
            "| `seal_hash` | " + "0" * 64 + " |\n"
        )
        return before_redecision, after_related

    closed_now = {}
    for i in a.ids:
        found = sorted(dec.glob(f"DR-*-{i}-*.md"))
        if len(found) != 1:
            fail(f"expected one record numbered {i}, found {len(found)}")
        path = found[0]
        rel = path.relative_to(root).as_posix()
        if exists(f"{parents[0]}:{rel}") or not exists(f"{full}:{rel}"):
            fail(f"{rel} was not added by {full[:7]} (it must be absent before that merge and present after it)")
        affirmed = git("show", f"{full}:{rel}")
        b = path.read_bytes()
        if b != affirmed:
            fail(f"{rel} differs from its affirmed version at {full[:7]}")
        t = b.decode("utf-8")
        if t.count("| `record_state` | drafted |\n") != 1 or any(f"| `{k}` |" in t for k in CLOSING):
            fail(f"{rel} is not a drafted record without closing rows")
        cid = charter_id(t)
        signed = text_for(text, src_charter, cid)
        if signed is None:
            fail(f"{rel} names no charter_id to put in the signed text")
        print(f"{rel}: Charter {cid}; signed text {len(signed)} characters, "
              f"sha256 {hashlib.sha256(signed.encode('utf-8')).hexdigest()}")
        before_redecision, after_related = closing_rows(signed)
        m1 = re.search(r"^\| `re_decision_trigger` \|", t, re.M)
        m2 = re.search(r"^\| `related_decisions` \|.*\n", t, re.M)
        if not m1 or not m2:
            fail(f"{rel} has no re_decision_trigger or related_decisions row to place the closing rows by")
        t = t.replace("| `record_state` | drafted |\n", "| `record_state` | closed |\n")
        m = re.search(r"^\| `re_decision_trigger` \|", t, re.M)
        t = t[:m.start()] + before_redecision + t[m.start():]
        m = re.search(r"^\| `related_decisions` \|.*\n", t, re.M)
        t = t[:m.end()] + after_related + t[m.end():]
        zeroed = t.encode("utf-8")
        seal = hashlib.sha256(zeroed).hexdigest()
        sealed = SEAL_LINE.sub(lambda mm: mm.group(1) + seal.encode() + mm.group(3), zeroed, count=1)
        assert len(SEAL_LINE.findall(sealed)) == 1
        rezeroed = SEAL_LINE.sub(lambda mm: mm.group(1) + b"0" * 64 + mm.group(3), sealed, count=1)
        assert hashlib.sha256(rezeroed).hexdigest() == seal
        undone = sealed.decode("utf-8")
        for row in (before_redecision + after_related.replace("0" * 64, seal)).splitlines(keepends=True):
            assert undone.count(row) == 1, row[:40]
            undone = undone.replace(row, "")
        undone = undone.replace("| `record_state` | closed |\n", "| `record_state` | drafted |\n")
        assert undone.encode("utf-8") == affirmed, rel
        closed_now[path] = (rel, sealed, seal)
    # Every record passed; only now is anything written.
    for path, (rel, sealed, seal) in closed_now.items():
        path.write_bytes(sealed)
        print(f"closed and sealed {rel}: seal_hash {seal}")

if __name__ == "__main__":
    main()
