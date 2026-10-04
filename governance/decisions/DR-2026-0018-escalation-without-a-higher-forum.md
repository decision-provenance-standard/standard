# DR-2026-0018: Escalation when a Charter has no higher forum

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0018 |
| `charter_id` | dps-text-authoring-2 |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-10-04T11:30:22Z |
| `record_type` | decision |
| `record_state` | drafted |
| `created_at` | 2026-10-04T11:30:22Z |
| `decision_statement` | Where a Charter has no higher forum, for example because its accountable owner decides alone, its escalation rule may now pair the exact trigger with what happens when it fires: the outcome is made public or is reviewed by someone other than the person who decided (§3.2, §7.2.1). A rule that elevates the decision to a higher forum stays valid, so this adds a way to meet the field and the Level 1 criterion and removes none. No record or Charter valid under v1.2 becomes invalid. |
| `context_at_decision` | • §3.2 and §7.2.1 (v1.2) define the escalation rule as an exact trigger that elevates a decision out of the Charter's standing forum, and do not say what a Charter with no higher forum can do.<br>• The declaration kit's help for this criterion therefore told users to grade such a Charter "not sure".<br>• The Steward's own Charter is such a Charter: its rule names an exact trigger, and the Steward then publishes an escalation record stating the call and the reason.<br>• An escalation record carries the escalation owner's call and the named outcome (§6.3.1), so making it public, or having someone else review it, puts the outcome before people other than the decider. |
| `options_considered` | • Add a second way to meet the rule: an exact trigger whose outcome is made public or reviewed by someone other than the decider. Chosen: it gives Charters with no higher forum a rule that can be checked, and every rule valid before stays valid.<br>• Require every Charter to name a higher forum. Considered because it keeps one definition. Rejected: Charters with no higher forum would then fail, which only a major release may cause.<br>• Leave the text silent and keep the kit's "not sure". Considered because it changes nothing. Rejected: a criterion that cannot be graded for a whole class of Charters leaves their Level 1 undecided.<br>• Accept any exact trigger, with no outcome named. Considered because it is the simplest. Rejected: a trigger whose outcome stays with the decider alone escalates nothing. |
| `required_inputs_used` | • Standard v1.2 (reading edition rev. 10): §3.2, §6.3.1 and §7.2.1 (the Steward, 2026-09-28; tag `v1.2-rev10`)<br>• The text of v1.3 (reading edition rev. 11) and reference files 5.2.0, as in the pull request that carries this record (the Steward, 2026-10-04; to be tagged `v1.3-rev11` and `ref-5.2.0`)<br>• The declaration kit's criterion L1-07, as released with v1.2 (the Steward, 2026-09-28; tag `v1.2-rev10`)<br>• The Charter `dps-text-authoring`, first version (the Steward, 2026-09-28) |
| `assumptions_depended_on` | • Making an outcome public, or having it reviewed by someone other than the decider, is a real check where no higher forum exists.<br>• A Charter that has a higher forum keeps elevating decisions to it; the added route is for Charters without one. |
| `success_criteria` | • T+2 (2 months after the v1.3 release): 0 confirmed reports that a Charter whose escalation rule was valid under v1.2 is invalid under v1.3 (metric: count of confirmed compatibility issues).<br>• T+6 (6 months after the v1.3 release): the declaration kit never tells users to grade the escalation criterion "not sure" for lack of a higher forum (metric: count of kit criteria whose help still says so).<br>• T+12 (12 months after the v1.3 release): each time the escalation rule of `dps-text-authoring-2` fires, an escalation record is listed in the records index (metric: count of firings without a listed record).<br>• At release: §3.2 and §7.2.1 state the added route and say that a rule that elevates the decision stays valid; the kit's criterion L1-07 says the same; and the escalation rule of `dps-text-authoring-2` cites the route. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `review_log` | • reviewer: a fresh AI-drafted pre-execution review of the v1.3 release plan made for the Steward; reviewed_at: 2026-10-03T10:15:59Z; outcome: proceed with changes; it asked that the route be added as a way to meet the rule, with rules that elevate the decision kept valid, as done here |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring-2<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-10-04 |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a Charter that used the added route although it had a higher forum, or an escalation whose outcome was neither made public nor reviewed; the Steward then clarifies the route in a later release and records it.<br>Market evidence: a second party joins the Steward in maintaining the Standard, which gives the Steward's own Charter a higher forum, or a standards body publishes a rule for escalation where there is no higher forum. |
| `record_location` | `governance/decisions/DR-2026-0018-escalation-without-a-higher-forum.md` and, once released, at tag `v1.3-rev11` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007<br>• DR-2026-0008<br>• DR-2026-0009<br>• DR-2026-0010<br>• DR-2026-0011<br>• DR-2026-0012<br>• DR-2026-0013<br>• DR-2026-0014<br>• DR-2026-0015<br>• DR-2026-0016<br>• DR-2026-0017 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-10-04T11:30:22Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
