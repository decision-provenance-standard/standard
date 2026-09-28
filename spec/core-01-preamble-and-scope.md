# Section 1 — Preamble + Scope

> ⚠️ **Not legal advice.** See the disclaimer block at the top of this document for the not-legal-advice notice and Jurisdiction Assumed. This Section inherits both.

---

## 1.1 The Decision Provenance Standard™

The Decision Provenance Standard™ ("the Standard") is an open standard for the production and maintenance of audit-ready decision provenance in organizations that dispatch consequential decisions through a mix of human and AI authorship. The Standard formalizes a single artifact set — Charters, decision records, schedules of records, conformance signals, conformance levels, and disclosure metadata — and a single dispatch grammar — Mode 1 (Human-Led, AI-Enforced) and Mode 2 (AI-Led, Human-Reviewed) — under which a deployer organization commits to a way of deciding that survives leadership transitions and supports counsel and auditors when they prepare evidence, certifications, or attestations.

The Decision Provenance Standard exists first and foremost as measurement infrastructure for decision quality: a structured way to record how decisions are made so the organization can learn from itself. The records also serve as audit-ready substrate that the deployer's counsel and auditors may use as input when preparing evidence, certifications, or attestations — the records inform that work without satisfying any regulatory obligation; whether any obligation applies, and to whom, is for the deployer to determine.

The open Decision Provenance Standard is the bridge between an organization's human custodianship of its decision system and the AI tooling that increasingly participates in it. The Standard makes a deploying organization's decisions affirmable, auditable, and resumable regardless of whether a human or a model produced the underlying analysis. That is what keeps custodianship human-held as AI participation deepens.

The Standard is the load-bearing record-format infrastructure for organizations operating governed decision-making about AI-mediated decisions. It is authored as a standalone normative artifact and is consumed by deployers, counsel, auditors, regulators, vendors, academics, and any party with a stake in the structural shape of audit-ready decision provenance.

## 1.2 Who Authored This

The principal author is Yohay Etsion, who operates as Founding Steward of the Standard under the institutional Steward role held by Etsion Brands Ltd., an Israeli holding company. The Standard is published under the Creative Commons Attribution 4.0 International License (CC-BY 4.0) as an open standard. By design, conformance is self-declared (the self-declared / no-certifying-body posture is stated authoritatively at §7 and §11.2). Etsion Brands Ltd., as Steward, holds the trademark on "Decision Provenance Standard" to prevent misrepresentation of the name, not to gate the text; the Founding Steward operates the Standard's authoring under a Charter consistent with §3 (see §11.1 for trademark convention; see §11.2 for Steward governance and succession). Other terms defined in Section 2 — "Charter," "Mode 1," "Mode 2," "audit-ready decision provenance," and so on — are open vocabulary: a deployer, a tool vendor, a consultancy, a regulator, an academic, or any other party may adopt the terms, extend them, fork them under attribution, or implement them in any product or service consistent with the CC-BY 4.0 license.

This Standard is authored by the Founding Steward under the Etsion Brands Ltd. Steward role. Drafting reflects iterative self-review against published legal, governance, and operational frameworks; it has not been reviewed by retained counsel and is not a substitute for that review. The public version represents the state of the work as published, with future revisions to follow the versioning conventions in Appendix G (References) §12. The drafting discipline is not a substitute for the human professional review every deployer's installation will require. **Where this Standard is read by counsel, auditors, regulators, or downstream deployers as the foundation of an installation, the Standard is the structural input; the human professional's review is what gives any implementation its weight.**

The Standard governs its own text and does not bind any companion implementation, commentary, or reference artifact. Where a third party references the Standard, the cross-reference is a neutral pointer to the structural definitions herein; substantive claims about regulatory state, evidentiary force, or compliance posture are for the deployer to determine, not for the Standard or any third-party artifact.

## 1.3 Who This Is For

This Standard is written for five reading audiences, each with a distinct entry point:

**Deployers** — Chief Product Officers, Chief Operating Officers, Chief Compliance Officers, Heads of Legal, and the executive teams who decide whether to install a Charter under the Standard in their organization. Deployers read Section 1 (this preamble) for scope, Section 3 (the Charter mechanism) for the operational commitment, Section 5 (Record Lifecycle) for how records progress to affirmed-and-sealed status, and Section 10 (Implementation Guidance) for the install path. Whether any legal obligation applies, and who carries it, is for the deployer to determine; the Standard structures inputs and does not discharge any obligation.

**Counsel** — General Counsel, in-house attorneys, outside counsel, employment counsel, privacy counsel, IP counsel, and compliance officers who advise the deployer on whether and how the Standard's records inform regulatory and litigation work. Counsel reads §1.4 ("What This Standard Claims — and What It Does Not Claim") first, then Section 8 (Regulatory Cross-References) for framework-by-framework treatment, then Section 6 (Required Artifact Set) and Section 5 (Record Lifecycle) for what the records actually contain and how they reach sealed status. Counsel converts audit-ready decision provenance into evidence, certifications, or attestations as the matter requires; the Standard does not.

**Auditors** — internal auditors, external auditors, SOC 2 examiners, ISO assessors, and the audit-adjacent professionals who read decision records and Charter states as inputs to their own attestation work. Auditors read Section 6 (the artifact set), Section 5 (the record lifecycle), Section 7 (Conformance Levels), and Section 8 (Regulatory Cross-References) to understand what a deployer self-declares against the Standard. Auditors form their own substantive judgments; the Standard's conformance signals are structured inputs the auditor reads as one input among others.

**Regulators reading and downstream readers of Mode 2 artifacts** — supervisory authorities reviewing a deployer's governance posture, AI Office staff considering Article 50 disclosure compliance, academic and policy researchers studying hybrid human-AI decision systems, and the natural persons who receive Mode 2 outputs as the audience for those outputs. These readers benefit from a stable open vocabulary and a stable open dispatch grammar against which deployers' implementations can be compared. The Standard is open to any regulator who wishes to read it. The Standard does not bind any regulator; no regulator has reviewed or endorsed it; the Standard's claims are the author's, made publicly under CC-BY 4.0.

**Board and oversight directors** — members of the board, audit-committee members, and the oversight directors who hold the organization's governance accountability for how consequential decisions are made. Board and oversight directors read §1.4 ("What This Standard Claims — and What It Does Not Claim") for the claim and the firewall, then Section 7 (Conformance Levels) for what their organization self-declares. Whether and how any board oversight duty is met (the *Caremark* line of cases, cited in Section 8) is for the board and the deployer to determine; the Standard structures the inputs the oversight function reads, and does not discharge the duty itself.

A reader who falls into more than one of the five audiences above reads each section against the role they are reading in at that moment. The Reading Guide in §1.8 enumerates the section-to-audience mapping in tabular form.

## 1.4 What This Standard Claims — and What It Does Not Claim

### 1.4.1 What This Standard Claims

The Standard claims a single thing: that the artifact set defined in Sections 2 through 7, produced and maintained per the requirements herein, constitutes **audit-ready decision provenance**.

The locked one-line definition of the term — load-bearing across every section of the Standard and every reader-facing surface — is reproduced here verbatim:

> **Audit-ready decision provenance is a structured record of how a decision was made — inputs, reviewers, dispatch mode, sign-offs — that counsel and auditors can use as input when preparing evidence, certifications, or attestations; the provenance itself is not evidence, certification, or attestation.**

The "is not evidence, certification, or attestation" clause is the Standard's core non-claim and is non-negotiable on every surface where the term is introduced. **Counsel and auditors convert audit-ready decision provenance into evidence, certifications, or attestations as their professional judgment requires; the artifacts produced under this Standard do not.**

### 1.4.2 What This Standard Does Not Claim

The Standard's claims are structural: the artifacts have a defined shape, the dispatch modes have a defined grammar, the conformance levels have defined criteria. The Standard makes no claim about regulatory state. To make this scope explicit, the following list enumerates what the Standard does **not** claim, in language a regulator or plaintiff's counsel would read against it:

- **Not evidence.** A decision record produced under this Standard is not legal evidence. Evidence is produced by counsel, by litigants, by examiners, and by the rules of the forum that admits it. The Standard's records are structured process records that counsel may use as input when preparing evidence; they are not evidence in themselves.
- **Not certification.** A conformance level declared under this Standard is not certification. No third-party body certifies conformance under this Standard. A deployer self-declares a conformance level using the Section 7 reporter; counsel and auditors read that self-declaration as one input among others when forming their own judgments.
- **Not attestation.** A decision record under this Standard is not an attestation. Attestation is a substantive professional judgment by qualified personnel against an enumerated framework (SOC 2, ISO/IEC 42001, etc.). The Standard structures the inputs an attestation work product consumes; the work product itself is the attesting professional's, not the Standard's.
- **Not a regulatory substitute.** Conformance with this Standard does not satisfy, ensure, certify, or substitute for any regulatory obligation under any framework — including but not limited to the EU AI Act, the EU GDPR, U.S. SOX 404, HIPAA, the Caremark line of fiduciary cases, NYC Local Law 144, Colorado SB 24-205, NIST AI RMF, ISO/IEC 42001, ISO/IEC 27001, SOC 2, or any successor or jurisdictionally analogous framework. Whether any regulatory obligation applies, and to whom, is for the deployer to determine. The Standard structures the inputs that compliance work consumes.
- **Not legal advice.** Nothing in this Standard, in any decision record produced under it, or in any Charter authored against it is legal advice. No attorney-client relationship is created by reading, citing, adopting, or extending this Standard. Jurisdiction-specific questions, contested matters, and any decision with material legal or regulatory consequences require review by a licensed attorney in the relevant jurisdiction.

The verbs the Standard uses are process verbs — *records*, *documents*, *structures*, *binds*, *commits*, *emits*, *informs*, *supports* — not regulatory verbs — *satisfies*, *ensures*, *certifies*, *guarantees*, *proves*. The verb discipline is intentional. A regulatory verb appearing anywhere in this Standard outside of a quoted regulatory framework name (e.g., "Article 50 transparency obligations" where "transparency obligations" is the framework's term, not the Standard's claim) is an editorial defect.

### 1.4.3 Audience Framing — Use Cases the Standard's Records Support

The Standard's records support four use-case audiences, each consuming the same structural substrate for different purposes:

- **Audit-readiness** (counsel, auditors, regulators per §1.3): the records are input substrate for evidence, attestations, and regulatory filings, prepared by qualified personnel under their own professional standards.
- **Deployer-internal optimization**: the records are input substrate for the deployer's own continuous improvement of its decision-making — replay decisions against outcomes, surface patterns across decision classes, identify Charters whose re-decision triggers are firing more often than expected.
- **Organizational learning**: the records are input substrate for the deployer's longitudinal record of how the organization's leaders develop as decision-makers, used in coaching, mentorship, and developmental conversations under the deployer's HR-of-record governance and the per-altitude consent and use-case scope-limit framing of Appendix G §G.11.3.
- **Team-level and (with separate consent) individual-altitude measurement**: the records aggregate at team altitude for team-level decision-quality patterns; at individual altitude they exist if and only if the affirmer has consented to individual-altitude record creation under the Charter's use-case scope-limit declaration (§3) and the deployer's HR-of-record governance.

The four use cases share a substrate. They are not co-equal in the Standard's posture: audit-readiness is the load-bearing claim of §1.4.1, and the firewall language at §1.4.2 (no evidence, no certification, no attestation, no regulatory substitute, no legal advice) governs all four use cases. The deployer's installation determines which use cases are in scope for which altitudes; the Charter's use-case scope-limit declaration (§3) records the deployer's choices.

## 1.5 Use of the Standard Notice

This is the artifact-scoped notice required by the Standard's notice architecture (the "Use of the Standard" notice). It governs the Standard document itself.

### 1.5.1 What Users May Do Under CC-BY 4.0

This Standard is licensed under the Creative Commons Attribution 4.0 International License (CC-BY 4.0). Under that license, any reader, deployer, vendor, consultancy, regulator, academic, or other party may:

- **Read** the Standard freely, in any jurisdiction, without paying any fee or accepting any non-CC-BY-4.0 terms
- **Cite** the Standard in academic work, regulatory submissions, vendor RFPs, internal governance documents, audit-engagement work papers, or any other work product, with attribution as set out below
- **Adopt** the Standard's vocabulary, dispatch grammar, conformance signals, and conformance levels in a deployer's installation, in a vendor's product, or in a consultancy's methodology, with attribution
- **Extend** the Standard with implementation-specific guidance, sector-specific overlays, jurisdiction-specific addenda, or deployer-specific tooling, with attribution and a clear marker that the extension is downstream of, and does not bind, the principal author's Standard
- **Fork** the Standard into a derivative open standard, with attribution, a clear divergence statement, and a different name to prevent confusion with this Standard

**Attribution form.** Where space permits: *"The Decision Provenance Standard, Yohay Etsion, [year], CC-BY 4.0, https://decisionprovenancestandard.org."* Where space is constrained: *"Decision Provenance Standard, CC-BY 4.0."* Where the deployer's installation is grounded in the Standard, the deployer's Charter (Section 3) cites the Standard at the version the Charter was authored against.

### 1.5.2 What Users May Not Do

The CC-BY 4.0 license is permissive on use; it does not authorize misuse. The following are outside the license:

- **Misrepresenting the Standard as certified, attested, or regulator-endorsed.** No certification track exists. No attestation body has reviewed the Standard. No regulator has endorsed it. Any party representing the Standard, or an installation grounded in the Standard, as carrying any of the foregoing forms of external validation is making a false claim, not a CC-BY 4.0 use.
- **Misrepresenting derivative or extended work as authored or endorsed by the principal author.** Forks, extensions, and downstream installations are downstream work. The CC-BY 4.0 attribution requirement protects the upstream author from misattribution; downstream authors are responsible for their own work and must mark their work as their own.
- **Removing the "is not evidence" clause.** The "is not evidence, certification, or attestation" tail on §1.4's locked one-line definition, and the equivalent language at every first use of "audit-ready decision provenance" in derivative or extended work, is part of the Standard's structural integrity. A derivative that strips the firewall language to make stronger claims has departed from the Standard and must mark itself as such.
- **Using the Standard's name to substitute for counsel review.** No reading, citing, adopting, extending, or forking of the Standard substitutes for counsel review of a deployer's specific installation, regulatory posture, contractual exposure, or litigation risk.
- **Misusing the trademark.** The trademark on "Decision Provenance Standard" is separate from the license on the text. Using the trademark to certify, accredit, audit, grade, or otherwise stamp a deployer organization, a tool vendor's customer organization, or any third party as "Standard-compliant" or "certified by the Standard" is a misuse and is not authorized by either the trademark or the CC-BY 4.0 license. See §11 for the trademark, Steward governance, and voluntary-adoption discipline.

### 1.5.3 How to Handle Misuse

Where a reader encounters a use of the Standard that appears to misrepresent its scope (a vendor pitching the Standard as a regulatory substitute; a consultancy claiming the Standard "satisfies" a named framework; a deployer claiming the Standard "ensures compliance"; a third party purporting to certify another organization "against the Standard"), the reader is invited to:

1. Re-read this §1.5, §1.4, and Appendix G §G.11.3 to confirm the scope, then form their own judgment about the claim being made
2. Request from the misusing party the citation in the Standard that supports the claim — there is none, by design, and the request will surface the gap
3. If the misuse is in a regulated context (an audit work paper, a regulatory submission, a contractual representation), bring it to the attention of qualified personnel for handling

Use of the text is governed by CC BY 4.0. The Steward does not monitor how the text is used. Permitted uses of the name are set out in §11.1. The structural protection is the firewall language and the verb discipline, both of which travel with the Standard wherever the Standard goes.

## 1.6 Jurisdiction Assumed

The Standard is authored against an explicit primary jurisdiction with named secondary jurisdictions:

- **Primary jurisdiction**: U.S. federal + Delaware
- **Named secondary jurisdictions**: United Kingdom (England & Wales for litigation framing), the European Union (with the EU AI Act, Regulation (EU) 2024/1689, as the load-bearing AI-specific framework — see §1.6.1 below for the disclosure-block scope), and the State of Israel

A deployer operating exclusively within one of the named jurisdictions reads Section 8's cross-references as pointers to frameworks cited for those jurisdictions. A deployer operating in any other jurisdiction reads the Standard as a hypothesis to verify with local counsel, with two implications:

1. The vocabulary, dispatch grammar, and conformance-signal architecture remain stable across jurisdictions — they are structural, not jurisdictional
2. The regulatory cross-references in Section 8, the audit-framework alignments, and the litigation-framing assumptions in §1.4.2 are jurisdictionally bounded to the named four; in any other jurisdiction, they require local-counsel verification

### 1.6.1 Disclosure Block Scope (Pointer to §4.6)

Section 4 §4.6 sets the Standard's own disclosure block for Mode 2 content. Whether Article 50 of the EU AI Act, Regulation (EU) 2024/1689, applies to a given artifact is for the deployer to determine.

A Charter MAY declare its Mode 2 outputs outside this requirement where the deployer has verified that those outputs are produced outside the European Union and will not reach, and are not reasonably foreseeable to reach, people in the European Union. Without that declaration the requirement applies. This scope is carried over from rev. 8 and is the Standard's own choice; it says nothing about where any law applies. A Charter written before v1.1 (reading edition rev. 9) whose Mode 2 outputs already met this test remains valid without the declaration. Full treatment, including the five required transparency-disclosure metadata fields and the Mode 1 content-level edge case, lives in **Section 4.6** of this Standard.

### 1.6.2 Other Jurisdictions

Deployers operating in jurisdictions outside the named four — including but not limited to Canada, Switzerland, Singapore, Australia, Japan, Brazil, Mexico, India, the Gulf Cooperation Council, and any other jurisdiction not explicitly enumerated above — read the Standard as structural input and verify every regulatory cross-reference, every conformance criterion, and every disclosure-metadata requirement against local counsel. The Standard's vocabulary and dispatch grammar are jurisdictionally portable; the regulatory cross-references and the litigation-framing assumptions are not.

## 1.7 Related Work

The Related Work section — the named academic, standards-body, and authored lineages this Standard converses with (Singh/Cobbe/Norval on decision provenance; W3C PROV-AGENT; AGENTSAFE; Trammell's *Chief Executive Operating System*; Gartner Bimodal IT) — is maintained in **Appendix G §G.1 (Related Work)**, with its supporting citations at Appendix G §12.3.3. The citations are placement, not contestation: the Standard occupies an altitude (open record format for human-judgment decisions at named executive accountability) that none of the cited works occupies, and claims no derivation from them.


## 1.8 Reading Guide

The Standard is sequential but not linear. The following table maps each section to the reading audience that finds it most load-bearing, with a one-line description of why:

| Section | Load-bearing for | Why |
|---|---|---|
| **1 — Preamble + Scope** | All five audiences | Establishes scope, jurisdiction, related work, and what the Standard claims (and does not). Read first. |
| **2 — Definitions** | All five audiences | Binding vocabulary. Every later section refers back. |
| **3 — Charter Mechanism** | Deployers; counsel | The operational commitment. Charters bind organizations to a way of deciding. |
| **4 — Mode Dispatch** | Deployers; auditors; regulators (§4.6) | The dispatch state machine, the Mode 1 / Mode 2 grammar, and the Standard's own disclosure block for AI-drafted content. |
| **5 — Record Lifecycle States** | All five audiences | The sequential lifecycle (draft → reviewed → affirmed) gated on explicit human affirmation; intentional non-coverage of real-time telemetry. |
| **6 — Required Artifact Set** | Auditors; counsel | What the records actually contain at the field level. |
| **7 — Conformance Levels** | Deployers; auditors | The named tiers (1, 2, 3) and the signals each tier requires. **Conformance is self-declared by the adopting organization.** |
| **8 — Regulatory Cross-References** | Counsel; compliance officers | Framework-by-framework treatment (EU AI Act, NIST AI RMF, ISO/IEC 42001, SOC 2, *Caremark*, etc.) — what the Standard **informs** without **satisfying**. |
| **9 — Worked Examples** | Deployers; auditors | Decisions dispatched under representative Charters, end-to-end. |
| **10 — Implementation Guidance** | Deployers | The install path: how to reach Conformance Level 1, then 2, then 3. |
| **11 — Trademark, Governance, and Voluntary Adoption** | All five audiences; counsel especially | Trademark convention; Steward role definition and succession; voluntary-adoption discipline; recognition of self-declaring adopters. |
| **12 — References** | All five audiences | Bibliographic and citation pointers to the frameworks referenced. |

A counsel reader reads §1.4 → Section 8 → Section 6 → Section 5 → §1.5 → Section 11. An auditor reads Section 6 → Section 5 → Section 7 → Section 8. A deployer reads Section 1 → Section 3 → Section 5 → Section 10 → Section 7 → Section 11. A regulator reads Section 1 → §4.6 → Section 5 → Section 8 → Section 11. A board or oversight director reads §1.4 → Section 7 → Section 8. The Standard supports all five reading paths; no path is privileged over the others.

---

