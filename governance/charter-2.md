# Charter: Authoring the Decision Provenance Standard (second Charter)

> Affiliated: the Standard's own use of itself by its Steward. The Charter declares a target of Level 1 because the text requires every complete Charter to declare one. This is not a conformance declaration. Etsion Brands is not listed as an adopter.

The fields follow the order of Standard §3.2. Where a value is a list, or has named parts, each item sits on its own line.

| Field | Value |
|---|---|
| `charter_id` | dps-text-authoring-2 |
| `charter_name` | Authoring the Decision Provenance Standard (second Charter) |
| `decision_class` | Changes to the Standard's text, reference files and governance files |
| `accountable_owner` | full_name: Yohay Etsion<br>role: Founding Steward<br>employer: Etsion Brands Ltd |
| `inside_decisions` | • Changes to `spec/`, `standard/`, `governance/` and the root documentation<br>• Whether a change is a patch, minor or major release<br>• Which contributions are merged |
| `outside_decisions` | • Any organization's Level or conformance (self-declared, never graded)<br>• Use of the name by others (§11.1 governs)<br>• The website's design<br>• Tooling code in `tools/`, `tests/` and `.github/` (handled as code, not as Standard text) |
| `mode_declaration` | mode-2 |
| `cadence` | frequency: on-trigger, plus each release<br>trigger: each pull request that touches the text, the reference files or the governance files |
| `record_location` | `governance/README.md` (the records index, shared with the first Charter, listing each record by id, type, state and date; the records themselves are in `governance/decisions/`) |
| `re_decision_triggers` | Outcome evidence: a confirmed issue shows that a released text contradicts itself, over-claims, or breaks a record that was valid under the previous release.<br>Market evidence: a second party asks to co-maintain the Standard, or a regulator or standards body publishes guidance that names the Standard. |
| `escalation_rule` | A disputed change to a section that GOVERNANCE.md lists as Steward-only, still open 30 days after it was raised: the Steward publishes an escalation record stating the call and the reason. While there is one Steward there is no higher forum, so the rule takes the route Standard §3.2 gives a Charter with no higher forum: the escalation record makes the outcome public. |
| `schedule_of_records` | • Decision records<br>• Re-decision records<br>• Escalation records<br>• Charter-amendment records<br>• Disclosure-review records (required, because the Charter is Mode 2; one at each release, reviewing the disclosure block in `governance/README.md`)<br>Retention, for every record type: at least 25 years from the record's `closed_at`. Records stay in the public repository history and are corrected only by a superseding record; none is removed at the end of that period unless a Charter-amendment record decides it, and any removal is itself recorded (§6.4.2). |
| `conformance_level_declared` | 1 (a target, as §3.2 requires; see the header line) |
| `disclosure_metadata_pointer` | The disclosure block in `governance/README.md`, which every record repeats |
| `created_at` | 2026-10-04T11:30:19Z |
| `closed_at` | null (not closed) |
| `charter_state` | fields-completed (the §3.3 lifecycle state) |

This Charter succeeds `dps-text-authoring` ([charter.md](charter.md)). That Charter closed when this one was created: its decision class is subsumed here (Standard §3.3), by Charter-amendment record DR-2026-0015. Records DR-2026-0001 to DR-2026-0015 stay under the first Charter; records from DR-2026-0016 on are made under this one.

Every record made under this Charter carries a `review_log` (Standard §6.2.3) that lists the reviews made before the merge that affirms it.

Records made under this Charter are listed in [README.md](README.md). This is the Charter's first version; any change to it is made by a Charter-amendment record.
