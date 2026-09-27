# Section 2 — Definitions

> **Disclaimer + Jurisdiction Assumed.** The "Use of the Standard" notice (artifact-scoped) and the "Jurisdiction Assumed" declaration live at the top of this document. Every term defined in this section inherits that disclaimer and that jurisdictional scope. Where a deployer's content concerns a different jurisdiction, every definition below is to be treated as a hypothesis to verify with local counsel.

---

## 2.1 Purpose of this Section

Section 2 establishes the **binding vocabulary** for the Decision Provenance Standard™. The terms defined here carry a single, precise meaning across Sections 3 through 12. Every Charter authored against this Standard, every decision record produced under it, and every conformance grade reported under it refers to the meanings declared here. Where a downstream section needs a refinement of a term (for example, Section 6 enumerating the field-level shape of a decision record, Section 5 enumerating the lifecycle states a record transits, or Section 7 enumerating the level criteria built on conformance signals), the refinement is in addition to the definition declared here, never in place of it.

**Drift introduced in this section propagates everywhere.** That is why the language-discipline rule — that the Standard's artifacts are *audit-ready decision provenance*, never *legal evidence*, *compliance certification*, or *regulatory substitute* — is load-bearing for every definition that follows.

This section does not contain examples; worked examples live in Section 9. This section does not map the terms to named regulatory frameworks; the cross-references to EU AI Act articles, NIST AI RMF, ISO/IEC 42001, *Caremark*, and the other frameworks the Standard speaks to live in Section 8. This section does not specify the lifecycle a decision record transits from creation to sealed status; that is Section 5. Section 2 is the vocabulary spine; Section 5 is the lifecycle layer; Section 7 is the conformance-grading layer; Section 8 is the regulatory-cross-reference layer; Section 9 is the worked-example layer.

---

## 2.2 Defined Terms

The terms below are listed in architectural order rather than alphabetically: Charter (the type) → decision (the instance) → decision record (the artifact) → schedule of records (the contract) → modes (dispatch shape) → audit-ready decision provenance (what the records collectively constitute) → conformance signal and conformance level (how a Charter grades) → mode-declaration field, disclosure metadata block (with disclosure metadata pointer as its reference form), declaring authority, accountable owner, re-decision trigger, dispatch mode, prior-state archive (the structural primitives the first nine compose into), affirmation event, seal, and supersedes (the Section 5 lifecycle primitives). Each term below carries a cross-reference to its operational use in Sections 3–12.

### 2.2.1 Charter

A **Charter** is the artifact that binds an organization to a decision-making mechanism for a recurring decision class. The Charter names the decision class, the accountable owner, the inputs the decision requires, the cadence on which the decision is made, the success criteria the decision is held against, the escalation rule the decision invokes when its scope is breached, and the re-decision trigger that reopens the decision when outcome or market evidence demands. A Charter is not a contract. A Charter is not a regulatory filing. A Charter is the operational commitment an organization makes to a way of deciding, recorded in a form that survives leadership transitions.

The Charter is the Standard's own structural unit of state on which the rest of the Standard's machinery operates: a decision dispatches under a Charter; a decision record is bound to the Charter under which the decision was made; a record progresses through the lifecycle of Section 5 under a Charter; a schedule of records is committed by a Charter; a conformance level grades a Charter.

*Operational use.* Section 3 specifies the Charter mechanism, including the lifecycle states a Charter transits and the fields a Charter carries at each state. Section 4 specifies which actor reads which Charter state at decision-open and decision-close, and the mode-declaration field the Charter must carry before any decision may dispatch under it. Section 5 specifies the lifecycle states a record produced under a Charter transits from `draft` through `reviewed` to `affirmed`. Section 6 specifies the schedule of records the Charter commits to maintain and the field-level decision-record schema. Section 7 specifies the conformance levels at which a Charter satisfies the Standard's structural requirements. Section 10 specifies installation guidance for the Charter mechanism in a deployer's organization.

### 2.2.2 Decision

A **decision** is a single instance of decision-making governed by a Charter. The Charter is the type; the decision is the instance. A decision opens under a Charter, transits a dispatch sequence under one of the modes the Charter declares, and closes with a decision record that progresses through the lifecycle states defined in Section 5. Decisions made outside a Charter are outside the scope of this Standard.

A decision in the sense of this Standard is a recurring, consequential, cross-functional decision — for example, launch readiness, pricing exceptions, platform intake, portfolio stop-continue. It is not a routine operational task, an individual tactical call, or a meeting outcome that does not warrant a record. The Charter governs which decision classes warrant Charter discipline; this Standard does not enumerate them.

*Operational use.* Section 4 specifies the dispatch states a decision transits and the actors who read and write at each state. Section 5 specifies the lifecycle states (`draft` → `reviewed` → `affirmed`) the decision's record transits from creation to sealed. Section 6 specifies the decision-record schema the record carries. Section 7 specifies the conformance signals that a properly dispatched and properly sealed decision record emits. Section 9 contains worked examples of decisions dispatched under representative Charters.

### 2.2.3 Decision Record

A **decision record** is a single instantiated, persistent, findable artifact that captures one decision. The decision record carries:

- a stable decision identifier;
- a single named accountable owner at the time of decision;
- a date decided;
- a pointer to the Charter under which the decision was made;
- the decision statement in plain language;
- the context at the time of decision;
- the options considered and the rationale for the option chosen;
- the inputs used (with version or date);
- the assumptions the decision depends on;
- the success criteria the decision is held against (with leading, mid, and lagging indicators);
- the re-decision trigger that reopens the decision;
- related decisions (parent, sibling, superseded);
- a record location that is durable, searchable, and linkable from the Charter that governs the decision class;
- the dispatch mode under which the decision was made; and
- the lifecycle state the record currently occupies (`draft`, `reviewed`, or `affirmed` per Section 5), with affirmation event and seal hash recorded at the moment the record reaches `affirmed`.

The decision record is the Standard's unit of audit-ready decision provenance: a decision record is what counsel and auditors read when they wish to understand how a decision was made, by whom, against which inputs, with what review, and with what affirmation. The decision record is not evidence in the legal sense; it is the structured record from which counsel and auditors prepare evidence, certifications, or attestations as their professional judgment requires.

The findability hygiene rule under this Standard: a decision record that cannot be found in 30 seconds by someone who was not in the room is not a decision record; it is a meeting note. The Standard's record location and findability requirements (Sections 6 and 7) operationalize the rule.

*Operational use.* Section 5 specifies the lifecycle states the record transits and the affirmation event and seal that gate `affirmed`. Section 6 specifies the decision-record schema and the schedule of records the Charter commits. Section 4 specifies the dispatch-mode field that every decision record carries. Section 7 specifies the conformance signals a complete decision record emits. Section 8 specifies the regulatory cross-references that a decision record may inform (without satisfying). Section 9 contains worked examples of decision records produced under representative Charters.

### 2.2.4 Schedule of Records

A **schedule of records** is the enumerated set of decision-record types a Charter commits to produce and maintain. The schedule names each record type, the trigger that opens a record of that type, the location at which records of that type live, and the retention discipline records of that type are held to. The schedule is the contract the Charter makes with its consumers — the deployer's executive line, the deployer's counsel and auditors, and any third party permitted to review under the deployer's policies — about what records will exist and where they will be findable.

The schedule of records is governed by the Standard's findability hygiene rule (the 30-second findability rule) and by the Charter's `record_location` field. The Standard formalizes the schedule as the level-1 commitment the Charter must make at the `fields-completed` lifecycle state (per Section 3), as the level-2 commitment that every record under the schedule carries its mode-declaration (per Section 4) and reaches `affirmed` per the Section 5 lifecycle, and as the level-3 commitment that the schedule is queryable and exportable for review (per Section 7).

*Operational use.* Section 6 specifies the schedule's field-level shape, including the per-record-type fields the schedule names. Section 7 specifies the conformance-level criteria that read against the schedule. Section 10 specifies installation guidance for committing and maintaining a schedule.

### 2.2.5 Mode 1 — Human-Led, AI-Enforced

**Mode 1 — Human-Led, AI-Enforced** is the canonical name for the dispatch mode in which a human authors the decision and an AI worker checks the human's work against the Charter. The human is the author of record. The AI worker is the discipline mechanism: it reads the Charter state, monitors decision-record completeness against the Charter's required fields, and emits conformance signals on the decision record. The AI worker does not author the substantive decision content under Mode 1.

*Operational use.* Section 4 specifies the Mode 1 dispatch state machine, including the read and write boundaries between the human author and the AI worker, and the conformance signals Mode 1 emits at each dispatch state. Section 5 specifies how a Mode 1 record progresses through `draft` → `reviewed` → `affirmed`. Section 6 specifies the Mode 1 fields the decision record carries. Section 7 specifies the Mode 1 conformance signals at level 2 and level 3.

### 2.2.6 Mode 2 — AI-Led, Human-Reviewed

**Mode 2 — AI-Led, Human-Reviewed** is the canonical name for the dispatch mode in which an AI worker authors the decision (analysis, options framing, recommendation) and a human reviews the AI-authored draft before action. The AI worker is the author of record. The human is the reviewer of record. The human reviewer signs off, requests revision, or invokes Mode 2 → Mode 1 demotion when the AI-authored draft requires substantive human re-authoring rather than revision.

A Mode 2 decision may incorporate disclosure obligations on the deployer's part under named regulatory frameworks. The structural input the deployer's declaring authority needs in order to discharge such obligations is captured in the disclosure-metadata block (Section 2.2.11 below). The cross-reference to specific regulatory frameworks (including EU AI Act Article 50) lives in Section 8. **Nothing in this definition or in the disclosure-metadata block satisfies, ensures, or certifies any regulatory obligation.** The obligation belongs to the human declaring authority; the Standard structures the inputs.

*Where the human reviewer of a Mode 2 draft is also the Charter's `accountable_owner`, the reviewer's affirmation gates the record into `affirmed` directly. Where the human reviewer is a named delegate of the `accountable_owner` per the Charter's authorized-delegation declaration, the delegate's affirmation gates the record into `affirmed` and the affirmation event records the delegate's identity per §5.1(3); the `accountable_owner` remains the single named human accountable for the Charter under §2.2.13.*

*Operational use.* Section 4 specifies the Mode 2 dispatch state machine, including the read and write boundaries between the AI worker, the human reviewer, and the disclosure-metadata block. Section 5 specifies how a Mode 2 record progresses through `draft` → `reviewed` → `affirmed`, with the human reviewer's affirmation as the load-bearing event. Section 6 specifies the Mode 2 fields the decision record carries. Section 7 specifies the Mode 2 conformance signals at level 2 and level 3. Section 8 specifies the regulatory cross-references that Mode 2 decisions may inform.

### 2.2.7 Audit-Ready Decision Provenance

**Audit-ready decision provenance** is a structured record of how a decision was made — inputs, reviewers, dispatch mode, sign-offs — that counsel and auditors can use as input when preparing evidence, certifications, or attestations. **The provenance itself is not evidence, certification, or attestation.** Counsel and auditors convert audit-ready decision provenance into evidence, certifications, or attestations as their professional judgment requires; the artifacts produced under this Standard do not.

This term is the load-bearing object across the Standard. It is the term the Standard uses where a less-disciplined drafter might write "evidence," "compliance record," or "audit defense." Each of those drift terms imports a regulatory or legal-force claim the Standard cannot make. "Audit-ready decision provenance" is true, defensible, and useful. It describes what the Standard's records *are* (structured process records) without describing what they *do to a regulatory state* (which only counsel, auditors, and regulators determine).

The one-line locked definition of this term is: *"Audit-ready decision provenance is a structured record of how a decision was made — inputs, reviewers, dispatch mode, sign-offs — that counsel and auditors can use as input when preparing evidence, certifications, or attestations; the provenance itself is not evidence, certification, or attestation."* This sentence (or its verbatim first clause) is the Standard's first-use definition of the term across every section that introduces it. The "is not evidence, certification, or attestation" tail is the Standard's core non-claim and is non-negotiable on every surface where the term is introduced.

*Operational use.* Section 1 (Preamble) introduces the term and the firewall tail. Section 5 specifies the lifecycle states the record transits (and the affirmation event and seal that lock the record into a state useful for audit work). Section 6 specifies the field-level shape of the records that collectively constitute audit-ready decision provenance for a Charter. Section 7 specifies the conformance levels at which a Charter's records meet the structural requirements that the term names. Section 8 specifies the regulatory frameworks the term informs (without satisfying). Section 10 specifies installation guidance for producing audit-ready decision provenance from day one of a Charter install.

### 2.2.8 Conformance Signal

A **conformance signal** is a named, machine-readable field on a Charter or decision record that records whether a structural requirement of the Standard is met. A signal is a field-level fact: a state has been reached, a field is populated, a sample has been audited, a cadence has fired on schedule. A signal is not a narrative claim. A signal does not record that a Charter "is compliant," "satisfies regulation," or "ensures governance"; those verbs belong to counsel, auditors, and regulators, not to a metadata field.

Conformance signals are the inputs the conformance-level grading in Section 7 reads. Signals are emitted by the dispatch state machine (per Section 4) when a decision transits a state, by the lifecycle state transitions (per Section 5) when a record reaches `reviewed` and `affirmed`, by the Charter lifecycle (per Section 3) when a Charter reaches a state, and by the schedule-of-records audit (per Section 6) when records are sampled. The Standard binds a small set of named signals to each conformance level, listed in Section 7.

*Operational use.* Section 4 specifies the dispatch states at which signals emit. Section 5 specifies the lifecycle transitions at which signals emit. Section 6 specifies the schedule-of-records audit that reads signals on sampled records. Section 7 specifies the conformance-level criteria that read signals into a level grade.

### 2.2.9 Conformance Level

A **conformance level** is the named tier (1, 2, or 3) at which a Charter or decision record satisfies the structural requirements of the Standard. Section 7 defines the criteria for each level. The level is a structured fact: it is the function the conformance-level reporter computes from the conformance signals read against a Charter and its schedule of records.

A conformance level is **not certification.** No third-party certifying body grades conformance levels under this Standard, because the Standard is published as an open standard and not as a certified product. **Conformance Levels are self-declared by the adopting organization.** The Standard's Steward (see §11.2) does NOT certify, grade, or audit conformance. A deployer self-declares a Charter's level using the conformance-level reporter; counsel and auditors read the level grade as one input among others when preparing their own work. A regulator's determination of compliance with any named regulatory framework is a separate determination, made by the regulator against the deployer's actual implementation, with the conformance level grade serving (where the regulator chooses to read it) as one structural input among others.

*Operational use.* Section 7 specifies the level criteria, including the named signals each level requires. Section 10 specifies installation guidance for reaching level 1, then level 2, then level 3. Section 8 specifies how a level grade may inform (without satisfying) regulatory cross-references. Section 11 specifies the trademark and governance posture that distinguishes self-declaration from certification.

### 2.2.10 Mode-Declaration Field

The **mode-declaration field** is the required field on a Charter's state, and on each decision record produced under a Charter, that declares the dispatch mode in use. The field's value is one of three enumerated states: `mode-1`, `mode-2`, or `mode-1-with-embedded-mode-2-summary` (the last names the structural edge case in which a human-authored decision incorporates an AI-generated summary as a sub-output).

The mode-declaration field is required at any Charter state past the initial `open` lifecycle state (per Section 3), and at every decision-record state past `dispatched` (per Section 4). Without the field declared at the Charter level, no decision may dispatch under the Charter; without the field declared at the decision-record level, no record may close. The field is enumerated, not free-text, to prevent drift into invented modes, hybrid descriptors, or marketing labels.

*Operational use.* Section 3 specifies the Charter lifecycle gating on this field. Section 4 specifies the per-decision-record requirement and the dispatch state machine that reads the field. Section 7 specifies the level-2 conformance signal `every_record_carries_mode_declaration` that reads against the schedule of records.

### 2.2.11 Disclosure Metadata Block

The **disclosure metadata block** is the structured input attached to a Charter or decision record under which a Mode 2 decision (or a Mode 1 decision incorporating an AI-generated summary as a sub-output) has been made. The block carries: the named human declaring authority responsible for discharging any disclosure obligation that attaches to the decision; the AI system identity (system name, version, model provider, deployment context, model-card pointer); the jurisdictional applicability the disclosure is scoped against; the Mode 1 edge-case flag where applicable; a pointer to the disclosure text the declaring authority has approved; timestamps for attachment and last review; and the disclosure provenance (who approved, on what review, against which Charter version).

The disclosure metadata block **structures the inputs** the declaring authority needs in order to discharge a disclosure obligation. The block does not generate disclosure text. The block does not satisfy a disclosure obligation. The block does not certify that a disclosure was adequate. The obligation belongs to the human declaring authority; the block records the structural inputs the declaring authority's work consumes.

The cross-reference to specific regulatory frameworks (including EU AI Act Article 50 disclosure obligations) lives in Section 8. The block's field-level shape is specified in this Standard at §4.6.2; the Standard's normative wrapper in Section 4 specifies the prose around the block.

*Operational use.* Section 4 specifies the conditions under which the block attaches to a Charter or decision record, the field-level schema, and the Mode 1 edge-case handling. Section 6 specifies the per-record presence of a disclosure block on Mode 2 records. Section 7 specifies the level-2 conformance signal `every_mode_2_record_has_disclosure_block`. Section 8 specifies the regulatory cross-reference (EU AI Act Article 50 and adjacent frameworks).

The **disclosure metadata pointer** is the reference-form of the Disclosure Metadata Block as it appears on the Charter and on individual decision records. Where the block is the structured input (this section's primary definition above), the pointer is the field name (`disclosure_metadata_pointer`) under which the Charter or decision record references the block. Section 3 specifies the Charter-level pointer (required at `fields-completed` when `mode_declaration` is `mode-2` or `mode-1-with-embedded-mode-2-summary`). Section 6 specifies the per-decision-record pointer (required at decision-record state `drafted` when `dispatch_mode` is `mode-2` or `mode-1-with-embedded-mode-2-summary`).

### 2.2.12 Declaring Authority

The **declaring authority** is the single named human responsible for discharging any disclosure obligation that attaches to a Mode 2 decision (or to a Mode 1 decision incorporating an AI-generated summary as a sub-output). The declaring authority is not the AI system; not the Charter; not the organization at large. The obligation belongs to a person.

The declaring authority and the Charter's accountable owner (Section 2.2.13 below) are both single named humans. The two roles may or may not be the same person, depending on the deployer's role design and the disclosure framework's requirements; both are individually named in the relevant artifact. **No Charter and no disclosure metadata block authorizes a non-human or unnamed declaring authority.**

*Operational use.* Section 4 specifies the declaring-authority field on the disclosure metadata block. Section 6 specifies the per-record reference to the declaring authority on Mode 2 records. Section 8 specifies how the declaring authority's role maps to regulatory frameworks that name a disclosure obligation.

### 2.2.13 Accountable Owner

The **accountable owner** is the single named human accountable for a Charter. Each Charter names one and only one accountable owner at any one time. The accountable owner is the human role at which Charter authorship and Charter ownership reside in the deployer's organization, regardless of reporting line. **The accountable owner is also the human whose explicit affirmation event (Section 5) gates a record into the `affirmed` state.**

The single-named-accountability discipline is a requirement of this Standard: one and only one named human is accountable for a Charter at any one time. The Standard formalizes single-name accountability as a level-1 conformance signal (`accountable_owner_named`).

*Operational use.* Section 3 specifies the accountable-owner field on the Charter. Section 5 specifies the accountable owner's load-bearing role in the affirmation event that gates `affirmed`. Section 6 specifies the per-record reference to the accountable owner at the time of decision. Section 7 specifies the level-1 signal that reads against the Charter.

### 2.2.14 Re-Decision Trigger

A **re-decision trigger** is a named outcome condition or market condition declared up-front on a Charter that, when fired, reopens the decision class the Charter governs, regardless of decision status. The Charter's re-decision triggers are at minimum: one outcome-evidence trigger (for example, a metric miss against a guardrail) and one market-evidence trigger (for example, a competitor launches a substitute in the target segment, a new entrant redefines the category, or a pricing move compresses the premium).

The re-decision trigger is a requirement of this Standard: a Charter declares the conditions that reopen its decision class before decisions begin to dispatch. The Standard formalizes the re-decision trigger as a level-1 structural requirement (the Charter must declare at least one outcome-evidence and one market-evidence trigger to reach the `fields-required` lifecycle state) and as a level-3 operating signal (re-decision triggers fire and produce records on schedule).

*Operational use.* Section 3 specifies the re-decision-trigger field on the Charter. Section 6 specifies the per-record reference to the re-decision trigger that closes the decision. Section 7 specifies the level-1 signal `re_decision_triggers_minimum_met` and the level-3 signal `re_decision_triggers_firing_on_schedule`.

### 2.2.15 Dispatch Mode

The **dispatch mode** is the field on a decision record that records the mode under which the specific decision dispatched. Its enumeration is identical to the Charter-level mode-declaration field (`mode-1`, `mode-2`, or `mode-1-with-embedded-mode-2-summary` per §2.2.10); the Charter declares the mode it authorizes (per §2.2.10) and the decision record records the mode it dispatched under. The two fields carry the same enumeration at different altitudes: `mode_declaration` is the field on the Charter, `dispatch_mode` is the field on the decision record. The Charter can authorize a mode without a specific decision having dispatched yet; a decision record carries its dispatch fact independent of any subsequent Charter amendment. The two fields are paired-but-distinct primitives, defined separately so that downstream sections may bind to either altitude without ambiguity.

The dispatch-mode field is specified in this Standard at Section 4 §4.4 (the paired mode-declaration / dispatch-mode fields) and §4.5 (Mode 2 → Mode 1 demotion semantics the field's enumeration must support).

*Operational use.* Section 4 specifies the dispatch state machine that writes this field at decision-record state `dispatched`. Section 6 specifies the field as required at decision-record state `dispatched` per the schema. Section 7 specifies the level-2 conformance signal `every_record_carries_mode_declaration` that reads this field across the schedule of records.

### 2.2.16 Prior-State Archive

The **prior-state archive** is a structured field on a decision record that captures the prior Mode 2 draft or audit finding when the decision results from a Mode 2 → Mode 1 demotion. The archive is required when the demotion produced the record; it is nullable otherwise. The field's structured shape carries a `demotion_path` enum tag whose values are `review-driven` (Mode 2 reviewer determines re-authoring needed), `audit-driven` (post-close audit/regulator/counsel finding on disclosure incompleteness), or `escalation-driven` (Charter escalation rule fires). The structured shape additionally carries a `prior_record_pointer` (reference to the prior Mode 2 decision record), a `trigger_reference` (review note, audit finding, or escalation record), a `demotion_reason` (string), and a `demoted_at` timestamp.

The prior-state archive is defined by this Standard's Mode 2 → Mode 1 demotion semantics (Section 4 §4.5). The field is the structural primitive that prevents silent re-moding: a Mode 2 → Mode 1 demotion produces a new decision record carrying the demotion's prior-state archive, not a quiet field mutation on the existing record. The original Mode 2 record persists, immutable (sealed per Section 5), in the schedule of records; the new Mode 1 record references the original via `prior_record_pointer` and records the demotion path discretely so the conformance reporter does not have to infer the path from `trigger_reference` contents.

*Operational use.* Section 4 specifies the demotion semantics (the substrate event the field records). Section 5 specifies how the supersedes mechanism interacts with affirmed/sealed records (a demotion produces a new record that supersedes the prior affirmed record via `supersedes`, with the prior record retained in full). Section 6 specifies the field as required at decision-record state `closed` when the record is a demotion record, with the `demotion_path` enum tag surfaced inside the structured field. Section 7 specifies the level-3 conformance signal `demotion_records_carry_prior_state_archive`.

### 2.2.17 Affirmation Event

An **affirmation event** is the discrete, time-stamped, actor-identified event that records the named decision owner's explicit affirmation of a decision record per Section 5. The event is captured in the `affirmation_record` field with three load-bearing properties: (i) a timestamp, (ii) the identity of the affirming actor (who must be the record's `accountable_owner` or, where the Charter authorizes delegation, a named human delegate of the accountable owner), and (iii) the affirmation method (signature, approval token, or equivalent human-actor signal — never a passive signal such as time elapsed or absence of objection).

The affirmation event is the load-bearing event of the lifecycle: a record cannot reach `affirmed` without one, and the act of affirmation is itself a recorded event with audit-relevant properties. Section 5.2 enumerates the requirement.

*Operational use.* Section 5 specifies the affirmation event's role in gating the `affirmed` state. Section 6 specifies the field-level schema. Section 7 specifies the conformance signal `every_affirmed_record_carries_affirmation_event`.

### 2.2.18 Seal

A **seal** is the cryptographic hash of an affirmed decision record, computed at the moment the record reaches `affirmed` and stored in the `seal_hash` field. The seal is the structural primitive that converts the affirmation event into a tamper-evident sealing of the record's content. The seal does not prevent corrections; corrections are made through the **supersedes** mechanism (§2.2.19 below) that produces a new record referencing the prior sealed record, with the original retained in full.

The seal does NOT claim cryptographic immutability against all attack surfaces — it is a hash, not a blockchain commitment, and the deployer's storage and access-control posture governs the record's integrity in operation. The seal claims only that an unaltered seal hash on a stored record means the stored record matches the record content at the moment of affirmation; tampering with both the record and the hash simultaneously is outside the seal's structural protection and is the deployer's responsibility to address through its broader integrity controls.

**Baseline algorithm.** The seal SHALL be computed using SHA-256, a NIST-approved hash function in the SHA-2 family with FIPS-validated implementations broadly available across the deployer ecosystems this Standard targets. SHA-256 is selected as the v1.0 baseline because the cryptographic strength it provides is appropriate to the integrity altitude at which the seal operates: tamper-evidence on a stored, access-controlled decision record under a deployer's broader integrity controls. The seal is a record-integrity primitive, not an adversarial-security boundary, and SHA-256 sits comfortably above the strength threshold that record-integrity at this altitude requires while carrying a long deprecation runway, mature tooling across implementation languages, and validation pathways that satisfy the regulatory cross-references this Standard speaks to in Companion A (Regulatory Cross-References).

**Deprecation conditions.** SHA-256 MAY be deprecated and replaced as the baseline seal algorithm under any of the following conditions: (i) NIST formally weakens, withdraws, or recommends migration away from SHA-256; (ii) published cryptanalytic results reduce the effective collision-resistance of SHA-256 below the strength threshold this Standard's integrity altitude requires, as determined by the Standard's Steward in consultation with qualified cryptographic counsel; or (iii) a successor algorithm — including, but not limited to, members of the SHA-3 family or BLAKE3 — reaches ecosystem maturity comparable to SHA-2's at the time of this v1.0 nomination, defined as broad availability of validated implementations across the deployer-runtime surfaces in use by Standard installations. A deprecation decision is itself a Standard revision and follows the §G.7.5 minor-release-or-major-release versioning rule per the change's field-shape impact. A deprecation announcement carries a migration window of no less than twelve months from announcement to deprecation effective date, matching the §G.7.5 backwards-compatibility commitment.

**Algorithm rotation and corpus migration.** Because the Standard anticipates algorithm rotation across the lifetime of long-lived record corpora, the seal field carries an algorithm-identifier sub-structure (per the §6.2.3 `seal_algorithm` schema row) that names the hash algorithm under which each individual record's seal was computed. A deployer rotating from SHA-256 to a successor algorithm SHALL hold the prior corpus under the prior algorithm-identifier and seal new records under the new algorithm-identifier from the rotation date forward; the prior corpus is not re-sealed under the new algorithm in place. Where a deployer chooses to recompute seals against the migrated corpus — for example, to unify the corpus under a single algorithm at a future migration boundary — the original `seal_hash` and original `seal_algorithm` SHALL be retained in the record's `revision_history` per §6.2.3, preserving the audit trail of the prior algorithm's seal alongside the recomputed seal. Mixed-algorithm corpora are an expected operational state during a migration window and are conformant against this Standard.

*Operational use.* Section 5 specifies seal computation at the moment of affirmation. Section 6 specifies the `seal_hash` and `seal_algorithm` fields. Section 7 specifies the conformance signal `every_affirmed_record_carries_seal_hash`.

### 2.2.19 Supersedes

The **supersedes** field on a decision record is the reference to a prior affirmed record that the current record corrects, replaces, or otherwise updates. The supersedes mechanism is the only path by which a deployer makes a substantive change to a decision after the prior record reached `affirmed`. The new record is itself a decision record with its own lifecycle (it transits `draft` → `reviewed` → `affirmed` per Section 5); the prior record is retained in full in the schedule of records, immutable from its own affirmation moment forward.

The supersedes mechanism is the structural primitive that preserves the audit trail across corrections: a reader walking the schedule of records can always reconstruct the full decision history by following supersedes pointers from current state back to the original record. There is no path under the Standard by which an affirmed record is silently modified, deleted, or replaced without leaving a supersedes trace.

*Operational use.* Section 5 specifies the supersedes mechanism's role in the lifecycle. Section 6 specifies the `supersedes` field. Section 7 specifies the conformance signal `superseded_records_retained_in_full`.

---

## 2.3 Vocabulary Discipline

The defined terms in this section follow the verb discipline that governs every artifact across the Decision Provenance Standard surface. **Definitions describe what an artifact *is* and what an actor *does*; definitions do not describe what an artifact *does to a regulatory state*.** A Charter *binds an organization to a decision-making mechanism*; a Charter does not *ensure compliance*. A decision record *captures how a decision was made*; a decision record does not *prove regulatory adequacy*. A conformance level *grades structural conformance to this Standard*; a conformance level does not *certify regulatory conformance*. The disclosure metadata block *structures the inputs a declaring authority needs*; the block does not *discharge a disclosure obligation*. An affirmation event *records the named owner's explicit affirmation*; the event does not *certify the substantive correctness of the decision*. A seal *captures the record's content at the moment of affirmation*; the seal does not *prove the record's legal admissibility*.

The seven drift patterns apply to the use of the terms above across Sections 3–12:

1. *"produces evidence"* drift → Use *"produces audit-ready decision provenance"* (per §2.2.7).
2. *"satisfies oversight obligations"* drift → Use *"supports the human reviewer's oversight obligation"* (per §2.2.6 and §2.2.12).
3. *"ensures compliance"* drift → Use *"facilitates the compliance review qualified personnel conduct"* (the compliance review is not a verb the Standard performs).
4. *"certifies the decision is sound"* drift → Use *"records the decision-making process per the Charter"* (per §2.2.3).
5. *"replaces the legal review"* drift → Use *"structures the inputs the legal review consumes"* (the Standard never replaces a review).
6. *"proves the decision met regulatory requirements"* drift → Use *"documents that the decision followed the Charter"* (we make process claims; regulators make regulatory claims).
7. *"the Charter is a legally binding governance document"* drift → Use *"the Charter binds the organization to a decision-making mechanism"* (per §2.2.1; "legally binding" pulls in contract and fiduciary law the Standard does not opine on).

### 2.3.1 Canonical names only in this Section

Mode 1 and Mode 2 are the canonical names declared in §2.2.5 and §2.2.6. The accessible-alias pair does not appear in this section and does not appear anywhere in the Standard. The aliases are reserved for surfaces outside the Standard's normative envelope. Any Standard surface that introduces Mode 1 or Mode 2 uses the canonical names alone; any deployer-facing artifact (a Charter, a decision record, a conformance-level report) likewise uses the canonical names alone.

### 2.3.2 Vocabulary escalations and the consumer relationship with Section 6

This section is the consumer-facing vocabulary spine for downstream sections. Section 6 (the "Required Artifact Set") consumes this vocabulary verbatim: where Section 6 names a decision-record field, the field name and its meaning come from this section; where Section 6 commits a Charter to a schedule of records, the schedule's structure comes from this section. **Where Section 6 needs a term not yet defined in this section, the resolution is to add the term through the Standard's governance process, not by silent invention.**

One candidate term is flagged here: the *disclosure-text generator output* (a draft disclosure-text producer the declaring authority reviews and approves) is not a defined term in this section. If Section 4 or Section 6 needs to bind a term to the generator's output, separate from the disclosure metadata block, the term would be added through governance. The disclosure metadata block records the *pointer* to the approved text, not the text itself. No other vocabulary gaps are anticipated.

---

## 2.4 Non-Claim — Section 8 Maps Terms onto Regulatory Frameworks; Nothing in Section 2 Attempts a Regulatory-Substitute Claim

Nothing in this section maps any defined term onto a named regulatory framework; Section 8 (Regulatory Cross-References, maintained in Companion A) is where the terms defined here are mapped onto named frameworks. No defined term in this section substitutes for counsel review, regulatory determination, or auditor attestation — see §1.4.2 for the global non-claim set.

---

