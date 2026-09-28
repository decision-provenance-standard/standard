### 6.2.3.2 Access-policy binding for redaction events

The redaction-event record schema (`record_type: redaction_event` and the eight associated field rows in §6.2.3 above) operationalizes the §5.5 redaction-as-new-affirmed-record framing at the access-policy layer. A conformant deployer's access-policy layer SHALL enforce the following bindings on redaction events:

1. **Affirmation-time binding.** A redaction-event record SHALL NOT be affirmed without a populated `operational_store_deletion_attestation` field (all four sub-fields: `attesting_actor`, `attestation_timestamp`, `deletion_method`, `verification_method`). The access-policy layer rejects the affirmation transition where any sub-field is unpopulated. The substantive correctness of the attestation (whether the deletion actually occurred in the operational store) is for the deployer to determine; the structural completeness of the attestation is the access-policy layer's responsibility.

2. **Read-time binding on the target record.** Where a target record (the record named in `target_record_hash` and `target_decision_id`) carries an affirmed redaction event against it, a reader of the archival record SHALL receive the `redacted_fields` list and a notification that the deployer has recorded the named fields as removed from operational use (a notification in rev. 8's wording also meets this). The original record's `seal_hash` remains valid; the read-time binding makes the discrepancy between the archival record and the operational data store visible to the reader without altering the sealed archival content.

3. **Conformance signal.** A deployer whose redaction events are affirmed without the `operational_store_deletion_attestation` field has departed from §6.2.3 conformance and SHALL NOT self-declare Conformance Level 2 or above per §7. The §7 Level 2 signal `every_redaction_event_carries_operational_store_deletion_attestation` reads the field population at sample-level audit events per the emission cadence in §4.8.2.

The access-policy binding for redaction events is parallel in structure to the §6.2.3.1 access-policy binding for the altitude field: in both cases, the Standard does not specify the implementation mechanism; it specifies the bindings any access-policy layer MUST perform. A deployer integrating redaction events with the deployer's broader privacy-program tooling SHOULD ensure that the privacy-intake system, the legal-basis-review surface, and the operational-store deletion pipeline all resolve back to the redaction-event record's `redaction_authority.request_record_pointer`, `redaction_authority.legal_basis_review_pointer`, and `operational_store_deletion_attestation.verification_method` fields respectively.

**Stable record IDs and seal-hash continuity through migrations.** A decision record's `decision_id` is a stable identifier that persists across the deployer's tooling migrations, ownership changes within the deployer's organization, and surface migrations of the schedule of records. A migration that re-issues IDs has broken the audit trail; a migration that preserves IDs and recomputes-and-re-stores `seal_hash` against the migrated record contents while retaining the original `seal_hash` in `revision_history` preserves the audit trail. Where a deployer migrates the schedule of records to a new system, the deployer's migration record (itself a decision record under a Charter governing migration decisions) carries a pointer to the migration's stable-ID-and-seal-continuity verification: that every pre-migration `decision_id` resolves under the post-migration system, that every pre-migration `seal_hash` is recoverable from the migration record's audit trail, and that every superseded record is retained in full per §5.1(3). The Standard does not specify the migration mechanism; the Standard specifies the audit-trail integrity properties any migration mechanism MUST preserve. A migration that fails to preserve these properties has departed from the Standard's audit-trail integrity at §5.1(3) and §6.4 and is recorded as such in the deployer's migration decision record.

### 6.2.1 Required at decision-record state `dispatched`

These fields are required at the moment a decision opens under a Charter; absence prevents the dispatch state machine from authorizing the decision.

| Field | Type | Notes |
|---|---|---|
| `decision_id` | string (slug; format DR-YYYY-NNN) | Stable identifier; survives ownership and rename changes. |
| `charter_id` | reference (Charter slug) | The Charter under which this decision dispatches. Foreign-key into the Charter state model (Section 3 §3.2). |
| `accountable_owner` | reference (single named human) | The named human accountable for the decision at time of dispatch. One and only one. The single-accountable-owner rule is a requirement of this Standard. |
| `decision_class` | string | Inherited from the Charter; required on the record because the record outlives the Charter version it dispatched under. |
| `dispatch_mode` | enum: `mode-1`, `mode-2`, `mode-1-with-embedded-mode-2-summary` | The dispatch mode authorized by the Charter and active for this decision. Required at dispatch; cannot be silently mutated thereafter (mutation is a re-dispatch event with its own decision record). |
| `dispatched_at` | timestamp | When the decision opened. |

### 6.2.2 Required at decision-record state `drafted`

These fields are required by the time a decision-record reaches the `drafted` lifecycle state. The dispatch state machine emits a `drafted` event when substantive content has been written; required fields below must be populated before the event closes.

| Field | Type | Notes |
|---|---|---|
| `decision_statement` | string (2–3 sentence form) | What was decided, in plain language. Active voice. |
| `context_at_decision` | structured (3–5 bullets) | What was true when the decision was decided. Captures the inputs the decision was authored against. |
| `options_considered` | structured (≥ 2 entries) | At least two options, with reason each was considered and reason the winning option was chosen. Activity that did not consider alternatives produces process records, not decision records; a decision record with one option fails this required field. |
| `required_inputs_used` | structured | Who provided what; version or date of each input. Threads the record back to the Charter's required-inputs list. |
| `assumptions_depended_on` | structured (2–4 entries) | The 2–4 assumptions whose invalidation would force a reopen. Threads to the Charter's re-decision triggers. |
| `success_criteria` | structured | T+2 / T+6 / T+12 indicators with named metric definitions, not just metric names. |
| `disclosure_metadata_pointer` | reference (nullable) | Required when `dispatch_mode` is `mode-2` or `mode-1-with-embedded-mode-2-summary`, except for outputs outside the §4.6 requirement under §4.6.1. Points to the disclosure block (Section 4 §4.6.2). The disclosure block is an attached structure, not an inlined field, because the disclosure decision is itself a decision and carries its own provenance. |

### 6.2.3 Required at decision-record state `closed`

These fields are required at the moment the record archives to the schedule of records. After `closed`, the record is immutable except through a re-decision event that opens a new record with a back-pointer.

| Field | Type | Notes |
|---|---|---|
| `closed_at` | timestamp | When the record archived. |
| `accountable_owner_signoff` | structured | Sign-off attestation from the accountable owner; in Mode 1, the human author; in Mode 2, the human reviewer of record. Carries a sign-off date and the reviewer's role at time of decision. |
| `re_decision_trigger` | structured | The exact condition that forces a formal reopen. At minimum one outcome-evidence trigger and one market-evidence trigger, matching the Charter's `re_decision_triggers` field. Triggers are conditions, not feelings. |
| `record_location` | string (URL or path) | Canonical location where the record persists. Must be durable, searchable, and linkable from the Charter that governs this decision class. The findability hygiene rule below grades this field. |
| `related_decisions` | structured (nullable) | Parent decision; sibling decisions; decisions this one supersedes. Empty when the record is the first under its Charter. |
| `prior_state_archive` | structured (nullable) | Required when the record results from a Mode 2 → Mode 1 demotion (per Section 4 §4.5). The structured shape carries: `demotion_path` (enum: `review-driven` / `audit-driven` / `escalation-driven`), `prior_record_pointer` (reference to the prior Mode 2 decision record), `trigger_reference` (review note, audit finding, or escalation record), `demotion_reason` (string), and `demoted_at` (timestamp). The `demotion_path` enum is surfaced as a discrete machine-readable tag inside the structured field so the conformance-level reporter does not have to infer the path from `trigger_reference` contents. The Standard's mode-migration semantics (Section 4 §4.5) control here; Section 6 surfaces them in the field schema. |

### 6.2.4 Field discipline

Field names are binding; type names are illustrative. A decision-record formatter that implements the Standard may serialize as JSON, YAML, or a typed object so long as field names match Section 6 verbatim. A field that is required at a lifecycle state but absent at that state is a Charter conformance failure at Level 1 (per Section 7). Fields that are nullable at a state are not "optional" in the marketing sense — they are not required at that state and may be required at a later state, in which case absence at the later state is a Level-1 conformance failure.

Verb discipline matters at the field-naming level. Field names use process verbs (`populated`, `committed`, `resolvable`, `archived`); they do not use regulatory verbs (`satisfies`, `ensures`, `certifies`). A field named `mode_declaration` records which mode the Charter declared; it does not certify that the decision met any regulatory requirement under that mode. The same constraint applies to derived signals downstream in Section 7; signals are facts about field population, not regulatory claims.

---

## 6.3 The Schedule of Records

The schedule of records is the enumerated set of decision records a Charter commits to maintain. The schedule is the contract a Charter makes with its consumers — accountable owners, reviewers, counsel, auditors, and a schedule-of-records exporter that implements the Standard — about what records will exist and where they will be findable.

The schedule is committed at the Charter `fields-completed` lifecycle state (per Section 3 §3.3). A Charter that has not enumerated its schedule cannot reach `fields-completed` and cannot grade against any conformance level under Section 7. The schedule is enumerated by **record-type**, not by individual record; the Charter commits to producing records of declared types as decisions arise, on the cadence the Charter declares.

### 6.3.1 Required record-types

A conformant Charter's schedule includes, at minimum, the following record-types. Additional record-types may be enumerated as the Charter's decision class warrants.

| Record-type | Trigger | Cadence |
|---|---|---|
| **Decision record** | Each decision that opens under the Charter. | On decision-close. |
| **Re-decision record** | Each time a Charter re-decision trigger fires (outcome-evidence or market-evidence per the Charter's `re_decision_triggers` field). | On trigger fire; the re-decision record carries a back-pointer to the prior decision record. |
| **Escalation record** | Each time the Charter's escalation rule is invoked. | On invocation; the escalation record carries the escalation owner's call and the named outcome. |
| **Charter-amendment record** | Each amendment to the Charter (mode change, decision-class boundary change, accountable-owner change, schedule-of-records change). | On amendment; amendments are decisions and produce decision records of their own. As Section 3 §3.3 specifies, the Charter-amendment decision dispatches under the Charter's declared `mode_declaration`; the amendment record carries the Charter's mode at the time of amendment. |
| **Disclosure-review record** | Each scheduled re-review of a disclosure block (when applicable per §7.2.1). | On the cadence the Charter declares for disclosure review (shown by the block's `last_reviewed_at`, or by the disclosure-review record itself; §7.4.1). |

### 6.3.2 Findability — the 30-second hygiene rule

A decision record that cannot be found in 30 seconds by someone who was not in the room is not a decision record; it is a meeting note. This is the findability hygiene rule of this Standard, the discoverability requirement for the schedule of records.

The rule is operationalized through the `record_location` field on each record (§6.2.3) and the Charter's `record_location` field (Section 3 §3.2). Both fields must resolve to a durable, searchable, linkable surface. The Charter's `record_location` resolves to the index that enumerates the schedule of records; each individual record's `record_location` resolves to the canonical instance of that record. A schedule whose Charter index resolves but whose individual records do not is a Charter that has committed to records it cannot produce on demand; that is a Level-1 conformance failure even if the schedule-enumeration field is populated.

Findability is audited on the Charter's declared cadence, per the Standard's findability hygiene rule and the Section 7 conformance-level signals. The audit verifies that a sampled set of records reaches a reader not in the room within 30 seconds; it does not assess the substantive content of the records. Findability and substance are distinct grades; findability is a Section 6 question, substance is for the accountable owner and the deployer to determine.

### 6.3.3 What the schedule does not commit

The schedule of records commits to the existence, location, and findability of records of declared types. It does not commit to the substantive correctness of any record, the regulatory adequacy of any record, or the legal interpretation of any record. A Charter whose schedule is fully populated and whose records are findable in 30 seconds may nonetheless contain decisions a regulator's substantive review would not accept. The schedule produces audit-ready provenance; counsel and auditors convert that provenance into evidence, certification, or attestation. The schedule itself does none of those things.

---

## 6.4 Discoverability and Retention

Discoverability and retention are the operational surfaces that make the schedule of records meaningful over time. A schedule that is findable today but inaccessible in eighteen months produces no audit-ready provenance for the time horizon counsel and auditors care about. A schedule that is retained but not discoverable produces no audit-ready provenance for any time horizon.

### 6.4.1 Discoverability requirements

A conformant Charter's schedule satisfies the following discoverability requirements **of the Standard**:

1. **Resolvable Charter index.** The Charter's `record_location` resolves to a surface (URL, path, document, query interface) that enumerates the schedule of records. The index is queryable by record-type and by date range at minimum. A schedule-of-records exporter that implements the Standard binds to this surface.
2. **Resolvable record location.** Each individual record's `record_location` resolves to a canonical instance of the record, accessible to the parties named in the Charter's distribution rule. "Resolvable" here means a reader with the appropriate access can retrieve the record; it does not impose a public-disclosure requirement.
3. **Stable identifiers.** The `decision_id` and `charter_id` fields are stable across ownership changes, surface migrations, and renamings. A record whose identifier mutates between dispatch and audit is a record that has lost its provenance chain.
4. **Versioning of the Charter the record dispatched under.** Each record references the Charter version at time of dispatch. A Charter amended after a decision was made does not retroactively re-Charter the prior decision; the prior record reads against the Charter version current at its `dispatched_at` timestamp.

### 6.4.2 Retention requirements

The Standard does not prescribe a single retention period. Retention periods can differ by jurisdiction and by decision class, so one Charter may declare a different period from another. Section 6 names the structural requirement; which period applies is for the deployer to determine.

A conformant Charter's schedule satisfies the following retention requirements **of the Standard**:

1. **Declared retention period.** The Charter declares a retention period for each record-type in its schedule. The period is named with a specific duration (e.g., "7 years from `closed_at`") or named as a regulatory reference (e.g., "per [the named retention requirement the deployer has identified for its decision class]"). A schedule that declares a retention period of "indefinite" or "as needed" is not a declared period and fails this requirement.
2. **Retention enforcement.** Records persist for the declared period in a state that satisfies **the Standard's** discoverability requirements above. A record retained but inaccessible (archived to cold storage with no resolution path within the retention window) does not satisfy retention.
3. **Disposition record.** When a record reaches the end of its retention period and is dispositioned (deleted, archived to inaccessible storage, transferred to a successor system), the disposition is itself a recorded event in the schedule. A record that is retained for seven years and then quietly disappears is a record whose retention disposition was not itself authored as a decision; that is a schedule-of-records discipline failure.
4. **Period choice.** Which retention period applies to a deployer's decision class is for the deployer to determine; this Standard records the structural requirement that a period is declared and enforced. Section 8 (Regulatory Cross-References) names regulatory frameworks that may inform retention period choice; it does not select the period for any deployer.

The retention requirement leaves period selection to the deployer, because which period applies can depend on law, and this Standard answers no legal question. The Standard structures the input the retention decision needs; the decision is the deployer's.

---

## 6.5 Relationship to Section 4 and Section 7

Section 6 is downstream of Section 3 (Charter mechanism) and Section 4 (Authority and Authorship), and upstream of Section 7 (Conformance Levels). The relationships are structural and load-bearing.

### 6.5.1 Section 4 — the mode-declaration field on records

Section 4 establishes that every Charter declares its dispatch mode and that every decision record carries a `dispatch_mode` field matching the Charter's authorization at time of dispatch. Section 6 incorporates the requirement at the record level: the `dispatch_mode` field is required at the `dispatched` lifecycle state per §6.2.1 above, and the `disclosure_metadata_pointer` field is required at `drafted` when the dispatch mode is `mode-2` or `mode-1-with-embedded-mode-2-summary` per §6.2.2.

The mode-declaration field is the structural primitive that Section 4 uses to gate authorship. Section 6 records it; Section 4 declares what the record means. A decision record without a mode-declaration field cannot be graded by Section 7 because the Section 7 signals (`every_record_carries_mode_declaration`, `every_mode_2_record_has_disclosure_block`, `every_mode_1_edge_case_record_has_disclosure_block`) all read the field this section requires. Section 6 is the substrate; Section 4 is the authority rule the substrate enables.

### 6.5.2 Section 7 — which fields drive conformance-level grading

Section 7 grades a Charter against three conformance levels using signals defined in Section 7 (the conformance-signal vocabulary). The signals read the fields Section 6 requires:

- **Level 1 — Charter-conformant.** Reads §6.3 (schedule enumerated and committed), §6.2.1 fields (`charter_id`, `accountable_owner`, `decision_class`), and the Charter's own `record_location` (Section 3 §3.2). A Charter whose schedule is enumerated, whose `record_location` resolves, whose `accountable_owner` is one named human, and whose required-at-state fields are populated to `fields-completed` grades at Level 1.
- **Level 2 — Mode-disambiguated.** Reads §6.2.1 (`dispatch_mode` on every record), §6.2.2 (`disclosure_metadata_pointer` on every Mode 2 and Mode 1 edge-case record), and the disclosure block's required fields (Section 4 §4.6.2). A Charter that grades at Level 1 and whose schedule of records carries no Mode 1 records that should have dispatched as Mode 2 (the silent-drift mitigation surface) grades at Level 2.
- **Level 3 — Continuously auditable.** Reads §6.3.1 (re-decision and escalation record-types firing on schedule), §6.4 (discoverability and retention currency), and whether disclosure blocks were reviewed within the cadence (§7.4.1). A Charter that grades at Level 2 and whose schedule operates over time per the Charter's declared cadence grades at Level 3.

Conformance-level grading is a structured fact about field population over time. It is not a certification, an attestation, or a regulatory determination. A Charter that grades at Level 3 has produced audit-ready provenance at the structural standard the Standard names; it has not produced evidence, satisfied an obligation, or substituted for a regulator's review.

---

## 6.6 Explicit Non-Claim

The artifact set defined in this section produces **audit-ready decision provenance**. The locked one-line definition, repeated here verbatim:

> *Audit-ready decision provenance is a structured record of how a decision was made — inputs, reviewers, dispatch mode, sign-offs — that counsel and auditors can use as input when preparing evidence, certifications, or attestations; the provenance itself is not evidence, certification, or attestation.*

Counsel and auditors convert that provenance into evidence, certifications, or attestations; the schema and schedule do not. An auditor who treats a populated decision record as a court-admissible record, a certification, or a discharge of any regulatory obligation is reading the artifact set for something it does not claim to be. For the global non-claim set, see §1.4.2.

---

