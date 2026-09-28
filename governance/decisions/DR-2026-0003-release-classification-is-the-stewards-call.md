# DR-2026-0003: Release classification is the Steward's call

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0003 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T04:23:16Z |
| `record_type` | decision |
| `record_state` | closed |
| `created_at` | 2026-09-28T04:23:16Z |
| `decision_statement` | The Founding Steward decides, and records publicly in this folder, whether a change to the Standard is a patch, minor or major release; the call concerns the Standard's text only and does not grade, confirm or change any organization's self-declared Level, and no deployer's Level waits on, or is restored by, the Steward's action, so a deployer's own classifier retrain is recorded under its own Charter, not through the Standard's amendment process (Appendix G §G.7.5.2). Anyone may raise the question as an issue, and the Steward aims to answer within 30 days of the issue being raised; no answer is not a ruling either way. GOVERNANCE.md, the §7.5 summary and Appendix G §G.7.7 say the same. |
| `context_at_decision` | • Rev. 8 §7.5 gave the call on contested release classification to "a single named agent (CPO)", and Appendix G §G.7.7 to "a single agent (CPO)".<br>• Rev. 8 left the arbiter's service level "TBD".<br>• Rev. 8 said that a deployer who accepts the arbiter's call is bound by it: "it binds the deployer's Conformance Level grade against the contested case".<br>• Rev. 8 Appendix G §G.7.5.2 said a deployer whose classifier lapsed its corpus separation "must route the change through the amendment process before reasserting Level 2 conformance", so a deployer's Level 2 would wait on the Standard's own amendment process.<br>• GOVERNANCE.md already names the Steward and says the Steward does not certify, audit or grade. |
| `options_considered` | • A named role. Considered because rev. 8 named a role. Rejected: no such role exists apart from the Steward, and GOVERNANCE.md already gives the call to the Steward by name.<br>• A committee. Considered because it would not rest the call on one person. Rejected: no committee exists.<br>• The Steward by name, for the Standard's own releases only, with a deployer's own classifier retrain recorded under its own Charter. Chosen: it matches GOVERNANCE.md and keeps the Steward's action away from any organization's Level.<br>• The Steward also ruling on adopters' contested cases. Considered because rev. 8 let the arbiter's call bind a deployer's grade. Rejected: that is grading, which the Steward does not do.<br>• Keep §G.7.5.2's route through the Standard's amendment process. Considered because rev. 8 treated a lapse as a change to the safety net itself. Rejected: a deployer's Level 2 would come back only when the Steward closed an amendment. |
| `required_inputs_used` | • Standard v1.0, reading edition rev. 8 (the Steward, 2026-05-30; tag `rev8-published`): §7.5, Appendix G §G.7.5.2 and §G.7.7<br>• GOVERNANCE.md (the Steward, 2026-09-26): the Steward's role, the release classes, and what the Steward does not do |
| `assumptions_depended_on` | • One named Steward can answer classification questions within the 30-day target.<br>• No adopter needs the Steward to rule on its own Level. |
| `success_criteria` | • T+2 (2 months after the v1.1 release): the first classification questions, those raised in months 1 and 2, are each answered within 30 days or carry a stated reason for the delay (metric: share of questions raised in months 1 and 2 answered within 30 days of being raised), and none of the answers grades an organization's Level (metric: count of answers that do, checked by the Steward).<br>• T+6 (6 months after the v1.1 release): the questions raised in months 3 to 6 meet the same 30-day target, so the target holds beyond the first weeks (metric: share of questions raised in months 3 to 6 answered within 30 days of being raised), and still no answer grades an organization's Level (metric: count of answers that do, checked by the Steward).<br>• T+12 (12 months after the v1.1 release): over the whole first year, no question went past 30 days without a stated reason, and no two questions in a row went unanswered past the target (metric: share of the year's questions answered within 30 days of being raised); across the year's answers, 0 grade an organization's Level (metric: count of answers that do, checked by the Steward).<br>• At release: no v1.1 sentence gives the Steward a call over any organization's Level or makes a deployer's Level wait on the Steward's action, §G.7.5.2 included; and GOVERNANCE.md, the §7.5 summary and §G.7.7 agree on the call, the "does not grade" limit and the 30-day target. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `closed_at` | 2026-09-28T05:48:09Z |
| `accountable_owner_signoff` | signed_by: Yohay Etsion, Founding Steward<br>signed_at: 2026-09-28T05:48:09Z |
| `re_decision_trigger` | Outcome evidence: a classification question goes unanswered past the 30-day target twice in a row.<br>Market evidence: a second party asks to share the role, or a maintainer lane is named. |
| `record_location` | `governance/decisions/DR-2026-0003-release-classification-is-the-stewards-call.md` and, once released, at tag `v1.1-rev9` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0004<br>• DR-2026-0005 |
| `affirmation_record` | timestamp: 2026-09-28T05:48:09Z<br>actor_identity: Yohay Etsion (GitHub account yohayetsion), the accountable owner<br>method: merge of pull request #5, which added this record to the repository (merge commit 78bc2a9d4d258a54b88445d9fb060cd1b5d8bba6) |
| `mode_classification_attestation` | attestor_full_name: Yohay Etsion<br>attestor_role_title: Founding Steward<br>attestor_employer: Etsion Brands Ltd<br>attestation_timestamp: 2026-09-28T05:48:09Z<br>jurisdiction: IL<br>attestation_language_version: v1.0<br>attestation_text_signed: I, Yohay Etsion, in my role as Founding Steward at Etsion Brands Ltd, confirm that I have reviewed the substantive content of this decision record and that the Mode classification recorded in its metadata, mode-2, accurately reflects the substantive role of AI worker output in framing the options under consideration: the record was drafted with AI and affirmed by me. I make this confirmation within the scope of my role on behalf of Etsion Brands Ltd. This confirmation is made under the Charter dps-text-authoring; it makes no conformance claim and does not constitute legal advice or legal certification.<br>attestor_capacity: director |
| `seal_algorithm` | SHA-256 |
| `seal_hash` | 2817b4136eab64a9b4f5654beb9b4a2ff305080c000b917640e5c90a9644a177 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T04:23:16Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
