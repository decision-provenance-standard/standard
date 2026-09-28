# SPDX-License-Identifier: Apache-2.0
"""Integrity check for the Standard's text in spec/.

The text is stored as several files. spec/editions.json (format dps-spec-editions/3) says which
files, in which order, make up each published document ("edition"). Joining an edition is plain
byte concatenation. Each edition also lists its releases: for each, the release tag and the
SHA-256 and size of the joined text at that release.

This check FAILS when:
  - editions.json is not format 3, or its baseline_tag is not a well-formed tag name, or is not
    the rev. 8 baseline tag;
  - a Markdown file in spec/ belongs to no edition, belongs to two, or a listed part is missing;
  - a part of a split document does not start at a heading line;
  - an edition's rev. 8 `published` block is missing, or it, or the edition's `published_name`,
    differs from the published rev. 8 values fixed in this file (digest, size, release label
    and file name; the published release never changes);
  - a part uses a different line-ending convention from the one its edition was published
    with (the core text is CRLF throughout; every other document is LF throughout);
  - the joined text differs from editions.json's `current_sha256` (every text change must be
    declared in the same pull request, so no byte changes by accident);
  - compared with the published baseline (the `rev8-published` tag), a part has been
    dropped, parts have been reordered, or top-level headings have been reordered, dropped or
    renamed; a top-level heading may change only through an entry in `heading_renames`, and
    every such entry must match a heading at the baseline and a heading in the text;
  - a release entry is malformed, or its digest does not hold:
      * when the release tag exists, the parts joined at that tag must equal the entry's
        `sha256` and `bytes` (a released digest never changes);
      * before the tag exists (only in the release pull request and on the push before
        tagging), the entry's `sha256` and `bytes` must equal the joined text now;
      * only the newest release of an edition may be untagged, and a release tag reachable from
        the commit being checked must be listed for every edition (a release is never dropped
        from the record);
  - the text differs from the published release and the baseline tag is not available to
    prove the split is still lossless.

It prints "identical to published" only when the joined bytes equal the published digest
fixed in this file, and it says that order, headings and line endings are preserved only
after every check has passed.

Usage:  python tools/check_split.py [--write-joined DIR]
  --write-joined DIR   after every check passes, write each edition's joined text to DIR,
                       named by the release whose digest it equals (the builder's input is
                       then provably the bytes the digest covers).
Exit code 0 = pass, 1 = fail.
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec"
FORMAT = "dps-spec-editions/3"
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
# The rest of each rev. 8 'published' block, and the file name, as in the same bundle's md/ folder.
PUBLISHED_BYTES = {"core": 276948, "companion-A": 90809, "companion-B": 61721,
                   "companion-C": 32582, "companion-D": 24634, "appendix-G": 65872}
PUBLISHED_RELEASE = "Decision Provenance Standard v1.0, rev. 8"
PUBLISHED_NAME = {
    "core": "decision-provenance-standard-v1.0-rev8-core.md",
    "companion-A": "decision-provenance-standard-v1.0-companion-A-regulatory-cross-reference.md",
    "companion-B": "decision-provenance-standard-v1.0-companion-B-worked-charter-library.md",
    "companion-C": "decision-provenance-standard-v1.0-companion-C-implementation-guidance.md",
    "companion-D": "decision-provenance-standard-v1.0-companion-D-diagrams.md",
    "appendix-G": "decision-provenance-standard-v1.0-appendix-G-governance-and-references.md",
}
PUBLISHED_LINE_ENDINGS = {"core": "crlf", "companion-A": "lf", "companion-B": "lf",
                          "companion-C": "lf", "companion-D": "lf", "appendix-G": "lf"}
TAG_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
RELEASE_TAG = re.compile(r"^v(\d+)\.(\d+)-rev(\d+)$")
FILE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
RELEASE_KEYS = {"revision": str, "tag": str, "sha256": str, "bytes": int,
                "published_name": str, "page_name": str, "bundle_name": str}
NAME_SUFFIX = {"published_name": ".md", "page_name": ".html", "bundle_name": ".zip"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True)


def git_show(ref: str, path: str) -> bytes:
    if not TAG_NAME.match(ref):
        raise ValueError(f"refusing unusual ref name {ref!r}")
    r = git("show", f"{ref}:{path}")
    if r.returncode != 0:
        raise FileNotFoundError(f"{ref}:{path}")
    return r.stdout


def tag_exists(tag: str) -> bool:
    if not TAG_NAME.match(tag):
        return False
    return git("rev-parse", "--verify", "--quiet", f"refs/tags/{tag}^{{commit}}").returncode == 0


def release_tags_in_repo():
    """Release tags reachable from the commit being checked (a later release's tag does not bind an older checkout)."""
    r = git("tag", "--list", "--merged", "HEAD")
    if r.returncode != 0:
        return []
    return sorted(t for t in r.stdout.decode("utf-8", "replace").split() if RELEASE_TAG.match(t))


def joined_at(ref: str, eid: str) -> bytes:
    """The edition's parts, as listed in editions.json at `ref`, joined as they stand at `ref`."""
    manifest = json.loads(git_show(ref, "spec/editions.json"))
    ed = {x["id"]: x for x in manifest["editions"]}[eid]
    return b"".join(git_show(ref, f"spec/{p}") for p in ed["parts"])


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


def release_label(tag: str) -> str:
    m = RELEASE_TAG.match(tag)
    return f"v{m.group(1)}.{m.group(2)} rev. {m.group(3)}"


def check_release_entry(eid, i, r, problems):
    """Shape of one releases[] entry. Returns True when it is well formed."""
    where = f"{eid}: releases[{i}]"
    if not isinstance(r, dict):
        problems.append(f"{where} is not an object")
        return False
    ok = True
    for key, typ in RELEASE_KEYS.items():
        if not isinstance(r.get(key), typ) or isinstance(r.get(key), bool):
            problems.append(f"{where}: '{key}' is missing or not a {typ.__name__}")
            ok = False
    extra = sorted(set(r) - set(RELEASE_KEYS))
    if extra:
        problems.append(f"{where}: unexpected key(s) {extra}")
        ok = False
    if not ok:
        return False
    if not RELEASE_TAG.match(r["tag"]):
        problems.append(f"{where}: tag {r['tag']!r} is not of the form v<major>.<minor>-rev<n>")
        return False
    if r["revision"] != release_label(r["tag"]):
        problems.append(f"{where}: revision {r['revision']!r} does not match tag {r['tag']!r} "
                        f"(expected {release_label(r['tag'])!r})")
        ok = False
    if not HEX64.match(r["sha256"]):
        problems.append(f"{where}: sha256 is not 64 lowercase hexadecimal digits")
        ok = False
    if r["bytes"] <= 0:
        problems.append(f"{where}: bytes must be a positive size")
        ok = False
    for key, suffix in NAME_SUFFIX.items():
        if not FILE_NAME.match(r[key]) or not r[key].endswith(suffix):
            problems.append(f"{where}: {key} {r[key]!r} must be a plain file name ending in {suffix}")
            ok = False
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description="Integrity check for the Standard's text in spec/.")
    ap.add_argument("--write-joined", metavar="DIR",
                    help="after every check passes, write each edition's joined text to DIR")
    args = ap.parse_args(argv)

    problems, notes = [], []
    manifest = json.loads((SPEC / "editions.json").read_text(encoding="utf-8"))

    # 0. format and baseline tag
    if manifest.get("format") != FORMAT:
        problems.append(f"editions.json format is {manifest.get('format')!r}, expected {FORMAT!r}")
    bt = manifest.get("baseline_tag")
    if not isinstance(bt, str) or not TAG_NAME.match(bt):
        problems.append(f"editions.json baseline_tag {bt!r} is not a well-formed tag name")
    elif bt != BASELINE_TAG:
        problems.append(f"editions.json baseline_tag is {bt!r}, expected {BASELINE_TAG!r}")
    editions = {e["id"]: e for e in manifest["editions"]}

    # 1. every published edition present; its rev. 8 'published' block and file name untouched
    for eid, digest in PUBLISHED.items():
        e = editions.get(eid)
        if not e:
            problems.append(f"edition {eid!r} is missing from editions.json")
            continue
        pub = e.get("published")
        frozen = {"release": PUBLISHED_RELEASE, "sha256": digest, "bytes": PUBLISHED_BYTES[eid]}
        if not isinstance(pub, dict):
            problems.append(f"{eid}: editions.json has no rev. 8 'published' block (the published release never changes; "
                            f"it must read {frozen})")
        else:
            if pub.get("sha256") != digest:
                problems.append(f"{eid}: editions.json 'published' digest was altered (the published release never changes)")
            for key in ("bytes", "release"):
                if pub.get(key) != frozen[key]:
                    problems.append(f"{eid}: editions.json 'published' {key} is {pub.get(key)!r}, published as "
                                    f"{frozen[key]!r} (the published release never changes)")
            extra = sorted(set(pub) - set(frozen))
            if extra:
                problems.append(f"{eid}: editions.json 'published' block has unexpected key(s) {extra}")
        if e.get("published_name") != PUBLISHED_NAME[eid]:
            problems.append(f"{eid}: editions.json published_name is {e.get('published_name')!r}, published as "
                            f"{PUBLISHED_NAME[eid]!r} (the published release never changes)")
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

    # 3. per edition: line endings, heading starts, declared current digest, identity with published
    joined_now, changed, identical = {}, [], []
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
        if digest != e.get("current_sha256"):
            pending = [r.get("tag") for r in e.get("releases", []) if isinstance(r, dict)
                       and isinstance(r.get("tag"), str) and not tag_exists(r["tag"])]
            extra = (f" While release tag {pending[-1]} is not yet created, set that release's sha256 to the same "
                     f"value and its bytes to {len(joined)}." if pending else "")
            problems.append(f"{e['id']}: the joined text does not match editions.json current_sha256.\n"
                            f"      declared: {e.get('current_sha256')}\n"
                            f"      joined:   {digest}\n"
                            f"      To declare this change, set current_sha256 for {e['id']} in spec/editions.json to the 'joined' value above, "
                            f"in the same pull request.{extra}")
        pub = PUBLISHED.get(e["id"])
        if pub and digest == pub:
            identical.append(e)
        else:
            changed.append(e)

    # 4. heading renames: declared, well formed, one edition each
    renames = {}
    hr = manifest.get("heading_renames", [])
    if not isinstance(hr, list):
        problems.append("editions.json heading_renames must be a list")
        hr = []
    for i, x in enumerate(hr):
        if not (isinstance(x, dict) and set(x) == {"edition", "from", "to"}
                and all(isinstance(x[k], str) for k in x)):
            problems.append(f"heading_renames[{i}] must be an object with exactly 'edition', 'from' and 'to' strings")
            continue
        if x["edition"] not in PUBLISHED:
            problems.append(f"heading_renames[{i}]: unknown edition {x['edition']!r}")
            continue
        if not (x["from"].startswith("# ") and x["to"].startswith("# ")) or x["from"] == x["to"] \
                or any(c in x["from"] + x["to"] for c in "\r\n"):
            problems.append(f"heading_renames[{i}]: 'from' and 'to' must be different single top-level headings ('# ...')")
            continue
        m = renames.setdefault(x["edition"], {})
        if x["from"].encode("utf-8") in m:
            problems.append(f"heading_renames[{i}]: {x['edition']} renames the same heading twice")
            continue
        m[x["from"].encode("utf-8")] = x["to"].encode("utf-8")

    # 5. compare with the baseline tag: parts, part order, heading order, reproducibility
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
        if renames:
            problems.append(f"heading_renames cannot be checked without the tag '{BASELINE_TAG}'")
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
            base_heads = top_headings(at_tag)
            now_heads = top_headings(joined_now.get(eid, b""))
            declared = renames.get(eid, {})
            for old, new in declared.items():
                if old not in base_heads:
                    problems.append(f"{eid}: heading_renames 'from' is not a top-level heading at the baseline: {old.decode('utf-8')!r}")
                if new not in now_heads:
                    problems.append(f"{eid}: heading_renames 'to' is not a top-level heading in the text: {new.decode('utf-8')!r}")
            if not is_subsequence([declared.get(h, h) for h in base_heads], now_heads):
                problems.append(f"{eid}: top-level headings were reordered, dropped or renamed without a declaration "
                                "in heading_renames, compared with the baseline")

    # 6. releases: each digest tied to its tag, or to the text now before the tag exists
    release_status = {}
    for e in manifest["editions"]:
        eid = e["id"]
        rels = e.get("releases")
        if eid in PUBLISHED and not isinstance(rels, list):
            problems.append(f"{eid}: editions.json must carry a 'releases' list (it may be empty)")
            continue
        untagged, tags = [], []
        for i, r in enumerate(rels or []):
            if not check_release_entry(eid, i, r, problems):
                continue
            if r["tag"] in tags:
                problems.append(f"{eid}: release tag {r['tag']} is listed twice")
                continue
            tags.append(r["tag"])
            if tag_exists(r["tag"]):
                try:
                    at = joined_at(r["tag"], eid)
                except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError):
                    problems.append(f"{eid}: release {r['revision']}: cannot read the edition's parts at tag {r['tag']}")
                    continue
                if sha(at) != r["sha256"] or len(at) != r["bytes"]:
                    problems.append(f"{eid}: release {r['revision']}: the parts joined at tag {r['tag']} "
                                    f"({sha(at)}, {len(at)} bytes) do not match releases[{i}] "
                                    f"({r['sha256']}, {r['bytes']} bytes). A released digest never changes.")
                else:
                    release_status.setdefault(r["tag"], []).append((eid, "at the tag"))
            else:
                untagged.append(i)
                now = joined_now.get(eid, b"")
                if sha(now) != r["sha256"] or len(now) != r["bytes"]:
                    problems.append(f"{eid}: release {r['revision']}: tag {r['tag']} does not exist yet, so releases[{i}] "
                                    f"must equal the joined text now.\n"
                                    f"      declared: {r['sha256']}, {r['bytes']} bytes\n"
                                    f"      joined:   {sha(now)}, {len(now)} bytes")
                else:
                    release_status.setdefault(r["tag"], []).append((eid, "tag not yet created; equal to the text now"))
        if len(untagged) > 1 or (untagged and untagged[-1] != len(rels) - 1):
            problems.append(f"{eid}: only the newest release may be untagged (untagged entries: {untagged})")
    by_tag = {}
    for e in manifest["editions"]:
        for r in e.get("releases") or []:
            if isinstance(r, dict) and isinstance(r.get("tag"), str):
                by_tag.setdefault(r["tag"], []).append((e["id"], r))
    for tag, entries in by_tag.items():
        for key in ("revision", "bundle_name"):
            if len({r.get(key) for _, r in entries}) > 1:
                problems.append(f"release tag {tag}: editions disagree on {key}")
    for tag in release_tags_in_repo():
        for eid in PUBLISHED:
            if eid in editions and tag not in [r.get("tag") for r in editions[eid].get("releases") or []
                                               if isinstance(r, dict)]:
                problems.append(f"{eid}: release tag {tag} exists but is not listed in its releases "
                                "(a release is never dropped from the record)")

    # report: facts first; "preserved" and "verified" only when every check passed
    for e in identical:
        print(f"[identical] {e['id']}: {len(e['parts'])} part(s), {len(joined_now[e['id']])} bytes, identical to published rev. 8")
    for e in changed:
        if problems:
            print(f"[changed]   {e['id']}: differs from published rev. 8; not confirmed (see FAIL below)")
        else:
            print(f"[changed]   {e['id']}: differs from published rev. 8 (declared in editions.json); "
                  f"baseline order, headings and line endings preserved")
    if not problems:
        for tag, rows in by_tag.items():
            how = sorted({h for _, h in release_status.get(tag, [])})
            print(f"[release]   {release_label(tag)} (tag {tag}): {len(rows)} edition digest(s) verified, {'; '.join(how)}")
    for n in notes:
        print("note:", n)
    if problems:
        print("\nFAIL")
        for p in problems:
            print("  -", p)
        return 1
    print("\nPASS: every file is accounted for, line endings and order are intact, and every text change is declared.")

    if args.write_joined:
        out = pathlib.Path(args.write_joined).resolve()
        if out == SPEC or SPEC in out.parents:
            print(f"refusing to write joined files inside {SPEC}")
            return 1
        out.mkdir(parents=True, exist_ok=True)
        for e in manifest["editions"]:
            b = joined_now[e["id"]]
            match = [r for r in e.get("releases") or [] if r["sha256"] == sha(b)]
            name = match[-1]["published_name"] if match else f"{e['id']}-unreleased.md"
            (out / name).write_bytes(b)
            label = f"release {match[-1]['revision']}" if match else "no release"
            print(f"[written]   {out / name}: {sha(b)}, {len(b)} bytes ({label})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
