# DR-2026-0004: The mode-drift layers: the text governs

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0004 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T04:23:35Z |
| `record_type` | decision |
| `record_state` | drafted |
| `created_at` | 2026-09-28T04:23:35Z |
| `decision_statement` | Sections 4.8.1 to 4.8.3 are the normative statement of the mode-drift safety net; the files in `standard/v5.0/mode-drift/` describe them, the text governs where they differ, and no sentence points normatively at an unpublished document. A Mode 1 record now routes to Layer 3 when the declaring authority answers Yes or Uncertain to any of Q1-Q3, answers anything but Yes to Q4, or declines to answer, or when Layer 1 and Layer 2 disagree; this sends one answer pattern, Yes to all four questions, to review where rev. 8's core sentence closed it, and records that closed before v1.1 (reading edition rev. 9) keep the route recorded with them (`routing_decision`, with the `challenge_prompt_version` they were shown). The Layer 4 attestation records who signed and in what capacity; the Standard makes no claim about how that capacity, or any indemnity a deployer offers, affects anyone's personal liability. |
| `context_at_decision` | • Rev. 8 pointed at a private document, which it called the sub-spec, in 43 lines, including Level 2 criteria, and said it was "referenced normatively"; nobody outside could read it.<br>• Rev. 8's core Layer 2 sentence ("any non-Yes answer" routes the record to Layer 3) contradicted its own questions, so every clean Mode 1 record, which answers No to Q1-Q3, would go to peer review. Rev. 8's Layer 2 reference file carried both routes: its summary line and the attestation text signers read used the core sentence's route, and only its routing table used the corrected one.<br>• Under rev. 8's core sentence, a record answered Yes to all four questions closed as Mode 1. Yes to Q1-Q3 means its author says AI shaped its framing, recommendation or prose, so its Mode 1 label was already wrong.<br>• Rev. 8 said the attestation "cabins personal liability to the employer", and the Layer 4 reference file supplied legal wording for signers in several jurisdictions. |
| `options_considered` | • Keep the text. Considered because it changes nothing. Rejected: it keeps a normative pointer nobody can read, a route that contradicts its own questions, and claims about signers' liability.<br>• Point at the public layer files as normative. Considered because they are published. Rejected: they are informative MIT files and carried the same defects.<br>• Make the text normative and fix the route, with a transition for records already closed. Chosen: the rule then lives where readers can check it, the route matches its own questions, and no record closed under rev. 8 becomes invalid.<br>• Fix the route with no transition. Considered as the simpler rule. Rejected: a record closed under rev. 8's route would be judged by a route it was never shown.<br>• Leave the route contradiction as a known issue. Considered as the fallback if the route were not fixed now. Rejected: the corrected release would republish a rule that contradicts itself. |
| `required_inputs_used` | • Standard v1.0, reading edition rev. 8 (the Steward, 2026-05-30; tag `rev8-published`): §4.8, §7.3, Appendix G §G.7, Companion B, and Companion D (figure D5)<br>• Reference files, release 5.1.0 (the Steward; tag `rev8-published`): `standard/v5.0/mode-drift/`, layers 1 to 4 |
| `assumptions_depended_on` | • No implementation depends on the private document, since it was never published.<br>• Few implementations, if any, close a record answered Yes to all four questions: rev. 8's Layer 2 routing table already sent it to review, although the rest of that file used the core sentence's route.<br>• Records keep the attestation and challenge wording they were shown and the route recorded with them (`attestation_language_version`, `challenge_prompt_version`, `routing_decision`), so neither the new route nor the removal of the liability wording changes a record already closed. |
| `success_criteria` | • T+2 (2 months after the v1.1 release): 0 confirmed issues reporting a normative pointer to an unpublished document (metric: count of such issues the Steward confirms).<br>• T+6 (6 months after the v1.1 release): 0 confirmed reports that the Layer 2 route and its questions disagree anywhere (metric: count of such reports the Steward confirms).<br>• T+12 (12 months after the v1.1 release): 0 confirmed reports that a record closed under rev. 8 is invalid under v1.1 because of this change (metric: count of confirmed compatibility issues).<br>• At release: a search for "sub-spec" finds nothing normative; no sentence states where an attestor's liability sits; and the text states the new route together with its transition for records that closed before v1.1 (reading edition rev. 9), naming `routing_decision` as the field that holds each record's route. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `re_decision_trigger` | Outcome evidence: a confirmed issue of a kind the success criteria count.<br>Market evidence: a deployer reports that its own attestation practice needs wording the Standard no longer supplies. |
| `record_location` | `governance/decisions/DR-2026-0004-mode-drift-layers-text-governs.md` and, once released, at tag `v1.1-rev9` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0005 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T04:23:35Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
