# Governance of the Decision Provenance Standard&trade;

## Who decides

- **Yohay Etsion, Founding Steward, has the final say** on what the Standard says. This follows Standard §11.2.
- **Etsion Brands Ltd.** holds the Steward role institutionally, as a stable home and a succession backstop (§11.2).
- There is no committee and no vote. When there are enough regular contributors, the Steward may name **maintainers** for the lanes below. That change will be recorded here.

## Who may approve what

| Lane | Covers | Who approves |
|---|---|---|
| **Steward only** | §5 (Record Lifecycle); §6, including the decision-record schema, §6.2.3.1 and §6.2.3.2; §7 (Conformance Levels); §11; Appendix G; Companion A; every "what this is not" passage, including §1.4 and the non-claim sections; `spec/editions.json`; `NOTICE`; the license files; the reference files under `standard/`; the Steward's own Charter and decision records (`governance/`); the automated checks (`tools/`, `tests/`, `.github/`); this file; `CODEOWNERS`; release tags | The Steward |
| **Maintainer** (no maintainers yet; the Steward meanwhile) | Wording fixes that don't change meaning, broken links, Companion B, C and D examples, diagram text alternatives, translations | A named maintainer |
| **Anyone** | Opening issues and pull requests on anything | No approval needed to open one |

A change is a **rule change**, and goes to the Steward, if it touches a MUST, SHALL, SHOULD or MAY sentence, a field, an allowed value, a conformance signal or a "required at this state" rule, wherever it sits.

## How the Steward's own changes are handled

- The Steward uses the same route as everyone: branch, pull request, automated checks, merge. Nobody pushes directly to `main`.
- GitHub does not let anyone approve their own pull request. The Steward may therefore **bypass the approval rule, but never the automated checks**. The two are kept in separate rule sets for exactly this reason, and GitHub records every bypass.
- **Every rule change carries a decision record**, written in the Standard's own format and kept in this repository. The Steward affirms it by merging the pull request.
- These records are the Standard's own use of itself. They are affiliated use, not independent adoption.

## Versions and the compatibility promise

| Release | What it may do |
|---|---|
| Patch | Fix wording or errors; change no rule |
| Minor | Add and clarify, never making a previously valid record invalid (Standard §11.2; Appendix G §G.7.5–§G.7.6) |
| Major | Make some previously valid records invalid; needs at least 12 months' notice and a migration note |

- **Renamed values.** When an allowed value is renamed, the old value stays accepted and is marked deprecated. It is removed only in a major release.
- **What each release publishes.** Each release names the text revision, the reference-files release and the repository commit, and gives the SHA-256 digest of every published file.
- **Whether a change is a patch, minor or major release** is decided by the Steward, by name, and recorded publicly as a decision record. The call concerns the Standard's text; it does not grade, confirm or change any organization's self-declared Level. Anyone may raise the question as an issue. The Steward aims to answer within 30 days of the issue being raised. No answer is not a ruling either way. Appendix G §G.7.7 says the same.

## What the Steward does not do

- The Steward does not certify, audit or grade anyone's conformance, and runs no registry of conformant organizations (§11.2). Conformance is self-declared.
- When reviewing a listing of self-declared adopters, the Steward checks only that it has the structural elements Appendix G §G.11.4 names.

## Succession

- If the Founding Steward can no longer steward, the succession rules in Standard §11.2 apply.
- Etsion Brands Ltd. appoints a successor. On a change of control, the role passes to a successor entity or a community-governance body named at the Standard's canonical address.
- The text stays available under its license throughout.

## Where decisions are recorded

- Decisions about the Standard are recorded in this repository.
- Discussion takes place in issues and pull requests.
- Changes to this file are Steward-only and are themselves recorded as decisions.
