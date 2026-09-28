# DR-2026-0002: Redaction, consent and privacy wording

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0002 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T04:22:58Z |
| `record_type` | decision |
| `record_state` | closed |
| `created_at` | 2026-09-28T04:22:58Z |
| `decision_statement` | A redaction-event record records the deployer's statement that the named fields have been removed from operational use; the record does not by itself remove or erase anything, whether the removal meets any erasure right is for the deployer to determine, and the same wording is used in §5.5, the §6.2.3.2 reader notice, and Companion A §A.2.bis and §A.bis. The consent gate for records about individuals stays unchanged as the Standard's own voluntary gate, makes no claim about the legal basis for processing, and records a consent withdrawal as a new affirmed record, without the undefined field name `consent_withdrawal_event`. Appendix G §G.11.3 points to whatever law applies to the deployer instead of describing it and keeps every SHALL in it and the list of works-council regimes it cites; Companion A §A.11 leaves to the deployer, for each law it cites, whether the law applies, what it requires and who carries any duty under it; and §A.bis's SHOULD for a deployer under both UK and EU GDPR now applies where the deployer determines that both apply, against whichever the deployer determines is more demanding. |
| `context_at_decision` | • Rev. 8 §5.5 and the `redacted_fields` description said the named fields are "legally erased".<br>• Rev. 8 Appendix G §G.11.3 said the redaction pattern "operationalizes the erasure", and Companion A §A.2.bis said the named fields "are erased from the operational data store, operationalizing the deployer's Article 17 erasure obligation".<br>• Rev. 8's §6.2.3.2 read-time notice told a reader that "the named fields are erased from operational use".<br>• §G.11.3 described what GDPR, CCPA, Israeli, German, French and U.S. law require, and attributed numbers to regulators.<br>• §G.11.3 referred to a field, `consent_withdrawal_event`, that §6.2.3 never defines. |
| `options_considered` | • Keep the wording. Considered because it changes nothing. Rejected: it keeps the claim that a record erases data, and the descriptions of what named laws require.<br>• Define a new `consent_withdrawal_event` field. Considered because the text already used the name. Rejected: it adds a new field for a wording fix.<br>• Reword, point to the law instead of describing it, and drop the undefined reference. Chosen: it removes the legal claims, keeps every SHALL, and adds or removes no field. |
| `required_inputs_used` | • Standard v1.0, reading edition rev. 8 (the Steward, 2026-05-30; tag `rev8-published`): §5.5, §6.2.3, §6.2.3.2, Appendix G §G.11.3, Companion A §A.2.bis, §A.bis and §A.11, and the §3 pointers to the list of works-council regimes<br>• observations from an outside reviewer (credited in the release notes in a form they approve, or without a name if they have not answered) |
| `assumptions_depended_on` | • No adopter relies on a redaction record as proof of erasure.<br>• Keeping every SHALL while removing the law descriptions leaves the gate usable on its own. |
| `success_criteria` | • T+2 (2 months after the v1.1 release): 0 confirmed issues reporting that a redaction record is presented as erasing data or meeting an erasure right (metric: count of such issues the Steward confirms).<br>• T+6 (6 months after the v1.1 release): 0 confirmed reports that a redaction or consent record valid under rev. 8 fails v1.1 (metric: count of confirmed compatibility issues).<br>• T+12 (12 months after the v1.1 release): no later release has had to amend §5.5 or §G.11.3 for a legal over-claim (metric: count of such amendments).<br>• At release: no sentence says a redaction record erases data; no sentence in §G.11.3 states, as a rule of this Standard, what a named law requires; every Companion A §A.11 entry leaves to the deployer whether the law applies, what it requires and who carries any duty under it; law names remain as citations; no field is added or removed. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `closed_at` | 2026-09-28T05:48:09Z |
| `accountable_owner_signoff` | signed_by: Yohay Etsion, Founding Steward<br>signed_at: 2026-09-28T05:48:09Z |
| `re_decision_trigger` | Outcome evidence: a confirmed issue of a kind the success criteria count.<br>Market evidence: a data-protection authority publishes guidance on provenance or audit records and erasure that the §5.5 wording conflicts with. |
| `record_location` | `governance/decisions/DR-2026-0002-redaction-consent-and-privacy-wording.md` and, once released, at tag `v1.1-rev9` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005 |
| `affirmation_record` | timestamp: 2026-09-28T05:48:09Z<br>actor_identity: Yohay Etsion (GitHub account yohayetsion), the accountable owner<br>method: merge of pull request #5, which added this record to the repository (merge commit 78bc2a9d4d258a54b88445d9fb060cd1b5d8bba6) |
| `mode_classification_attestation` | attestor_full_name: Yohay Etsion<br>attestor_role_title: Founding Steward<br>attestor_employer: Etsion Brands Ltd<br>attestation_timestamp: 2026-09-28T05:48:09Z<br>jurisdiction: IL<br>attestation_language_version: v1.0<br>attestation_text_signed: I, Yohay Etsion, in my role as Founding Steward at Etsion Brands Ltd, confirm that I have reviewed the substantive content of this decision record and that the Mode classification recorded in its metadata, mode-2, accurately reflects the substantive role of AI worker output in framing the options under consideration: the record was drafted with AI and affirmed by me. I make this confirmation within the scope of my role on behalf of Etsion Brands Ltd. This confirmation is made under the Charter dps-text-authoring; it makes no conformance claim and does not constitute legal advice or legal certification.<br>attestor_capacity: director |
| `seal_algorithm` | SHA-256 |
| `seal_hash` | 90ddd5e6e07c4ab15c4ff0b12729142eefc4afe76bdcb90045a70210ab258a0b |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T04:22:58Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
