# SPDX-License-Identifier: Apache-2.0
"""Developer Certificate of Origin (DCO 1.1) sign-off check.

Every non-merge commit being added must carry at least one line
    Signed-off-by: Full Name <email>
that belongs to the commit's author: its email matches the author's or the committer's
email, or its name matches the author's name (case-insensitive). The name rule keeps a
legitimate contributor green when GitHub records their private no-reply address as the
author while they sign off with their public address. A commit with no sign-off, or
signed off only by someone else, fails.
See https://developercertificate.org/ and CONTRIBUTING.md.

Which commits are checked (from the GitHub event):
  pull_request                  every commit in the pull request (base.sha..head.sha)
  push to main                  before..after, or every commit on a first push
  push / manual run elsewhere   every commit on the branch that is not on origin/main
  local use                     python tools/check_dco.py <rev-range>, e.g. origin/main..HEAD

Exit code 0 = every checked commit is signed off, 1 = at least one is not.
"""
import json
import os
import re
import subprocess
import sys

ZERO = "0" * 40
SIGNOFF = re.compile(r"^Signed-off-by:[ \t]*(?P<name>[^<\n]+?)[ \t]*<(?P<email>[^>\n]+)>[ \t]*$", re.MULTILINE)


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or f"git {' '.join(args)} failed")
    return r.stdout


def has_ref(ref):
    return subprocess.run(["git", "rev-parse", "--verify", "-q", ref], capture_output=True).returncode == 0


def rev_range_from_event():
    event = os.environ.get("GITHUB_EVENT_NAME")
    path = os.environ.get("GITHUB_EVENT_PATH")
    ref = os.environ.get("GITHUB_REF", "")
    if not event or not path:
        return None
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    if event == "pull_request":
        return f"{payload['pull_request']['base']['sha']}..{payload['pull_request']['head']['sha']}"
    if ref == "refs/heads/main":
        before = payload.get("before", ZERO) if event == "push" else ZERO
        after = payload.get("after") or "HEAD"
        return after if before == ZERO else f"{before}..{after}"
    return "origin/main..HEAD" if has_ref("origin/main") else "HEAD"


def belongs_to_author(signoffs, author_name, author_email, committer_email):
    for name, email in signoffs:
        if email in (author_email, committer_email) or name == author_name:
            return True
    return False


def main(argv):
    rng = argv[0] if argv else (rev_range_from_event() or "HEAD")
    try:
        shas = git("rev-list", "--no-merges", rng).split()
    except RuntimeError as exc:
        print(f"FAIL: cannot list commits for {rng!r}: {exc}")
        return 1
    print(f"checking {len(shas)} commit(s) in {rng}")
    bad = []
    for sha in shas:
        fields = git("show", "-s", "--format=%an%x00%ae%x00%ce%x00%s", sha).rstrip("\n").split("\x00")
        author_name, author_email, committer_email, subject = fields[0], fields[1], fields[2], fields[3]
        body = git("show", "-s", "--format=%B", sha)
        signoffs = [(m.group("name").strip().lower(), m.group("email").strip().lower()) for m in SIGNOFF.finditer(body)]
        if signoffs and belongs_to_author(signoffs, author_name.strip().lower(), author_email.strip().lower(),
                                          committer_email.strip().lower()):
            print(f"  ok       {sha[:10]} {subject[:70]}")
            continue
        why = "no Signed-off-by line" if not signoffs else \
            f"signed off by {[s[0] for s in signoffs]}, not by the author {author_name}"
        print(f"  MISSING  {sha[:10]} {subject[:70]}  ({why})")
        bad.append(sha)
    if bad:
        print(f"\nFAIL: {len(bad)} commit(s) without a DCO sign-off by their author.")
        print("Fix: `git commit --amend -s` for the last commit, or `git rebase --signoff <base>` for several, then force-push your branch.")
        return 1
    print("\nPASS: every commit carries a DCO 1.1 sign-off by its author.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
