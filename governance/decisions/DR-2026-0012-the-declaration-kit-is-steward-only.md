# DR-2026-0012: The declaration kit is Steward-only

> Affiliated: the Standard's own use of itself by its Steward, not independent adoption. This record makes no conformance claim, and Etsion Brands is not listed as an adopter.

| Field | Value |
|---|---|
| `decision_id` | DR-2026-0012 |
| `charter_id` | dps-text-authoring |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `dispatch_mode` | mode-2 |
| `dispatched_at` | 2026-09-28T13:35:52Z |
| `record_type` | decision |
| `record_state` | drafted |
| `created_at` | 2026-09-28T13:35:52Z |
| `decision_statement` | The declaration kit (`kit/`) is added to GOVERNANCE.md's Steward-only lane and to CODEOWNERS, because its criteria restate the Conformance Level rules and a change to it could drift from the text. This record is made under the Charter because it changes GOVERNANCE.md, which is root documentation; the Charter itself is unchanged. |
| `context_at_decision` | • The kit's criteria restate the Level criteria of §7 and are built into a prompt and a coding-agent skill that organizations and product makers use to write their self-declarations.<br>• GOVERNANCE.md's Steward-only lane covers the text's rules, the reference files, the automated checks and the governance records, but not `kit/`.<br>• An automated check keeps the kit's generated files in sync with its own sources, not with the text. |
| `options_considered` | • Leave `kit/` open to any reviewer. Considered because it is Apache-2.0 tooling. Rejected: a change to its criteria changes how organizations read their Level.<br>• Add `kit/` to the Steward-only lane and to CODEOWNERS. Chosen: the Steward already owns the rules the kit restates.<br>• Move the kit's criteria into the text. Considered because the text binds. Rejected: the kit's wording is drafting guidance and should not become normative text. |
| `required_inputs_used` | • GOVERNANCE.md and CODEOWNERS (the Steward, 2026-09-26)<br>• The declaration kit, `kit/declaration/criteria.json` (the Steward, 2026-09-28)<br>• The Charter `dps-text-authoring`, first version (no Charter-amendment record exists) (the Steward, 2026-09-28)<br>• Records DR-2026-0001 to DR-2026-0007 (the Steward, 2026-09-28) |
| `assumptions_depended_on` | • The kit's criteria will keep restating the text's Level rules.<br>• The Steward can review changes to the kit as they come. |
| `success_criteria` | • T+2 (2 months after the v1.2 release): every pull request that changed `kit/` since v1.2 has the Steward's review (metric: count of such pull requests without it).<br>• T+6 (6 months after the v1.2 release): 0 confirmed issues that a kit criterion contradicts the text (metric: count of confirmed issues).<br>• T+12 (12 months after the v1.2 release): every release in the year after v1.2 updated the kit on the day it was released (metric: count of releases where it did not).<br>• At release: GOVERNANCE.md's Steward-only lane lists `kit/`; CODEOWNERS lists `/kit/`; the merging rules are otherwise unchanged. |
| `disclosure_metadata_pointer` | The disclosure block below (the same block as in `governance/README.md`) |
| `altitude` | executive |
| `drafting_authority` | deployer_role_pointer: drafting assistant to the Founding Steward, under Charter dps-text-authoring<br>system_name: Anthropic Claude Opus 5.5<br>version: claude-opus-5-5, as used on 2026-09-28 |
| `re_decision_trigger` | Outcome evidence: a confirmed issue shows a kit criterion drifted from the text; the Steward then corrects the kit and reviews how kit changes are approved.<br>Market evidence: an outside contributor asks to maintain the kit, or the kit moves to its own repository. |
| `record_location` | `governance/decisions/DR-2026-0012-the-declaration-kit-is-steward-only.md` and, once released, at tag `v1.2-rev10` |
| `related_decisions` | • DR-2026-0001<br>• DR-2026-0002<br>• DR-2026-0003<br>• DR-2026-0004<br>• DR-2026-0005<br>• DR-2026-0006<br>• DR-2026-0007<br>• DR-2026-0008<br>• DR-2026-0009<br>• DR-2026-0010<br>• DR-2026-0011 |

## Disclosure block

| Field | Value |
|---|---|
| `declaring-authority` | Yohay Etsion, for Etsion Brands Ltd |
| `ai-system-identity` | Anthropic / Claude Opus 5.5 |
| `jurisdictional-applicability-tag` | eu, us-federal, uk, israel |
| `content-type-tag` | decision-summary |
| `generation-timestamp` | 2026-09-28T13:35:52Z |

Carried because this Standard requires it for AI-drafted records; this says nothing about whether any law applies.
