# DR-2026-0008: Appendix G is informative, and named counsel is a recommendation

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0008 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T13:35:48Z |
| `record_type` | decision |
| `record_state` | drafted |
| `created_at` | 2026-09-28T13:35:48Z |
| `decision_statement` | Appendix G stays informative apart from its version-stability rules: where §G.11.3 states a requirement that a core section also states, the core section binds, and a §G.11.3 requirement that no core section states is a recommendation and reads as SHOULD. The named employment counsel of record moves into §3.1 as a recommendation, §6.4.2 no longer requires counsel review of the retention period, and the sentence that deployers SHALL engage U.S. employment counsel becomes a statement that the Standard makes no claim to be a defense to any employment claim. Under either reading of v1.1's Appendix G, informative or normative, no record or Charter valid under v1.1 (reading edition rev. 9) becomes invalid, because each change removes a requirement or states where the binding rule already sits. |
| `context_at_decision` | • v1.1's Appendix G calls §G.11.3 informative, yet §G.11.3 words 28 requirements with SHALL, so a reader could take it either way.<br>• The core already binds what the HR-altitude rules protect: the works-council requirement (§3.1), an active consent record and the access bindings (§6.2.3.1), and the redaction attestation (§6.2.3.2).<br>• Of §G.11.3's 28 SHALL-worded requirements, 10 go (the counsel field's 9, including its write-reject, which also covered Charters missing the works-council sub-field, and "SHALL engage U.S. employment counsel"), 3 bind through the core, and 15 read as SHOULD (the team-size floor rules and the consent-withdrawal handling rules); the qualities of consent (separately obtained, revocable, scoped) also read as SHOULD, since the core requires an active consent record.<br>• Where §G.11.3 set the works-council pre-consultation before a Charter is authored, §3.1's timing (before the Charter advances past `fields-completed`) binds.<br>• §6.4.2 item 4 required counsel review of the retention period; the Steward's rule is that the Standard states no legal duty and requires no counsel, and its non-claims stay word for word. |
| `options_considered` | • Keep §G.11.3 as it is. Considered because it changes nothing. Rejected: its SHALL wording contradicts the Appendix's informative status and leaves readers unsure which rules bind.<br>• Declare §G.11.3 normative. Considered because it would settle the question the other way. Rejected: it could invalidate Charters and records that relied on "informative", which only a major release may do.<br>• Keep Appendix G informative, read §G.11.3 requirements that have no core twin as SHOULD, move the counsel field into §3.1 as a recommendation, and drop the counsel requirements. Chosen: it only removes or loosens requirements, under either reading.<br>• Delete the counsel field. Considered because the Standard requires no counsel. Rejected: removing a field name could break records that carry it; a recommendation keeps the name. |
| `required_inputs_used` | • Standard v1.1 (reading edition rev. 9) and reference files 5.1.1 (the Steward, 2026-09-28; tag `v1.1-rev9`)<br>• The text of v1.2 (reading edition rev. 10) and reference files 5.1.2, as in the pull request that carries this record (the Steward, 2026-09-28; to be tagged `v1.2-rev10`)<br>• GOVERNANCE.md (the Steward, 2026-09-26): the release classes and the compatibility promise<br>• The Charter `dps-text-authoring`, first version (no Charter-amendment record exists) (the Steward, 2026-09-28)<br>• Records DR-2026-0001 to DR-2026-0007 (the Steward, 2026-09-28) |
| `assumptions_depended_on` | • No adopter needs a §G.11.3 requirement to be binding for its own records or Charter to stay valid.<br>• The core rules carry what a reader of the HR-altitude rules relies on.<br>• Readers take a SHOULD as a recommendation, not as a condition of validity. |
| `success_criteria` | • T+2 (2 months after the v1.2 release): 0 confirmed reports that a record or Charter valid under v1.1 is invalid under v1.2 because of these changes (metric: count of confirmed compatibility issues).<br>• T+6 (6 months after the v1.2 release): 0 issues asking which §G.11.3 rules bind that stay open more than 30 days (metric: count of such issues).<br>• T+12 (12 months after the v1.2 release): no release in the year after v1.2 has had to restore a removed §G.11.3 or counsel requirement (metric: count of such changes).<br>• At release: §3.1 has the recommended counsel paragraph; Appendix G's opening note says a §G.11.3 requirement without a core twin reads as SHOULD; a search of the released text and figures finds no "SHALL carry the `named_employment_counsel_of_record`", no "SHALL engage", no "Standard-conformant records" and no "Counsel review of period choice"; §11.3's summary no longer says §G.11.3's gates remain binding; the field name is unchanged. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a record or Charter valid under v1.1 that is invalid under v1.2 because of these changes; the Steward then restores its validity in a patch and records it.<br>Market evidence: an adopter or reader reports relying on a §G.11.3 requirement as binding, or a later text release moves an HR-altitude rule into the core. |
| `record_location` | `governance/decisions/DR-2026-0008-appendix-g-is-informative-and-counsel-is-a-recommendation.md` and, once released, at tag `v1.2-rev10` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T13:35:48Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
