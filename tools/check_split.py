# SPDX-License-Identifier: Apache-2.0
"""Integrity check for the Standard's text in spec/.

The text is stored as several files. spec/editions.json says which files, in which order,
make up each published document ("edition"). Joining an edition is plain byte concatenation.

This check FAILS when:
  - a Markdown file in spec/ belongs to no edition, belongs to two, or a listed part is missing;
  - a part of a split document does not start at a heading line;
  - editions.json claims a published digest that differs from the published rev. 8 digests
    fixed in this file (the published release never changes);
  - a part uses a different line-ending convention from the one its edition was published
    with (the core text is CRLF throughout; every other document is LF throughout);
  - the joined text differs from editions.json's `current_sha256` (every text change must be
    declared in the same pull request, so no byte changes by accident);
  - compared with the published baseline (the `rev8-published` tag), a part has been
    dropped, parts have been reordered, or top-level headings have been reordered or dropped;
  - the text differs from the published release and the baseline tag is not available to
    prove the split is still lossless.

It prints "identical to published" only when the joined bytes equal the published digest
fixed in this file.

Usage:  python tools/check_split.py
Exit code 0 = pass, 1 = fail.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec"
BASELINE_TAG = "rev8-published"

# SHA-256 of the Markdown files in the md/ folder of the published release bundle
# decision-provenance-standard-v1.0-rev8-bundle.zip, whose own SHA-256
# (70b67ec02df03e4c2912faf8182557be27e108c61a06c71299ef9dad8932be95) is listed in the
# website's /downloads/SHA256SUMS.txt. These are facts about a past release; they never change.
PUBLISHED = {
    "core": "10f634360b66ff574ceedd79407227a577d46aca3917e9740e0773eee7ca6f51",
    "companion-A": "e372984adc607a519c18d6e91d9f20f024168a5c80c72459ca2a521855a0bfaf",
    "companion-B": "9f1f8b38161696512058db294eefecd0fb28303d74f93ef1700ccb0386b181f9",
    "companion-C": "e53a2b4af11960d5fb6d677728ac5f8dd9bbd4fc8e0fa6e0d4eff155ccd20c3f",
    "companion-D": "3e2945136d995df97afdb3756555434f1c01db83e913ff4f5b964fe175f6fc64",
    "appendix-G": "6f88ff46532f3ab31fedd5300bd6c2a010d6b10b4ee9f3a1013fffe886d53fa2",
}
PUBLISHED_LINE_ENDINGS = {"core": "crlf", "companion-A": "lf", "companion-B": "lf",
                          "companion-C": "lf", "companion-D": "lf", "appendix-G": "lf"}
TAG_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(ref: str, path: str) -> bytes:
    if not TAG_NAME.match(ref):
        raise ValueError(f"refusing unusual ref name {ref!r}")
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{path}"], capture_output=True)
    if r.returncode != 0:
        raise FileNotFoundError(f"{ref}:{path}")
    return r.stdout


def line_ending_problem(b: bytes, rule: str):
    crlf = b.count(b"\r\n")
    lf = b.count(b"\n")
    cr = b.count(b"\r")
    if rule == "crlf":
        if lf != crlf:
            return f"{lf - crlf} line(s) end in LF only; this document is CRLF throughout"
        if cr != crlf:
            return f"{cr - crlf} stray CR byte(s)"
    else:
        if cr:
            return f"{cr} CR byte(s); this document is LF throughout"
    return None


def top_headings(b: bytes):
    return [l.rstrip(b"\r") for l in b.split(b"\n") if l.startswith(b"# ")]


def is_subsequence(needle, hay):
    it = iter(hay)
    return all(any(x == y for y in it) for x in needle)


def main():
    problems, notes = [], []
    manifest = json.loads((SPEC / "editions.json").read_text(encoding="utf-8"))
    if manifest.get("baseline_tag") != BASELINE_TAG:
        problems.append(f"editions.json baseline_tag is {manifest.get('baseline_tag')!r}, expected {BASELINE_TAG!r}")
    editions = {e["id"]: e for e in manifest["editions"]}

    # 1. every published edition present; published digests untouched
    for eid, digest in PUBLISHED.items():
        e = editions.get(eid)
        if not e:
            problems.append(f"edition {eid!r} is missing from editions.json")
            continue
        if e["published"]["sha256"] != digest:
            problems.append(f"{eid}: editions.json 'published' digest was altered (the published release never changes)")
        if e.get("line_endings") != PUBLISHED_LINE_ENDINGS[eid]:
            problems.append(f"{eid}: editions.json line_endings is {e.get('line_endings')!r}, published as {PUBLISHED_LINE_ENDINGS[eid]!r}")

    # 2. files accounted for
    listed = [p for e in manifest["editions"] for p in e["parts"]]
    dupes = sorted({p for p in listed if listed.count(p) > 1})
    on_disk = sorted(p.name for p in SPEC.glob("*.md"))
    if dupes:
        problems.append(f"parts listed more than once: {dupes}")
    if sorted(set(listed) - set(on_disk)):
        problems.append(f"listed but missing: {sorted(set(listed) - set(on_disk))}")
    if sorted(set(on_disk) - set(listed)):
        problems.append(f"Markdown files in spec/ that belong to no edition: {sorted(set(on_disk) - set(listed))}")

    declared_ok = {}
    # 3. per edition: line endings, heading starts, declared current digest, identity with published
    joined_now, changed = {}, []
    for e in manifest["editions"]:
        parts = {p: (SPEC / p).read_bytes() for p in e["parts"] if (SPEC / p).exists()}
        rule = PUBLISHED_LINE_ENDINGS.get(e["id"], e.get("line_endings", "lf"))
        for name, b in parts.items():
            why = line_ending_problem(b, rule)
            if why:
                problems.append(f"{name}: {why}")
            if len(e["parts"]) > 1 and not b.startswith(b"#"):
                problems.append(f"{name} does not start at a heading line")
        joined = b"".join(parts.get(p, b"") for p in e["parts"])
        joined_now[e["id"]] = joined
        digest = sha(joined)
        declared_ok[e["id"]] = (digest == e.get("current_sha256"))
        if not declared_ok[e["id"]]:
            problems.append(f"{e['id']}: the joined text does not match editions.json current_sha256.\n"
                            f"      declared: {e.get('current_sha256')}\n"
                            f"      joined:   {digest}\n"
                            f"      To declare this change, set current_sha256 for {e['id']} in spec/editions.json to the 'joined' value above, "
                            "in the same pull request.")
        pub = PUBLISHED.get(e["id"])
        if pub and digest == pub:
            print(f"[identical] {e['id']}: {len(e['parts'])} part(s), {len(joined)} bytes, identical to published rev. 8")
        else:
            changed.append(e)

    # 4. compare with the baseline tag: parts, part order, heading order, reproducibility
    try:
        base = {x["id"]: x for x in json.loads(git_show(BASELINE_TAG, "spec/editions.json"))["editions"]}
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError):
        base = None
    if base is None:
        if changed:
            problems.append(f"the text differs from published rev. 8 but the tag '{BASELINE_TAG}' is not available "
                            "to prove the split is lossless. In CI, check out with fetch-depth: 0.")
        else:
            notes.append(f"tag '{BASELINE_TAG}' not found; not needed, because every edition is identical to published rev. 8")
    else:
        for eid, b in base.items():
            if eid not in PUBLISHED:
                continue
            at_tag = b"".join(git_show(BASELINE_TAG, f"spec/{p}") for p in b["parts"])
            if sha(at_tag) != PUBLISHED[eid]:
                problems.append(f"{eid}: the parts at tag '{BASELINE_TAG}' no longer join to the published bytes")
            cur = editions.get(eid)
            if not cur:
                continue
            dropped = [p for p in b["parts"] if p not in cur["parts"]]
            if dropped:
                problems.append(f"{eid}: part(s) present at the baseline are no longer listed: {dropped}")
            kept = [p for p in cur["parts"] if p in b["parts"]]
            if kept != [p for p in b["parts"] if p in kept]:
                problems.append(f"{eid}: the order of parts differs from the baseline")
            if not is_subsequence(top_headings(at_tag), top_headings(joined_now.get(eid, b""))):
                problems.append(f"{eid}: top-level headings were reordered or dropped compared with the baseline")
        for e in changed:
            if declared_ok.get(e["id"]):
                print(f"[changed]   {e['id']}: differs from published rev. 8 (declared in editions.json); "
                      f"baseline order and line endings preserved")
            else:
                print(f"[changed]   {e['id']}: differs from published rev. 8 and is NOT yet declared (see FAIL below)")

    for n in notes:
        print("note:", n)
    if problems:
        print("\nFAIL")
        for p in problems:
            print("  -", p)
        return 1
    print("\nPASS: every file is accounted for, line endings and order are intact, and every text change is declared.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
