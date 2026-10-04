# Read This First — Executive On-Ramp

> This On-Ramp is a one-screen orientation, not part of the normative Standard. It front-loads the claim and routes each reader to the right section in seconds. Sections 1 through 7 (and the companions) are the Standard; nothing here adds to, removes from, or overrides any requirement, definition, or conformance criterion below.

## What this is, in one line

This Standard gives an organization a way to make its consequential decisions **affirmable, auditable, and resumable** — regardless of whether a human or an AI produced the underlying analysis. That is how the people accountable for a decision stay accountable for it as AI does more of the work underneath. The record of how a decision was made is *input* that counsel and auditors can build on; it is never a stand-in for their judgment.

## The mechanism, in four parts

The whole Standard rests on four primitives. Get these four and you have the thesis:

- **The Charter** — binds a recurring decision class to one named owner, a declared dispatch mode, a schedule of records, and the triggers that reopen the decision when outcomes or the market demand it.
- **The Mode 1 / Mode 2 dispatch grammar** — records who *authored* the analysis and who *reviewed* it. Mode 1 is Human-Led, AI-Enforced; Mode 2 is AI-Led, Human-Reviewed. This is the primitive that carries the AI-authorship claim and the Standard's own disclosure block (§4.6).
- **The affirmation-and-seal lifecycle** — a record only reaches sealed status when a named human affirms it. Nothing is promoted to affirmed by default, by elapsed time, or by silence. This is what separates the Standard from a logging format.
- **Self-declared conformance levels** — the deployer declares which level its Charter meets, and improves against the named criteria over time. No one grades it from outside.

## The firewall

> **Audit-ready decision provenance is *input* to your counsel and your auditors — never a substitute for their judgment. The records produced under this Standard are not evidence, certification, or attestation, and nothing in this Standard is legal advice or a regulatory substitute, and no attorney-client relationship is created by reading, citing, or adopting it. Counsel and auditors convert audit-ready decision provenance into evidence, certifications, or attestations as their professional judgment requires; the artifacts produced under this Standard do not. There is no certifying body and no certification track: every conformance level is self-declared. Where a decision carries material legal or regulatory consequences, a licensed attorney in the relevant jurisdiction should review it. Do not rely on this Standard, or on any record produced under it, as the sole basis for any legal, compliance, or employment decision.**

## The three conformance levels, at a glance

Each level builds on the one before it. All three are self-declared; see §7 for the authoritative self-declared / no-certifying-body statement.

| Level | What it declares | Core criteria (verbatim from §7) |
|---|---|---|
| **Conformance Level 1 — Charter-Conformant** | The Charter is a structurally complete artifact: it names what it governs, who owns it, the mode it dispatches in, where its records live, and what reopens its decisions. | Charter has reached the `fields-completed` lifecycle state; `mode_declaration` populated with one of three enumerated values (`mode-1`, `mode-2`, `mode-1-with-embedded-mode-2-summary`); Schedule of records committed and non-empty; `record_location` resolves to a durable surface; `accountable_owner` names one human; `re_decision_triggers` meets two-class minimum; `escalation_rule` populated with a named, exact trigger. |
| **Conformance Level 2 — Mode-Disambiguated** | The Charter's records are authorship-disambiguated at the per-record level, disclosure metadata is attached where required, and the silent-drift safety net is operating. | Every decision record under the Charter carries its `dispatch_mode` field; Every Mode 2 record within the §4.6 requirement (§4.6.1) carries a complete disclosure block (the five fields of §4.6.2); Every Mode 1 edge-case record whose embedded content is within the §4.6 requirement (§4.6.1) carries a per-record disclosure block at the embed point; The schedule-of-records sample audit returns no silent drift findings. |
| **Conformance Level 3 — Continuously Auditable** | The Charter's mechanism has run over time as it declared it would: triggers fire on cadence, escalations produce records, disclosures stay current, and the schedule is queryable on demand. | Re-decision triggers fire and produce records on the Charter's declared cadence; Escalation rule produces records when invoked; Disclosure blocks are reviewed within the Charter's review cadence; Schedule of records is queryable and exportable for counsel and auditor review on demand. |

The full criteria, reporter signals, and grading mechanics are in Section 7. A Charter that does not yet grade at Level 1 is in the install phase; Companion C covers the path in.

## Where to start, by role

The Standard is sequential but not linear. Read the sections your role finds load-bearing first; everything else is reference you can reach when you need it.

| You are | Start with | Then | Reference when you need it |
|---|---|---|---|
| **CIO / CAIO / executive deciding whether to adopt** | This On-Ramp, then §1 (Preamble + Scope) and §3 (the Charter Mechanism) | §5 (Record Lifecycle) for how records reach sealed status; §7 (Conformance Levels) for what you commit to | Companion C (Implementation Guidance) for the install path |
| **General Counsel / counsel** | §1.4 (What This Standard Claims — and What It Does Not Claim) | §6 (Required Artifact Set) and §5 (Record Lifecycle) for what the records contain | Companion A (Regulatory Cross-Reference Mapping) for framework-by-framework treatment and the per-framework non-claims |
| **Technical architect** | §3 (the Charter Mechanism), §5 (Record Lifecycle), §6 (Required Artifact Set) | §4 (Authority and Authorship) for the dispatch state machine and §7 for conformance signals | Companion C for sequencing; Appendix G for the reference files |
| **AI-governance researcher** | §1 (Preamble + Scope) and §4 (Authority and Authorship in AI-Mediated Decisions) | §5 (Record Lifecycle) and §7 (Conformance Levels) for the novel contributions | Appendix G (Governance & References, including Related Work) |
| **Board / oversight director** | This On-Ramp, then §1.4 (the claim and the firewall) | §7 (Conformance Levels) for what your organization self-declares | Companion A §A.6 (Caremark / board oversight duties) |

The Standard is open to every reader under CC-BY 4.0. No reading path is privileged over the others; read each section against the role you are reading in at that moment.

---

