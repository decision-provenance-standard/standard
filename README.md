# Decision Provenance Standard&trade;

An open standard for audit-ready provenance of consequential decisions made by humans and AI systems together. The Standard defines a Charter object, a decision-record lifecycle, a disclosure block for AI-drafted content, and a self-declared conformance ladder, so that an organization can show how a decision was reached, who was accountable, and how the record was produced.

**Website:** https://decisionprovenancestandard.org

> The current release is version 1.2 (reading edition rev. 10), tag `v1.2-rev10`, released 2026-09-28, with reference files 5.1.2. Versions 1.1 (rev. 9, tag `v1.1-rev9`) and 1.0 (rev. 8, tag `rev8-published`) stay available unchanged. Between releases, `main` may carry corrections not yet released: cite a release, not `main`.

The published text is on the website. Its source and proposed corrections live here. Only a tagged release changes the Standard.

## What the Standard is not

> The records are input, not evidence. The Standard informs frameworks without satisfying them. Conformance is self-declared; no body certifies it. It is not legal advice and not a regulatory substitute.

These limits are deliberate. A record produced under the Standard is structured input to the people who judge it — counsel, auditors, internal-controls officers, board fiduciaries — not, by its existence, legal evidence, certification, or attestation. The Standard's primitives map as an input substrate to regulatory and control frameworks; they inform that work without satisfying, replacing or discharging any framework's obligations.

## What is in this repository

| Path | What it is |
|---|---|
| `spec/` | The Standard's text. Core v1.2 (reading edition rev. 10) is stored one file per section. Companions A to D, Appendix G and the diagrams are also here. |
| `spec/editions.json` | Which files, in which order, make up each published document, with the SHA-256 digest of each release and of the current text |
| `standard/v5.0/` | Reference files, **release 5.1.2**: JSON schemas, state machines, the conformance-signal list, the reporter contract and the test plan. Same path as on the website. |
| `governance/` | The Steward's Charter for authoring the Standard, and the decision records made under it |
| `kit/` | A prompt and a coding-agent skill that help an organization or a product write its self-declaration (Apache-2.0) |
| `tools/`, `tests/`, `.github/` | The automated checks that run on every pull request, and the Steward's tool for closing records |

Licenses differ by folder. Text (`spec/`, `governance/`, and the other documentation files at the repository root, including `CITATION.cff` and `NOTICE`): CC BY 4.0. `standard/v5.0/`, including its Markdown files: MIT for all of 5.x. Code (`tools/`, `tests/`, `.github/`) and any folder of reference files or tooling added later: Apache-2.0. [NOTICE](NOTICE) has the details.

## The text here is the text that was published

- At each release tag, joining the files in `spec/`, in the order given by `spec/editions.json`, gives that release's Markdown **byte for byte**. `spec/editions.json` records each release's SHA-256 digest and size, and `python tools/check_split.py --write-joined <folder>` writes the joined files.
- The first commit, tagged `rev8-published`, is exactly the text of version 1.0 (rev. 8): joined, it reproduces byte for byte the Markdown in the `md/` folder of the published rev. 8 release bundle. The bundle's own checksum is published in the website's `/downloads/SHA256SUMS.txt`.
- Version 1.1 (rev. 9) is tagged `v1.1-rev9`, and version 1.2 (rev. 10) `v1.2-rev10`. Corrections arrive as pull requests.
- `tools/check_split.py` checks on every pull request that:
  - no byte of the text changes without being declared;
  - the order of sections and the line endings stay as published, and a top-level heading changes only where `spec/editions.json` declares the change;
  - each release's digest still matches the text at its tag;
  - it says "identical to published" only when that is true.
- The core text keeps the Windows line endings (CRLF) it was published with. The other documents use Unix line endings (LF).

## Versions

- The current text is **version 1.2 (reading edition rev. 10)**, tag `v1.2-rev10`. It is paired with **reference release 5.1.2**, tag `ref-5.1.2` (Standard §11.2).
- Version 1.1 (reading edition rev. 9) and reference release 5.1.1 stay available unchanged at tags `v1.1-rev9` and `ref-5.1.1`.
- Version 1.0 (reading edition rev. 8) and reference release 5.1.0 stay available unchanged at tag `rev8-published`. Their published files, download addresses and checksums do not change.
- The folder keeps its `v5.0` name so that existing links keep working.
- Where the text and the reference files disagree, the text is the binding one. Known differences are listed and tested in [`tests/known-defects/`](tests/known-defects/).

## Release notes

### Version 1.2 (reading edition rev. 10), with reference files 5.1.2, released 2026-09-28

**A minor release.** The Steward classifies version 1.2 as a minor release ([DR-2026-0013](governance/decisions/DR-2026-0013-v1.2-is-a-minor-release.md)). No record or Charter valid under v1.1 (rev. 9) becomes invalid, under either reading of Appendix G, and no field, allowed value or signal is renamed or removed.

**What changed**

| Change | Decision record |
|---|---|
| Appendix G stays informative apart from its version-stability rules; a §G.11.3 requirement that no core section states reads as a recommendation. The named employment counsel of record becomes a recommended §3.1 field, not a condition of any state or Level. The Standard makes no claim to be a defense to any employment claim, and no longer requires counsel review of the retention period | [DR-2026-0008](governance/decisions/DR-2026-0008-appendix-g-is-informative-and-counsel-is-a-recommendation.md) |
| §7.1 points to the Level rules that sit outside the §7 tables. A minor release can no longer break a Level by listing the break; a change that would break one ships only in a major release | [DR-2026-0009](governance/decisions/DR-2026-0009-level-rules-in-section-7-and-no-breaks-in-minor-releases.md) |
| The §4.6.1 exclusion reaches every Level 2 disclosure check, including the Mode 1 edge case. Level 3's disclosure-review criterion accepts a disclosure-review record as proof of review, as well as `last_reviewed_at` | [DR-2026-0010](governance/decisions/DR-2026-0010-exclusion-in-the-level-checks-and-disclosure-review-evidence.md) |
| Level 2 checks with nothing yet to check do not apply until there is something to check; "cannot be silently mutated" is judged from the records as they stand | [DR-2026-0011](governance/decisions/DR-2026-0011-level-2-checks-with-nothing-to-check.md) |
| The declaration kit (`kit/`) is in the Steward's approval lane | [DR-2026-0012](governance/decisions/DR-2026-0012-the-declaration-kit-is-steward-only.md) |
| Wording: PROV-AGENT is cited as the 2025 research paper it is; the block is called "the disclosure block"; role abbreviations are written out; sentences in the core and the Companions that assumed counsel or said who decides a legal matter now say it is for the deployer to determine; a fourth mode or a disputed classification is raised as an issue or pull request | None needed for wording; the field descriptions that no longer assume counsel are recorded in [DR-2026-0008](governance/decisions/DR-2026-0008-appendix-g-is-informative-and-counsel-is-a-recommendation.md) |
| Figures D1, D2, D4, D5 and D7 follow the text | None needed: explanatory figures |
| Reference files 5.1.2: wording only; the decision-record state machine's Mode 1 close states the Layer 2 route the text states, which 5.1.1 missed | See [`standard/v5.0/release/RELEASE-NOTES.md`](standard/v5.0/release/RELEASE-NOTES.md) |

**Governance records.** Records DR-2026-0007 to DR-2026-0013 are closed and sealed in this release. DR-2026-0014, the disclosure review at v1.2, is affirmed by the merge that adds it and is closed at the next release.

**What stays as it was.** The published rev. 8 and v1.1 files, their download addresses and their checksums stay unchanged, and the tags `rev8-published`, `v1.1-rev9`, `ref-5.1.0` and `ref-5.1.1` never move.

**If you declared a Level with the v1.1 declaration kit,** re-check it with the v1.2 kit. The v1.2 kit also asks about the fields each record must carry at its state (§6.2.4) and about retention (§6.4), rules that already bound under v1.1 and that §7.1 now points to.

**Known issues.** The differences between the text and the reference files are listed and tested in [`tests/known-defects/`](tests/known-defects/) (KD-01 to KD-11), held for reference release 5.2.0.

**What this release publishes.** Text: version 1.2, reading edition rev. 10 (tag `v1.2-rev10`). Reference files: release 5.1.2 (tag `ref-5.1.2`). The repository commit is named in the GitHub release and on the website's downloads page. SHA-256 digests: each document's Markdown in [`spec/editions.json`](spec/editions.json) under `releases`, and every downloadable file in the website's checksum list for this release.

We thank Laurent Lemonnier, iSoluce (laurent@isoluce.net), whose observations led to several of these corrections.

### Version 1.1 (reading edition rev. 9), with reference files 5.1.1, released 2026-09-28

**A minor release.** The Steward classifies version 1.1 as a minor release ([DR-2026-0005](governance/decisions/DR-2026-0005-v1.1-is-a-minor-release.md)), and the change recorded in [DR-2026-0006](governance/decisions/DR-2026-0006-products-implement-the-standard.md) keeps it minor. No record or Charter valid under rev. 8 becomes invalid, and no field, allowed value or signal is renamed or removed.

**What changed**

| Change | Decision record |
|---|---|
| Cleanup with no rule change: internal leftovers removed (internal codes, project terms, private paths, draft notes, launch plans); the Standard's own legal claims removed; the machine-readable files called "reference files" | None needed: no rule changed (pull request #4) |
| The disclosure block is the Standard's own requirement, and whether any law applies is for the deployer to determine. The exclusion keeps rev. 8's output-based test. The declaring authority may name the person, the organization, or both. The text says when disclosure-review records are required, and lists six lifecycle signals in the per-level tables | [DR-2026-0001](governance/decisions/DR-2026-0001-disclosure-block-is-the-standards-own-requirement.md) |
| A redaction record no longer claims to erase anything. The consent gate is the Standard's own. Appendix G §G.11.3 points to the law instead of describing it | [DR-2026-0002](governance/decisions/DR-2026-0002-redaction-consent-and-privacy-wording.md) |
| Whether a change is a patch, minor or major release is the Steward's call, recorded publicly; it never grades anyone's Level | [DR-2026-0003](governance/decisions/DR-2026-0003-release-classification-is-the-stewards-call.md) |
| The mode-drift layers: the text governs over the reference files, the Layer 2 route matches its own questions, and the attestation no longer says where anyone's liability sits | [DR-2026-0004](governance/decisions/DR-2026-0004-mode-drift-layers-text-governs.md) |
| Products and tools "implement" the Standard; they are never called conformant | [DR-2026-0006](governance/decisions/DR-2026-0006-products-implement-the-standard.md) |
| Reference files 5.1.1: wording only; no schema structure, allowed value or signal name changes | See [`standard/v5.0/release/RELEASE-NOTES.md`](standard/v5.0/release/RELEASE-NOTES.md) |

**Governance records.** The Steward's Charter and records are in [`governance/`](governance/). Records DR-2026-0001 to DR-2026-0006 are closed and sealed in this release. The first disclosure-review record, DR-2026-0007, is affirmed by the merge that adds it and is closed at the next release.

**What stays as it was.** The published rev. 8 files, their download addresses and their checksums stay unchanged, and the tag `rev8-published` never moves. Reference release 5.1.0 stays recoverable at that tag.

**Known issue.** Already true in rev. 8 and not changed in this release: the conformance test in §4.6.2, the `disclosure_metadata_pointer` row of §6.2.2 and the Level 2 criteria in §7.3.1 require the disclosure block, or a pointer to it, for every Mode 2 artifact or record. None of them repeats the exclusion for outputs that a Charter declares outside the disclosure requirement under §4.6.1. This will be addressed in a later release. (Addressed in version 1.2: DR-2026-0010.)

**Found after release.** The v1.1 Markdown downloads link figures in a `diagrams/` folder that the release folder did not include; the figures, as released at tag `v1.1-rev9`, were added beside them on the website on 2026-09-28, with new checksum lines, and the v1.1 bundle is unchanged. The two links on the last page of the v1.1 Companion A PDF point at a local address used when it was printed; the PDF stays as released.

**What this release publishes.** Text: version 1.1, reading edition rev. 9 (tag `v1.1-rev9`). Reference files: release 5.1.1. The repository commit is named in the GitHub release and on the website's downloads page, because a commit cannot contain its own id. SHA-256 digests: each document's Markdown in [`spec/editions.json`](spec/editions.json) under `releases`, and every downloadable file in the website's checksum list for this release.

We thank Laurent Lemonnier, iSoluce (laurent@isoluce.net), whose observations led to several of these corrections.

## Contributing

Issues and pull requests are welcome. Every commit carries a Developer Certificate of Origin sign-off (`git commit -s`), and contributions come in under the same license as the folder they change. See [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md).

The licenses in this repository cover the text and files, not the name "Decision Provenance Standard" or its mark. Permitted uses of the name are set out in Standard §11.1. See [NOTICE](NOTICE).

## How to cite

See [`CITATION.cff`](CITATION.cff), or cite as:

> Etsion, Yohay. *Decision Provenance Standard*, version 1.2 (rev. 10). 2026. https://decisionprovenancestandard.org. Licensed CC BY 4.0.

To cite an earlier release, use version 1.1 (rev. 9) and the tag `v1.1-rev9`, or version 1.0 (rev. 8) and the tag `rev8-published`.

## Stewardship

Founding Steward: Yohay Etsion. Institutional Steward: Etsion Brands Ltd. See [GOVERNANCE.md](GOVERNANCE.md).
