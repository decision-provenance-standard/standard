# DR-2026-0017: A schedule may list record types not yet produced

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0017 |
| `charter_id` | dps-text-authoring-2 |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-10-04T11:30:21Z |
| `record_type` | decision |
| `record_state` | drafted |
| `created_at` | 2026-10-04T11:30:21Z |
| `decision_statement` | Section 3.5 no longer says that a Charter whose schedule names record types no decisions have produced is non-conformant at Level 1. Section 7.2.1 requires every schedule to list re-decision, escalation and Charter-amendment records before any exist, so a new Charter could not meet both; a Charter whose decisions produce records absent from its schedule still fails. The change only removes a way to fail, so no record or Charter valid under v1.2 becomes invalid, and no Level a Charter could declare against v1.2 changes. |
| `context_at_decision` | • §3.5 (v1.2) called a Charter non-conformant at Level 1 "by construction" when its schedule names record types that no decisions have produced.<br>• §7.2.1 (v1.2) requires the schedule to list decision, re-decision, escalation and Charter-amendment records, and disclosure-review records for a Mode 2 Charter, whether or not any has been produced.<br>• A run of the declaration kit against the Steward's own Charter found the contradiction: that Charter lists re-decision and escalation records, as §7.2.1 requires, although none exists.<br>• No other section, reference file, kit criterion or check repeats the removed clause. |
| `options_considered` | • Delete the clause. Chosen: §7.2.1 is the Level 1 criterion and requires listing the types in advance, and deleting the clause removes a failure without adding one.<br>• Reword the clause to apply only after a set time without a record of a listed type. Considered because it keeps a check on schedules that list types never used. Rejected: it would add a failure condition, which a minor release may not do, and the text gives no basis for the time.<br>• Drop the advance listing from §7.2.1 instead. Considered because it also removes the contradiction. Rejected: the schedule is the Charter's commitment about what records will exist (§3.5, §6.3), and the list is that commitment. |
| `required_inputs_used` | • Standard v1.2 (reading edition rev. 10): §3.5, §6.3.1 and §7.2.1 (the Steward, 2026-09-28; tag `v1.2-rev10`)<br>• The text of v1.3 (reading edition rev. 11) and reference files 5.2.0, as in the pull request that carries this record (the Steward, 2026-10-04; to be tagged `v1.3-rev11` and `ref-5.2.0`)<br>• A run of the declaration kit (`kit/declaration`) against the Charter `dps-text-authoring` and its records (the Steward, 2026-09-28)<br>• A fresh AI-drafted pre-execution review of the v1.3 release plan (made for the Steward, 2026-10-03), which found the §3.5 clause in one place only and that deleting it makes nothing invalid |
| `assumptions_depended_on` | • No adopter relies on the removed clause to fail a Charter.<br>• Readers take §7.2.1's list as a commitment to produce records of those types when they arise, not as a claim that they exist. |
| `success_criteria` | • T+2 (2 months after the v1.3 release): 0 confirmed reports that this change makes a record or Charter valid under v1.2 invalid (metric: count of confirmed compatibility issues).<br>• T+6 (6 months after the v1.3 release): 0 open issues reporting a contradiction between §3.5 and §7.2.1 (metric: count of such issues open more than 30 days).<br>• T+12 (12 months after the v1.3 release): no later release has restored the clause or a stricter form of it (metric: count of such changes).<br>• At release: §3.5 no longer contains "record types that no decisions have produced"; §7.2.1's list is unchanged; and no section, reference file or kit criterion repeats the removed clause. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `review_log` | • reviewer: a fresh AI-drafted compatibility and records review of this pull request made for the Steward; reviewed_at: 2026-10-04T11:57:29Z; outcome: merge after changes, with its findings folded into the pull request before the merge |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring-2<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-10-04 |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a schedule that lists record types the Charter's decision class can never produce, used to hide missing records; the Steward then proposes a check for that case in a later release and records it.<br>Market evidence: an adopter or a reporter implementer asks for a rule on listed record types that stay unused, or a standards body sets one. |
| `record_location` | `governance/decisions/DR-2026-0017-a-schedule-may-list-record-types-not-yet-produced.md` and, once released, at tag `v1.3-rev11` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007<br>• DR-2026-0008<br>• DR-2026-0009<br>• DR-2026-0010<br>• DR-2026-0011<br>• DR-2026-0012<br>• DR-2026-0013<br>• DR-2026-0014<br>• DR-2026-0015<br>• DR-2026-0016 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-10-04T11:30:21Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
