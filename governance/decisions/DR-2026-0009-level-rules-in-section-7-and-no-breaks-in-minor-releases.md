# DR-2026-0009: Level rules in Section 7, and no breaks in minor releases

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0009 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T13:35:49Z |
| `record_type` | decision |
| `record_state` | drafted |
| `created_at` | 2026-09-28T13:35:49Z |
| `decision_statement` | Section 7.1 now points to sections that bar or grade a Level outside the §7 tables, naming §6.2.4 (a record missing a field required at its lifecycle state fails Level 1) and §6.5.2 (Level 3 reads the discoverability and retention rules of §6.4), both of which already bind as core text. Appendix G and §7.5 no longer let a minor release break a Conformance Level by listing the break: a change that would break a Level ships only in a major release, whose release notes list what it breaks (§G.7.7.1). This changes no grade the v1.1 text allowed and no rule for records or Charters, and no record or Charter valid under v1.1 (reading edition rev. 9) becomes invalid; it narrows only what the Steward's own releases may do. |
| `context_at_decision` | • Several sections outside the §7 tables bar or grade a Level (for example §3.1, §6.2.3.1, §6.2.3.2, §6.2.4, §6.3.2 and §6.5.2), and §7 did not point to all of them; the rules in §6.2.4 and §6.4 already bound under v1.1, but the Steward's v1.1 declaration kit did not ask about them, so a Level declared with that kit may need to be checked again.<br>• v1.1's Appendix G let a minor release break a Level where Section 11 listed the break, but Section 11 lists no breaks, and a change that makes a previously valid record invalid is a major release.<br>• v1.1 listed no breaks, so no Charter relied on one. |
| `options_considered` | • Leave both as they are. Considered because neither changes a grade today. Rejected: a reader cannot find two Level rules from §7, and the listing mechanism points at a list that does not exist.<br>• Point §7.1 to the Level rules outside the tables, and send any Level break to a major release. Chosen: it restates binding rules and narrows only the Steward.<br>• Write a list of breaks into Section 11. Considered because the old text pointed there. Rejected: a minor release that breaks a Level would contradict the compatibility promise. |
| `required_inputs_used` | • Standard v1.1 (reading edition rev. 9) and reference files 5.1.1 (the Steward, 2026-09-28; tag `v1.1-rev9`)<br>• The text of v1.2 (reading edition rev. 10) and reference files 5.1.2, as in the pull request that carries this record (the Steward, 2026-09-28; to be tagged `v1.2-rev10`)<br>• GOVERNANCE.md (the Steward, 2026-09-26): the release classes and the compatibility promise<br>• The Charter `dps-text-authoring`, first version (no Charter-amendment record exists) (the Steward, 2026-09-28)<br>• Records DR-2026-0001 to DR-2026-0007 (the Steward, 2026-09-28) |
| `assumptions_depended_on` | • Readers look for Level rules in Section 7 first.<br>• No adopter relied on a minor release being able to break its Level. |
| `success_criteria` | • T+2 (2 months after the v1.2 release): 0 confirmed reports that a grade the v1.1 text allowed changed because of §7.1's new paragraph (metric: count of confirmed issues).<br>• T+6 (6 months after the v1.2 release): 0 issues asking where a Level rule outside §7 lives that the §7.1 paragraph does not answer (metric: count of such issues).<br>• T+12 (12 months after the v1.2 release): every release in the year after v1.2 that would break a Level is a major release that lists the break in its notes (metric: count of minor releases that break a Level).<br>• At release: a search of the released text finds no "Section 11 enumerat", "enumerates the breaks", "Section 11's break" or "Section 11 lists"; §7.1 names §6.2.4 and §6.5.2; §G.7.6 and §G.7.7.1 agree. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `review_log` | • reviewer: a fresh AI-drafted legal-claims review made for the Steward; reviewed_at: 2026-09-28T13:55:59Z; outcome: go with changes, with its findings folded into the pull request before the merge<br>• reviewer: a fresh AI-drafted compatibility review made for the Steward; reviewed_at: 2026-09-28T14:11:01Z; outcome: go with changes, with no record or Charter valid under v1.1 made invalid, and its findings folded into the pull request before the merge |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a grade changed by §7.1's paragraph, or a minor release that broke a Level; the Steward then corrects it in a patch or reclassifies the release.<br>Market evidence: an adopter or standards body asks for a published list of breaks, or for the Level rules to be moved into the §7 tables. |
| `record_location` | `governance/decisions/DR-2026-0009-level-rules-in-section-7-and-no-breaks-in-minor-releases.md` and, once released, at tag `v1.2-rev10` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007<br>• DR-2026-0008 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T13:35:49Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
