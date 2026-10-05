# DR-2026-0015: The successor Charter, and the first Charter closed

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0015 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-10-04T11:30:18Z |
| `record_type` | charter_amendment |
| `record_state` | closed |
| `created_at` | 2026-10-04T11:30:18Z |
| `decision_statement` | The Founding Steward closes the Charter `dps-text-authoring` by subsumption and adopts the successor Charter `dps-text-authoring-2` for the same decision class, with the same accountable owner, mode and target, and with a `review_log` on every record made under it (Standard §3.3). Records DR-2026-0001 to DR-2026-0015 stay under the first Charter, no record is dispatched under it after its `closed_at`, and every record from DR-2026-0016 on is made under the successor. The successor differs from the first Charter only where the text asks it to: its escalation rule uses the route §3.2 gives a Charter with no higher forum, and its retention is named as a period (§6.4.2). |
| `context_at_decision` | • The first Charter cannot reach its target Level 1: records DR-2026-0001 to DR-2026-0007 were affirmed without a `review_log`, which the text requires from `reviewed` on (§6.2.3, §6.2.4), and an affirmed record is never edited.<br>• Standard §3.3 closes a Charter when its decision class is subsumed by another Charter; a successor is a new Charter with a new `charter_id`, and the records made under the closed Charter stay bound to it.<br>• v1.3 removes the §3.5 clause a new Charter could not meet (DR-2026-0017) and adds a way to meet the escalation rule for a Charter with no higher forum (DR-2026-0018); the first Charter's rule already makes the call public in an escalation record.<br>• The first Charter declared its retention as "permanent"; §6.4.2 asks for a specific duration or a named requirement and does not accept "indefinite", so the successor names a duration and still commits to keeping every record.<br>• DR-2026-0014, affirmed by the merge of the v1.2 release, is closed under the first Charter at the v1.3 release; closing a record is not a new dispatch. |
| `options_considered` | • Keep the first Charter and add records under it. Considered because it changes no Charter. Rejected: the seven records without a `review_log` can never be fixed, so the Charter could never reach its target.<br>• Amend the first Charter to require a `review_log` from now on. Considered because it keeps one Charter. Rejected: an amendment does not cure the seven earlier records, so the Charter still could not reach its target.<br>• Close the first Charter by subsumption and adopt a successor with the same decision class, owner and mode. Chosen: it is the route §3.3 names, it leaves every earlier record unchanged and bound to the Charter it was made under, and every record under the successor can meet the field rule.<br>• Keep both Charters open over the same decision class. Considered because the first Charter stays as it is. Rejected: two open Charters over one decision class leave unclear which one a new record belongs to. |
| `required_inputs_used` | • The Charter `dps-text-authoring`, first version (the Steward, 2026-09-28)<br>• Records DR-2026-0001 to DR-2026-0014 (the Steward, 2026-09-28)<br>• Standard v1.2 (reading edition rev. 10): §3.3, §6.2.3, §6.2.4, §6.4.2 and §7.2.1 (the Steward, 2026-09-28; tag `v1.2-rev10`)<br>• The text of v1.3 (reading edition rev. 11) and reference files 5.2.0, as in the pull request that carries this record (the Steward, 2026-10-04; to be tagged `v1.3-rev11` and `ref-5.2.0`)<br>• A run of the declaration kit (`kit/declaration`) against the first Charter and its records (the Steward, 2026-10-03)<br>• A second fresh AI-drafted pre-execution review of the v1.3 release plan (made for the Steward, 2026-10-03), which found that the governance tools had to learn about a second Charter first<br>• A fresh AI-drafted pre-execution review of the v1.3 release plan (made for the Steward, 2026-10-03), which recommended closing the first Charter by subsumption |
| `assumptions_depended_on` | • A reader can tell which Charter a record was made under from its `charter_id` and the records index.<br>• Both Charters can share one records index and one disclosure block, because they have the same owner, decision class and mode. |
| `success_criteria` | • T+2 (2 months after the v1.3 release): 0 records dispatched under `dps-text-authoring` after its `closed_at` (metric: count of such records, checked by `tools/check_governance.py` on every pull request).<br>• T+6 (6 months after the v1.3 release): every record under `dps-text-authoring-2` carries a well-formed `review_log` (metric: count of records without one).<br>• T+12 (12 months after the v1.3 release): a run of the declaration kit against `dps-text-authoring-2` finds no Level 1 criterion unmet (metric: count of unmet Level 1 criteria).<br>• At release: `governance/charter.md` reads `closed`, with a `closed_at` no earlier than this record's `dispatched_at`; `governance/charter-2.md` carries every §3.2 field at `fields-completed`; and the records index lists the records of both Charters. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `review_log` | • reviewer: a fresh AI-drafted compatibility and records review of this pull request made for the Steward; reviewed_at: 2026-10-04T11:57:29Z; outcome: merge after changes, with its findings folded into the pull request before the merge |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-10-04 |
| `closed_at` | 2026-10-05T11:38:50Z |
| `accountable_owner_signoff` | signed_by: Yohay Etsion, Founding Steward<br>signed_at: 2026-10-05T11:38:50Z |
| `re_decision_trigger` | Outcome evidence: a record is found dispatched under `dps-text-authoring` after its `closed_at`, or a record under `dps-text-authoring-2` without a `review_log`; the Steward then records a correcting record and fixes the check that missed it.<br>Market evidence: a second party joins the Steward in maintaining the Standard, which would give the successor a higher forum, or a reader reports that two Charters over one decision class are hard to follow. |
| `record_location` | `governance/decisions/DR-2026-0015-successor-charter-and-first-charter-closed.md` and, once released, at tag `v1.3-rev11` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007<br>• DR-2026-0008<br>• DR-2026-0009<br>• DR-2026-0010<br>• DR-2026-0011<br>• DR-2026-0012<br>• DR-2026-0013<br>• DR-2026-0014 |
| `affirmation_record` | timestamp: 2026-10-05T11:38:50Z<br>actor_identity: Yohay Etsion (GitHub account yohayetsion), the accountable owner<br>method: merge of pull request #25, which added this record to the repository (merge commit 4567df661d085e44d2e67daeec891e1865b4952a) |
| `mode_classification_attestation` | attestor_full_name: Yohay Etsion<br>attestor_role_title: Founding Steward<br>attestor_employer: Etsion Brands Ltd<br>attestation_timestamp: 2026-10-05T11:38:50Z<br>jurisdiction: IL<br>attestation_language_version: v1.0<br>attestation_text_signed: I, Yohay Etsion, in my role as Founding Steward at Etsion Brands Ltd, confirm that I have reviewed the substantive content of this decision record and that the Mode classification recorded in its metadata, mode-2, accurately reflects the substantive role of AI worker output in framing the options under consideration: the record was drafted with AI and affirmed by me. I make this confirmation within the scope of my role on behalf of Etsion Brands Ltd. This confirmation is made under the Charter dps-text-authoring; it makes no conformance claim and does not constitute legal advice or legal certification.<br>attestor_capacity: director |
| `seal_algorithm` | SHA-256 |
| `seal_hash` | 8bf3a26dd6f6b458e814cbb4b8428252ebcdccccc43f4ea6576e1d91b9470809 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-10-04T11:30:18Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
