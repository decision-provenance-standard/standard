# DR-2026-0019: Our own statements of readers' obligations become recommendations

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0019 |
| `charter_id` | dps-text-authoring-2 |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-10-04T11:30:23Z |
| `record_type` | decision |
| `record_state` | closed |
| `created_at` | 2026-10-04T11:30:23Z |
| `decision_statement` | Where the Standard stated an obligation of its readers, it now recommends or requests instead: the not-legal-advice notice says legal matters should be reviewed by a licensed attorney, where it said they require that review (the title page, Read This First, §1.2, §1.4.2 and §4.1). Section 1.5 states what the Steward asks of users, where it said which uses are outside the CC BY 4.0 license and that derivative authors must mark their work, and the conditions §1.5.1 attached to extending and forking (a downstream marker, a divergence statement, a different name) become the Steward's requests. No record or Charter valid under v1.2 becomes invalid, and no Level a Charter could declare against v1.2 changes, because none of these sentences is a field, a Charter requirement or a conformance criterion. |
| `context_at_decision` | • Record DR-2026-0008 decided that the Standard requires no counsel, yet the notice still said legal matters "require review by a licensed attorney" in four places and "must review it" in a fifth, and §1.2 said every installation "will require" professional review.<br>• §1.5.2 said certain uses were "outside the license", "not a CC-BY 4.0 use" and "not authorized by ... the CC-BY 4.0 license"; what the license permits is set by its own terms, not by the Standard.<br>• §1.5.2 said derivative authors "must mark their work as their own" and that a derivative that strips the firewall language "must mark itself as such"; §1.5.1 listed a downstream marker, a divergence statement and a different name as conditions of extending and forking under the license.<br>• No conformance criterion in §7, no field in §3 or §6, no reference file and no check reads any of these sentences.<br>• The notice keeps everything else word for word: the Standard is not legal advice, creates no attorney-client relationship, and is not to be relied on as the sole basis for any legal, compliance or employment decision. |
| `options_considered` | • Keep the wording. Considered because it changes nothing. Rejected: it states obligations the Standard does not impose and contradicts DR-2026-0008.<br>• Delete the review sentence from the notice. Considered because the Standard requires no counsel. Rejected: the recommendation is useful to readers and keeps the notice's protective purpose.<br>• Recommend review ("should") and turn §1.5's license statements and "must" duties into the Steward's requests. Chosen: it removes requirements only, and keeps the advice and the requests.<br>• Delete §1.5.2's list. Considered because the license governs use of the text. Rejected: the requests still tell readers what the Steward considers misuse, and the trademark item stands on the Steward's own permission. |
| `required_inputs_used` | • Standard v1.2 (reading edition rev. 10) and reference files 5.1.2 (the Steward, 2026-09-28; tag `v1.2-rev10`)<br>• The text of v1.3 (reading edition rev. 11), as in the pull request that carries this record (the Steward, 2026-10-04; to be tagged `v1.3-rev11`)<br>• GOVERNANCE.md (the Steward, 2026-09-26): the release classes and the compatibility promise<br>• Record DR-2026-0008 (the Steward, 2026-09-28)<br>• An AI-drafted legal-claims review made for the Steward in the final audit of v1.2 (the Steward, 2026-09-28)<br>• A fresh AI-drafted pre-execution review of the v1.3 release plan (made for the Steward, 2026-10-03), which asked that the requests made of derivative authors be covered by this record |
| `assumptions_depended_on` | • No adopter relies on the notice or on §1.5 as a requirement for its own records or Charter to be valid.<br>• Readers take "should" and "the Steward asks" as a recommendation and a request, not as conditions of validity or of the license. |
| `success_criteria` | • T+2 (2 months after the v1.3 release): 0 confirmed reports that a record or Charter valid under v1.2 is invalid under v1.3 because of these changes (metric: count of confirmed compatibility issues).<br>• T+6 (6 months after the v1.3 release): 0 open issues reporting a sentence of the released text that states what a law or the license requires (metric: count of such issues open more than 30 days).<br>• T+12 (12 months after the v1.3 release): no release has had to restore one of these requirements (metric: count of such changes).<br>• At release: a search of the released text finds no "require review by a licensed attorney", no "must review it", no "will require.", no "outside the license", no "not a CC-BY 4.0 use", no "not authorized by either the trademark or the CC-BY 4.0 license" and no "must mark"; and the website's hand-written FAQ, academic summary and firewall pages say the same as the text. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `review_log` | • reviewer: a fresh AI-drafted compatibility and records review of this pull request made for the Steward; reviewed_at: 2026-10-04T11:57:29Z; outcome: merge after changes, with its findings folded into the pull request before the merge |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring-2<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-10-04 |
| `closed_at` | 2026-10-05T11:38:50Z |
| `accountable_owner_signoff` | signed_by: Yohay Etsion, Founding Steward<br>signed_at: 2026-10-05T11:38:50Z |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a record or Charter valid under v1.2 that is invalid under v1.3 because of these changes; the Steward then restores its validity in a patch and records it.<br>Market evidence: a reader reports a sentence of the released text that states what a law or the license requires; the Steward rewrites it as a non-claim before the next release. |
| `record_location` | `governance/decisions/DR-2026-0019-readers-obligations-become-recommendations.md` and, once released, at tag `v1.3-rev11` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007<br>• DR-2026-0008<br>• DR-2026-0009<br>• DR-2026-0010<br>• DR-2026-0011<br>• DR-2026-0012<br>• DR-2026-0013<br>• DR-2026-0014<br>• DR-2026-0015<br>• DR-2026-0016<br>• DR-2026-0017<br>• DR-2026-0018 |
| `affirmation_record` | timestamp: 2026-10-05T11:38:50Z<br>actor_identity: Yohay Etsion (GitHub account yohayetsion), the accountable owner<br>method: merge of pull request #25, which added this record to the repository (merge commit 4567df661d085e44d2e67daeec891e1865b4952a) |
| `mode_classification_attestation` | attestor_full_name: Yohay Etsion<br>attestor_role_title: Founding Steward<br>attestor_employer: Etsion Brands Ltd<br>attestation_timestamp: 2026-10-05T11:38:50Z<br>jurisdiction: IL<br>attestation_language_version: v1.0<br>attestation_text_signed: I, Yohay Etsion, in my role as Founding Steward at Etsion Brands Ltd, confirm that I have reviewed the substantive content of this decision record and that the Mode classification recorded in its metadata, mode-2, accurately reflects the substantive role of AI worker output in framing the options under consideration: the record was drafted with AI and affirmed by me. I make this confirmation within the scope of my role on behalf of Etsion Brands Ltd. This confirmation is made under the Charter dps-text-authoring-2; it makes no conformance claim and does not constitute legal advice or legal certification.<br>attestor_capacity: director |
| `seal_algorithm` | SHA-256 |
| `seal_hash` | 980008a83195edf0a1787e772614c063fba739221175d682079de25900228228 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-10-04T11:30:23Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
