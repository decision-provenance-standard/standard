# DR-2026-0007: Disclosure review at the v1.1 release

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0007 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T06:34:38Z |
| `record_type` | disclosure_review |
| `record_state` | drafted |
| `created_at` | 2026-09-28T06:34:38Z |
| `decision_statement` | The Founding Steward's disclosure review at the v1.1 release (reading edition rev. 9) finds the disclosure blocks of records DR-2026-0001 to DR-2026-0006, and the block in `governance/README.md` to which the Charter's `disclosure_metadata_pointer` points, accurate as written: each names Yohay Etsion, for Etsion Brands Ltd, as the declaring authority and Anthropic / Claude Opus 5.5 as the AI system that drafted the records, tags where the records are intended to be read and their content type, and, in each record, gives that record's own drafting time. No block is changed, and no correcting record is needed. |
| `context_at_decision` | • The Charter is Mode 2, and its schedule of records commits to a disclosure-review record at each release, reviewing the disclosure block in `governance/README.md` (Standard §6.3.1 and §7.2.1).<br>• Records DR-2026-0001 to DR-2026-0005 were drafted with AI and affirmed by the Steward's merge of pull request #5 on 2026-09-28; DR-2026-0006 was drafted with AI on 2026-09-28 in a separate pull request.<br>• Each record repeats the block from `governance/README.md` with its own generation time, and names the AI system that drafted it in `drafting_authority`.<br>• This is the first disclosure-review record under the Charter, so there is no earlier review to compare with. |
| `options_considered` | • Find the blocks accurate as written and change nothing. Chosen: every field matches how the records were made, and an affirmed record is never edited.<br>• Issue correcting records with a new block. Considered because a review may find a field to correct. Rejected: no field is inaccurate, so superseding the records would add records without adding information.<br>• Defer the review to the next release. Considered because DR-2026-0006 is not yet affirmed when this record is drafted. Rejected: the Charter commits to a review at each release, and v1.1 is the first.<br>• Add the reference schema's `disclosure_text_pointer` and `attached_at` fields to every block. Considered because the reference schema requires them. Rejected: the text requires five fields and binds where it differs from the reference files (known defect KD-06). |
| `required_inputs_used` | • Records DR-2026-0001 to DR-2026-0005 and their disclosure blocks (the Steward, affirmed 2026-09-28 by the merge of pull request #5)<br>• Record DR-2026-0006 and its disclosure block (the Steward, drafted 2026-09-28)<br>• The Charter `dps-text-authoring` and the disclosure block in `governance/README.md` (the Steward, 2026-09-28)<br>• Standard v1.1 (reading edition rev. 9): §4.6.2 (the five disclosure fields), §6.3.1 and §7.2.1 (disclosure-review records) (the Steward, 2026-09-28; to be tagged `v1.1-rev9`) |
| `assumptions_depended_on` | • Every record under the Charter was drafted with the same AI system and declared by the same person, so one block fits them all.<br>• The places where the records are intended to be read have not changed since the records were drafted. |
| `success_criteria` | • T+2 (2 months after the v1.1 release): 0 confirmed issues reporting that a disclosure block on a record under the Charter is inaccurate (metric: count of such issues the Steward confirms).<br>• T+6 (6 months after the v1.1 release): every record added under the Charter since v1.1 carries all five disclosure fields, with a generation time equal to its drafting time (metric: count of records that do not, checked by the Steward at each release).<br>• T+12 (12 months after the v1.1 release): every release in the year after v1.1 has its own disclosure-review record (metric: count of releases without one).<br>• At release: this record lists every record whose block it reviewed; each of those blocks has the five fields and a generation time equal to its record's `created_at`; and `governance/README.md` lists this record in the records index. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a reviewed block to be inaccurate; the Steward then records a correcting record that supersedes the affected record, and a new disclosure review.<br>Market evidence: the Steward starts drafting records with a different AI system or version, or a reader reports that the jurisdiction tag misdescribes where the records are read. |
| `record_location` | `governance/decisions/DR-2026-0007-disclosure-review-at-v1.1.md`, first released at `drafted` with tag `v1.1-rev9`; once closed, at the tag of the release that closes it |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T06:34:38Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
