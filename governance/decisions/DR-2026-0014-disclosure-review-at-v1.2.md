# DR-2026-0014: Disclosure review at the v1.2 release

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0014 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T14:23:25Z |
| `record_type` | disclosure_review |
| `record_state` | closed |
| `created_at` | 2026-09-28T14:23:25Z |
| `decision_statement` | The Founding Steward's disclosure review at the v1.2 release (reading edition rev. 10) finds the disclosure blocks of records DR-2026-0007 to DR-2026-0013, and the block in `governance/README.md` to which the Charter's `disclosure_metadata_pointer` points, accurate as written: each names Yohay Etsion, for Etsion Brands Ltd, as the declaring authority and Anthropic / Claude Opus 5.5 as the AI system that drafted the records, tags where the records are intended to be read and their content type, and, in each record, gives that record's own drafting time. No block is changed, and no correcting record is needed. |
| `context_at_decision` | • The Charter is Mode 2, and its schedule of records commits to a disclosure-review record at each release, reviewing the disclosure block in `governance/README.md` (Standard §6.3.1 and §7.2.1).<br>• DR-2026-0007, the review at v1.1, was affirmed by the Steward's merge of pull request #7; records DR-2026-0008 to DR-2026-0013 were drafted with AI and affirmed by the Steward's merge of the pull request that added them.<br>• Each record repeats the block from `governance/README.md` with its own generation time, and names the AI system that drafted it in `drafting_authority`.<br>• v1.2 lets a Level 3 disclosure review be shown by a disclosure-review record as well as by `last_reviewed_at` (Standard §7.4.1); this record is such a review for the blocks of records DR-2026-0007 to DR-2026-0013. |
| `options_considered` | • Find the blocks accurate as written and change nothing. Chosen: every field matches how the records were made, and an affirmed record is never edited.<br>• Issue correcting records with a new block. Considered because a review may find a field to correct. Rejected: no field is inaccurate, so superseding the records would add records without adding information.<br>• Defer the review to the next release. Considered because some records are not yet closed when this record is drafted. Rejected: the Charter commits to a review at each release. |
| `required_inputs_used` | • Records DR-2026-0007 to DR-2026-0013 and their disclosure blocks (the Steward, 2026-09-28)<br>• The Charter `dps-text-authoring`, first version (no Charter-amendment record exists) (the Steward, 2026-09-28)<br>• The disclosure block in `governance/README.md` (the Steward, 2026-09-28)<br>• Standard v1.2 (reading edition rev. 10): §4.6.2 (the five disclosure fields), §6.3.1, §7.2.1 and §7.4.1 (disclosure-review records) (the Steward, 2026-09-28; to be tagged `v1.2-rev10`) |
| `assumptions_depended_on` | • Every record under the Charter was drafted with the same AI system and declared by the same person, so one block fits them all.<br>• The places where the records are intended to be read have not changed since the records were drafted. |
| `success_criteria` | • T+2 (2 months after the v1.2 release): 0 confirmed issues reporting that a disclosure block on a record under the Charter is inaccurate (metric: count of such issues the Steward confirms).<br>• T+6 (6 months after the v1.2 release): every record added under the Charter since v1.2 carries all five disclosure fields, with a generation time equal to its drafting time (metric: count of records that do not, checked by the Steward at each release).<br>• T+12 (12 months after the v1.2 release): every release in the year after v1.2 has its own disclosure-review record (metric: count of releases without one).<br>• At release: this record lists every record whose block it reviewed; each of those blocks has the five fields and a generation time equal to its record's `created_at`; and `governance/README.md` lists this record in the records index. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `review_log` | • reviewer: a fresh AI-drafted release review made for the Steward; reviewed_at: 2026-09-28T16:39:19Z; outcome: go with changes, with its findings folded into the pull request before the merge |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `closed_at` | 2026-09-28T16:49:50Z |
| `accountable_owner_signoff` | signed_by: Yohay Etsion, Founding Steward<br>signed_at: 2026-09-28T16:49:50Z |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a reviewed block to be inaccurate; the Steward then records a correcting record that supersedes the affected record, and a new disclosure review.<br>Market evidence: the Steward starts drafting records with a different AI system or version, or a reader reports that the jurisdiction tag misdescribes where the records are read. |
| `record_location` | `governance/decisions/DR-2026-0014-disclosure-review-at-v1.2.md`, first released at `drafted` with tag `v1.2-rev10`; once closed, at the tag of the release that closes it |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007<br>• DR-2026-0008<br>• DR-2026-0009<br>• DR-2026-0010<br>• DR-2026-0011<br>• DR-2026-0012<br>• DR-2026-0013 |
| `affirmation_record` | timestamp: 2026-09-28T16:49:50Z<br>actor_identity: Yohay Etsion (GitHub account yohayetsion), the accountable owner<br>method: merge of pull request #16, which added this record to the repository (merge commit 60a938f553a96f40ec276d0b46d17c29f366d06d) |
| `mode_classification_attestation` | attestor_full_name: Yohay Etsion<br>attestor_role_title: Founding Steward<br>attestor_employer: Etsion Brands Ltd<br>attestation_timestamp: 2026-09-28T16:49:50Z<br>jurisdiction: IL<br>attestation_language_version: v1.0<br>attestation_text_signed: I, Yohay Etsion, in my role as Founding Steward at Etsion Brands Ltd, confirm that I have reviewed the substantive content of this decision record and that the Mode classification recorded in its metadata, mode-2, accurately reflects the substantive role of AI worker output in framing the options under consideration: the record was drafted with AI and affirmed by me. I make this confirmation within the scope of my role on behalf of Etsion Brands Ltd. This confirmation is made under the Charter dps-text-authoring; it makes no conformance claim and does not constitute legal advice or legal certification.<br>attestor_capacity: director |
| `seal_algorithm` | SHA-256 |
| `seal_hash` | 93fd281373056a2a8076fcfc9454a72ec917f04d27c80084539b98d0b8b00d0c |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T14:23:25Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
