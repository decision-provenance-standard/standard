# DR-2026-0010: The exclusion in the Level checks, and disclosure-review evidence

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0010 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T13:35:50Z |
| `record_type` | decision |
| `record_state` | drafted |
| `created_at` | 2026-09-28T13:35:50Z |
| `decision_statement` | The Level 2 disclosure checks (§4.3, §4.6.2's conformance test, §4.7's edge case, the `disclosure_metadata_pointer` row of §6.2.2, and the §7 criteria and signals) apply only to outputs within the §4.6 requirement, so an output a Charter places outside it under §4.6.1 needs no block, and a record for it needs no pointer. Level 3's disclosure-review criterion and the signal `disclosure_review_cadence_current` are met when each block was reviewed within the Charter's cadence, shown by the block's `last_reviewed_at` or by a disclosure-review record dated within the cadence that names the record, and an affirmed record whose block is stored inside it can show review through such a record. Both changes only loosen, so no record or Charter valid under v1.1 (reading edition rev. 9) becomes invalid; no signal is renamed or changes Level, and the reference schema's requirement of a pointer on every Mode 2 record is listed as known defect KD-10. |
| `context_at_decision` | • v1.1's §4.6.1 lets a Charter place outputs outside the disclosure requirement, but the Level 2 checks still asked every Mode 2 record for a block; v1.1's release notes list this as a known issue.<br>• An affirmed record is not edited after close (§6.2.3), so a block stored inside it cannot be given a new `last_reviewed_at` then; a disclosure-review record can show such a review.<br>• Implementations that keep `last_reviewed_at` on an attached block and update it after close still meet the criterion.<br>• Figures 4-1 and 7-1 state the Level 2 and Level 3 criteria, and follow the text. |
| `options_considered` | • Leave the checks as they are. Considered because v1.1 is released. Rejected: excluded outputs would fail Level 2 for a block the text says they do not need.<br>• Extend the exclusion to every Level 2 disclosure check, and accept a disclosure-review record as proof of review. Chosen: both only loosen, and every record and Charter valid under v1.1 stays valid.<br>• Require a disclosure-review record for every review. Considered because affirmed records cannot be edited. Rejected: it would fail implementations that meet the v1.1 criterion with `last_reviewed_at`. |
| `required_inputs_used` | • Standard v1.1 (reading edition rev. 9) and reference files 5.1.1 (the Steward, 2026-09-28; tag `v1.1-rev9`)<br>• The text of v1.2 (reading edition rev. 10) and reference files 5.1.2, as in the pull request that carries this record (the Steward, 2026-09-28; to be tagged `v1.2-rev10`)<br>• GOVERNANCE.md (the Steward, 2026-09-26): the release classes and the compatibility promise<br>• The Charter `dps-text-authoring`, first version (no Charter-amendment record exists) (the Steward, 2026-09-28)<br>• Records DR-2026-0001 to DR-2026-0007 (the Steward, 2026-09-28) |
| `assumptions_depended_on` | • Charters that use the exclusion declare it, or were written before v1.1 and meet its test, so a reader can tell which outputs are outside the requirement.<br>• A disclosure-review record names the records whose blocks it reviews. |
| `success_criteria` | • T+2 (2 months after the v1.2 release): 0 confirmed reports of a Level 2 finding against an output outside the §4.6 requirement (metric: count of confirmed issues).<br>• T+6 (6 months after the v1.2 release): 0 confirmed reports that a Charter meeting v1.1's Level 3 disclosure criterion fails v1.2's (metric: count of confirmed issues).<br>• T+12 (12 months after the v1.2 release): KD-10 is either fixed in the reference files or still listed with its case (metric: KD-10's status in `tests/known-defects/`).<br>• At release: the exclusion appears in §2.2.11, §4.3, §4.6.2, §4.7, §6.2.2, §6.5.1, §6.5.2, §7.1, §7.3 and the read-this-first table; Figures 4-1 and 7-1 match; KD-10 is listed; the v1.1 release notes' known issue is marked addressed. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `review_log` | • reviewer: a fresh AI-drafted legal-claims review made for the Steward; reviewed_at: 2026-09-28T13:55:59Z; outcome: go with changes, with its findings folded into the pull request before the merge<br>• reviewer: a fresh AI-drafted compatibility review made for the Steward; reviewed_at: 2026-09-28T14:11:01Z; outcome: go with changes, with no record or Charter valid under v1.1 made invalid, and its findings folded into the pull request before the merge |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a record or Charter valid under v1.1 failing a v1.2 disclosure check; the Steward then restores its validity in a patch.<br>Market evidence: an adopter reports that the exclusion or the review evidence is unclear, or a reference-files release fixes KD-10. |
| `record_location` | `governance/decisions/DR-2026-0010-exclusion-in-the-level-checks-and-disclosure-review-evidence.md` and, once released, at tag `v1.2-rev10` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007<br>• DR-2026-0008<br>• DR-2026-0009 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T13:35:50Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
