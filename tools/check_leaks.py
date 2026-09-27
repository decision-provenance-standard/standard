# SPDX-License-Identifier: Apache-2.0
"""Leak guard: internal material must not enter the public text through a change.

Scans only what a change ADDS: the added lines of every text file, the paths of files
it adds or renames, and the messages of its commits. Text already on the base branch
never fails. Three kinds of finding:

  internal record id              ids from the Steward's private decision register
  private path or session trace   local folder paths and AI-session links
  internal name                   names on a hashed list (tools/leak-guard-names.txt)

The name list is stored as salted SHA-256 hashes, so the list itself does not publish
the names. Each word, and each run of two or three words, of every added line is hashed
and compared. This hides the list from a reader; it does not stop someone who already
guesses a name from testing it.

Deliberate exceptions: tools/leak-guard-allow.txt holds the SHA-256 of an exact added
line. `python tools/check_leaks.py --hash-line "the line"` prints that value.

The rules (name list and exceptions) are read from the BASE commit when it has them, so
a change cannot allow its own findings. The workflow likewise runs the base commit's
copy of this script when one exists.

Which change is checked (from the GitHub event):
  pull_request                  base.sha...head.sha (only what the pull request adds)
  push to main                  before...after; nothing on a first push
  local use                     python tools/check_leaks.py [--base origin/main] [--head HEAD]
Other modes:
  --files PATH...               treat the whole of each file as added (to measure findings)
  --self-test                   plant one synthetic example of each kind; each must be found

Exit code 0 = nothing found, 1 = findings (or the check could not run).
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ZERO = "0" * 40
NAMES_FILE = "tools/leak-guard-names.txt"
ALLOW_FILE = "tools/leak-guard-allow.txt"

# Some literals below are split or bracketed so this file does not match its own rules.
ID_PATTERNS = [
    # Register ids carry a year. Years 2090-2099 are left free for made-up examples,
    # such as the record ids in tests/known-defects/cases.json.
    re.compile(r"(?<![A-Za-z0-9])(?:DR|FB|SB|DOC)-20[2-8]\d-\d{3}(?!\d)"),
    re.compile(r"(?<![A-Za-z0-9])IX-20[2-8]\d-\d+"),
    # Learning and assumption ids: L or A, a hyphen, three or more digits. Not when followed
    # by a number, as in SVG path data, and not inside a longer token.
    re.compile(r"(?<![A-Za-z0-9.\-])[LA]-\d{3,}(?!\d)(?!\.\d)(?!\s*,?\s*-?\d)"),
]
PATH_PATTERNS = [
    re.compile(r"(?i)\b[A-Z]:[\\/]+(?:My Driv[e]|de[v]\b)"),
    re.compile(r"(?i)\b[A-Z]:[\\/]+User[s][\\/]"),
    re.compile(r"(?i)[\\/]Users[\\/]yoha[y]"),
    re.compile(r"(?i)(?<![A-Za-z0-9])_backup[s]\b"),
    re.compile(r"(?i)\bcontext[\\/]decision[s]\b"),
    re.compile(r"(?i)(?<![A-Za-z0-9])\.pba[w]\b"),
    re.compile(r"(?i)Claude-Sessio[n]"),
    re.compile(r"(?i)claude\.ai/code/sessio[n]"),
    re.compile(r"(?i)\bsession_[0]"),
]
KIND_ID = "internal record id"
KIND_PATH = "private path or session trace"
KIND_NAME = "internal name (from the hashed list)"
WORD = re.compile(r"[a-z0-9]+")


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or f"git {' '.join(args)} failed")
    return r.stdout


def short(ref):
    return ref[:10] if re.fullmatch(r"[0-9a-f]{40}", ref) else ref


def has_ref(ref):
    return subprocess.run(["git", "rev-parse", "--verify", "-q", ref + "^{commit}"],
                          capture_output=True).returncode == 0


def read_rules_file(path, base):
    """The file as it is on the base commit if it exists there, else the working tree."""
    if base and has_ref(base):
        r = subprocess.run(["git", "show", f"{base}:{path}"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode == 0:
            return r.stdout, f"{path} from {short(base)}"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return fh.read(), f"{path} from the working tree"
    return "", f"{path} (missing)"


def load_names(text):
    salt, hashes = None, set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("salt:"):
            salt = line.split(":", 1)[1].strip()
        elif re.fullmatch(r"[0-9a-f]{64}", line):
            hashes.add(line)
    return salt, hashes


def load_allow(text):
    return {m.group(0) for m in re.finditer(r"(?m)^[0-9a-f]{64}", text)}


def name_hash(salt, phrase):
    return hashlib.sha256(f"{salt}\n{phrase}".encode("utf-8")).hexdigest()


def line_hash(line):
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def find(line, salt, names):
    """Findings on one line: (kind, the text as it appears in the line)."""
    out = []
    for pat in ID_PATTERNS:
        out += [(KIND_ID, m.group(0)) for m in pat.finditer(line)]
    for pat in PATH_PATTERNS:
        out += [(KIND_PATH, m.group(0)) for m in pat.finditer(line)]
    if salt and names:
        spans = [(m.start(), m.end()) for m in WORD.finditer(line.lower())]
        words = [line.lower()[a:b] for a, b in spans]
        for n in (1, 2, 3):
            for i in range(len(words) - n + 1):
                if name_hash(salt, " ".join(words[i:i + n])) in names:
                    out.append((KIND_NAME, line[spans[i][0]:spans[i + n - 1][1]]))
    return out


def added_lines(base, head):
    """(where, text) for every added line, added or renamed path, and commit message line."""
    items = []
    diff = git("diff", "--unified=0", "--no-color", "--no-ext-diff", "--no-renames",
               f"{base}...{head}")
    path, lineno = None, 0
    for raw in diff.splitlines():
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else None
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            lineno = int(m.group(1)) if m else 0
        elif raw.startswith("+") and path:
            items.append((f"{path}:{lineno}", raw[1:].rstrip("\r")))
            lineno += 1
    for p in git("diff", "--name-only", "--diff-filter=AR", f"{base}...{head}").splitlines():
        items.append((f"file name {p}", p))
    for sha in git("rev-list", f"{base}..{head}").split():
        for i, text in enumerate(git("show", "-s", "--format=%B", sha).splitlines(), 1):
            items.append((f"commit {sha[:10]} message, line {i}", text))
    return items


def whole_files(paths):
    items = []
    for p in paths:
        with open(p, encoding="utf-8", errors="replace") as fh:
            for i, text in enumerate(fh.read().splitlines(), 1):
                items.append((f"{p}:{i}", text.rstrip("\r")))
    return items


def range_from_event():
    event, path = os.environ.get("GITHUB_EVENT_NAME"), os.environ.get("GITHUB_EVENT_PATH")
    if not event or not path:
        return None
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    if event == "pull_request":
        return payload["pull_request"]["base"]["sha"], payload["pull_request"]["head"]["sha"]
    if os.environ.get("GITHUB_REF") == "refs/heads/main" and event == "push":
        return payload.get("before", ZERO), payload.get("after") or "HEAD"
    return ("origin/main" if has_ref("origin/main") else ZERO), "HEAD"


def report(items, salt, names, allow):
    findings = []
    for where, text in items:
        if line_hash(text) in allow:
            continue
        for kind, hit in find(text, salt, names):
            findings.append((where, kind, hit))
    return findings


def self_test(salt, names):
    planted = {
        KIND_ID: "See " + "DR-" + "2089-999" + " for the reason.",
        KIND_PATH: "Saved in " + "G:" + "/My Drive/example" + " last week.",
        KIND_NAME: "Tested with " + "zz" + "leak" + "canary" + " today.",
    }
    ok = True
    for kind, text in planted.items():
        found = {k for k, _ in find(text, salt, names)}
        print(f"  {'found  ' if kind in found else 'MISSED '} {kind}")
        ok &= kind in found
    clean = ("Conformance Level 2 applies. See §7.3.1, Companion A, record " + "DR-" + "2099-001"
             + " and path L112 -85.5 L-112 85.5.")
    extra = find(clean, salt, names)
    print(f"  {'clean  ' if not extra else 'FALSE  '} ordinary text ({len(extra)} finding(s))")
    return ok and not extra


def main(argv):
    ap = argparse.ArgumentParser(description="Leak guard for added text.")
    ap.add_argument("--base")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--files", nargs="+")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--hash-line")
    a = ap.parse_args(argv)

    if a.hash_line is not None:
        print(line_hash(a.hash_line))
        return 0

    base, head = (a.base, a.head) if a.base else (range_from_event() or ("origin/main", a.head))
    names_text, names_src = read_rules_file(NAMES_FILE, None if base == ZERO else base)
    allow_text, allow_src = read_rules_file(ALLOW_FILE, None if base == ZERO else base)
    salt, names = load_names(names_text)
    allow = load_allow(allow_text)
    print(f"rules: {names_src} ({len(names)} hashed names); {allow_src} ({len(allow)} exceptions)")
    if not salt or not names:
        print("FAIL: the hashed name list is missing or has no salt.")
        return 1

    if a.self_test:
        print("self-test: one planted example of each kind must be found")
        if self_test(salt, names):
            print("PASS: the guard finds every kind of leak.")
            return 0
        print("FAIL: the guard missed a planted leak or flagged ordinary text.")
        return 1

    if a.files:
        items, what = whole_files(a.files), f"{len(a.files)} whole file(s)"
    elif base == ZERO:
        print("first push to this branch: nothing to compare against, nothing checked.")
        return 0
    else:
        try:
            items, what = added_lines(base, head), f"what {short(base)}...{short(head)} adds"
        except RuntimeError as exc:
            print(f"FAIL: cannot compute the change: {exc}")
            return 1

    findings = report(items, salt, names, allow)
    print(f"checked {len(items)} added line(s), path(s) and message line(s) in {what}")
    for where, kind, hit in findings:
        print(f"  {where}  {kind}: {hit!r}")
    if findings:
        print(f"\nFAIL: {len(findings)} finding(s). Remove them from the change.")
        print("If one is deliberate, the Steward adds the line's value (--hash-line) to "
              f"{ALLOW_FILE} in a separate pull request first.")
        return 1
    print("\nPASS: nothing internal in what this change adds.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
