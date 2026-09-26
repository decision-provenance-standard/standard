# Decision Provenance Standard&trade;

An open standard for audit-ready provenance of consequential decisions made by humans and AI systems together. The Standard defines a Charter object, a decision-record lifecycle, an Article 50-style disclosure block, and a self-declared conformance ladder, so that an organization can show how a decision was reached, who was accountable, and how the record was produced.

**Website:** https://decisionprovenancestandard.org

This repository holds the Standard's official text and its machine-readable reference files. Corrections and proposals are made here, in the open.

## What the Standard is not

> The records are input, not evidence. The Standard informs frameworks without satisfying them. Conformance is self-declared; no body certifies it. It is not legal advice and not a regulatory substitute.

These limits are deliberate. A record produced under the Standard is structured input to the people who judge it — counsel, auditors, internal-controls officers, board fiduciaries — not, by its existence, legal evidence, certification, or attestation. The Standard's primitives map as an input substrate to regulatory and control frameworks; they inform that work without satisfying, replacing, or discharging any framework's obligations, which remain the deployer's.

## What is in this repository

| Path | What it is |
|---|---|
| `spec/` | The Standard's text. Core v1.0 (reading edition rev. 8) is stored one file per section. Companions A to D, Appendix G and the diagrams are also here. |
| `spec/editions.json` | Which files, in which order, make up each published document, with the published and current SHA-256 digests |
| `standard/v5.0/` | Reference files, **release 5.1.0**: JSON schemas, state machines, the conformance-signal list, the reporter contract and the test plan. Same path as on the website. |
| `tools/`, `tests/`, `.github/` | The automated checks that run on every pull request |

Licences differ by folder. [NOTICE](NOTICE) says which licence applies where.

## The text here is the text that was published

- Joining the files in `spec/`, in the order given by `spec/editions.json`, reproduces **byte for byte** the Markdown in the `md/` folder of the published rev. 8 release bundle. The bundle's own checksum is published in the website's `/downloads/SHA256SUMS.txt`.
- The first commit, tagged `rev8-published`, is exactly that text. Corrections arrive afterwards as pull requests.
- `tools/check_split.py` checks on every pull request that:
  - no byte of the text changes without being declared;
  - the order of sections and the line endings stay as published;
  - it says "identical to published" only when that is true.
- The core text keeps the Windows line endings (CRLF) it was published with. The other documents use Unix line endings (LF).

## Versions

- The text is **Core v1.0, rev. 8**. It is paired with **reference release 5.1.0** (Standard §11.2).
- The folder keeps its `v5.0` name so that existing links keep working.
- Where the text and the reference files disagree, the text is the binding one. Known differences are listed and tested in [`tests/known-defects/`](tests/known-defects/).

## Contributing

Issues and pull requests are welcome. Every commit carries a Developer Certificate of Origin sign-off (`git commit -s`), and contributions come in under the same licence as the folder they change. See [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md).

The name "Decision Provenance Standard" and its mark are not licensed by any of the licences in this repository. See [NOTICE](NOTICE).

## How to cite

See [`CITATION.cff`](CITATION.cff), or cite as:

> Etsion, Yohay. *Decision Provenance Standard*, version 1.0 (rev. 8). 2026. https://decisionprovenancestandard.org. Licensed CC BY 4.0.

## Stewardship

Founding Steward: Yohay Etsion. Institutional Steward: Etsion Brands Ltd. See [GOVERNANCE.md](GOVERNANCE.md).
