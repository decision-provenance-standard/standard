# Governance records

This folder holds the Standard's own use of itself by its Steward: a Charter for how the Standard is authored, and the decision records made under it. This is affiliated use, not independent adoption, and it is not a conformance declaration. Etsion Brands is not listed as an adopter.

- [`charter.md`](charter.md) is the Charter `dps-text-authoring`, with every field of Standard §3.2. It declares a target of Level 1 only because the text requires every complete Charter to declare one.
- [`decisions/`](decisions/) holds one file per record, with its fields in the order of Standard §6.2.

**Which text these files follow.** The files are written against the Standard's text on `main` as corrected for v1.1 (reading edition rev. 9), which the release pull request tags as `v1.1-rev9`. Section numbers refer to that text.

## Records index

Every record under the Charter is listed here by id, type, state and date. Standard §6.4.1 requires the Charter's index to list its records so they can be found by record type and by date range; the findability rule of §6.3.2 requires any record to be found within 30 seconds by someone who was not in the room.

| Record | Type | State | Dispatched (UTC) | Decision |
|---|---|---|---|---|
| [DR-2026-0001](decisions/DR-2026-0001-disclosure-block-is-the-standards-own-requirement.md) | decision | drafted | 2026-09-28T04:22:41Z | The disclosure block is the Standard's own requirement |
| [DR-2026-0002](decisions/DR-2026-0002-redaction-consent-and-privacy-wording.md) | decision | drafted | 2026-09-28T04:22:58Z | Redaction, consent and privacy wording |
| [DR-2026-0003](decisions/DR-2026-0003-release-classification-is-the-stewards-call.md) | decision | drafted | 2026-09-28T04:23:16Z | Release classification is the Steward's call |
| [DR-2026-0004](decisions/DR-2026-0004-mode-drift-layers-text-governs.md) | decision | drafted | 2026-09-28T04:23:35Z | The mode-drift layers: the text governs |
| [DR-2026-0005](decisions/DR-2026-0005-v1.1-is-a-minor-release.md) | decision | drafted | 2026-09-28T05:18:01Z | v1.1 is a minor release |
| [DR-2026-0006](decisions/DR-2026-0006-products-implement-the-standard.md) | decision | drafted | 2026-09-28T06:13:32Z | Products and tools implement the Standard |

The Charter is in its first version. Any change to it is made by a Charter-amendment record listed here.

## How a record is affirmed, closed and sealed

- **Drafted.** Each record is drafted with AI (Mode 2) and added to the repository at `drafted`.
- **Affirmed.** The affirmation event is the Steward's merge of the pull request that adds the record. Nothing else counts as the affirmation.
- **Closed.** The closing fields that record that event are written in the release pull request: the affirmation record, the accountable owner's sign-off, `closed_at` and the Layer 4 attestation. Their times and their actor are taken from that merge commit's own data: who merged it, and when. The record then moves to `closed`.
- **Sealed.** The seal is computed in the release pull request, after the closing fields are written, over the complete closed record, closing fields included. It does not cover only the text as it stood before the merge. Standard §6.2 describes the seal as "computed at the affirmation moment"; here it is computed after the affirmation, not at that moment, because the affirmation is the Steward's merge and a file cannot contain its own merge.
- **In between.** From the merge that affirms a record until the release pull request merges, the record on `main` is affirmed but still reads `drafted`, with no closing fields and no seal.
- **After.** A closed record is never edited. It can only be superseded by a new record.

**Success checks.** Each record has a check at release plus checks at 2, 6 and 12 months after the v1.1 release (T+2, T+6, T+12). They are the Steward's own targets, not forecasts.

## The seal

A record's seal is the SHA-256 of the complete closed record file at the release tag, computed with the `seal_hash` value replaced by 64 zeros.

- The file carries its seal in one table row: `` | `seal_hash` | `` followed by 64 lowercase hexadecimal digits and a closing `|`.
- Each record names, in `record_location`, its path and the tag its seal covers.

To check a seal, run this from a clone of the repository, with `FILE` replaced by the record's file name. The first 64 characters of the output must equal the record's `seal_hash`.

```sh
git show v1.1-rev9:governance/decisions/FILE | sed -E '/^\| `seal_hash` \|/s/[0-9a-f]{64}/0000000000000000000000000000000000000000000000000000000000000000/' | sha256sum
```

Without a clone, replace `git show v1.1-rev9:governance/decisions/FILE` with `curl -s https://raw.githubusercontent.com/decision-provenance-standard/standard/v1.1-rev9/governance/decisions/FILE`. Where `sha256sum` is not installed, use `shasum -a 256`.

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

The jurisdiction tag lists where the records are intended to be read. The Steward reviews this block at each release and records the review as a disclosure-review record, as the Charter's schedule of records commits. The first one is added at the v1.1 release.

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.

## License

The files in this folder are text, licensed under CC BY 4.0, as the root [README](../README.md) states for `governance/`.
