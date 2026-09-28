# Governance records

This folder holds the Standard's own use of itself by its Steward: a Charter for how the Standard is authored, and the decision records made under it. This is affiliated use, not independent adoption, and it is not a conformance declaration. Etsion Brands is not listed as an adopter.

- [`charter.md`](charter.md) is the Charter `dps-text-authoring`, with every field of Standard §3.2. It declares a target of Level 1 only because the text requires every complete Charter to declare one.
- [`decisions/`](decisions/) holds one file per record, with its fields in the order of Standard §6.2.

**Which text these files follow.** Each record is written against the Standard's text as released in the release its `record_location` names; section numbers refer to that release's text.

## Records index

Every record under the Charter is listed here by id, type, state and date. Standard §6.4.1 requires the Charter's index to list its records so they can be found by record type and by date range; the findability rule of §6.3.2 requires any record to be found within 30 seconds by someone who was not in the room.

| Record | Type | State | Dispatched (UTC) | Decision |
|---|---|---|---|---|
| [DR-2026-0001](decisions/DR-2026-0001-disclosure-block-is-the-standards-own-requirement.md) | decision | closed | 2026-09-28T04:22:41Z | The disclosure block is the Standard's own requirement |
| [DR-2026-0002](decisions/DR-2026-0002-redaction-consent-and-privacy-wording.md) | decision | closed | 2026-09-28T04:22:58Z | Redaction, consent and privacy wording |
| [DR-2026-0003](decisions/DR-2026-0003-release-classification-is-the-stewards-call.md) | decision | closed | 2026-09-28T04:23:16Z | Release classification is the Steward's call |
| [DR-2026-0004](decisions/DR-2026-0004-mode-drift-layers-text-governs.md) | decision | closed | 2026-09-28T04:23:35Z | The mode-drift layers: the text governs |
| [DR-2026-0005](decisions/DR-2026-0005-v1.1-is-a-minor-release.md) | decision | closed | 2026-09-28T05:18:01Z | v1.1 is a minor release |
| [DR-2026-0006](decisions/DR-2026-0006-products-implement-the-standard.md) | decision | closed | 2026-09-28T06:13:32Z | Products and tools implement the Standard |
| [DR-2026-0007](decisions/DR-2026-0007-disclosure-review-at-v1.1.md) | disclosure_review | drafted | 2026-09-28T06:34:38Z | Disclosure review at the v1.1 release |
| [DR-2026-0008](decisions/DR-2026-0008-appendix-g-is-informative-and-counsel-is-a-recommendation.md) | decision | drafted | 2026-09-28T13:35:48Z | Appendix G is informative, and named counsel is a recommendation |
| [DR-2026-0009](decisions/DR-2026-0009-level-rules-in-section-7-and-no-breaks-in-minor-releases.md) | decision | drafted | 2026-09-28T13:35:49Z | Level rules in Section 7, and no breaks in minor releases |
| [DR-2026-0010](decisions/DR-2026-0010-exclusion-in-the-level-checks-and-disclosure-review-evidence.md) | decision | drafted | 2026-09-28T13:35:50Z | The exclusion in the Level checks, and disclosure-review evidence |
| [DR-2026-0011](decisions/DR-2026-0011-level-2-checks-with-nothing-to-check.md) | decision | drafted | 2026-09-28T13:35:51Z | Level 2 checks with nothing to check |
| [DR-2026-0012](decisions/DR-2026-0012-the-declaration-kit-is-steward-only.md) | decision | drafted | 2026-09-28T13:35:52Z | The declaration kit is Steward-only |
| [DR-2026-0013](decisions/DR-2026-0013-v1.2-is-a-minor-release.md) | decision | drafted | 2026-09-28T13:35:53Z | v1.2 is a minor release |
| [DR-2026-0014](decisions/DR-2026-0014-disclosure-review-at-v1.2.md) | disclosure_review | drafted | 2026-09-28T14:23:25Z | Disclosure review at the v1.2 release |

The Charter is in its first version. Any change to it is made by a Charter-amendment record listed here.

## How a record is affirmed, closed and sealed

- **Drafted.** Each record is drafted with AI (Mode 2) and added to the repository at `drafted`.
- **Affirmed.** The affirmation event is the Steward's merge of the pull request that adds the record. Nothing else counts as the affirmation.
- **Closed.** The closing fields that record that event are written in the release pull request: the affirmation record, the accountable owner's sign-off, `closed_at` and the Layer 4 attestation. Their times and their actor are taken from that merge commit's own data: who merged it, and when. The record then moves to `closed`.
- **Sealed.** The seal is computed in the release pull request, after the closing fields are written, over the complete closed record, closing fields included. It does not cover only the text as it stood before the merge. Standard §6.2 describes the seal as "computed at the affirmation moment"; here it is computed after the affirmation, not at that moment, because the affirmation is the Steward's merge and a file cannot contain its own merge.
- **In between.** From the merge that affirms a record until the release pull request merges, the record on `main` is affirmed but still reads `drafted`, with no closing fields and no seal.
- **After.** A closed record is never edited. It can only be superseded by a new record.
- **Review log.** The text requires a `review_log` from the `reviewed` state onward (Standard §6.2.3). Records DR-2026-0001 to DR-2026-0007 were affirmed without one; affirmed records are never edited, so they stay as they are. Records from DR-2026-0008 on list the reviews made before the merge that affirms them.
- **Checked on every pull request.** `python tools/check_governance.py` checks every record's fields against the text, each closed record's closing values against the merge that affirmed it, and each seal.

**Success checks.** Each record has a check at release plus checks at 2, 6 and 12 months after the release named in the record (T+2, T+6, T+12). They are the Steward's own targets, not forecasts.

## The seal

A record's seal is the SHA-256 of the complete closed record file at the release tag, computed with the `seal_hash` value replaced by 64 zeros.

- The file carries its seal in one table row: `` | `seal_hash` | `` followed by 64 lowercase hexadecimal digits and a closing `|`.
- Each record names, in `record_location`, its path and the tag its seal covers.

To check a seal, run this from a clone of the repository, with `FILE` replaced by the record's file name. The first 64 characters of the output must equal the record's `seal_hash`.

```sh
git show v1.1-rev9:governance/decisions/FILE | sed -E '/^\| `seal_hash` \|/s/[0-9a-f]{64}/0000000000000000000000000000000000000000000000000000000000000000/' | sha256sum
```

For each record, use the tag in the index's "Sealed at tag" column in place of `v1.1-rev9`. Without a clone, replace `git show v1.1-rev9:governance/decisions/FILE` with `curl -s https://raw.githubusercontent.com/decision-provenance-standard/standard/v1.1-rev9/governance/decisions/FILE`. Where `sha256sum` is not installed, use `shasum -a 256`.

## Where the records follow the text over the reference files

The records are written to the Standard's text, which binds where the text and the reference files in `standard/v5.0/` differ. Four differences show when the records are checked against the reference schemas:

- **Disclosure block (known defect KD-06).** The text requires five disclosure fields; the reference schema requires seven, adding `disclosure_text_pointer` and `attached_at`. The schema also rejects the text's spellings of the jurisdiction values (`eu`, `us-federal`, `uk`, `israel`, and `other:<...>`). The records carry the text's five fields in the text's spellings.
- **Plain values.** The records write `declaring-authority` and `ai-system-identity` as the text's plain values: a person and the organization they act for; a vendor, model and version. The reference schema expects objects with sub-fields.
- **Peer-reviewer pool.** The reference Charter state machine asks for a `peer_reviewer_pool` of at least three named people before a Charter reaches `fields-completed`. Sections 3.2 and 3.3 of the text do not require one (known defect KD-09), and this Charter has one Steward.
- **Attestation link (known defect KD-01).** The decision-record schema links to the Layer 4 attestation schema by an address that a standard validator cannot resolve. A closed record's attestation object is therefore checked on its own against `standard/v5.0/mode-drift/layer-4-attestation.schema.json`, and the rest of the record against the decision-record schema.

The known defects are listed and tested in [`tests/known-defects/`](../tests/known-defects/).

## The disclosure block

The Charter's `disclosure_metadata_pointer` points here. Every record repeats this block, with its own generation time.

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | In each record's copy: the time that record was drafted |

The jurisdiction tag lists where the records are intended to be read. The Steward reviews this block at each release and records the review as a disclosure-review record, as the Charter's schedule of records commits. There is one at each release: DR-2026-0007 at v1.1, DR-2026-0014 at v1.2.

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.

## License

The files in this folder are text, licensed under CC BY 4.0, as the root [README](../README.md) states for `governance/`.
