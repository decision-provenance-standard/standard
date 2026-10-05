<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Generated from criteria.json by build.py. Do not edit by hand. -->

# Conformance Level criteria

Standard: Decision Provenance Standard v1.3, reading edition rev. 11 (https://decisionprovenancestandard.org/dps-v1.3-rev11-core.html)

## How to check

Check one Level at a time, starting with Level 1. Check every criterion of that Level, even after one is not met, so the list of gaps is complete. Only if every criterion of the Level is met, go on to the next Level. Stop at the first Level with any criterion not met, report that Level's gaps, and do not check the Levels above it.

## The rule

Levels are graded per Charter. A Charter reaches a Level only when every criterion of that Level, and of every Level below it, is met (§7.2.1, §7.3.1, §7.4.1). A criterion whose "applies only if" condition is false counts as met; record it as "does not apply", with the reason. Record "not met" when the evidence shows the criterion is not met, or when the person is sure a part is missing (for example "we record who and when, but not how"). Record "not sure" when the person does not know. "Not sure" also counts as not met. Evidence counts when someone can say where it is kept: a file, a field or a system, or a document kept elsewhere, named with its reference (for example "kept by HR, reference HR-2026-007"). When checking a repository, mark evidence kept outside it as "outside the repository". A claim with no location counts as "not sure"; the fix is to record that evidence and say where. A Charter field may use another name if it means the same thing (§3.2). Record fields use the Standard's names, which "match Section 6 verbatim" (§6.2.4): a record field under another name does not count; note the mapping in the report and list renaming as the fix. A Charter whose works_council_consultation_record was added after it reached "fields-completed" can reach Level 1 only, until it is re-authored as a new version (§3.1). A declaration lists exactly the Charters it covers, and its Level applies to those Charters only: it is the lowest Level any of them reaches. A Charter may be left out, for example one that reaches no Level; then say which Charter was left out and why.

## No Charter yet

When there is no Charter, or the person does not know what one is, say this in two plain sentences:

> A Charter is the written setup for one area of decisions: who owns them, how they are drafted, which records are kept and where. The Standard's Levels are about Charters, so an organization cannot declare any Level until it has at least one.

Then offer a product declaration instead, in case they make a product that implements the Standard, and point them to the Standard's section on Charters (Section 3): https://decisionprovenancestandard.org/dps-v1.3-rev11-core.html#section-3-the-charter-mechanism. No Level and no declaration.

## Level 1: Charter-Conformant (§7.2)

The Charter is written down in full, and every record under it carries the fields required at its state.

- **L1-01** Is there a written Charter for this area of decisions, with every field the Standard requires filled in, so that it has reached the "fields-completed" state?
  - How to judge: Check the fields themselves. A "fields-completed" label on the Charter is not evidence on its own: "A Charter that omits any required field at the field's required-at-state has not reached that state" (§3.2). A field counts when it is present and meets its definition in §3.2: for example, accountable_owner must name one person, not a role. (Which record types the schedule lists is judged under L1-03, not here.) Every Charter at "fields-completed" has these filled in (§3.2, §3.3): charter_id, charter_name, decision_class, accountable_owner, created_at, inside_decisions, outside_decisions, mode_declaration, cadence, record_location, re_decision_triggers, escalation_rule, schedule_of_records and conformance_level_declared. It also needs disclosure_metadata_pointer when mode_declaration is mode-2 or mode-1-with-embedded-mode-2-summary (§3.2). Two more are needed only in some cases (§3.1): use_case_scope_limit_declaration, when any record would describe a person below executive level; and works_council_consultation_record, when the Charter works in an EU or UK country with a works council (such as Germany, France or the Netherlands) and covers records at function-leader level or below. Recommended, not required (§3.1): for Charters whose records describe people at function-leader level or below, the employment counsel of record (named_employment_counsel_of_record). Missing it does not fail this criterion; list it as a suggestion. The use_case_scope_limit_declaration must be one of the scopes §3.1 lists (audit-readiness; internal-optimization; team-level-measurement, at team-leader level and above; or individual-development-coaching with its three sub-fields affirmer_consent.coaching_consent_record_pointer, excluded_downstream_uses and hr_of_record_charter_scope_confirmation): "free-text or hybrid scopes are not conformant" (§3.1). In the works_council_consultation_record, the consultation completion date must be on or before the Charter's "fields-completed" date (§3.1). A record's level is its altitude field (§6.2.3): executive, function-leader, team-leader or individual-professional; if the records carry no such field, ask which levels they are at. A field may use another name if it means the same thing (§3.2). One missing or wrong field can fail two criteria: for example, a role named as owner fails L1-01 and L1-05, and a missing escalation rule fails L1-01 and L1-07. That is intended: record it under both.
  - In plain words, the Charter has: an ID and a name (charter_id, charter_name); when it was created (created_at); the kind of decisions it governs, and which decisions are inside it and outside it (decision_class, inside_decisions, outside_decisions); one named person who owns it (accountable_owner); how its decisions are drafted (mode_declaration); how often decisions are made (cadence); where its records live (record_location); what reopens a decision, and what escalates one (re_decision_triggers, escalation_rule); which records it keeps (schedule_of_records); the Level it aims for (conformance_level_declared); if an AI system drafts, or drafts parts: a link to its disclosure block (disclosure_metadata_pointer); if records describe people below executive level: what the records may be used for (use_case_scope_limit_declaration); if you work in an EU or UK country with a works council and records cover function-leader level or below: the works-council consultation record (works_council_consultation_record).
  - Evidence: The Charter document or record, and each of the fields listed under "How to judge".
  - Standard: §7.2.1, §3.2, §3.3, §3.1. Signal: charter_state_is_fields_completed.
- **L1-02** Does the Charter declare how its decisions are drafted, using exactly one of these three values: "mode-1" (a person drafts), "mode-2" (an AI system drafts and a named person reviews and signs off), or "mode-1-with-embedded-mode-2-summary" (a person drafts, with an AI-drafted summary inside)?
  - Evidence: The Charter's mode_declaration field.
  - Standard: §7.2.1, §3.4, §4.4. Signal: mode_declaration_populated.
- **L1-03** Does the Charter commit to a list of the records it will keep, at least by type: decision records, re-decision records, escalation records and Charter-amendment records, plus disclosure-review records when the Charter needs them?
  - How to judge: Disclosure-review records must be listed when the Charter's mode_declaration is mode-2 or mode-1-with-embedded-mode-2-summary (§7.2.1). They should be listed when a mode-1 Charter's records embed AI-drafted content that carries a disclosure block (§4.7): that is a recommendation, so leaving them out does not fail this criterion, but put it on the list of fixes. They are not needed for a mode-1 Charter whose records carry no AI-generated content. Nor are they needed for AI-drafted outputs outside the Standard's disclosure requirement (§4.6): outputs made outside the EU that, as the organization has checked, will not reach, and are not reasonably foreseeable to reach, people in the EU, which the Charter declares outside it (§4.6.1; a Charter written before v1.1 of the Standard may rely on this without the declaration). Such outputs carry no disclosure block, so they need no disclosure-review record. A Charter written before v1.1 whose schedule met revision 8's requirement remains valid without adding disclosure-review records (§7.2.1). Ask about this only for a mode-2 or mode-1-with-embedded-mode-2-summary Charter that does not list disclosure-review records.
  - Evidence: The Charter's schedule of records and its mode_declaration, whether any record under it carries a disclosure block, and any statement in the Charter that its AI-drafted outputs are outside the disclosure requirement.
  - Standard: §7.2.1, §3.2, §6.3.1, §4.6.1, §4.7. Signal: schedule_of_records_committed.
- **L1-04** Does the Charter point to one lasting place (an index) where its records live, can that index be searched at least by record type and by date range, and does each record listed there open from its own location?
  - How to judge: A table or list that gives each record's type and date counts as searchable by record type and by date range. Each record must also open from its own record_location: "A schedule whose Charter index resolves but whose individual records do not ... is a Level-1 conformance failure even if the schedule-enumeration field is populated" (§6.3.2).
  - Evidence: The Charter's record_location, the index it points to, and a few records opened from it.
  - Standard: §7.2.1, §3.2, §6.4, §6.3.2. Signal: record_location_resolvable.
- **L1-05** Does the Charter name exactly one person as its accountable owner (a person, not a role, a team or a department)?
  - Evidence: The Charter's accountable_owner field.
  - Standard: §7.2.1, §3.2. Signal: accountable_owner_named.
- **L1-06** Does the Charter set at least two triggers that reopen a decision: at least one based on outcome evidence (how the decision is working out) and at least one based on market evidence (a change outside the organization)?
  - Evidence: The Charter's re_decision_triggers field.
  - Standard: §7.2.1, §3.2. Signal: re_decision_triggers_minimum_met.
- **L1-07** Does the Charter set an escalation rule with a named, exact trigger (not "when it feels stuck") that moves the decision out of its usual forum or, where the Charter has no higher forum, makes the outcome public or has it reviewed by someone other than the person who decided?
  - How to judge: What counts is a named, exact trigger (§3.2). When it fires, the rule either moves the decision out of the Charter's standing forum, or, where the Charter has no higher forum (for example, its accountable owner decides alone), makes the outcome public or has it reviewed by someone other than the person who decided (§3.2, §7.2.1). Either meets the criterion, and a rule that moves the decision to a higher forum always does. Record "not met" if there is no exact trigger, or if a Charter with no higher forum neither makes the outcome public nor has it reviewed by someone else.
  - Evidence: The Charter's escalation_rule field.
  - Standard: §7.2.1, §3.2. Signal: none named in §7.
- **L1-08** Does every record carry every field the Standard requires at the state it is in?
  - How to judge: "A field that is required at a lifecycle state but absent at that state is a Charter conformance failure at Level 1" (§6.2.4, pointed to from §7.1). Section 6 lists each record field with the state at which it becomes required: §6.2.1 when the decision opens (for example decision_id, charter_id, accountable_owner, dispatch_mode and dispatched_at), §6.2.2 when it is drafted, and §6.2.3 when it is closed, with the rows that name their own state (for example altitude from draft onward, review_log from reviewed, and affirmation_record, seal_hash and seal_algorithm at affirmed, §5.1(3)). Some fields are required only in some cases: for example drafting_authority when an AI system drafts, consent_posture below executive level, and the redaction fields on a redaction-event record. A field that becomes required only at a later state is not missing before that state. Record fields use the Standard's names (see the rule on record field names). One missing field can fail this criterion and a Level 2 criterion too, for example a missing seal_hash on an affirmed record (L2-06): that is intended; record it under both. A closed (affirmed) record has passed through reviewed (§5.1), so review_log is required on it. A field missing from an affirmed record cannot be added later, because affirmed records are never edited (§5.1(3)), and superseding the record keeps the original in full, so the gap stays; record it honestly. If the Charter has no records yet, there is nothing to check, and this criterion is met.
  - Evidence: The records themselves, checked field by field against Section 6's list for the state each record is in.
  - Standard: §7.1, §6.2.4, §6.2.1, §6.2.2, §6.2.3. Signal: none named in §7.

## Level 2: Mode-Disambiguated (§7.3)

Every record says whether a person or an AI system drafted it, and carries the disclosure and sign-off the Standard asks for.

- **L2-01** Does every decision record under the Charter carry its dispatch_mode field (who drafted it: a person or an AI system), set when the record was opened and never silently changed?
  - How to judge: Met when every decision record carries dispatch_mode and no record's dispatch_mode was changed on the record itself: the mode "cannot be silently mutated thereafter (mutation is a re-dispatch event with its own decision record)" (§6.2.1). A change of mode appears as a new, re-dispatched record; for a demotion from AI-drafted to person-drafted, the new record carries prior_state_archive pointing to the earlier one (§4.5). A Charter amendment does not change the mode of records already made: they "remain bound to the pre-amendment Mode" (§4.5). A history of past values is not required: a record's current value is its dispatched value (§7.3.1).
  - Evidence: The dispatch_mode field on each decision record.
  - Standard: §7.3.1, §6.2.1, §4.5. Signal: every_record_carries_mode_declaration.
- **L2-02** Does every AI-drafted (mode-2) record that the Standard's disclosure requirement covers carry a complete disclosure block with all five required fields: declaring authority, AI system identity, jurisdictions it applies to, content type, and generation timestamp?
  - Applies only if: The Charter has any records drafted by an AI system (mode-2), other than outputs outside the Standard's disclosure requirement: those the Charter declares outside it, or, for a Charter written before v1.1, outputs that already met the §4.6.1 test (§4.6.1; see L1-03).
  - How to judge: The declaring authority may name the person who prepares the disclosure, the organization they act for, or both: any of the three counts, though the Standard asks new records to name both (§4.6.2). It is never the AI system's vendor. The signal every_mode_2_record_carries_disclosure_pointer reports this same criterion: it checks that each record's disclosure_metadata_pointer is there from the drafted state on, not only at close (§7.3.2, §4.3, §6.2.2). It adds no criterion. A record with an embedded AI-drafted summary (mode-1-with-embedded-mode-2-summary) within the requirement needs the pointer from drafted too; a missing pointer is judged under L1-08 (§6.2.2, §6.2.4).
  - Evidence: The disclosure block on each mode-2 record, and its disclosure_metadata_pointer.
  - Standard: §7.3.1, §4.6, §4.6.1, §4.6.2, §6.2.2. Signal: every_mode_2_record_has_disclosure_block, disclosure_block_required_fields_populated, every_mode_2_record_carries_disclosure_pointer.
- **L2-03** Does every person-drafted record whose AI-drafted content the Standard's disclosure requirement covers carry a disclosure block at the point where that content sits?
  - Applies only if: The Charter has any person-drafted records with AI-drafted content inside them (records flagged mode_1_edge_case_flag), other than embedded content outside the Standard's disclosure requirement: content the Charter places outside it, or, for a Charter written before v1.1, content that already met the §4.6.1 test (§4.6.1, §4.7; see L1-03). Until the Charter has such a record, there is nothing to check and this criterion does not apply (§7.3.2, "When there is nothing yet to check").
  - Evidence: The mode_1_edge_case_flag and the per-record disclosure pointer.
  - Standard: §7.3.1, §7.3.2, §4.7, §4.6.1, §6.2.2. Signal: every_mode_1_edge_case_record_has_disclosure_block.
- **L2-04** Has the sample audit run at the rate the Standard sets (15% rolling; every one of a Charter's first 100 records; 30% for Charters declaring the embedded-summary mode), with a designated peer reviewer confirming the records it flagged, and did the most recent run end with no peer-confirmed findings of records that should have been marked as AI-drafted?
  - Applies only if: The Charter has person-drafted records to sample (mode-1 records, including those with AI-drafted content inside). Until it has, there is nothing to audit and this criterion does not apply (§7.3.1; §7.3.2, "When there is nothing yet to check").
  - Evidence: The record of the most recent sample audit, its date, and the peer reviewer's findings on the records it flagged. The confirmation is a person's work; look for its record.
  - Standard: §7.3.1, §7.3.2, §4.8. Signal: no_silent_mode_drift_in_sample.
- **L2-05** Does every affirmed record carry an affirmation record saying when, by whom (the accountable owner or a named delegate) and how a person affirmed it?
  - Applies only if: The Charter has any affirmed records: records that are closed, or marked affirmed. Drafts and records still awaiting sign-off are not affirmed records. Until the Charter has one, there is nothing to check and this criterion does not apply (§7.3.2, "When there is nothing yet to check").
  - How to judge: Met only when each affirmed record says all three: when, by whom and how. L2-05 and L2-07 both turn on how each affirmation was made, so ask about it once and use the answer for both. The person who affirmed must be the accountable owner or a named delegate (§6.2.3). A closed record counts as affirmed here, because the Standard expects every closed decision record to have been affirmed by a person, with that affirmation recorded (§7.1): a closed record with no affirmation recorded fails this criterion. If the person does not know how the affirmations were made, record "not sure"; if they say it is not recorded, "not met".
  - Evidence: The affirmation_record field on each affirmed record.
  - Standard: §7 lifecycle signals, §7.3.2, §5.1(3), §7.1. Signal: every_affirmed_record_carries_affirmation_event.
- **L2-06** Does every affirmed record carry a seal (the seal_hash field) stored when it was affirmed?
  - Applies only if: The Charter has any affirmed records (closed, or marked affirmed; see L2-05). Until the Charter has one, there is nothing to check and this criterion does not apply (§7.3.2, "When there is nothing yet to check").
  - How to judge: The seal is computed and stored at the moment the record is affirmed (§5.1(3)). A seal added later does not count, so a record affirmed before sealing began cannot meet this criterion. Seal every record at the moment it is affirmed from now on: that stops the gap growing, but it does not close it for records already affirmed without a seal.
  - Evidence: The seal_hash field on each affirmed record.
  - Standard: §7 lifecycle signals, §7.3.2, §5.1(3). Signal: every_affirmed_record_carries_seal_hash.
- **L2-07** In the organization's own recorded sample of affirmed records, was every affirmation an active act by a person, never time passing, silence, or a default approval?
  - Applies only if: The Charter has any affirmed records (closed, or marked affirmed; see L2-05). Until the Charter has one, there is nothing to check and this criterion does not apply (§7.3.2, "When there is nothing yet to check").
  - How to judge: The sample is one the organization took and recorded itself (for example in a review log). Do not pick a sample yourself. This turns on the same fact as L2-05 (how each affirmation was made): use the answer already given. If no sample has been taken and recorded, record "not met"; if the person does not know whether one exists, "not sure".
  - Evidence: The organization's record of its sample, and the affirmation method on each sampled record.
  - Standard: §7 lifecycle signals, §7.3.2, §5.2. Signal: no_passive_promotion_to_affirmed_in_sample.
- **L2-08** Does every affirmed record that is AI-drafted, or carries an AI-drafted summary, record its drafting authority: a pointer to the role under which your organization lets the AI system draft (the system's name and version are optional)?
  - Applies only if: The Charter has any affirmed records (closed, or marked affirmed; see L2-05) that are AI-drafted (mode-2) or carry an AI-drafted summary (mode-1-with-embedded-mode-2-summary). Until the Charter has one, there is nothing to check and this criterion does not apply (§7.3.2, "When there is nothing yet to check").
  - How to judge: The drafting authority is the record's drafting_authority field (§6.2.3). Its deployer_role_pointer points to the role under which your organization authorizes the AI system to draft (for example "pricing team drafting assistant under Charter pricing-decision"); the system's name and version are optional. It is not the person who affirmed the record (affirmed_by or affirmation_record), and not the disclosure block's declaring authority: those name people or the organization, not the AI system. It must use the Standard's field name, drafting_authority (see the rule on record field names).
  - Evidence: The drafting_authority field and its deployer_role_pointer.
  - Standard: §7 lifecycle signals, §7.3.2, §6.2.3. Signal: every_mode_2_record_carries_drafting_authority.
- **L2-09** For records about one person's own work (individual-professional level): was each written only where the Charter's use-case scope allows that level for the use the record serves, does each carry a pointer to that person's active consent record, are no records added or affirmed after consent was withdrawn, and can only the person who affirmed the record and the readers named in the Charter's use-case scope read them? And for records at function-leader or team-leader level: does each sign-off check that the Charter's use-case scope allows that level before the record is sealed?
  - Applies only if: The Charter has any records at function-leader, team-leader or individual-professional level (see L1-01). Until the Charter has one, there is nothing to check and this criterion does not apply (§7.3.2, "When there is nothing yet to check").
  - How to judge: §6.2.3.1 sets these checks for the system that controls access to the records, and applies them to AI systems too: an AI system drafting at these levels must act under a role the Charter's use-case scope allows. An organization whose access control does not perform them "SHALL NOT self-declare Conformance Level 2 or above" (§6.2.3.1). Recommended, not required (the text recommends documenting it before declaring Level 2; missing it does not fail this criterion): for records at team-leader level or below, a minimum group size for team-level records, set by the organization (for example through a data protection impact assessment), written down (in the Charter's works_council_consultation_record, or in your data protection impact assessment where no works council applies) and enforced when records are written. This comes from Appendix G §G.11.3, which no core section repeats, so it reads as a recommendation; if it is missing, list it as a suggestion.
  - Evidence: The consent_posture fields, the access policy, and how sign-offs at function-leader and team-leader level check the Charter's use-case scope.
  - Standard: §7 lifecycle signals, §7.3.2, §6.2.3.1, §6.2.3.1 item 3. Signal: altitude_to_consent_posture_binding_enforced.
- **L2-11** Does every redaction-event record carry a deletion attestation with all four parts: who attested, when, how the data was deleted, and how the deletion was checked?
  - Applies only if: The Charter has any redaction-event records (records of removing information). Until the Charter has one, there is nothing to check and this criterion does not apply (§7.3.2, "When there is nothing yet to check").
  - Evidence: The operational_store_deletion_attestation on each redaction-event record.
  - Standard: §7.3.2, §6.2.3, §6.2.3.2. Signal: every_redaction_event_carries_operational_store_deletion_attestation.

## Level 3: Continuously Auditable (§7.4)

The Charter runs as declared over time, and its records can be searched and exported on demand and are kept findable for as long as the Charter declares.

- **L3-01** Have the Charter's re-decision triggers produced re-decision records on the cadence the Charter declares, with no missed firings?
  - Evidence: Re-decision records and their dates, against the declared cadence.
  - Standard: §7.4.1, §3.2, §6.3.1. Signal: re_decision_triggers_firing_on_schedule.
- **L3-02** Each time the escalation rule fired, was an escalation record produced, stating the outcome and the escalation owner's call?
  - Evidence: Escalation records, matched to the times the rule fired.
  - Standard: §7.4.1, §3.2, §6.3.1. Signal: escalation_rule_records_present_when_invoked.
- **L3-03** Was every disclosure block reviewed within the review cadence the Charter declares: shown by a last_reviewed_at date on the block, or by a disclosure-review record dated within the cadence that names the record?
  - Applies only if: The Charter has any records carrying a disclosure block.
  - How to judge: Either counts (§7.4.1): the block's last_reviewed_at, where the implementation keeps one, or a disclosure-review record (§6.3.1) dated within the cadence that names the block's record. Where the block is stored inside an affirmed record, which is not edited after close (§6.2.3), a disclosure-review record can show its review (§7.4.1). A review that has expired does not meet this criterion.
  - Evidence: The last_reviewed_at date on each disclosure block, or the disclosure-review records that name each record, against the declared cadence.
  - Standard: §7.4.1, §4.6, §4.6.2, §6.3.1. Signal: disclosure_review_cadence_current.
- **L3-04** Can the records be searched and exported on demand for lawyers and auditors, by record type, date range, drafting mode, accountable owner and re-decision trigger, within the response time your organization has stated?
  - Evidence: The export or query tool, and a recent export.
  - Standard: §7.4.1, §6.3, §6.4. Signal: schedule_of_records_queryable.
- **L3-05** Has your level check (the Standard calls it the conformance-level reporter) been run within the reporting cadence the Charter declares?
  - Evidence: The date of the most recent level check, against the declared reporting cadence.
  - Standard: §7.4.2. Signal: conformance_level_reporter_output_recent.
- **L3-06** When a record is replaced by a newer one, is the old record kept in full and unchanged, with the new record pointing to it (supersedes)?
  - Evidence: A superseded record and the record that supersedes it.
  - Standard: §7 lifecycle signals, §5.1(3). Signal: superseded_records_retained_in_full.
- **L3-07** Are the records findable and retained as §6.4 requires: each location resolves, identifiers are stable, each record names the Charter version it was made under, and retention follows the schedule?
  - How to judge: Level 3 reads the discoverability and retention rules of §6.4 (§6.5.2, pointed to from §7.1). Findable (§6.4.1): the Charter's index and each record open from their record_location for the people the Charter's distribution rule names; decision_id and charter_id never change, including through a move to another system; and each record names the version of the Charter it was made under. Retained (§6.4.2): the Charter declares a retention period for each record type in its schedule, either as a specific duration or by naming the retention requirement it follows ("indefinite" or "as needed" is not a declared period); records stay findable for that period; and when a record is deleted, moved out of reach or transferred to a successor system at the end of it, that is itself recorded. Which period applies is for the organization to determine (§6.4.2); this criterion checks only that a period is declared and kept.
  - Evidence: The Charter's index and a few records opened from it, the Charter version each record names, the retention period the Charter declares for each record type, and any records of removal at the end of a period.
  - Standard: §7.1, §6.5.2, §6.4. Signal: none named in §7.

## The declaration in plain text

Fill the braces. Name each Charter as "Name (ID)", from its charter_name and charter_id fields; separate several Charters with "; ". For {where}, use the publication page; if none was given, leave that line out, so the text never points at a page that does not exist yet.

For an organization:

```text
Decision Provenance Standard: self-declaration
Organization: {name}
Standard: Decision Provenance Standard v1.3, reading edition rev. 11 (https://decisionprovenancestandard.org/dps-v1.3-rev11-core.html)
Charters covered: {charters}
Conformance Level claimed: Level {level} ({level_name}), self-declared on {date}
Where this declaration can be read: {where}
Stands behind it: {affirmed_name}, {affirmed_role}
This is our own self-declaration, not a statement by the Standard's Steward. The Steward has not audited our records.
```

For a product:

```text
Decision Provenance Standard: self-declaration
Product: {name}
Standard: Decision Provenance Standard v1.3, reading edition rev. 11 (https://decisionprovenancestandard.org/dps-v1.3-rev11-core.html)
Claim: this product implements the Decision Provenance Standard, self-declared on {date}
Where this declaration can be read: {where}
Stands behind it: {affirmed_name}, {affirmed_role}
This is our own statement about our product, not a statement by the Standard's Steward. The Steward has not reviewed or tested our product.
```

Level names: Level 1 = Charter-Conformant; Level 2 = Mode-Disambiguated; Level 3 = Continuously Auditable.

Use "v1.3-rev11" as standard_version: declarations are drafted against this version only.

Only when the organization declaring is the Standard's Steward, use this statement instead of the organization statement above, in the plain text and in the JSON (the schema allows both):

> This is a self-declaration by the organization named here. The Standard's Steward does not certify it, including when the Steward is that organization.

Only when the Standard's Steward made the product, use this statement instead of the product statement above, in the plain text and in the JSON (the schema allows both):

> This is a self-declaration for the product named here. The Standard's Steward does not certify it, including when the Steward made the product.
